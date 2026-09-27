#!/usr/bin/env bash
# Installs the dubbing pipeline and downloads Nile TTS + Whisper.
# Needs pypi.org, an apt mirror, and huggingface.co / *.hf.co to be reachable.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="${VENV:-$HERE/.venv}"

if ! command -v ffmpeg >/dev/null; then
  apt-get update -qq && apt-get install -y -qq ffmpeg
fi
# Arabic fonts for burned-in subtitles (assemble.py --burn)
fc-list :lang=ar family | grep -qi "Noto Sans Arabic" || apt-get install -y -qq fonts-noto-core

python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install -q --upgrade pip wheel
# transformers 5 removed an API that coqui-tts' XTTS still imports
"$VENV/bin/python" -m pip install -q "torch==2.8.0" "torchaudio==2.8.0" "coqui-tts==0.27.5" \
  "transformers>=4.57,<5" faster-whisper soundfile numpy huggingface_hub

cd "$HERE"
"$VENV/bin/python" download_models.py
echo "ready: activate with  source $VENV/bin/activate"
