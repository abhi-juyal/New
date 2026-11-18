#!/usr/bin/env python3
"""Search and download free sound effects and music from Openverse.

Openverse (https://openverse.org) indexes openly licensed audio from
Freesound, Wikimedia Commons and Jamendo. No API key is needed.

Examples:
  python3 tools/media_search.py search whoosh --type sfx
  python3 tools/media_search.py search "upbeat corporate" --type music --commercial
  python3 tools/media_search.py download <id>            # saves to assets/sfx or assets/music
  python3 tools/media_search.py download <id> --name whoosh_01

Every download is logged with its license and attribution in
assets/<folder>/CREDITS.md. Check the license before publishing:
  cc0 / pdm          free for anything, no credit needed
  by / by-sa         credit the creator (by-sa: share alike)
  *-nc               non-commercial only (not for monetized/client work)
  *-nd               no derivatives (risky for edited videos)
"""
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.openverse.org/v1/audio/"
UA = "ai-video-workspace/1.0"
ROOT = Path(__file__).resolve().parent.parent
# Freesound sounds carry no category in Openverse, so SFX = search the SFX sources.
SFX_SOURCES = "freesound,wikimedia_audio"


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def search(args):
    params = {"q": args.query, "page_size": args.n, "mature": "false"}
    if args.type == "music":
        params["category"] = "music"
    elif args.type == "sfx" and not args.source:
        params["source"] = SFX_SOURCES
    if args.commercial:
        params["license_type"] = "commercial,modification"
    if args.source:
        params["source"] = args.source
    if args.max_seconds:
        params["length"] = "short" if args.max_seconds <= 30 else "medium"
    data = get_json(API + "?" + urllib.parse.urlencode(params))
    rows = data["results"]
    if args.json:
        print(json.dumps(rows, indent=2))
        return
    print(f"{data['result_count']} results for '{args.query}' (showing {len(rows)})\n")
    for r in rows:
        secs = (r.get("duration") or 0) / 1000
        print(f"{r['id']}  {secs:6.1f}s  {r['license']:<8} {r['source']:<15} {r['title'][:60]}")
    print("\nDownload with: python3 tools/media_search.py download <id>")


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:50] or "audio"


def download(args):
    info = get_json(f"{API}{args.id}/")
    category = info.get("category") or ""
    is_music = category == "music" or info.get("source") == "jamendo"
    folder = args.to or ("assets/music" if is_music else "assets/sfx")
    dest_dir = ROOT / folder
    dest_dir.mkdir(parents=True, exist_ok=True)
    ext = (info.get("filetype") or Path(urllib.parse.urlparse(info["url"]).path).suffix.lstrip(".") or "mp3")
    if ext == "mp32":
        ext = "mp3"
    dest = dest_dir / f"{args.name or slug(info['title'])}.{ext}"

    req = urllib.request.Request(info["url"], headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
            f.write(r.read())
    except Exception as e:  # source CDN refused (rate limit, region/IP block)
        sys.exit(f"Download failed from {info['source']} ({e}). Try another result, "
                 f"or open {info.get('foreign_landing_url')} in a browser.")

    credits = dest_dir / "CREDITS.md"
    if not credits.exists():
        credits.write_text("# Credits\n\n| File | Title | Creator | License | Source |\n|---|---|---|---|---|\n")
    lic = f"{info['license']} {info.get('license_version') or ''}".strip()
    with open(credits, "a") as f:
        f.write(f"| {dest.name} | {info['title']} | {info.get('creator') or 'unknown'} | "
                f"[{lic}]({info.get('license_url')}) | {info.get('foreign_landing_url')} |\n")
    print(f"Saved {dest.relative_to(ROOT)}  ({info['license']}, by {info.get('creator')})")
    if info.get("attribution"):
        print(f"Attribution: {info['attribution']}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="search Openverse audio")
    s.add_argument("query")
    s.add_argument("--type", choices=["sfx", "music", "any"], default="any")
    s.add_argument("--commercial", action="store_true", help="only licenses allowing commercial use + edits")
    s.add_argument("--source", help="comma list: freesound,wikimedia_audio,jamendo")
    s.add_argument("--max-seconds", type=int, help="prefer short clips")
    s.add_argument("-n", type=int, default=15)
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=search)
    d = sub.add_parser("download", help="download a result by id")
    d.add_argument("id")
    d.add_argument("--to", help="folder relative to workspace (default assets/sfx or assets/music)")
    d.add_argument("--name", help="file name without extension")
    d.set_defaults(func=download)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
