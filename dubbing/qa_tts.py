"""Round-trip check of the synthesized narration.

    python dubbing/qa_tts.py --script script/script_ar.json

Transcribes the whole narration back with Whisper in one pass (units joined with silence),
maps the words back to units, and flags units where Arabic words went missing, Whisper heard
far more or less than was written (XTTS babbling or truncation), or the speaking rate looks
wrong. Writes work/tts/qa.json; regenerate flagged units with synthesize.py --only.

English terms are not scored: Whisper (language=ar) writes them in Latin or in Arabic letters
unpredictably, so they are listed for reading instead.
"""

from __future__ import annotations

import argparse
import difflib
import re
from pathlib import Path

import numpy as np
import soundfile as sf

from common import MODELS, WORK, latin_runs, load_json, save_json

AR_DIACRITICS = re.compile(r"[ً-ْـ]")
ARABIC_WORD = re.compile(r"[ء-ي]{2,}")


def norm_ar(text: str) -> str:
    text = AR_DIACRITICS.sub("", text)
    text = re.sub("[إأآا]", "ا", text)
    text = text.replace("ى", "ي").replace("ة", "ه")
    text = re.sub(r"[^ء-يa-zA-Z0-9 ]", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


_AR_CONSONANTS = str.maketrans({
    "ب": "b", "ت": "t", "ث": "t", "ج": "g", "خ": "k", "د": "d", "ذ": "z", "ر": "r", "ز": "z", "س": "s", "ش": "s",
    "ص": "s", "ض": "d", "ط": "t", "ظ": "z", "غ": "g", "ف": "f", "ق": "k", "ك": "k", "ل": "l", "م": "m", "ن": "n",
    "ڤ": "f", "پ": "b", "گ": "g",
})


def skeleton(text: str) -> str:
    """Script-agnostic consonant skeleton: 'probate' and «بروبيت» both give 'brbt'."""
    t = text.lower()
    for a, b in (("ph", "f"), ("ck", "k"), ("th", "t"), ("sh", "s"), ("ch", "s")):
        t = t.replace(a, b)
    t = re.sub(r"c(?=[eiy])", "s", t)
    t = t.replace("c", "k").replace("q", "k").replace("x", "ks").replace("p", "b").replace("v", "f").replace("j", "g")
    t = t.translate(_AR_CONSONANTS)
    return re.sub(r"[^bdfgklmnrstz]", "", t)


def term_recall(expected: str, heard: str) -> float:
    """Share of the Latin-script English terms in the spoken line that Whisper heard, in either script."""
    terms = [t for lang, t in latin_runs(expected) if lang == "en" and len(skeleton(t)) >= 2]
    if not terms:
        return 1.0
    h = skeleton(heard)
    hits = 0
    for term in terms:
        k = skeleton(term)
        windows = [h[i : i + len(k)] for i in range(max(1, len(h) - len(k) + 1))]
        if max((difflib.SequenceMatcher(None, k, w).ratio() for w in windows), default=0.0) >= 0.8:
            hits += 1
    return hits / len(terms)


def arabic_recall(expected: str, heard: str) -> float:
    """Share of the expected Arabic words that Whisper heard (clitic-tolerant)."""
    want = ARABIC_WORD.findall(norm_ar(expected))
    pool = ARABIC_WORD.findall(norm_ar(heard))
    hits = 0
    for w in want:
        m = next((h for h in pool if h == w or (len(w) > 3 and (w in h or h in w))), None)
        if m is not None:
            hits += 1
            pool.remove(m)
    return hits / max(1, len(want))


def batch_transcribe(units: list[dict], manifest: dict, tts_dir: Path, model_dir: Path, gap: float) -> dict[int, str]:
    """One Whisper pass over all units; Whisper pads each call to 30 s, so per-unit calls cost ~5x more."""
    from faster_whisper import WhisperModel

    pieces, spans, cursor, sr = [], {}, 0.0, 24000
    for u in units:
        audio, sr = sf.read(tts_dir / manifest["units"][str(u["id"])]["file"], dtype="float32")
        spans[u["id"]] = (cursor, cursor + len(audio) / sr)
        pieces += [audio, np.zeros(int(gap * sr), dtype=np.float32)]
        cursor += len(audio) / sr + gap
    batch = WORK / "qa_narration.wav"
    sf.write(batch, np.concatenate(pieces), sr)

    model = WhisperModel(str(model_dir), device="cpu", compute_type="int8", cpu_threads=4)
    segments, _ = model.transcribe(
        str(batch), language="ar", beam_size=5, vad_filter=False, word_timestamps=True,
        condition_on_previous_text=False, hallucination_silence_threshold=gap * 0.8,
    )
    heard: dict[int, list[str]] = {u["id"]: [] for u in units}

    def distance(uid: int, t: float) -> float:
        start, end = spans[uid]
        return 0.0 if start <= t <= end else min(abs(t - start), abs(t - end))

    for seg in segments:
        for w in seg.words or []:
            mid = (w.start + w.end) / 2
            heard[min(spans, key=lambda uid: distance(uid, mid))].append(w.word)
        print(f"  heard up to {seg.end / 60:5.2f} min of {cursor / 60:.2f}", flush=True)
    return {uid: "".join(words).strip() for uid, words in heard.items()}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--script", type=Path, required=True)
    ap.add_argument("--tts", type=Path, default=WORK / "tts")
    ap.add_argument("--model", type=Path, default=MODELS / "faster-whisper-large-v3")
    ap.add_argument("--gap", type=float, default=1.2, help="silence between units in the batched pass (s)")
    ap.add_argument("--min-recall", type=float, default=0.75, help="share of expected Arabic words that must be heard")
    ap.add_argument("--min-term-recall", type=float, default=0.75, help="share of English terms that must be heard (either script)")
    ap.add_argument("--max-length-ratio", type=float, default=1.45, help="heard/written text above this looks like babbling")
    ap.add_argument("--min-length-ratio", type=float, default=0.6, help="heard/written text below this looks truncated")
    ap.add_argument("--min-rate", type=float, default=9.0, help="chars/s below this looks like babbling")
    ap.add_argument("--max-rate", type=float, default=22.0, help="chars/s above this looks truncated")
    ap.add_argument("--only", help="comma-separated unit ids to check (e.g. after regenerating them)")
    args = ap.parse_args()

    script = load_json(args.script)
    manifest = load_json(args.tts / "manifest.json")
    only = {int(x) for x in args.only.split(",")} if args.only else None
    units = [u for u in script["units"] if str(u["id"]) in manifest["units"] and (only is None or u["id"] in only)]
    heard = batch_transcribe(units, manifest, args.tts, args.model, args.gap)

    report, flagged = [], []
    for u in units:
        entry = manifest["units"][str(u["id"])]
        expected = " ".join(p.get("tts") or p["ar"] for p in u["parts"])
        recall = arabic_recall(expected, heard[u["id"]])
        terms = term_recall(expected, heard[u["id"]])
        length_ratio = len(norm_ar(heard[u["id"]])) / max(1, len(norm_ar(expected)))
        similarity = difflib.SequenceMatcher(None, norm_ar(expected), norm_ar(heard[u["id"]])).ratio()
        rate = len(expected) / max(entry["duration"], 0.1)
        issues = []
        if recall < args.min_recall:
            issues.append(f"Arabic words missing (recall {recall:.2f})")
        if terms < args.min_term_recall:
            issues.append(f"English terms unclear (term recall {terms:.2f})")
        if length_ratio > args.max_length_ratio:
            issues.append(f"heard {length_ratio:.2f}x the written text (possible babbling)")
        if length_ratio < args.min_length_ratio:
            issues.append(f"heard {length_ratio:.2f}x the written text (possible truncation)")
        if rate < args.min_rate:
            issues.append(f"slow {rate:.1f} chars/s")
        if rate > args.max_rate:
            issues.append(f"fast {rate:.1f} chars/s")
        report.append({
            "id": u["id"], "arabic_recall": round(recall, 3), "term_recall": round(terms, 3), "length_ratio": round(length_ratio, 2),
            "similarity": round(similarity, 3), "rate": round(rate, 1), "expected": expected, "heard": heard[u["id"]],
            "english_terms": [t for lang, t in latin_runs(expected) if lang == "en"], "issues": issues,
        })
        if issues:
            flagged.append(u["id"])
        print(f"unit {u['id']:3d}: recall {recall:.2f} terms {terms:.2f} length {length_ratio:.2f} rate {rate:4.1f} {'; '.join(issues)}")

    save_json({"flagged": flagged, "units": report}, args.tts / ("qa.json" if only is None else "qa_only.json"))
    print(f"{len(flagged)} flagged units: {flagged}")


if __name__ == "__main__":
    main()
