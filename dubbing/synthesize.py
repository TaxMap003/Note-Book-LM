"""Synthesize the Egyptian Arabic narration with Nile TTS (XTTS v2 fine-tuned on Egyptian Arabic).

    python dubbing/synthesize.py --script script/script_ar.json --voice auto --match-video input/original.mp4

Every part of a unit is one XTTS call (and later one subtitle cue). Parts are joined into
work/tts/unit_NNN.wav; work/tts/manifest.json records durations and part offsets for the
assembler. Units whose text and settings did not change are reused on re-runs.

--code-switch mixed   whole part in Arabic mode; English terms stay in Latin script (default)
--code-switch split   English runs synthesized in English mode with the same cloned voice
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import tempfile
import time
from pathlib import Path

import numpy as np
import soundfile as sf

from common import MODELS, WORK, check_tts_text, latin_runs, load_json, run, save_json

SR = 24000
AR_CHARS_PER_SEC = 14.0  # typical Nile TTS speaking rate, used only to catch runaway/truncated output


def estimate_f0(video: Path, seconds: int = 60) -> float:
    import librosa

    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "a.wav"
        run(["ffmpeg", "-y", "-i", str(video), "-t", str(seconds), "-vn", "-ac", "1", "-ar", "16000", str(wav)])
        y, sr = librosa.load(wav, sr=16000)
    # YIN on the louder (voiced) frames; pYIN is far slower for the same answer here
    f0 = librosa.yin(y, fmin=60, fmax=400, sr=sr, frame_length=1024, hop_length=256)
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0]
    n = min(len(f0), len(rms))
    voiced = rms[:n] > np.percentile(rms[:n], 60)
    return float(np.median(f0[:n][voiced]))


def resolve_voice(voice: str, match_video: Path | None, voices_dir: Path) -> tuple[list[Path], str]:
    p = Path(voice)
    if p.is_file():
        return [p], p.stem
    if p.is_dir():
        return sorted(p.glob("*.wav")), p.name
    if voice == "auto":
        if match_video is None:
            raise SystemExit("--voice auto needs --match-video to pick the speaker matching the original narrator")
        f0 = estimate_f0(match_video)
        voice = "female" if f0 >= 165 else "male"
        print(f"original narrator median F0 {f0:.0f} Hz -> {voice} Nile TTS voice")
    files = sorted((voices_dir / voice).glob("*.wav"))
    if not files:
        raise SystemExit(f"no reference clips in {voices_dir / voice}; run dubbing/download_models.py first")
    return files, voice


def load_model(model_dir: Path, threads: int):
    import torch
    from TTS.tts.configs.xtts_config import XttsConfig
    from TTS.tts.models.xtts import Xtts

    torch.set_num_threads(threads)
    config = XttsConfig()
    config.load_json(str(model_dir / "config.json"))
    model = Xtts.init_from_config(config)
    ckpt = model_dir / "model_slim.pth"
    if not ckpt.exists():
        ckpt = model_dir / "model.pth"
    model.load_checkpoint(config, checkpoint_path=str(ckpt), vocab_path=str(model_dir / "vocab.json"), eval=True)
    return model


def trim_silence(wav: np.ndarray, top_db: float = 40.0, pad: float = 0.05) -> np.ndarray:
    import librosa

    if wav.size == 0:
        return wav
    _, (start, end) = librosa.effects.trim(wav, top_db=top_db, frame_length=1024, hop_length=256)
    p = int(pad * SR)
    return wav[max(0, start - p) : min(len(wav), end + p)]


class Synth:
    def __init__(self, model, refs: list[Path], args):
        import torch

        self.torch = torch
        self.model = model
        self.args = args
        self.latent, self.embedding = model.get_conditioning_latents(
            audio_path=[str(r) for r in refs], gpt_cond_len=args.gpt_cond_len, gpt_cond_chunk_len=6, max_ref_length=15
        )

    def _once(self, text: str, lang: str, seed: int) -> np.ndarray:
        self.torch.manual_seed(seed)
        out = self.model.inference(
            text,
            lang,
            self.latent,
            self.embedding,
            temperature=self.args.temperature,
            repetition_penalty=self.args.repetition_penalty,
            top_p=self.args.top_p,
            speed=self.args.speed,
            enable_text_splitting=False,
        )
        return trim_silence(np.asarray(out["wav"], dtype=np.float32))

    def say(self, text: str, lang: str, seed: int) -> np.ndarray:
        """Synthesize with retries when the duration is implausible (XTTS babbling or truncation)."""
        expected = max(0.6, len(text) / AR_CHARS_PER_SEC)
        best, best_err = None, math.inf
        for attempt in range(self.args.retries + 1):
            wav = self._once(text, lang, seed + 1000 * attempt)
            ratio = (len(wav) / SR) / expected
            err = abs(math.log(max(ratio, 1e-3)))
            if err < best_err:
                best, best_err = wav, err
            if 0.55 <= ratio <= 1.9:
                break
            print(f"    retry: {len(wav) / SR:.1f}s for {len(text)} chars (ratio {ratio:.2f})")
        return best

    def best(self, text: str, seed: int, takes: int) -> np.ndarray:
        """Voice several takes and keep the one Whisper hears best (Arabic words + English terms)."""
        from qa_tts import arabic_recall, norm_ar, term_recall
        from scipy.signal import resample_poly

        if getattr(self, "whisper", None) is None:
            from faster_whisper import WhisperModel

            self.whisper = WhisperModel(str(MODELS / "faster-whisper-large-v3"), device="cpu", compute_type="int8",
                                        cpu_threads=self.args.threads)
        best, best_score = None, -math.inf
        for k in range(takes):
            wav = self.part(text, seed + 7919 * k)
            segments, _ = self.whisper.transcribe(resample_poly(wav, 2, 3).astype(np.float32), language="ar",
                                                  beam_size=5, vad_filter=False)
            heard = " ".join(s.text.strip() for s in segments)
            ratio = len(norm_ar(heard)) / max(1, len(norm_ar(text)))
            score = arabic_recall(text, heard) + term_recall(text, heard) - 2 * max(0.0, abs(math.log(max(ratio, 1e-3))) - math.log(1.25))
            print(f"    take {k + 1}: score {score:.2f} heard: {heard}")
            if score > best_score:
                best, best_score = wav, score
        return best

    def part(self, text: str, seed: int) -> np.ndarray:
        if self.args.code_switch == "mixed":
            return self.say(text, "ar", seed)
        pieces = []
        for i, (lang, chunk) in enumerate(latin_runs(text)):
            pieces.append(self.say(chunk, lang, seed + i))
            pieces.append(np.zeros(int(0.04 * SR), dtype=np.float32))
        return np.concatenate(pieces[:-1]) if pieces else np.zeros(0, dtype=np.float32)


def unit_key(unit: dict, voice_files: list[Path], args) -> str:
    payload = {
        "parts": [p.get("tts") or p["ar"] for p in unit["parts"]],
        "voice": [f.name for f in voice_files],
        "settings": [args.code_switch, args.temperature, args.repetition_penalty, args.top_p, args.speed, args.gpt_cond_len, args.seed,
                     args.pick_best],
    }
    return hashlib.sha1(json.dumps(payload, ensure_ascii=False).encode()).hexdigest()[:16]


def validate(units: list[dict]) -> None:
    bad = []
    for u in units:
        if not u.get("parts"):
            bad.append(f"unit {u['id']}: no parts (not translated yet)")
        for j, p in enumerate(u.get("parts", []), start=1):
            for problem in check_tts_text(p.get("tts") or p["ar"]):
                bad.append(f"unit {u['id']} part {j}: {problem}")
    if bad:
        raise SystemExit("script problems:\n  " + "\n  ".join(bad))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--script", type=Path, required=True)
    ap.add_argument("--model-dir", type=Path, default=MODELS / "NileTTS-XTTS")
    ap.add_argument("--voice", default="auto", help="auto | male | female | path to a .wav or a folder of .wav")
    ap.add_argument("--match-video", type=Path, help="original video, used by --voice auto")
    ap.add_argument("--out", type=Path, default=WORK / "tts")
    ap.add_argument("--code-switch", choices=["mixed", "split"], default="mixed")
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--repetition-penalty", type=float, default=5.0)
    ap.add_argument("--top-p", type=float, default=0.85)
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--gpt-cond-len", type=int, default=24)
    ap.add_argument("--retries", type=int, default=2)
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--only", help="comma-separated unit ids to (re)generate")
    ap.add_argument("--pick-best", type=int, default=1, help="voice N takes per part and keep the one Whisper hears best")
    ap.add_argument("--pause", type=float, default=0.22, help="silence between parts (s)")
    ap.add_argument("--sentence-pause", type=float, default=0.38, help="silence after a part ending a sentence (s)")
    args = ap.parse_args()

    script = load_json(args.script)
    units = script["units"]
    only = {int(x) for x in args.only.split(",")} if args.only else None
    todo = [u for u in units if only is None or u["id"] in only]
    validate(todo)

    voice_files, voice_name = resolve_voice(args.voice, args.match_video, MODELS / "voices")
    args.out.mkdir(parents=True, exist_ok=True)
    manifest_path = args.out / "manifest.json"
    manifest = load_json(manifest_path) if manifest_path.exists() else {"units": {}}
    manifest["voice"] = voice_name

    synth = None
    t0 = time.time()
    for n, unit in enumerate(todo, start=1):
        key = unit_key(unit, voice_files, args)
        wav_path = args.out / f"unit_{unit['id']:03d}.wav"
        entry = manifest["units"].get(str(unit["id"]))
        if entry and entry.get("key") == key and wav_path.exists():
            continue
        if synth is None:
            print(f"loading Nile TTS from {args.model_dir} (voice: {voice_name}, {len(voice_files)} reference clips)")
            synth = Synth(load_model(args.model_dir, args.threads), voice_files, args)

        pieces, offsets, cursor = [], [], 0.0
        for j, part in enumerate(unit["parts"]):
            text = part.get("tts") or part["ar"]
            seed = args.seed + unit["id"] * 10 + j
            audio = synth.best(text, seed, args.pick_best) if args.pick_best > 1 else synth.part(text, seed)
            offsets.append({"start": round(cursor, 3), "end": round(cursor + len(audio) / SR, 3)})
            pieces.append(audio)
            cursor += len(audio) / SR
            if j < len(unit["parts"]) - 1:
                gap = args.sentence_pause if text.rstrip().endswith((".", "؟", "?", "!", ":")) else args.pause
                pieces.append(np.zeros(int(gap * SR), dtype=np.float32))
                cursor += gap
        audio = np.concatenate(pieces)
        peak = float(np.max(np.abs(audio))) or 1.0
        sf.write(wav_path, audio / peak * 0.9, SR, subtype="PCM_16")
        manifest["units"][str(unit["id"])] = {"file": wav_path.name, "duration": round(len(audio) / SR, 3), "parts": offsets, "key": key}
        save_json(manifest, manifest_path)
        elapsed = time.time() - t0
        print(f"[{n}/{len(todo)}] unit {unit['id']}: {len(audio) / SR:.1f}s audio ({elapsed / 60:.1f} min elapsed)")

    print(f"done -> {manifest_path}")


if __name__ == "__main__":
    main()
