"""Shared helpers for the Egyptian Arabic dubbing pipeline."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MODELS = REPO / "dubbing" / "models"
WORK = REPO / "work"

# XTTS truncates Arabic input above 166 characters; keep a safety margin.
AR_CHAR_LIMIT = 160

_LATIN_RUN = re.compile(r"[A-Za-z][A-Za-z0-9'’&/.\-]*(?:\s+[A-Za-z0-9][A-Za-z0-9'’&/.\-]*)*")
_DIGIT = re.compile(r"[0-9٠-٩۰-۹]")


def load_json(path: Path | str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(obj, path: Path | str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def run(cmd: list[str], quiet: bool = True) -> subprocess.CompletedProcess:
    """Run a command, raising with its stderr on failure."""
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stderr[-4000:]}")
    if not quiet:
        print(proc.stdout)
    return proc


def probe(path: Path | str) -> dict:
    """Return duration (s), fps, width, height and whether an audio stream exists."""
    out = run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)]).stdout
    info = json.loads(out)
    video = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    has_audio = any(s["codec_type"] == "audio" for s in info["streams"])
    fps, fps_str = None, None
    if video is not None:
        fps_str = video.get("avg_frame_rate", "0/1")
        num, den = fps_str.split("/")
        fps = float(num) / float(den) if float(den) else None
    return {
        "duration": float(info["format"]["duration"]),
        "fps": fps,
        "fps_str": fps_str,
        "width": int(video["width"]) if video else None,
        "height": int(video["height"]) if video else None,
        "has_audio": has_audio,
    }


def latin_runs(text: str) -> list[tuple[str, str]]:
    """Split text into ("ar", ...) / ("en", ...) runs by script."""
    runs: list[tuple[str, str]] = []
    pos = 0
    for m in _LATIN_RUN.finditer(text):
        if m.start() > pos:
            runs.append(("ar", text[pos:m.start()]))
        runs.append(("en", m.group(0)))
        pos = m.end()
    if pos < len(text):
        runs.append(("ar", text[pos:]))
    return [(lang, chunk.strip()) for lang, chunk in runs if chunk.strip(" ،,.؛;:")]


def check_tts_text(text: str) -> list[str]:
    """Problems that would make XTTS mispronounce or truncate a speech line."""
    problems = []
    if _DIGIT.search(text):
        problems.append("contains digits (XTTS expands them into MSA words) - spell the number out")
    if any(sym in text for sym in "$%€£"):
        problems.append("contains a currency/percent symbol - write it as words")
    if len(text) > AR_CHAR_LIMIT:
        problems.append(f"{len(text)} characters (limit {AR_CHAR_LIMIT}) - split into more parts")
    return problems


def fmt_srt_time(seconds: float) -> str:
    ms = max(0, int(round(seconds * 1000)))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
