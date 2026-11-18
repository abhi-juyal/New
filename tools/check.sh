#!/usr/bin/env bash
# Quick health check for the video toolchain. Usage: bash tools/check.sh
cd "$(dirname "$0")/.."
export PATH="$HOME/.local/bin:$PATH"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
ok(){ printf "  [OK]   %-12s %s\n" "$1" "$2"; }
bad(){ printf "  [FAIL] %-12s %s\n" "$1" "$2"; }

ffmpeg -v error -f lavfi -i testsrc=d=1:s=320x240 -c:v libx264 "$T/t.mp4" 2>/dev/null \
  && ok ffmpeg "$(ffmpeg -version | head -1 | cut -d' ' -f3)" || bad ffmpeg "encode failed"
yt-dlp --version >/dev/null 2>&1 && ok yt-dlp "$(yt-dlp --version)" || bad yt-dlp "not installed"
if have_tts=$(command -v espeak-ng) && espeak-ng -w "$T/s.wav" "testing one two three" \
   && whisper "$T/s.wav" --model tiny.en --fp16 False --output_dir "$T" --output_format txt >/dev/null 2>&1; then
  ok whisper "heard: $(tr -d '\n' < "$T/s.txt")"
else bad whisper "transcription failed"; fi
(cd templates/remotion-starter && timeout 300 npx remotion render MyComp "$T/r.mp4" --frames=0-9 >/dev/null 2>&1) \
  && ok remotion "$(node -p "require('./templates/remotion-starter/node_modules/remotion/package.json').version")" || bad remotion "render failed"
(cd templates/hyperframes-starter && timeout 300 hyperframes render -o "$T/h.mp4" -q draft --quiet >/dev/null 2>&1) \
  && ok hyperframes "$(hyperframes --version)" || bad hyperframes "render failed"
python3 tools/media_search.py search whoosh --type sfx -n 1 >/dev/null 2>&1 \
  && ok openverse "search API reachable" || bad openverse "search failed"
