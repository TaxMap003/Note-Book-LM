"""Round-trip check of the synthesized narration.

    python dubbing/qa_tts.py --script script/script_ar.json

Transcribes every unit back with Whisper and flags units where Arabic words went missing,
English terms became unrecognizable, or the speaking rate looks wrong (runaway or truncated
XTTS output). Writes work/tts/qa.json; regenerate flagged units with synthesize.py --only.
"""

from __future__ import annotations

import argparse
import difflib
import re
from pathlib import Path

from common import MODELS, WORK, latin_runs, load_json, save_json

AR_DIACRITICS = re.compile(r"[ً-ْـ]")


def norm_ar(text: str) -> str:
    text = AR_DIACRITICS.sub("", text)
    text = re.sub("[إأآا]", "ا", text)
    text = text.replace("ى", "ي").replace("ة", "ه")
    text = re.sub(r"[^ء-يa-zA-Z0-9 ]", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--script", type=Path, required=True)
    ap.add_argument("--tts", type=Path, default=WORK / "tts")
    ap.add_argument("--model", type=Path, default=MODELS / "faster-whisper-large-v3")
    ap.add_argument("--min-similarity", type=float, default=0.72)
    ap.add_argument("--min-rate", type=float, default=9.0, help="chars/s below this looks like babbling")
    ap.add_argument("--max-rate", type=float, default=22.0, help="chars/s above this looks truncated")
    args = ap.parse_args()

    from faster_whisper import WhisperModel

    script = load_json(args.script)
    manifest = load_json(args.tts / "manifest.json")
    model = WhisperModel(str(args.model), device="cpu", compute_type="int8", cpu_threads=4)

    report, flagged = [], []
    for u in script["units"]:
        entry = manifest["units"].get(str(u["id"]))
        if not entry:
            continue
        expected = " ".join(p.get("tts") or p["ar"] for p in u["parts"])
        segments, _ = model.transcribe(str(args.tts / entry["file"]), language="ar", beam_size=5, vad_filter=False)
        heard = " ".join(s.text.strip() for s in segments)
        similarity = difflib.SequenceMatcher(None, norm_ar(expected), norm_ar(heard)).ratio()
        terms = [t for lang, t in latin_runs(expected) if lang == "en"]
        heard_low = heard.lower()
        missing_terms = [t for t in terms if t.lower() not in heard_low]
        rate = len(expected) / max(entry["duration"], 0.1)
        issues = []
        if similarity < args.min_similarity:
            issues.append(f"similarity {similarity:.2f}")
        if rate < args.min_rate:
            issues.append(f"slow {rate:.1f} chars/s (possible babbling)")
        if rate > args.max_rate:
            issues.append(f"fast {rate:.1f} chars/s (possible truncation)")
        row = {"id": u["id"], "similarity": round(similarity, 3), "rate": round(rate, 1), "heard": heard,
               "english_terms": terms, "terms_not_heard_in_latin": missing_terms, "issues": issues}
        report.append(row)
        if issues:
            flagged.append(u["id"])
        print(f"unit {u['id']:3d}: sim {similarity:.2f} rate {rate:4.1f} {'; '.join(issues)}")

    save_json({"flagged": flagged, "units": report}, args.tts / "qa.json")
    print(f"{len(flagged)} flagged units: {flagged}")


if __name__ == "__main__":
    main()
