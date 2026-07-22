#!/usr/bin/env python3
"""remotion_scenes.py — fill slate beats with palette-matched Remotion scenes.

Template-first, create-on-gap, human-gated promotion. Renders each slate beat that
carries a `shot.remotion.pattern` to `media/<BID>.mp4`, stamps provenance back into the
beat sheet, and maintains the pattern->consumers reverse index. The compiler
(compile.py) then picks up media/<BID>.mp4 as the top slot and conforms its
duration to the beat's actual_duration_s.

Usage:
  python3 scripts/remotion_scenes.py <REEL> [--list] [--only B04] [--force]
                                         [--outro] [--now <iso8601>]

Browser: on the Mac, Remotion's default works. In a constrained/allowlisted env set
  ART_CHROME=<chrome or headless-shell binary>  ART_CHROME_MODE=chrome-for-testing
"""
import argparse, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]                       # runtime/
PROJECT = HERE / "remotion"        # the Remotion project
ENTRY = "src/index.ts"
CONSUMERS = HERE / "remotion" / "_bench" / "consumers.json"
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")


def load(p):
    return json.loads(Path(p).read_text())


def slate_resolves(folder: Path, bid: str) -> bool:
    """True if the beat currently has no filled video slot (would be a slate)."""
    for rel in (f"media/{bid}.mp4", f"manim/{bid}.mp4", f"manim/{bid}.mov"):
        if (folder / rel).exists():
            return False
    return True


def browser_flags():
    flags = []
    chrome = os.environ.get("ART_CHROME")
    mode = os.environ.get("ART_CHROME_MODE")
    if chrome:
        flags += [f"--browser-executable={chrome}"]
    if mode:
        flags += [f"--chrome-mode={mode}"]
    return flags


def extend_clip_to_duration(out: Path, duration_s: float) -> None:
    """Extend a rendered clip to duration_s by freeze-holding the last frame.
    Eliminates extreme slow-mo stretching in compile.py for short Remotion
    compositions (e.g. ClaudeWindow=12s matched to 60s+ audio beats).
    """
    tmp = out.parent / f"_ext_{out.name}"
    cmd = [FFMPEG, "-y", "-i", str(out),
           "-vf", f"tpad=stop_mode=clone:stop_duration={duration_s:.3f}",
           "-t", f"{duration_s:.3f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "12",
           "-pix_fmt", "yuv420p", str(tmp)]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode == 0:
        shutil.move(str(tmp), str(out))
    else:
        tmp.unlink(missing_ok=True)


def render_beat(folder: Path, beat: dict, force: bool) -> str:
    bid = beat["beat_id"]
    rem = beat.get("shot", {}).get("remotion") or {}
    pattern = rem.get("pattern")
    if not pattern:
        return "skip: no shot.remotion.pattern"
    out = folder / "media" / f"{bid}.mp4"
    if out.exists() and not force:
        return f"exists: {out.name} (use --force to re-render)"
    out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(rem.get("props", {}), f)
        props_path = f.name
    # --scale=2 renders the 1920x1080 comps at true 3840x2160 (supersampled text).
    # --image-format=png removes Remotion's default JPEG-q80 frame step (the hidden
    # quality ceiling on flat brand color + text). --crf=16 for a clean master.
    cmd = ["npx", "remotion", "render", ENTRY, pattern, str(out.resolve()),
           f"--props={props_path}", "--concurrency=1",
           "--scale=2", "--image-format=png", "--crf=16"] + browser_flags()
    r = subprocess.run(cmd, cwd=PROJECT, capture_output=True, text=True)
    os.unlink(props_path)
    if r.returncode != 0:
        return f"FAIL: {pattern}\n{r.stderr[-800:]}"

    # If beat has a measured audio duration, extend the render with freeze-hold so
    # compile.py gets a clip at the exact beat length (no extreme slow-mo stretching).
    duration_s = beat.get("actual_duration_s") or beat.get("estimated_duration_s")
    if duration_s:
        extend_clip_to_duration(out, float(duration_s))
        return f"ok: {pattern} -> media/{bid}.mp4 (extended to {float(duration_s):.1f}s)"
    return f"ok: {pattern} -> media/{bid}.mp4"


def stamp(beat: dict, folder: Path, now: str):
    bid = beat["beat_id"]
    rem = beat["shot"]["remotion"]
    rem["rendered"] = {"out": f"media/{bid}.mp4", "at": now}


def update_consumers(sheet: dict, folder: Path):
    video = sheet.get("metadata", {}).get("slug", folder.name)
    idx = load(CONSUMERS) if CONSUMERS.exists() else {}
    for b in sheet["beats"]:
        rem = b.get("shot", {}).get("remotion") or {}
        pat = rem.get("pattern")
        if not pat or "rendered" not in rem:
            continue
        rows = idx.setdefault(pat, [])
        row = {"video": video, "beat": b["beat_id"]}
        if row not in rows:
            rows.append(row)
    CONSUMERS.parent.mkdir(parents=True, exist_ok=True)
    CONSUMERS.write_text(json.dumps(idx, indent=1, sort_keys=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reel", type=Path)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--outro", action="store_true")
    ap.add_argument("--now", default="", help="iso8601 timestamp to stamp (scripts have no clock)")
    a = ap.parse_args()
    folder = a.reel.resolve()
    sheet_path = folder / "beat_sheet.json"
    sheet = load(sheet_path)

    # remotion candidates = beats carrying a shot.remotion.pattern
    cands = [b for b in sheet["beats"]
             if (b.get("shot", {}).get("remotion") or {}).get("pattern")]
    if a.only:
        cands = [b for b in cands if b["beat_id"] == a.only]

    if a.list:
        if not cands:
            print("[remotion] no beats carry shot.remotion.pattern")
            return
        for b in cands:
            bid = b["beat_id"]
            rem = b["shot"]["remotion"]
            state = "SLATE" if slate_resolves(folder, bid) else "filled"
            print(f"  {bid:5} {state:6} scene_type={b['shot'].get('scene_type','?'):14} "
                  f"pattern={rem['pattern']}  ({rem.get('provenance','reel-local')})")
        return

    if a.outro:
        # spec: OutroSeries from ABOUT.MD, OutroCTA from AUTHOR.MD (book = reel/../../).
        book = folder.parents[1]
        for name, comp in (("ABOUT.MD", "OutroSeries"), ("AUTHOR.MD", "OutroCTA")):
            src = book / name
            print(f"[remotion] outro {comp}: source {src} "
                  f"({'found' if src.exists() else 'MISSING'})")
        print("[remotion] outro compositions build after the core loop is in use "
              "(see SKILL.md 'Next phase').")
        return

    if not cands:
        print("[remotion] nothing to do — no shot.remotion.pattern beats")
        return

    changed = False
    for b in cands:
        bid = b["beat_id"]
        if not a.force and not slate_resolves(folder, bid):
            print(f"[remotion] {bid}: filled already (skip)")
            continue
        msg = render_beat(folder, b, a.force)
        print(f"[remotion] {bid}: {msg}")
        if msg.startswith("ok:"):
            stamp(b, folder, a.now)
            changed = True

    if changed:
        sheet_path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False))
        update_consumers(sheet, folder)
        print(f"[remotion] stamped provenance in beat_sheet.json + updated {CONSUMERS.name}")
    print("[remotion] done — run `bash scripts/run.sh <REEL>` to compile the cut")


if __name__ == "__main__":
    main()
