# Design — Medhavy OPT Monthly Recap Videos

**Date:** 2026-07-30
**Author:** Varun Nayyar (with Claude)
**Status:** Approved design, ready for implementation plan

---

## 1. Purpose

Three videos, one per month of the May 1 – Jul 31, 2026 Medhavy contract period,
showcasing volunteer work on the Medhavy project at Humanitarians AI. The videos
serve the agreement renewal and double as a public portfolio artifact.

**Audience:** Humanitarians AI leadership (Prof. Nik, Prof. Sridhar, Riya,
Rishabh) *and* a general public viewer who has never heard of Medhavy. Both must
be served by the same cut — internal jargon gets explained on first use, and
nothing assumes prior context.

**What a viewer must walk away believing:** the contribution was real, technical,
degree-relevant, sustained across all three months, and honestly reported
including its friction.

## 2. Source of truth

`hai_reports_weeks_1-12.md` — OPT Weekly Reports, Weeks 1–12, compiled by the
Addams OPT Volunteer Documentation System. Covers May 1 – Jul 23, 2026.

**Hard constraint:** nothing appears on screen or in narration that is not in
this file. No invented metrics, no estimated figures presented as measured, no
smoothing of thin weeks. Where the reports are candid about friction, the videos
are too.

**Week 13 (Jul 24–31) is out of scope and must not be referenced anywhere** — not
in narration, not on a card, not as an "in progress" note. The July video ends at
Week 12.

## 3. The three videos

Weeks are assigned to the month containing the majority of their days.

### 3.1 `2026-05-medhavy-may` — Weeks 1–4 (May 1–28)

Working title theme: **Two Fronts.**

| Week | Beat content |
|---|---|
| 1 (May 1–7) | HELIX prompt work on the `improve-helix-prompt` branch for the EM textbook tutor; EM textbook rendering fixes (equations, images, cover page); GitHub repo access requested from Prof. Nik, unresolved at week end. |
| 2 (May 8–14) | Epic FHIR sandbox pipeline: `get_patient_demographics.py` parsing nested FHIR demographics → CSV; `fetch_health_data.py` extracting six clinical categories; `/AllergyIntolerance` endpoint setup; `NameError` in `nb.ipynb` traced to an unquoted patient ID. Access invite found unread in inbox. |
| 3 (May 15–21) | Densest EPIC week: OAuth missing-scope authorization failure diagnosed and resolved; sandbox data-sparsity limitation identified and reported honestly upward; long-pending PR merged; cross-volunteer support task taken on. |
| 4 (May 22–28) | Prof. Sridhar discontinues the EPIC workstream citing the accumulated blockers Varun had already documented; same-day reassignment to Manim instructional video production; access requested same day. |

Narrative spine: two parallel workstreams, a pipeline built and honestly
assessed, and a workstream ended *on the strength of the volunteer's own
reporting* rather than despite it.

### 3.2 `2026-06-medhavy-june` — Weeks 5–9 (May 29 – Jul 2)

Working title theme: **Learning to Render.**

| Week | Beat content |
|---|---|
| 5 (May 29 – Jun 4) | Manim environment stood up: `.venv`, `uv`, rendering libraries; WSL/NTFS hardlink issue solved with `UV_LINK_MODE=copy`; `uv` path mismatch solved with `--active`; reference repo review; first verified render (`CreateCircle`). Invisible infrastructure hours. |
| 6 (Jun 5–11) | Observable Universe scene (correct radial star distribution, glow ring) and Milky Way scene (logarithmic spiral arms, galactic bulge); Jupyter `%%manim` integration; branding logo overlay; wildcard-import `NameError` fix. |
| 7 (Jun 12–18) | `BaseQuantities` animation logic bug: static elements erroneously cleared by a `FadeOut` inside a loop meant to cycle only variable content — diagnosed and fixed; `TransformMatchingShapes` replaces `ReplacementTransform`; explicit written and verbal approval from Prof. Sridhar to continue. |
| 8 (Jun 19–25) | Prof. Nik introduces Scout, with an instruction to scope video production only to topics genuinely requiring visualization; topic list compiled and submitted for review; ElevenLabs narration added to scope. Editorial judgment exercised collaboratively. |
| 9 (Jun 26 – Jul 2) | Videos produced with Scout per the approved topic list; ElevenLabs narration blocked by a disabled API key — a credentialing dependency outside Varun's control, reported rather than worked around. |

Narrative spine: from a broken environment to approved output in five weeks, with
one genuine debugging win and one blocker handled correctly.

### 3.3 `2026-07-medhavy-july` — Weeks 10–12 (Jul 3–23)

Working title theme: **Three Pivots, One Throughline.**

| Week | Beat content |
|---|---|
| 10 (Jul 3–9) | Narration blocker still unresolved and still outside his control; effort redirected to production efficiency — batch-building the first 4 chapters, chained render command setup, pruning a 12-video plan to the 4 topics that genuinely warranted animation. |
| 11 (Jul 10–16) | Third tooling/style pivot of the contract: Prof. Nik introduces Brutalist and a doodle-style visual direction — a creative-direction change, not a technical failure. Onboarding plus technical scoping of the style shift. |
| 12 (Jul 17–23) | Three sample videos completed and submitted to Prof. Sridhar in the new Brutalist/doodle style; awaiting review. |

