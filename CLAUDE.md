# AI Video Editing Workspace

This folder is my video editing workspace. Read this file first in every session,
then check the relevant folder's `README.md` before working with its files.

## Where my files live

| Folder              | Contents                                                                 |
|---------------------|--------------------------------------------------------------------------|
| `raw-videos/`       | Original, unedited footage. **Read-only — never modify or overwrite.**   |
| `references/`       | Clips showing exactly how an edit should look. Follow these closely.     |
| `inspirations/`     | Mood board: loose ideas for vibe, color, transitions. Use as guidance.   |
| `brand-kit/`        | Logos, colors, brand fonts, intros/outros, style guide.                  |
| `assets/music/`     | Background music tracks.                                                 |
| `assets/sfx/`       | Sound effects (whooshes, pops, risers…).                                 |
| `assets/images/`    | Stills, overlays, stickers, textures.                                    |
| `assets/fonts/`     | Font files for titles and captions.                                      |
| `skills/`           | My editing recipes. Read the matching one before doing that kind of edit.|
| `projects/`         | One folder per video in progress (brief, script, notes, working files).  |
| `exports/`          | Final, ready-to-publish renders only.                                    |

## Workflow

1. **Start from a brief.** For a new video, create `projects/YYYY-MM-DD_project-name/`
   with a `brief.md` (goal, platform, length, audience, deadline). Ask me if anything is unclear.
2. **Check style sources** — `brand-kit/`, any relevant `references/`, and `skills/` — before editing.
3. **Work non-destructively.** Pull footage from `raw-videos/`; put intermediates
   (proxies, cut lists, subtitles, test renders) in `projects/<name>/working/`.
4. **Log decisions** in `projects/<name>/notes.md` so edits are repeatable.
5. **Export** finals to `exports/` as `YYYY-MM-DD_project-name_platform_vN.ext`.
   Never overwrite a previous version — bump `vN`.

## How I like my videos edited

> Defaults — edit this section to match your taste. Project briefs override these.

- **Pacing:** tight. Cut silences, dead air, and filler words ("um", "uh", "like").
- **Hook:** the first 1–3 seconds must grab attention; lead with the strongest moment.
- **Captions:** on by default, burned in, large and readable, brand font, max ~2 lines, high contrast.
- **Audio:** dialogue clear and on top; music ducked under speech; loudness about -14 LUFS for social.
  Use SFX sparingly to punctuate cuts and text pop-ins.
- **Branding:** brand colors and fonts from `brand-kit/`; logo/outro where appropriate.
- **Visuals:** keep it clean — subtle zoom punch-ins and B-roll to hide jump cuts; avoid cheesy transitions.
- **Formats:**
  - Shorts / Reels / TikTok: 1080×1920 (9:16), 30 fps, under 60 s unless the brief says otherwise
  - YouTube / landscape: 1920×1080 (16:9) or 4K, 30 fps
  - Export H.264 MP4, AAC audio

## Tools

Install everything with `bash setup.sh` (skips what's already installed). Health check: `bash tools/check.sh`.

| Tool | Use it for | How |
|------|-----------|-----|
| **FFmpeg** | Cutting, joining, scaling, audio mixing, burning in captions | `ffmpeg` (has libx264, libass, AAC) |
| **yt-dlp** | Downloading reference/inspiration clips I link | `yt-dlp -o "references/%(title)s.%(ext)s" <url>` |
| **Whisper** | Transcripts and captions (SRT/VTT/word timings) | `whisper in.mp4 --model small.en --output_format srt --fp16 False` (CPU; `base.en` is faster, `small.en`/`medium.en` more accurate; drop `.en` for non-English) |
| **Remotion** | React-based motion graphics, title cards, animated captions | Starter in `templates/remotion-starter/`: copy it into the project, then `npx remotion render MyComp out.mp4` |
| **HyperFrames** | HTML + GSAP motion graphics; ~450 ready-made blocks (captions, titles, transitions) | Starter in `templates/hyperframes-starter/`; `hyperframes render`. Skills in `.claude/skills/hyperframes*` |
| **Openverse** | Searching free SFX and music (Freesound, Wikimedia, Jamendo) | `python3 tools/media_search.py search whoosh --type sfx --commercial`, then `... download <id>` (logs the license to `CREDITS.md`) |

- Use FFmpeg for cutting, concatenating, scaling, audio mixing and burning in subtitles unless a project says otherwise.
- Use Remotion or HyperFrames for animated graphics, then composite them over footage with FFmpeg.
- Show me the command plan before long or batch renders.
- For music and SFX, prefer `--commercial` (cc0 / by / by-sa) results. Never use `nc` or `nd` licenses for client or monetized videos. Credit `by` licenses in the video description.
- **Cloud-session limits:** Freesound and Wikimedia block or rate-limit downloads from this cloud server (search still works), and YouTube isn't reachable here. Jamendo music downloads work. On my own computer all of them work.

## Rules

- Never delete or modify anything in `raw-videos/`.
- Only use assets in `assets/` and `brand-kit/` (or ones I explicitly provide) — respect licenses.
- Large media files are git-ignored (see `.gitignore`); only structure and notes are committed.
