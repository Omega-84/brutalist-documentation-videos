#!/usr/bin/env python3
"""shorts.py — derive the 9:16 Shorts cut from a finished reel.

THE SHORTS LAW: a Short is a DERIVATIVE CUT, not a re-edit. Shorts exist —
in YouTube's world view — to get people to the 16:9 longs, and they have a
HARD 3:00 cap. So:

  1. CHECK LENGTH FIRST. At or under the cap → the whole reel reformats
     16:9 → 9:16 and posts as-is (no beats cut, silent endcard appended).
  2. OVER the cap → SHORTEN BY CUTTING BEATS, never by re-authoring —
     cutting saves regeneration. Auto-planned here (longest middle beats go
     first; the hook, the hero, and the outro are protected; --keep/--drop
     override the plan), reviewable in the printed plan before you compile.
  3. When beats were cut, the OUTRO IS REWRITTEN to say what was cut and to
     send the viewer to the long for the full story. That outro narration is
     the ONLY audio regenerated for a short — every other beat reuses the
     parent's mp3.
  4. Shorts ALWAYS post to the "Shorts" playlist, and the publisher points a
     short's description at its parent long (the funnel).

THE REFORMAT RULE (16:9 → 9:16): captured/user media is CENTER-CUT (biased
by shot.focus), written beside the source as <beat>-916.* — inspectable and
replaceable. THE HUMAN IS EXPECTED TO REPLACE a center cut that doesn't
work by adding a 9:16 version of the beat to the PANTRY:
pantry/<beat>-916.mp4|png always wins over everything else. GENERATED
GRAPHICS ARE NEVER CUT — and that includes Remotion renders even though
they live in media/:

THE ONDA CHECK: Onda terminal / Onda code beats (all REMOTION beats) are
used A LOT and a center cut chops their text mid-word. So every REMOTION
beat is detected BY ITS SHEET (shot.type == REMOTION), never by which
folder its render sits in. If Root.tsx has a portrait composition named
<pattern>916, the short's sheet is REWIRED to it and the beat re-renders
portrait via remotion_scenes.py on the short/ folder (props must still
match the 916 composition's zod schema — standing rule #4). If no 916
composition exists, the beat is flagged: add the composition to Root.tsx or
drop a pantry/<beat>-916.mp4. Manim GRAPHIC beats are re-laid-out for
portrait in the short's own scenes.py, as before. For generated beats the
ONLY human override slot is pantry/ — a media/<beat>-916.mp4 next to a
REMOTION render is assumed to be a stale auto-cut and is ignored.

Usage:
  python3 scripts/shorts.py reels/<slug>                      # auto: cap check + plan
  python3 scripts/shorts.py reels/<slug> --drop B14 B16       # manual plan
  python3 scripts/shorts.py reels/<slug> --keep B07 --recut   # protect + recut
Then (printed per run):
  python3 scripts/generate_audio_kokoro.py <reel>/short --only <outro>   # only if outro rewritten
  python3 scripts/compile.py <reel>/short --review --height 1920
  publish with --playlist "Shorts"

The endcard's Next: line defaults to the narration of the LAST dropped CARD
beat (the 16:9 outro's tease), override with --next.
"""
import argparse, json, shutil, subprocess, sys
from pathlib import Path

FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
CREAM = (243, 235, 221); INK = (47, 42, 38); TERRA = (211, 95, 67)
W, H = 1080, 1920

SHORTS_CAP_S = 180.0        # YouTube's hard cap for Shorts
CAP_HEADROOM_S = 2.0        # never plan right up against the cap
OUTRO_REWRITE_EST_S = 16.0  # planning estimate for the rewritten outro


def find_serif():
    for p in ("/System/Library/Fonts/Supplemental/Georgia.ttf",
              "/Library/Fonts/Georgia.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"):
        if Path(p).exists():
            return p
    return None


