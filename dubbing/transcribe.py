"""Transcribe the original English narration and draft translation units.

    python dubbing/transcribe.py --video input/original.mp4

Writes work/transcript_en.json (segments + word timings), work/transcript_en.md (readable),
and script/units_en.json: sentence-level units with timings, ready to be translated.
"""

from __future__ import annotations

import argparse
import re
import tempfile
from pathlib import Path

from common import MODELS, REPO, WORK, run, save_json

# Biases Whisper toward the spelling of exam vocabulary without dictating content.
TAX_PROMPT = (
    "CPA exam, Tax Compliance and Planning (TCP). Internal Revenue Code Section 1231, Section 1245, "
    "Section 1250, Section 179, Section 199A, adjusted basis, AGI, MAGI, QBI, NOL, AMT, E&P, AAA, "
    "S corporation, C corporation, partnership, Form 1040, Form 1065, Form 1120-S, Schedule K-1, MACRS."
)
SENTENCE_END = re.compile(r"[.?!…]['\"”’)]*$")


def transcribe(video: Path, model_dir: Path, beam_size: int) -> dict:
    from faster_whisper import WhisperModel

    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "audio.wav"
        run(["ffmpeg", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(wav)])
        model = WhisperModel(str(model_dir), device="cpu", compute_type="int8", cpu_threads=4)
        segments, info = model.transcribe(
            str(wav),
            language="en",
            beam_size=beam_size,
            word_timestamps=True,
            vad_filter=False,
            condition_on_previous_text=True,
            initial_prompt=TAX_PROMPT,
        )
        out = []
        for seg in segments:
            words = [{"start": round(w.start, 3), "end": round(w.end, 3), "word": w.word} for w in (seg.words or [])]
            out.append({"id": seg.id, "start": round(seg.start, 3), "end": round(seg.end, 3), "text": seg.text.strip(), "words": words})
            print(f"[{seg.start:7.2f} -> {seg.end:7.2f}] {seg.text.strip()}")
    return {"source": str(video), "duration": round(info.duration, 3), "language": info.language, "segments": out}


def build_units(transcript: dict, min_len: float, max_len: float) -> list[dict]:
    """Group words into sentence units; merge very short sentences, split very long ones at commas."""
    words = [w for s in transcript["segments"] for w in s["words"]]
    sentences, current = [], []
    for w in words:
        current.append(w)
        if SENTENCE_END.search(w["word"].strip()):
            sentences.append(current)
            current = []
    if current:
        sentences.append(current)

    def split_long(sent):
        if sent[-1]["end"] - sent[0]["start"] <= max_len:
            return [sent]
        # split at the comma closest to the middle, recursively
        mid = (sent[0]["start"] + sent[-1]["end"]) / 2
        cuts = [i for i, w in enumerate(sent[:-1]) if w["word"].strip().endswith((",", ";", ":"))]
        if not cuts:
            return [sent]
        i = min(cuts, key=lambda k: abs(sent[k]["end"] - mid))
        return split_long(sent[: i + 1]) + split_long(sent[i + 1 :])

    pieces = [p for s in sentences for p in split_long(s)]
    merged: list[list[dict]] = []
    for p in pieces:
        if merged and (merged[-1][-1]["end"] - merged[-1][0]["start"] < min_len) and (p[-1]["end"] - merged[-1][0]["start"] <= max_len):
            merged[-1].extend(p)
        else:
            merged.append(list(p))

    units = []
    for i, p in enumerate(merged, start=1):
        text = "".join(w["word"] for w in p).strip()
        units.append({"id": i, "start": p[0]["start"], "end": p[-1]["end"], "en": text, "parts": []})
    return units


def write_markdown(transcript: dict, units: list[dict], path: Path) -> None:
    lines = [f"# Transcript: {Path(transcript['source']).name}", "", f"Duration: {transcript['duration']:.1f}s", ""]
    for u in units:
        m, s = divmod(u["start"], 60)
        lines.append(f"**{u['id']:03d}** `{int(m):02d}:{s:05.2f}` {u['en']}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video", type=Path, required=True)
    ap.add_argument("--model", type=Path, default=MODELS / "faster-whisper-large-v3")
    ap.add_argument("--beam-size", type=int, default=5)
    ap.add_argument("--min-unit", type=float, default=2.5, help="merge sentences shorter than this (s)")
    ap.add_argument("--max-unit", type=float, default=14.0, help="split sentences longer than this (s)")
    args = ap.parse_args()

    transcript = transcribe(args.video, args.model, args.beam_size)
    save_json(transcript, WORK / "transcript_en.json")
    units = build_units(transcript, args.min_unit, args.max_unit)
    save_json({"source": transcript["source"], "duration": transcript["duration"], "units": units}, REPO / "script" / "units_en.json")
    write_markdown(transcript, units, WORK / "transcript_en.md")
    print(f"{len(transcript['segments'])} segments -> {len(units)} units")


if __name__ == "__main__":
    main()
