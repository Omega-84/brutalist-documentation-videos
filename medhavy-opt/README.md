# Medhavy — Monthly Work Record

Three short videos documenting volunteer engineering work on the **Medhavy**
project at Humanitarians AI, May–July 2026. One video per month.

| Month | Title | Runtime | Video |
|---|---|---|---|
| One (May) | *Two Fronts.* | 3:28 | [`2026-05-medhavy-may.mp4`](youtube/2026-05-medhavy-may/2026-05-medhavy-may.mp4) |
| Two (June) | *Learning to Render.* | 3:31 | [`2026-06-medhavy-june.mp4`](youtube/2026-06-medhavy-june/2026-06-medhavy-june.mp4) |
| Three (July) | *Scoped, Then Rebuilt.* | 2:29 | [`2026-07-medhavy-july.mp4`](youtube/2026-07-medhavy-july/2026-07-medhavy-july.mp4) |

1920×1080, narrated, no stock footage and no screen recordings — every frame is
a Remotion composition rendered from the beat sheet in the same folder.

---

## ▶ Where the output is · Where the code is

**THE OUTPUT — the three finished videos.** Download or click to play:

```
medhavy-opt/youtube/2026-05-medhavy-may/2026-05-medhavy-may.mp4      ← month one
medhavy-opt/youtube/2026-06-medhavy-june/2026-06-medhavy-june.mp4    ← month two
medhavy-opt/youtube/2026-07-medhavy-july/2026-07-medhavy-july.mp4    ← month three
```

**THE CODE — what produced them.** Two layers:

| | Path | What it is |
|---|---|---|
| **1. Content** | [`medhavy-opt/youtube/<month>/beat_sheet.json`](youtube/) | The source of truth for each video. Every beat's narration, its ordered list of on-screen events, and the props passed to its scene. Change this file, re-run the pipeline, get a different video. |
| **2. Visuals** | [`runtime/remotion/src/scenes/OptWeekMarker.tsx`](../runtime/remotion/src/scenes/OptWeekMarker.tsx)<br>[`OptHoursCard.tsx`](../runtime/remotion/src/scenes/OptHoursCard.tsx)<br>[`OptBlockerCard.tsx`](../runtime/remotion/src/scenes/OptBlockerCard.tsx) | The three React/Remotion components written for this project. Each is a pure function of frame number — deterministic, so the same beat sheet always renders the same frames. |
| **3. Pipeline** | [`runtime/scripts/`](../runtime/scripts/) | Toolkit code, not written by me: `generate_audio_kokoro.py` (narration), `remotion_scenes.py` (per-beat rendering), `compile.py` (assembly). |

Everything else in each month's folder is a **record, not code**: `PEDAGOGY.md`
is the full narration script with its sign-off, `SOURCES.md` documents
provenance. Per-beat renders, narration mp3s and QC frames are regenerable and
deliberately not committed.

---

## What the videos cover

**Month one** — two technical duties in parallel: prompt engineering on the
electron-microscopy textbook (repairs merged to the repository), and healthcare
systems integration research against Epic's FHIR sandbox. A clinical-data
extraction pipeline built end to end, a `403 Forbidden` diagnosed to a missing
`system/Binary.read` OAuth scope, and a data-sparsity limitation escalated with
evidence.

**Month two** — a rendering toolchain stood up from nothing on WSL, then two
physics scenes rebuilt on correct geometry (area-uniform polar sampling for the
star field, logarithmic spiral arms for the galaxy). A `FadeOut`-inside-the-loop
animation bug traced to its structural cause and fixed. Approved to continue.

**Month three** — batch production with chained renders, twelve planned topics
pruned to the four that warrant animation, and a new tool and visual direction
absorbed and delivered as samples for review.

## How they were built

Built with [brutalist.art](https://github.com/nikbearbrown/brutalist.art), an
audio-first video toolkit. The pipeline is free and local end to end — no API
keys, no paid services.

```
beat_sheet.json  →  PEDAGOGY.md (human sign-off)  →  narration  →  visuals  →  compile
```

Narration durations are the master clock; every visual conforms to the measured
audio rather than the other way round.

```bash
# from the toolkit root
venv/bin/python runtime/scripts/generate_audio_kokoro.py medhavy-opt/youtube/<slug>
venv/bin/python runtime/scripts/remotion_scenes.py       medhavy-opt/youtube/<slug>
venv/bin/python runtime/scripts/compile.py               medhavy-opt/youtube/<slug> --height 1080
```

`ART_SCALE=1` renders native 1080p; the default `ART_SCALE=2` supersamples to
true 4K and takes roughly four times as long.

### Components written for this project

Three Remotion scenes, in [`runtime/remotion/src/scenes/`](../runtime/remotion/src/scenes/):

- **`OptWeekMarker.tsx`** — the spine card. A topic or week position, a thesis
  line, and up to four evidence bullets that wipe in one at a time. Blocks are
  distributed across the full title-safe height rather than stacked from the
  top, so a two-bullet card and a four-bullet card both fill the frame.
- **`OptHoursCard.tsx`** — the monthly hours ledger. Deliberately *not* a bar
  chart: every week in the record is exactly 20 hours, so bars would draw four
  identical full-width blocks and imply a variance that does not exist.
- **`OptBlockerCard.tsx`** — the dependency register. A heavier ground and a
  rule across the top mark it as a distinct kind of beat, so friction reads as a
  deliberate editorial choice rather than something buried in narration.

The voice is Kokoro `am_michael`, running locally.

## Per-video files

Each folder under [`youtube/`](youtube/) contains:

- `beat_sheet.json` — the source of truth. One beat per moment; narration, the
  ordered `show` block of visual events, and the scene props. Everything
  downstream derives from it.
- `PEDAGOGY.md` — full narration, beat by beat, with the sign-off that gates
  audio generation.
- `SOURCES.md` *(month one)* — provenance and the restraints applied.
- `<slug>.mp4` — the final cut.

Per-beat renders, narration mp3s and QC frames are regenerable and not
committed.

## A note on sources

These videos are built from weekly work reports covering the contract period.
Those reports are an internal document and are **not** included here: they name
colleagues and describe internal decisions that aren't mine to publish. The
videos themselves name only the supervising professors.

Every factual claim in the videos traces to a line in that record. Nothing is
reconstructed or estimated beyond what the reports state, and hours are
described as *documented* rather than tracked, which is what the record
supports.