def endcard_png(out, handle, next_text, dark=True):
    from PIL import Image, ImageDraw, ImageFont
    bg, fg = (INK, CREAM) if dark else (CREAM, INK)
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    font = find_serif()

    def f(size):
        try:
            return ImageFont.truetype(font, size)
        except Exception:
            return ImageFont.load_default()

    fh = f(64)
    hb = d.textbbox((0, 0), handle, font=fh)
    hw = hb[2] - hb[0]
    d.text(((W - hw) / 2, H * 0.30), handle, font=fh, fill=fg)
    y = H * 0.30 + (hb[3] - hb[1]) + 26
    d.line([((W - hw) / 2, y), ((W + hw) / 2, y)], fill=TERRA, width=4)

    # wrap the Next: line
    fn = f(44)
    words, lines, cur = next_text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textbbox((0, 0), t, font=fn)[2] > W * 0.84 and cur:
            lines.append(cur); cur = wd
        else:
            cur = t
    lines.append(cur)
    y = H * 0.52
    for ln in lines:
        b = d.textbbox((0, 0), ln, font=fn)
        d.text(((W - (b[2] - b[0])) / 2, y), ln, font=fn, fill=fg)
        y += (b[3] - b[1]) + 22
    img.save(out)


def beat_dur(b):
    return float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0)


def is_remotion(b):
    shot = b.get("shot") or {}
    return (str(shot.get("type", "")).upper() == "REMOTION"
            or bool(shot.get("remotion")))


def root_tsx_text():
    """The Remotion composition registry (for the ONDA CHECK's 916 lookup)."""
    p = Path(__file__).resolve().parents[2] / "runtime" / "remotion" / "src" / "Root.tsx"
    try:
        return p.read_text()
    except Exception:
        return ""


def portrait_pattern(pattern, tsx):
    """<pattern>916 if Root.tsx registers a portrait composition for it."""
    cand = f"{pattern}916"
    return cand if f'id="{cand}"' in tsx else None


def beat_topic(b):
    """A 2–5 word human handle for a beat, for the 'what was cut' line."""
    g = (b.get("graphic") or {}).get("production_viz") or {}
    if g.get("label"):
        return str(g["label"])
    props = ((b.get("shot") or {}).get("remotion") or {}).get("props") or {}
    if props.get("segment"):
        return str(props["segment"]).lower()
    words = (b.get("narration_text") or "").split()
    return " ".join(words[:5]) + ("…" if len(words) > 5 else "")


def is_protected(b, beats, keep_ids):
    """The hook (first), the outro (last), the hero, and --keep ids never drop."""
    if b["beat_id"] in keep_ids:
        return True
    if b is beats[0] or b is beats[-1]:
        return True
    if (b.get("act") or "").upper() in ("INTRO", "OUTRO"):
        return True
    mech = (((b.get("graphic") or {}).get("production_viz") or {})
            .get("mechanic", "")) + " " + \
           (((b.get("graphic") or {}).get("production_viz") or {})
            .get("label", ""))
    return "hero" in mech.lower()


def plan_drops(beats, keep_ids, end_s):
    """Greedy: drop the LONGEST unprotected middle beats until the short —
    including the endcard and the rewritten-outro estimate — fits under the
    cap. Returns the list of beat ids to drop."""
    budget = SHORTS_CAP_S - CAP_HEADROOM_S - end_s
    total = sum(beat_dur(b) for b in beats)
    if total <= budget:
        return []
    # once anything drops, the outro is rewritten — swap its measured
    # duration for the planning estimate
    total = total - beat_dur(beats[-1]) + OUTRO_REWRITE_EST_S
    droppable = sorted((b for b in beats if not is_protected(b, beats, keep_ids)),
                       key=beat_dur, reverse=True)
    drops = []
    for b in droppable:
        if total <= budget:
            break
        drops.append(b["beat_id"])
        total -= beat_dur(b)
    return drops


