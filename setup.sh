#!/usr/bin/env bash
# Installs the AI video editing toolchain. Safe to re-run: skips what is already installed.
# Run from the workspace root:  bash setup.sh
set -euo pipefail
cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:$PATH"

have() { command -v "$1" >/dev/null 2>&1; }

# FFmpeg (+ espeak-ng for quick local voice tests)
if ! have ffmpeg || ! have espeak-ng; then
  apt-get update -qq && apt-get install -y -qq ffmpeg espeak-ng
fi

# uv (Python tool installer)
have uv || curl -LsSf https://astral.sh/uv/install.sh | sh

# yt-dlp
have yt-dlp || uv tool install "yt-dlp[default]"

# Whisper (OpenAI) with CPU-only PyTorch, in its own venv
if ! have whisper; then
  uv venv -q -p 3.12 "$HOME/.venvs/whisper"
  VIRTUAL_ENV="$HOME/.venvs/whisper" uv pip install -q torch --index-url https://download.pytorch.org/whl/cpu
  VIRTUAL_ENV="$HOME/.venvs/whisper" uv pip install -q openai-whisper
  mkdir -p "$HOME/.local/bin" && ln -sf "$HOME/.venvs/whisper/bin/whisper" "$HOME/.local/bin/whisper"
fi

# HyperFrames CLI
have hyperframes || npm install -g hyperframes@latest

# Remotion starter dependencies
if [ -f templates/remotion-starter/package.json ] && [ ! -d templates/remotion-starter/node_modules ]; then
  (cd templates/remotion-starter && npm ci --no-audit --no-fund)
fi

echo "Setup complete: ffmpeg, yt-dlp, whisper, remotion, hyperframes."
