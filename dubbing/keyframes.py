"""Extract one frame per slide/scene change so on-screen examples and numbers can be read.

    python dubbing/keyframes.py --video input/original.mp4

Writes work/frames/scene_NNNN.jpg and work/frames/scenes.json ([{file, time}]).
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from common import WORK, probe, save_json

PTS = re.compile(r"pts_time:([0-9.]+)")


def extract(video: Path, out_dir: Path, threshold: float, width: int) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("scene_*.jpg"):
        old.unlink()
    vf = f"select='eq(n,0)+gt(scene,{threshold})',showinfo,scale={width}:-2"
    proc = subprocess.run(
        ["ffmpeg", "-y", "-i", str(video), "-vf", vf, "-fps_mode", "vfr", "-q:v", "3", str(out_dir / "scene_%04d.jpg")],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr[-3000:])
    times = [float(m.group(1)) for line in proc.stderr.splitlines() if "showinfo" in line for m in [PTS.search(line)] if m]
    files = sorted(out_dir.glob("scene_*.jpg"))
    return [{"file": f.name, "time": round(t, 3)} for f, t in zip(files, times)]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=WORK / "frames")
    ap.add_argument("--threshold", type=float, default=0.25, help="ffmpeg scene score (lower = more frames)")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--min-frames-per-minute", type=float, default=4.0, help="lower the threshold until reached")
    args = ap.parse_args()

    minutes = probe(args.video)["duration"] / 60
    threshold = args.threshold
    scenes = extract(args.video, args.out, threshold, args.width)
    while len(scenes) < args.min_frames_per_minute * minutes and threshold > 0.06:
        threshold = round(threshold * 0.6, 3)
        scenes = extract(args.video, args.out, threshold, args.width)
    save_json({"threshold": threshold, "scenes": scenes}, args.out / "scenes.json")
    print(f"{len(scenes)} frames at scene threshold {threshold} -> {args.out}")


if __name__ == "__main__":
    main()
