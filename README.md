# Note-Book-LM: Egyptian Arabic CPA TCP videos

Turns a NotebookLM Video Overview into an Egyptian Arabic version for CPA **TCP** exam study.
The narration is re-voiced with [Nile TTS](https://huggingface.co/KickItLikeShika/NileTTS-XTTS), an XTTS v2 model fine-tuned for Egyptian Arabic.
Tax terminology, definitions, IRC sections, forms, and the original examples stay exactly as in the English video.

## Videos

| Source | Egyptian Arabic version | Length |
|---|---|---|
| TCP M4: Financial Planning (release `v1`) | [MP4 with Arabic + English subtitle tracks](output/TCP_M4_Financial_Planning_Egyptian_Arabic.mp4) · [MP4 with Arabic subtitles burned in](output/TCP_M4_Financial_Planning_Egyptian_Arabic_subtitled.mp4) · [bilingual script + glossary](output/TCP_M4_Financial_Planning_Egyptian_Arabic.script.md) | 10:35 (original 8:26) |

Every line was checked by transcribing the Nile TTS audio back with Whisper. Lines with slurred words, trailing babble or an unclear exam term were re-voiced, keeping the best of four takes.

## Pipeline

| Step | Script | Output |
|---|---|---|
| 1. Transcribe the English narration (faster-whisper large-v3) | `dubbing/transcribe.py` | `script/units_en.json` |
| 2. Pull one frame per slide to read tables and numbers | `dubbing/keyframes.py` | `work/frames/` |
| 3. Egyptian Arabic script, English terminology kept ([rules](docs/translation_style.md)) | written by hand | `script/script_ar.json` |
| 4. Synthesize the narration with Nile TTS | `dubbing/synthesize.py` | `work/tts/` |
| 5. Round-trip check of the audio with Whisper | `dubbing/qa_tts.py` | `work/tts/qa.json` |
| 6. Re-time the slides to the Arabic audio and add subtitles | `dubbing/assemble.py` | `output/` |

`assemble.py` cuts the video where each English sentence starts. When the Arabic runs longer, it slows that stretch (up to ×1.25) and then holds the last frame, so the slide on screen always matches the narration.
The MP4 carries two soft subtitle tracks: Egyptian Arabic, and the original English wording. `--burn` also writes a copy with the Arabic subtitles burned in.

## Run

```bash
bash dubbing/setup.sh                       # deps + Nile TTS + Whisper (needs huggingface.co)
source dubbing/.venv/bin/activate
python dubbing/transcribe.py --video input/original.mp4
python dubbing/keyframes.py  --video input/original.mp4
# write script/script_ar.json from script/units_en.json
python dubbing/synthesize.py --script script/script_ar.json --voice auto --match-video input/original.mp4
python dubbing/qa_tts.py     --script script/script_ar.json
python dubbing/assemble.py   --video input/original.mp4 --script script/script_ar.json \
    --out output/video_egyptian_arabic.mp4 --burn
```

`--voice auto` picks the Nile TTS male or female voice to match the original narrator's pitch; `--voice male` or `--voice female` forces one.

Re-voice lines the QA step flags with `synthesize.py --only 12,34 --pick-best 4` (four takes each, Whisper keeps the clearest), check them with `qa_tts.py --only 12,34`, and re-run `assemble.py`. After subtitle-only edits, `assemble.py --reuse-video` skips re-rendering the video.

## Credits

Nile TTS model and dataset by Ahmed Khamis and Hesham Ali Ahmed, Apache-2.0 ([paper](https://arxiv.org/abs/2602.15675), [code](https://github.com/KickItLikeShika/NileTTS)).
