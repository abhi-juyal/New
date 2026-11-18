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

Use `ffmpeg` for cutting, concatenating, scaling, audio mixing, and burning in subtitles
unless a project says otherwise. Show me the command plan before long or batch renders.

## Rules

- Never delete or modify anything in `raw-videos/`.
- Only use assets in `assets/` and `brand-kit/` (or ones I explicitly provide) — respect licenses.
- Large media files are git-ignored (see `.gitignore`); only structure and notes are committed.
