"""Re-time the original video to the Egyptian Arabic narration and mux audio + subtitles.

    python dubbing/assemble.py --video input/original.mp4 --script script/script_ar.json \
        --out output/video_egyptian_arabic.mp4

The timeline is cut where each unit's original English speech starts. A piece of video is
kept as-is when the Arabic audio fits in it; otherwise it is slowed down (up to --max-slow)
and then held on its last frame, so the slide on screen always matches what is being said.

Outputs: the MP4 (Arabic audio, soft subtitles: Egyptian Arabic + original English),
matching .ar.srt / .en.srt files, and a bilingual script (.script.md).
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

import numpy as np
import soundfile as sf

from common import WORK, fmt_srt_time, load_json, probe, run, save_json

SR = 24000
RLM = "‏"
# "$50,000", "20%", "59½" - kept left-to-right inside RTL lines: "½" is bidi-neutral and lands on the
# wrong side of the number in any compliant renderer, and libass also misorders a leading "$"
LTR_NUMBER = re.compile(r"[$€£]?\d[\d,.]*\d[%½]?|[$€£]?\d[%½]?")


def plan(units: list[dict], manifest: dict, duration: float, gap: float, max_slow: float, min_piece: float) -> list[dict]:
    pieces = []
    if units[0]["start"] > 0.05:
        pieces.append({"kind": "intro", "src_start": 0.0, "src_end": units[0]["start"], "slow": 1.0, "freeze": 0.0})
    for i, u in enumerate(units):
        src_start = u["start"]
        src_end = units[i + 1]["start"] if i + 1 < len(units) else duration
        span = max(src_end - src_start, min_piece)
        audio = manifest["units"][str(u["id"])]["duration"]
        # the last unit keeps the original outro (end card) after the speech
        tail = gap if i + 1 < len(units) else max(gap, duration - u["end"])
        need = audio + tail
        slow, freeze = 1.0, 0.0
        if need > span:
            slow = min(need / span, max_slow)
            freeze = need - span * slow
        pieces.append({"kind": "unit", "unit": u["id"], "src_start": src_start, "src_end": src_start + span, "slow": slow, "freeze": freeze})
    return pieces


def render_piece(video: Path, piece: dict, fps: str, crf: int, dst: Path) -> float:
    span = piece["src_end"] - piece["src_start"]
    vf = f"setpts={piece['slow']:.6f}*(PTS-STARTPTS)"
    if piece["freeze"] > 0.001:
        vf += f",tpad=stop_mode=clone:stop_duration={piece['freeze']:.3f}"
    vf += f",fps={fps},format=yuv420p"
    run([
        "ffmpeg", "-y", "-ss", f"{piece['src_start']:.3f}", "-t", f"{span:.3f}", "-i", str(video),
        "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf),
        "-video_track_timescale", "90000", str(dst),
    ])
    return probe(dst)["duration"]


def extract_audio(video: Path, start: float, end: float) -> np.ndarray:
    tmp = WORK / "tmp_intro.wav"
    run(["ffmpeg", "-y", "-ss", f"{start:.3f}", "-t", f"{end - start:.3f}", "-i", str(video), "-vn", "-ac", "1", "-ar", str(SR), str(tmp)])
    audio, _ = sf.read(tmp, dtype="float32")
    tmp.unlink()
    return audio


def wrap(text: str, width: int, rtl: bool) -> str:
    """Break into at most two balanced lines at a space near the middle."""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > width:
        mid = len(text) // 2
        spaces = [i for i, c in enumerate(text) if c == " "]
        if spaces:
            cut = min(spaces, key=lambda i: abs(i - mid))
            text = text[:cut] + "\n" + text[cut + 1 :]
    if rtl:
        text = LTR_NUMBER.sub(lambda m: "‪" + m.group(0) + "‬", text)
        text = "\n".join(RLM + line for line in text.split("\n"))
    return text


def split_sentences(text: str, max_chars: int) -> list[str]:
    parts = re.split(r"(?<=[.?!;:,])\s+", text.strip())
    chunks, cur = [], ""
    for p in parts:
        if cur and len(cur) + 1 + len(p) > max_chars:
            chunks.append(cur)
            cur = p
        else:
            cur = f"{cur} {p}".strip()
    if cur:
        chunks.append(cur)
    return chunks


def write_srt(cues: list[list], path: Path) -> None:
    lines = []
    for n, (start, end, text) in enumerate(cues, start=1):
        lines += [str(n), f"{fmt_srt_time(start)} --> {fmt_srt_time(end)}", text, ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_ass(cues: list[list], path: Path, width: int, height: int, font: str) -> None:
    """ASS copy of the Arabic cues for burning in; Encoding=-1 lets libass detect RTL lines."""

    def t(sec: float) -> str:
        cs = max(0, int(round(sec * 100)))
        h, cs = divmod(cs, 360000)
        m, cs = divmod(cs, 6000)
        s, cs = divmod(cs, 100)
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

    size, margin = round(height * 0.047), round(height * 0.035)
    lines = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {width}", f"PlayResY: {height}", "WrapStyle: 0",
        "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
        "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
        "MarginR, MarginV, Encoding",
        f"Style: Default,{font},{size},&H00FFFFFF,&H000000FF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,3,"
        f"{max(2, size // 8)},0,2,{margin},{margin},{margin},-1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for s, e, text in cues:
        lines.append(f"Dialogue: 0,{t(s)},{t(e)},Default,,0,0,0,,{text.replace(chr(10), chr(92) + 'N')}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def settle(cues: list[list], hold: float = 0.4, min_len: float = 1.0) -> list[list]:
    """Let each cue linger a little, without overlapping the next one."""
    for i, cue in enumerate(cues):
        nxt = cues[i + 1][0] - 0.04 if i + 1 < len(cues) else cue[1] + hold
        cue[1] = min(max(cue[1] + hold, cue[0] + min_len), nxt)
    return cues


def write_script_doc(script: dict, units: list[dict], unit_start: dict, manifest: dict, path: Path) -> None:
    title = script.get("title", path.stem)
    lines = [f"# {title}", "", "Egyptian Arabic narration (Nile TTS) · English terminology kept · timestamps refer to the Arabic video", ""]
    if script.get("glossary"):
        lines += ["## Glossary / المصطلحات", "", "| Term (English) | الشرح بالمصري |", "|---|---|"]
        lines += [f"| {g['term']} | {g['ar']} |" for g in script["glossary"]]
        lines.append("")
    lines += ["## Script", ""]
    for u in units:
        t = unit_start[u["id"]]
        m, s = divmod(t, 60)
        lines.append(f"### {u['id']:03d} · {int(m):02d}:{s:04.1f}")
        lines.append("")
        lines.append(f"> **EN:** {u['en']}")
        lines.append("")
        lines.append(RLM + " ".join(p["ar"] for p in u["parts"]))
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video", type=Path, required=True)
    ap.add_argument("--script", type=Path, required=True)
    ap.add_argument("--tts", type=Path, default=WORK / "tts")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--gap", type=float, default=0.35, help="minimum silence after each unit (s)")
    ap.add_argument("--max-slow", type=float, default=1.25, help="max video slow-down before holding the last frame")
    ap.add_argument("--min-piece", type=float, default=0.2)
    ap.add_argument("--crf", type=int, default=20)
    ap.add_argument("--no-intro-audio", action="store_true", help="do not keep the original audio before the first unit")
    ap.add_argument("--burn", action="store_true", help="also write a copy with Arabic subtitles burned in")
    ap.add_argument("--reuse-video", action="store_true", help="skip re-rendering when the timing plan is unchanged (subtitle-only edits)")
    ap.add_argument("--font", default="Noto Sans Arabic", help="font for --burn")
    args = ap.parse_args()

    script = load_json(args.script)
    units = sorted(script["units"], key=lambda u: u["start"])
    manifest = load_json(args.tts / "manifest.json")
    missing = [u["id"] for u in units if str(u["id"]) not in manifest["units"]]
    if missing:
        raise SystemExit(f"no synthesized audio for units {missing}; run synthesize.py")
    info = probe(args.video)
    pieces = plan(units, manifest, info["duration"], args.gap, args.max_slow, args.min_piece)

    video_only = WORK / "video_retimed.mp4"
    report_path = WORK / "assembly_report.json"
    reused = False
    if args.reuse_video and video_only.exists() and report_path.exists():
        old = load_json(report_path)["pieces"]
        keys = ("kind", "unit", "src_start", "src_end", "slow", "freeze")
        if len(old) == len(pieces) and all(all(o.get(k) == p.get(k) for k in keys) for o, p in zip(old, pieces)):
            for o, p in zip(old, pieces):
                p["out_start"], p["out_duration"] = o["out_start"], o["out_duration"]
            reused = True
            print(f"timing unchanged: reusing {video_only}")
        else:
            print("timing changed since the last run: re-rendering the video")

    if not reused:
        seg_dir = WORK / "segments"
        shutil.rmtree(seg_dir, ignore_errors=True)
        seg_dir.mkdir(parents=True)
        cursor = 0.0
        for n, piece in enumerate(pieces):
            dst = seg_dir / f"seg_{n:04d}.mp4"
            piece["out_start"] = cursor
            piece["out_duration"] = render_piece(args.video, piece, info["fps_str"], args.crf, dst)
            cursor += piece["out_duration"]
            print(f"piece {n + 1}/{len(pieces)}: {piece['kind']} slow x{piece['slow']:.2f} hold {piece['freeze']:.2f}s -> {piece['out_duration']:.2f}s")
        concat_list = seg_dir / "list.txt"
        concat_list.write_text("".join(f"file '{p.name}'\n" for p in sorted(seg_dir.glob("seg_*.mp4"))), encoding="utf-8")
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(video_only)])
    total = sum(p["out_duration"] for p in pieces)

    narration = np.zeros(int((total + 1.0) * SR), dtype=np.float32)
    unit_start = {}
    for piece in pieces:
        at = int(round(piece["out_start"] * SR))
        if piece["kind"] == "intro":
            if args.no_intro_audio or not info["has_audio"]:
                continue
            audio = extract_audio(args.video, piece["src_start"], piece["src_end"])
            fade = min(len(audio), int(0.3 * SR))
            audio[len(audio) - fade :] *= np.linspace(1, 0, fade, dtype=np.float32)
        else:
            unit_start[piece["unit"]] = piece["out_start"]
            audio, _ = sf.read(args.tts / manifest["units"][str(piece["unit"])]["file"], dtype="float32")
        narration[at : at + len(audio)] += audio[: len(narration) - at]
    narration = narration[: int(total * SR)]
    narration_wav = WORK / "narration_ar.wav"
    sf.write(narration_wav, narration, SR, subtype="PCM_16")

    ar_cues, en_cues = [], []
    for u in units:
        base = unit_start[u["id"]]
        entry = manifest["units"][str(u["id"])]
        for part, off in zip(u["parts"], entry["parts"]):
            ar_cues.append([base + off["start"], base + off["end"], wrap(part["ar"], 48, rtl=True)])
        chunks = split_sentences(u["en"], 84)
        weights = np.cumsum([0] + [len(c) for c in chunks]) / max(1, sum(len(c) for c in chunks))
        for c, w0, w1 in zip(chunks, weights[:-1], weights[1:]):
            en_cues.append([base + w0 * entry["duration"], base + w1 * entry["duration"], wrap(c, 46, rtl=False)])

    args.out.parent.mkdir(parents=True, exist_ok=True)
    stem = args.out.with_suffix("")
    ar_srt, en_srt = Path(f"{stem}.ar.srt"), Path(f"{stem}.en.srt")
    ar_cues, en_cues = settle(ar_cues), settle(en_cues)
    write_srt(ar_cues, ar_srt)
    write_srt(en_cues, en_srt)

    run([
        "ffmpeg", "-y", "-i", str(video_only), "-i", str(narration_wav), "-i", str(ar_srt), "-i", str(en_srt),
        "-map", "0:v", "-map", "1:a", "-map", "2:s", "-map", "3:s",
        "-c:v", "copy", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", "-c:a", "aac", "-b:a", "160k",
        "-c:s", "mov_text",
        "-metadata:s:a:0", "language=ara", "-metadata:s:a:0", "title=Egyptian Arabic (Nile TTS)",
        "-metadata:s:s:0", "language=ara", "-metadata:s:s:0", "title=Egyptian Arabic",
        "-metadata:s:s:1", "language=eng", "-metadata:s:s:1", "title=English (original narration)",
        "-disposition:s:0", "default", "-disposition:s:1", "0",
        "-movflags", "+faststart", str(args.out),
    ])

    if args.burn:
        burned = Path(f"{stem}_subtitled.mp4")
        ass = WORK / "subtitles_ar.ass"
        write_ass(ar_cues, ass, info["width"], info["height"], args.font)
        ass_arg = str(ass).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
        run([
            "ffmpeg", "-y", "-i", str(args.out), "-map", "0:v", "-map", "0:a",
            "-vf", f"ass='{ass_arg}':shaping=complex",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", str(args.crf), "-c:a", "copy", "-movflags", "+faststart", str(burned),
        ])
        print("burned-in copy ->", burned)

    write_script_doc(script, units, unit_start, manifest, Path(f"{stem}.script.md"))
    save_json({"source_duration": info["duration"], "output_duration": round(total, 3), "pieces": pieces}, WORK / "assembly_report.json")
    print(f"{info['duration']:.1f}s original -> {total:.1f}s Egyptian Arabic video: {args.out}")


if __name__ == "__main__":
    main()