def rewrite_outro(outro, dropped, long_title):
    """The shortened cut's outro: say what was cut, send them to the long.
    The ONLY regenerated audio in a short."""
    topics = [beat_topic(b) for b in dropped][:3]
    if len(topics) > 1:
        what = ", ".join(topics[:-1]) + " and " + topics[-1]
    else:
        what = topics[0] if topics else "the full detail"
    outro["narration_text"] = (
        f"That's the short version. The full video also covers {what} — "
        f"watch {long_title} for the whole story. The link is right below.")
    outro["actual_duration_s"] = 0           # re-measure after regeneration
    outro["audio_file"] = f"mp3/beat-{outro['beat_id']}.mp3"
    outro["short_outro_rewritten"] = True
    return outro


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", type=Path)
    ap.add_argument("--drop", nargs="*", default=None,
                    help="beat ids to cut (omit to let the cap check auto-plan)")
    ap.add_argument("--keep", nargs="*", default=[],
                    help="beat ids the auto-plan must NOT drop")
    ap.add_argument("--next", dest="next_text", default=None)
    ap.add_argument("--end-s", type=float, default=4.5)
    ap.add_argument("--handle", default="@nikbearbrown")
    ap.add_argument("--recut", action="store_true",
                    help="regenerate auto -916 cuts (never touches hand-made or pantry ones)")
    ap.add_argument("--no-endcard", action="store_true",
                    help="end on the last kept beat (e.g. the bio kicker) instead of the silent branded card")
    ap.add_argument("--no-outro-rewrite", action="store_true",
                    help="keep the parent outro narration even when beats were cut")
    a = ap.parse_args()
    folder = a.folder.resolve()
    sheet = json.loads((folder / "beat_sheet.json").read_text())
    slug = sheet["metadata"].get("slug", folder.name)
    title = sheet["metadata"].get("title", slug)
    beats = sheet["beats"]

    # ── 1. THE CAP CHECK ─────────────────────────────────────────────────
    full = sum(beat_dur(b) for b in beats)
    print(f"[short] parent reel: {len(beats)} beats · {full:.1f}s "
          f"({int(full//60)}:{full%60:04.1f}) · Shorts cap {int(SHORTS_CAP_S//60)}:00")
    if a.drop is not None:
        drops = list(a.drop)                      # human plan wins
        print(f"[short] manual plan: dropping {', '.join(drops) or 'nothing'}")
    else:
        drops = plan_drops(beats, set(a.keep), 0 if a.no_endcard else a.end_s)
        if drops:
            print(f"[short] over the cap → auto-plan drops "
                  f"{len(drops)} beat(s): {', '.join(drops)}")
            print("[short]   (re-run with --drop/--keep to override the plan)")
        else:
            print("[short] under the cap → full reformat, no beats cut")

    short = folder / "short"
    for d in ("media", "manim", "mp3"):
        (short / d).mkdir(parents=True, exist_ok=True)

    # a derivative inherits the parent's fact-check (Gate F)
    fc = short / "FACTCHECK.md"
    if (folder / "FACTCHECK.md").exists() and not fc.exists():
        fc.symlink_to(Path("..") / "FACTCHECK.md")

    kept = [json.loads(json.dumps(b)) for b in beats if b["beat_id"] not in drops]
    dropped = [b for b in beats if b["beat_id"] in drops]
    next_text = a.next_text or next(
        (b["narration_text"] for b in reversed(dropped)
         if b.get("shot", {}).get("type") == "CARD"), "")

    # ── 2. THE FUNNEL OUTRO — the only regenerated audio in a short ─────
    outro_rewritten = False
    if dropped and not a.no_outro_rewrite and kept:
        rewrite_outro(kept[-1], dropped, title)
        outro_rewritten = True
        print(f"[short] outro {kept[-1]['beat_id']} rewritten → mentions the cuts, "
              f"points to the long (audio must be regenerated)")

    # ── 3. resolve each kept slot to a 9:16 source ───────────────────────
    # precedence: pantry/<bid>-916.* (the human's replacement, wins always) →
    # THE ONDA CHECK for REMOTION beats (916 composition rewire, never a crop) →
    # portrait scenes for manim → auto center-cut for captured/user media only
    tsx = root_tsx_text()
    onda_rewired, onda_blocked = [], []
    for b in kept:
        bid = b["beat_id"]
        # narration link FIRST — every kept beat needs its audio regardless of
        # how (or whether) its visual slot resolves; the compiler is all-or-silent.
        # A rewritten outro is the exception: its mp3 is regenerated, not linked.
        if not b.get("short_outro_rewritten"):
            mp3 = folder / (b.get("audio_file") or f"mp3/beat-{bid}.mp3")
            mdst = short / "mp3" / mp3.name
            if mp3.exists() and not mdst.exists():
                mdst.symlink_to(Path("../..") / "mp3" / mp3.name)
        fx = float((b.get("shot", {}).get("focus") or [0.5, 0.5])[0])
        generated = is_remotion(b) or bool(b.get("graphic"))

        # pantry: the human's slot, wins over every path incl. the Onda check
        override = None
        for ext in (".mp4", ".png", ".jpg"):
            p = folder / "pantry" / f"{bid}-916{ext}"
            if p.exists():
                override = ("pantry", p, ext)
                break
        if override:
            print(f"[short] {bid}  pantry override → pantry/{override[1].name}")

        # THE ONDA CHECK — REMOTION beats (Onda terminal/code etc.) are never
        # cropped, no matter that their renders live in media/
        if override is None and is_remotion(b):
            pattern = ((b.get("shot") or {}).get("remotion") or {}).get("pattern", "")
            p916 = portrait_pattern(pattern, tsx)
            if p916:
                b["shot"]["remotion"]["pattern"] = p916
                b["shot"]["remotion"]["rendered"] = {"out": f"media/{bid}.mp4", "at": ""}
                onda_rewired.append(bid)
                print(f"[short] {bid}  ONDA CHECK: {pattern} → {p916} (portrait "
                      f"re-render on short/; match the 916 zod schema — rule #4)")
            else:
                onda_blocked.append((bid, pattern))
                print(f"[short] {bid}  ONDA CHECK ⚠ no {pattern}916 composition in "
                      f"Root.tsx — add one, or drop pantry/{bid}-916.mp4")
            continue    # never falls through to the crop path

        # hand-made -916 beside the source (captured media only — for generated
        # beats a media/<bid>-916.* is assumed to be a stale auto-cut)
        if override is None and not generated:
            for sub, exts in (("media", (".mp4", ".png", ".jpg")),
                              ("manim", (".mp4",))):
                for ext in exts:
                    p = folder / sub / f"{bid}-916{ext}"
                    if p.exists():
                        override = (sub, p, ext)
                        break
                if override:
                    break
        if override is None:
            # the parent slot's winner, per compile precedence
            src = None
            for sub, ext in (("media", ".mp4"), ("manim", ".mp4"),
                             ("manim", ".mov"), ("media", ".png"),
                             ("media", ".jpg")):
                p = folder / sub / f"{bid}{ext}"
                if p.exists():
                    src = (sub, p, ".mp4" if ext == ".mov" else ext)
                    break
            if src is None:
                continue                        # slate — nothing to cut
            sub, p, ext = src
            if sub == "manim" or generated:     # NEVER cut generated graphics
                print(f"[short] {bid}  GENERATED — no cut; needs a portrait "
                      f"scene in short/scenes.py (render via run), or add "
                      f"pantry/{bid}-916.mp4")
                continue
            cut = folder / sub / f"{bid}-916{ext}"
            if a.recut or not cut.exists():
                if ext == ".mp4":
                    vf = (f"crop='min(iw,ih*9/16)':ih:"
                          f"'max(0,min(iw-ow,iw*{fx:.4f}-ow/2))':0")
                    subprocess.run([FFMPEG, "-y", "-v", "error", "-i", str(p),
                                    "-vf", vf, "-c:v", "libx264", "-preset",
                                    "slow", "-crf", "16", "-an", str(cut)],
                                   check=True)
                else:
                    from PIL import Image
                    im = Image.open(p)
                    w, h = im.size
                    cw = min(w, int(h * 9 / 16))
                    x = max(0, min(w - cw, int(fx * w - cw / 2)))
                    im.crop((x, 0, x + cw, h)).save(cut)
                print(f"[short] {bid}  center-cut 16:9 -> {sub}/{cut.name} "
                      f"(focus x={fx:.2f}) — replace via pantry/{bid}-916{ext} "
                      f"if the cut doesn't work")
            override = (sub, cut, ext)
        sub, p, ext = override
        # pantry overrides mount into the short's media/ slot
        dsub = "media" if sub == "pantry" else sub
        dst = short / dsub / f"{bid}{ext}"
        if dst.is_symlink() or dst.exists():
            dst.unlink()
        dst.symlink_to(Path("../..") / sub / p.name)

    # ── 4. the silent endcard: branded, read-only ────────────────────────
    if not a.no_endcard:
        endcard_png(short / "media" / "END.png", a.handle, next_text, dark=True)
        subprocess.run([FFMPEG, "-y", "-v", "error", "-f", "lavfi",
                        "-i", "anullsrc=r=44100:cl=mono", "-t", f"{a.end_s:.2f}",
                        "-c:a", "libmp3lame", "-q:a", "9",
                        str(short / "mp3" / "beat-END.mp3")], check=True)
        kept.append({
            "beat_id": "END",
            "narration_text": "",
            "actual_duration_s": a.end_s,
            "audio_file": "mp3/beat-END.mp3",
            "shot": {"type": "CARD", "source": "own", "motion": "hold",
                     "treatment": "none"},
            "card": {"handle": a.handle, "next": next_text, "silent": True},
        })

    meta = dict(sheet["metadata"])
    meta.update({"slug": f"{slug}-short", "aspect_ratio": "9:16", "fit": "crop",
                 "kind": "short",
                 "reformat": ("center-cut, focus-aware; pantry/<bid>-916.* is the "
                              "human replacement slot; -916 overrides honored"),
                 "derived_from": slug, "dropped_beats": drops,
                 "playlist_short": "Shorts"})
    total = sum(beat_dur(b) for b in kept) + (OUTRO_REWRITE_EST_S if outro_rewritten else 0)
    meta["total_estimated_duration_seconds"] = round(total, 2)
    (short / "beat_sheet.json").write_text(
        json.dumps({"metadata": meta, "beats": kept}, indent=1, ensure_ascii=False))

    cap = ("OK" if total <= SHORTS_CAP_S
           else "⚠ STILL OVER the 3:00 Shorts cap — drop more (--drop) or check the plan")
    est = " (outro duration estimated until its audio regenerates)" if outro_rewritten else ""
    print(f"[short] {len(kept)} beats · ~{total:.1f}s "
          f"({int(total//60)}:{total%60:04.1f}) {cap}{est}")
    tail_note = ("ends on the last beat (no endcard)" if a.no_endcard
                 else f"silent endcard {a.end_s}s")
    print(f"[short] dropped: {', '.join(drops) or 'none'} · {tail_note}")
    if onda_rewired:
        print(f"[short] ONDA CHECK: {len(onda_rewired)} REMOTION beat(s) rewired to "
              f"916 compositions ({', '.join(onda_rewired)}) — they MUST be "
              f"re-rendered portrait before compiling; any old center-cut "
              f"media/<bid>-916.mp4 of a Remotion render is stale garbage (delete it).")
    if onda_blocked:
        print(f"[short] ONDA CHECK ⚠ BLOCKED: "
              + "; ".join(f"{bid} needs {pat}916 in Root.tsx (or pantry/{bid}-916.mp4)"
                          for bid, pat in onda_blocked))
    rel = folder.relative_to(folder.parents[1])
    step = 1
    print("[short] next:")
    if outro_rewritten:
        print(f"[short]   {step}. python3 runtime/scripts/generate_audio_kokoro.py {rel}/short   "
              f"# regenerates ONLY the rewritten outro (missing mp3)")
        step += 1
    if onda_rewired or onda_blocked:
        print(f"[short]   {step}. python3 runtime/scripts/remotion_scenes.py {rel}/short   "
              f"# FOREGROUND (rule #3) — portrait renders for the 916-rewired beats")
        step += 1
    print(f"[short]   {step}. python3 runtime/scripts/compile.py {rel}/short --review --height 1920")
    print(f"[short]   {step + 1}. publish the short with --playlist \"Shorts\" "
          f"(the funnel: its description links the parent long)")


if __name__ == "__main__":
    main()