Closing beat closes on the submitted samples. **No mention of Week 13.**

## 4. Format

- **Builder:** `ai-explainer` (the tight cut), `claude-hai` channel — Claude
  fidelity skin, Pragmatist register, `@HumanitariansAI` footer chip.
- **Persona:** `hai` (Pragmatist register).
- **Voice:** Kokoro `am_michael`. This is a user-directed deviation: the
  toolkit ships an `ALLOWED_VOICES = {"am_onyx", "af_bella"}` allowlist in
  `runtime/scripts/generate_audio_kokoro.py`, and `am_michael` must be added to
  it. The voice model file already contains all 54 Kokoro voices; only the
  allowlist blocks it. Kokoro remains the only engine — no paid voice is
  introduced. The register and channel chip are unchanged by the voice swap.
- **POV:** third person. The narrator reports *on* the work
  ("in week two, the extraction pipeline came together"), never impersonates
  Varun. A synthetic voice narrating about a person reads as documentation; one
  speaking as him does not.
- **Aspect:** 16:9 only. No vertical cuts, no `./art shorts`.
- **Target runtime:** roughly 3 minutes each. Per `duration-planner` doctrine
  duration is an output of the measured audio, never a target — if a month's
  beats run to 3:40, that is the runtime.
- **Structure per video:** cold open stating the month in one sentence → one beat
  block per week in chronological order → closing three-beat per `your-turn`
  doctrine.
- **Series consistency:** one shared brand config across all three so they read as
  a set; only a per-month accent color varies.

## 5. Visual design

**Synthetic only.** No screenshots, no terminal captures, no GitHub captures, no
Substack captures. Nothing enters `pantry/` from outside; the videos have no
dependency on asset gathering and nothing sensitive (Epic sandbox output,
private repos, credentials) can appear.

Visual vocabulary:

- **Week-marker cards** — week number and date range, the video's spine.
- **Hours beat** — the week's OPT hours table rendered as a typographic card.
  Figures are quoted from the reports as documented, never restated as measured.
- **Code-artifact cards** — filenames and the one or two lines that matter
  (`get_patient_demographics.py`, `UV_LINK_MODE=copy`, the `FadeOut`-in-loop fix),
  typeset from the report text rather than captured from a real editor.
- **Timeline strip** — a per-month progress element that fills as weeks advance,
  giving the chronology a visible shape.
- **Blocker register** — blockers get a visually distinct treatment so the candor
  is legible as a deliberate choice rather than buried in narration.

**One Manim exception:** the June video renders the star-distribution and
logarithmic-spiral-arm beats in actual Manim. In that one case recreating the
visual *is* the evidence of the skill being claimed, and a typographic card would
undersell it. Everywhere else, Remotion/typographic cards.

## 6. Pipeline

Standard toolkit flow, once per video:

1. Author `beat_sheet.json` — one beat per moment; everything downstream derives
   from it.
2. Write `PEDAGOGY.md`. **GATE P binds:** a human signs `VERDICT: PASS` before
   any audio is generated. Varun is the signer. This is a quality gate.
3. Generate narration with `runtime/scripts/generate_audio_kokoro.py` (Bella).
   Measured MP3 durations become the master clock. Timing is never hand-fixed —
   regenerate audio and recompile.
4. Render visuals. Remotion **only** via `runtime/scripts/remotion_scenes.py` in
   the foreground; never a hand-rolled `npx remotion render`. Manim for the June
   exception beats.
5. Assemble; any beat that cannot honestly be rendered comes out as a labeled
   slate naming exactly what is needed.
6. **Verify by looking at frames** — `_qc/` plus the qc-sheet. An mp4 probe alone
   is not verification.
7. `./art final`. No publishing step exists and none is added.

## 7. Output location

```
/home/nayya/brutalist.art/medhavy-opt/youtube/2026-05-medhavy-may/
/home/nayya/brutalist.art/medhavy-opt/youtube/2026-06-medhavy-june/
/home/nayya/brutalist.art/medhavy-opt/youtube/2026-07-medhavy-july/
```

This is a deliberate, user-directed deviation from toolkit rule 4 ("videos travel
with their book, never into this toolkit folder"). There is no Medhavy book on
this machine; Varun chose a folder at the toolkit root. Recorded here so the
deviation is intentional rather than accidental.

## 8. Build order

May → June → July, sequentially. May establishes the shared brand config, the
week-marker card, the hours card, the timeline strip, and the blocker register;
June and July reuse them. Building May first means the series vocabulary is
settled once and validated against a real render before it is reused twice.

## 9. Non-goals

- No publishing, uploading, or distribution. The master stays in its folder.
- No vertical/shorts cuts.
- No paid services and no API keys. Kokoro is the only TTS engine. If any step
  appears to require a key, that is a bug in the toolkit, not a missing
  credential.
- No Week 13 content.
- No coverage of work outside the May 1 – Jul 23, 2026 reports.

## 10. Success criteria

- Three 16:9 videos exist at the paths in §7, each assembled from measured audio.
- Each has a `PEDAGOGY.md` signed `VERDICT: PASS` before its audio was generated.
- Each has been verified by looking at `_qc/` frames, not by probe alone.
- Every factual claim in every video traces to a line in
  `hai_reports_weeks_1-12.md`.
- The July video contains no reference to Week 13.
- No slates remain in any final cut.
- The three read as one series.
