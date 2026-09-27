"""Download Nile TTS, a faster-whisper model, and Nile TTS reference voice clips.

Needs huggingface.co and *.hf.co to be reachable from this machine.

    python dubbing/download_models.py
"""

from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

import soundfile as sf
import torch
from huggingface_hub import HfApi, hf_hub_download, snapshot_download

from common import MODELS, save_json

NILE_REPO = "KickItLikeShika/NileTTS-XTTS"
DATASET_REPO = "KickItLikeShika/NileTTS-dataset"
WHISPER_REPO = "Systran/faster-whisper-large-v3"
# Speaker labels documented on the NileTTS dataset card.
SPEAKERS = {"male": "SPEAKER_01", "female": "SPEAKER_02"}


def download_nile(out: Path) -> Path:
    target = out / "NileTTS-XTTS"
    slim = target / "model_slim.pth"
    patterns = ["config.json", "vocab.json", "mel_stats.pth"]
    if not slim.exists():
        patterns.append("model.pth")
    snapshot_download(NILE_REPO, local_dir=target, allow_patterns=patterns)
    if not slim.exists():
        strip_checkpoint(target / "model.pth", slim)
    return target


def strip_checkpoint(src: Path, dst: Path) -> None:
    """The published model.pth is a 5.6 GB training checkpoint; keep only inference weights."""
    try:
        ckpt = torch.load(src, map_location="cpu", mmap=True, weights_only=False)
    except RuntimeError:
        ckpt = torch.load(src, map_location="cpu", weights_only=False)
    state = ckpt["model"] if "model" in ckpt else ckpt
    drop = ("dvae.", "xtts.dvae.", "torch_mel_spectrogram_dvae.", "xtts.torch_mel_spectrogram_dvae.")
    state = {k: v for k, v in state.items() if not k.startswith(drop)}
    torch.save({"model": state}, dst)
    print(f"slim checkpoint: {dst} ({dst.stat().st_size / 1e9:.2f} GB), removing {src.name}")
    src.unlink()


def download_reference_voices(out: Path, per_speaker: int, seed: int = 7) -> None:
    """Pick clean mid-length utterances per Nile TTS speaker for XTTS voice conditioning."""
    api = HfApi()
    files = api.list_repo_files(DATASET_REPO, repo_type="dataset")
    by_name = {Path(f).name: f for f in files if f.endswith(".wav")}
    metas = sorted((f for f in files if f.endswith(".csv")), key=lambda f: ("eval" not in f and "test" not in f, f))
    if not metas:
        raise SystemExit(f"no metadata CSV found in {DATASET_REPO}")
    meta_path = hf_hub_download(DATASET_REPO, metas[0], repo_type="dataset")
    with open(meta_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="|"))

    rng = random.Random(seed)
    catalog = {}
    for voice, label in SPEAKERS.items():
        # 90-180 characters is roughly 7-14 seconds of speech.
        pool = [r for r in rows if r.get("speaker_name") == label and 90 <= len(r.get("text", "")) <= 180]
        pool = [r for r in pool if Path(r["audio_file"]).name in by_name]
        general = [r for r in pool if Path(r["audio_file"]).name.startswith("general")]
        picks = rng.sample(general if len(general) >= per_speaker else pool, min(per_speaker, len(pool)))
        voice_dir = out / "voices" / voice
        voice_dir.mkdir(parents=True, exist_ok=True)
        catalog[voice] = []
        for r in picks:
            src = hf_hub_download(DATASET_REPO, by_name[Path(r["audio_file"]).name], repo_type="dataset")
            audio, sr = sf.read(src, dtype="float32")
            dst = voice_dir / Path(r["audio_file"]).name
            sf.write(dst, audio, sr)
            catalog[voice].append({"file": str(dst.relative_to(out)), "text": r["text"], "seconds": round(len(audio) / sr, 2)})
        print(f"{voice}: {len(catalog[voice])} reference clips")
    save_json(catalog, out / "voices" / "voices.json")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=MODELS)
    ap.add_argument("--whisper", default=WHISPER_REPO, help="faster-whisper model repo")
    ap.add_argument("--ref-clips", type=int, default=5, help="reference clips per speaker")
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    print("Nile TTS ->", download_nile(args.out))
    whisper_dir = args.out / args.whisper.split("/")[-1]
    snapshot_download(args.whisper, local_dir=whisper_dir)
    print("Whisper ->", whisper_dir)
    download_reference_voices(args.out, args.ref_clips)


if __name__ == "__main__":
    main()
