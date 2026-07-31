# Medhavy Monthly Recap Videos — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build three 16:9 explainer videos — one per month of the May 1 – Jul 31, 2026 Medhavy OPT contract — that recap Varun Nayyar's volunteer work week by week for the Humanitarians AI agreement renewal.

**Architecture:** Each video is a `beat_sheet.json` in its own reel folder. Narration MP3s are generated with Kokoro first and their measured durations become the master clock; visuals are Remotion compositions (plus Manim for two beats in the June video) rendered per beat into `media/<BID>.mp4`; `compile.py` conforms every clip to its beat's measured audio and muxes the cut. Three new Remotion scene components (week marker, hours card, blocker card) are built once during the May video and reused by June and July.

**Tech Stack:** Python 3 (runtime scripts), Kokoro ONNX TTS (`am_michael`), Remotion 16:9 1920×1080 @30fps (TypeScript/React), Manim (June only), ffmpeg.

## Global Constraints

- **Source of truth:** `hai_reports_weeks_1-12.md`. Nothing appears on screen or in narration that is not in that file. No invented metrics, no estimated figures presented as measured.
- **Week 13 (Jul 24–31) must not be referenced anywhere** — not in narration, not on a card, not as an "in progress" note.
- **Aspect: 16:9 only.** Never run `./art shorts`. Never render a `916` composition.
- **Voice:** Kokoro `am_michael` for every beat of every video.
- **Register:** Pragmatist (`hai`). Third-person narration — the narrator reports *on* Varun, never speaks as him.
- **Channel:** `metadata.channel_title` = `"@HumanitariansAI"`; `folderLabel` prop = `"@HumanitariansAI"`.
- **Palette:** `claude` fidelity tokens (`runtime/remotion/src/tokens/claude.ts`) — `PAGE #FAF9F5`, `INK #3D3929`, `SPARK #D97757`. One terracotta moment per beat. Do not retint.
- **Layout:** every essential element inside `SAFE` from `runtime/remotion/src/tokens/layout.ts` (x 96–1824, y 54–1026). Use `safeX`/`safeY`/`fitToSafe`; never nudge by pixels.
- **GATE P binds:** `PEDAGOGY.md` containing the literal string `VERDICT: PASS` must exist in a reel folder before its audio is generated. Never pass `--no-gate`.
- **Never hand-fix timing.** If a beat's pacing is wrong, change the narration text and regenerate audio.
- **Render Remotion only via** `python3 runtime/scripts/remotion_scenes.py <REEL>`, in the foreground. Never hand-roll `npx remotion render`, except for the standalone component smoke tests in Tasks 2–4, which render to a scratch path and are never slotted into a reel.
- **Verify by LOOKING at frames.** `Read` the PNGs. An ffprobe duration/frame count is a file check, not QC.
- **Never publish.** Masters stay in the reel folder.
- **DO NOT COMMIT ANYTHING TO GIT.** The user has explicitly forbidden commits for this work. No `git add`, no `git commit`, no branches, no PRs. Leave all changes in the working tree.
- **Repo root** for all relative paths: `/home/nayya/brutalist.art`. Run every command from there unless stated otherwise.
- **Use `venv/bin/python`, not `python3`, for every runtime script.** Verified in Task 1: the system `python3` has no `kokoro-onnx`, and `generate_audio_kokoro.py` exits with a misleading `pip install kokoro-onnx` message rather than a traceback. The repo venv at `venv/` has the full dependency set. Where this plan writes `python3 runtime/scripts/…`, read it as `venv/bin/python runtime/scripts/…`. `./art run` and `./art final` shell out to `python3` internally, so before using them either activate the venv (`source venv/bin/activate`) or call the underlying scripts directly.

---

## File Structure

**Toolkit files modified (2):**
- `runtime/scripts/generate_audio_kokoro.py:51` — add `am_michael` to `ALLOWED_VOICES`.
- `runtime/remotion/src/Root.tsx` — register three new Compositions.

**Toolkit files created (3):**
- `runtime/remotion/src/scenes/OptWeekMarker.tsx` — week number, date range, one-line thesis, and a timeline strip whose Nth pip is terracotta. One responsibility: mark where in the month we are and what that week was about.
- `runtime/remotion/src/scenes/OptHoursCard.tsx` — the month's OPT hours table as a typographic card with bars that grow to their values. One responsibility: show documented hours.
- `runtime/remotion/src/scenes/OptBlockerCard.tsx` — a blocker/finding in a visually distinct register: what blocked, whose court it was in, how it resolved. One responsibility: make candor legible.

**Reel folders created (3),** each self-contained:
```
medhavy-opt/youtube/2026-05-medhavy-may/
  beat_sheet.json      PEDAGOGY.md      SOURCES.md
  mp3/  media/  _qc/   (generated)
medhavy-opt/youtube/2026-06-medhavy-june/
  beat_sheet.json      PEDAGOGY.md      SOURCES.md
  scenes.py            FACTCHECK.md     SHOTLIST.md      PROMPTS.md
  mp3/  manim/  media/  _qc/   (generated)
medhavy-opt/youtube/2026-07-medhavy-july/
  beat_sheet.json      PEDAGOGY.md      SOURCES.md
  mp3/  media/  _qc/   (generated)
```

Only June carries `scenes.py` + the `FACTCHECK.md`/`SHOTLIST.md`/`PROMPTS.md` paperwork set, because only June renders Manim. May and July never invoke `run.sh` (which refuses a reel with no `scenes.py`); they call `remotion_scenes.py` and `compile.py` directly.

---

## Beat Sheet Reference (read before Task 5)

### Schema

A beat sheet is `{"metadata": {...}, "beats": [...]}`. Every beat:

```json
{
  "beat_id": "B01",
  "act": "WEEK 1",
  "narration_text": "The spoken line. 45-70 words for a body beat.",
  "shot": {
    "type": "GRAPHIC",
    "source": "remotion",
    "motion": "reveal",
    "scene_type": "week-marker",
    "show": [
      {"at": "0.0", "event": "WEEK 1 types in; date range fades beneath"},
      {"at": "0.4", "event": "timeline pip 1 fills terracotta"},
      {"at": "0.7", "event": "thesis line wipes in under the rule"}
    ],
    "remotion": {
      "pattern": "OptWeekMarker",
      "props": {}
    }
  },
  "estimated_duration_s": 12
}
```

`pattern` MUST be a Composition `id` registered in `runtime/remotion/src/Root.tsx`. `props` is passed verbatim to that composition. `generate_audio_kokoro.py` adds `audio_file` and `actual_duration_s`; `remotion_scenes.py` adds `shot.remotion.rendered`. Do not author those three fields by hand.

### Shared metadata block

Identical in all three sheets except `title`, `slug`, `topic`, `greeting`:

```json
{
  "metadata": {
    "title": "Two Fronts.",
    "slug": "2026-05-medhavy-may",
    "topic": "MEDHAVY · MAY 2026",
    "register": "Pragmatist",
    "audience": "HAI",
    "brand": "claude",
    "channel_title": "@HumanitariansAI",
    "engine": "kokoro",
    "voice_kokoro": "am_michael",
    "palette": "claude",
    "style_preset": "claude",
    "ground": "#FAF9F5",
    "aspect_ratio": "16:9",
    "greeting": "Hej, HAI",
    "source": "hai_reports_weeks_1-12.md",
    "note": "OPT monthly recap, Weeks 1-4. Third-person Pragmatist. Synthetic visuals only — no captures. Week 13 out of scope."
  }
}
```

Per-video overrides:

| Video | `title` | `slug` | `topic` | `greeting` | `note` weeks |
|---|---|---|---|---|---|
| May | `Two Fronts.` | `2026-05-medhavy-may` | `MEDHAVY · MAY 2026` | `Hej, HAI` | Weeks 1-4 |
| June | `Learning To Render.` | `2026-06-medhavy-june` | `MEDHAVY · JUNE 2026` | `Ciao, HAI` | Weeks 5-9 |
| July | `Three Pivots.` | `2026-07-medhavy-july` | `MEDHAVY · JULY 2026` | `Ola, HAI` | Weeks 10-12 |

Greetings use the short forms only (the persona word budget: HAI takes `Hi · Ola · Hej · Ciao`), and no language repeats across the three.

### Beat spines

Authored from the report sections named in the "Source" column. Narration is written during the task, from those sections — SHOW block first, words second.

**May — `2026-05-medhavy-may` (14 beats)**

| Beat | Act | Pattern | Content | Source |
|---|---|---|---|---|
| B00 | ASK | `ClaudeComposerAsk` | Cold open. Composer shows the ask "Recap what I built on Medhavy in May 2026, week by week — and don't skip what got stuck." `output` lines: three one-line month headlines. | header + all 4 weeks |
| B01 | WEEK 1 | `OptWeekMarker` | May 1–7. HELIX prompt on `improve-helix-prompt`; EM textbook rendering fixes. | Week 1 "Work Completed" |
| B02 | WEEK 1 | `OptBlockerCard` | Repo access requested from Prof. Nik, unresolved at week end. | Week 1 "Blockers" |
| B03 | WEEK 2 | `OptWeekMarker` | May 8–14. Epic FHIR sandbox pipeline. | Week 2 "Work Completed" |
| B04 | WEEK 2 | `ClaudeCodeBeat` | `get_patient_demographics.py` / `fetch_health_data.py` — six clinical categories to CSV. | Week 2 "Work Completed" |
| B05 | WEEK 2 | `OptBlockerCard` | The access invite had been sent; it was sitting unread. Resolved 5/14. | Week 2 "Blockers" |
| B06 | WEEK 3 | `OptWeekMarker` | May 15–21. Densest EPIC week. | Week 3 "Executive Summary" |
| B07 | WEEK 3 | `ClaudeCodeBeat` | The OAuth missing-scope authorization failure and its fix. | Week 3 "Work Completed" |
| B08 | WEEK 3 | `OptBlockerCard` | Sandbox data sparsity — identified, and reported upward rather than worked around. | Week 3 |
| B09 | WEEK 4 | `OptWeekMarker` | May 22–28. EPIC discontinued on the documented blockers; same-day reassignment to Manim. | Week 4 "Executive Summary" |
| B10 | HOURS | `OptHoursCard` | Four weeks, 20 documented hours each, 80 total. | the four hours tables |
| B11 | VERDICT | `ClaudeVerdictArtifact` | Three bare recap sentences. | — |
| B12 | YOUR TURN | `ClaudeComposerAsk` | `greeting: "Your turn."`; prompt read aloud verbatim. | — |
| B13 | OUTRO | `ClaudeTitleOutro` | Title restate, `@HumanitariansAI`. | — |

**June — `2026-06-medhavy-june` (17 beats, B00–B16)**

| Beat | Act | Pattern | Content | Source |
|---|---|---|---|---|
| B00 | ASK | `ClaudeComposerAsk` | Cold open for June. | all 5 weeks |
| B01 | WEEK 5 | `OptWeekMarker` | May 29 – Jun 4. Environment stood up; first verified render. | Week 5 |
| B02 | WEEK 5 | `ClaudeCodeBeat` | `UV_LINK_MODE=copy` (NTFS hardlinks) and `uv --active` (path mismatch). | Week 5 hours table |
| B03 | WEEK 6 | `OptWeekMarker` | Jun 5–11. Two substantive scenes built. | Week 6 |
| B04 | ASK | `ClaudeComposerAsk` | ASK→RESULT micro-beat. Composer typed with the Manim generation prompt; `runningText: "rendering Manim…"`. | — |
| B05 | WEEK 6 | Manim `B05` | **Manim.** Observable Universe — radial star distribution, glow ring. | Week 6 |
| B06 | WEEK 6 | Manim `B06` | **Manim.** Milky Way — logarithmic spiral arms, galactic bulge. | Week 6 |
| B07 | WEEK 7 | `OptWeekMarker` | Jun 12–18. The `BaseQuantities` bug week. | Week 7 |
| B08 | WEEK 7 | `ClaudeCodeBeat` | `FadeOut` inside a loop clearing static elements; `TransformMatchingShapes` replaces `ReplacementTransform`. | Week 7 |
| B09 | WEEK 7 | `ClaudeWindow` (`view: "artifact"`) | Prof. Sridhar's explicit written and verbal approval to continue. | Week 7 |
| B10 | WEEK 8 | `OptWeekMarker` | Jun 19–25. Scout adopted; scope narrowed to topics genuinely needing visualization. | Week 8 |
| B11 | WEEK 9 | `OptWeekMarker` | Jun 26 – Jul 2. Videos produced from the approved topic list. | Week 9 |
| B12 | WEEK 9 | `OptBlockerCard` | ElevenLabs narration blocked by a disabled API key — outside his control, reported not worked around. | Week 9 |
| B13 | HOURS | `OptHoursCard` | Five weeks × 20 = 100. | the five hours tables |
| B14 | VERDICT | `ClaudeVerdictArtifact` | Three bare recap sentences. | — |
| B15 | YOUR TURN | `ClaudeComposerAsk` | `greeting: "Your turn."` | — |
| B16 | OUTRO | `ClaudeTitleOutro` | Title restate. | — |

June runs one beat longer than a five-week month would suggest because B04 is the ASK micro-beat of the ASK→RESULT pair; beat ids run B00–B16.

**July — `2026-07-medhavy-july` (12 beats)**

| Beat | Act | Pattern | Content | Source |
|---|---|---|---|---|
| B00 | ASK | `ClaudeComposerAsk` | Cold open for July. | Weeks 10-12 |
| B01 | WEEK 10 | `OptWeekMarker` | Jul 3–9. Narration still blocked; effort redirected to production efficiency. | Week 10 |
| B02 | WEEK 10 | `ClaudeCodeBeat` | The chained render command; batch build of the first four chapters. | Week 10 hours table |
| B03 | WEEK 10 | `OptBlockerCard` | 12 planned topics pruned to the 4 that genuinely warranted animation. | Week 10 |
| B04 | WEEK 11 | `OptWeekMarker` | Jul 10–16. Third pivot: Brutalist plus a doodle-style visual direction. | Week 11 |
| B05 | WEEK 11 | `ClaudeWindow` (`view: "artifact"`) | A creative-direction change, not a technical failure; doodle-style technical scoping. | Week 11 |
| B06 | WEEK 12 | `OptWeekMarker` | Jul 17–23. Three sample videos completed and submitted to Prof. Sridhar. | Week 12 |
| B07 | WEEK 12 | `OptBlockerCard` | Awaiting review — a dependency blocker, not a technical one. | Week 12 "Blockers" |
| B08 | HOURS | `OptHoursCard` | Three weeks × 20 = 60. | the three hours tables |
| B09 | VERDICT | `ClaudeVerdictArtifact` | Three bare recap sentences. | — |
| B10 | YOUR TURN | `ClaudeComposerAsk` | `greeting: "Your turn."` | — |
| B11 | OUTRO | `ClaudeTitleOutro` | Title restate. | — |

**No July beat may mention Week 13, Jul 24–31, "in progress", or "the final week".**

### Fully worked example beat (the pattern to copy)

This is May B05 authored end to end. Every other body beat is written the same way: `show` first, then narration reacting to what is on screen, 45–70 words.

```json
{
  "beat_id": "B05",
  "act": "WEEK 2",
  "narration_text": "The access request looked like organizational slowness. It wasn't. The invite had been sent on the eleventh and was sitting unread in his own inbox until the fourteenth. Worth stating plainly, because the honest version is less flattering than the excuse — and because it's the version that tells you where to look next time.",
  "shot": {
    "type": "GRAPHIC",
    "source": "remotion",
    "motion": "reveal",
    "scene_type": "blocker",
    "show": [
      {"at": "0.0", "event": "BLOCKER rule draws left to right; label 'Repo access' types in"},
      {"at": "0.25", "event": "'Requested May 7' and 'Resolved May 14' anchor the two ends of a 7-day span bar"},
      {"at": "0.55", "event": "the span bar fills terracotta as the days count up 7"},
      {"at": "0.8", "event": "resolution line wipes in: 'The invite was sent May 11. It was unread.'"}
    ],
    "remotion": {
      "pattern": "OptBlockerCard",
      "props": {
        "label": "Repo access",
        "opened": "Requested May 7",
        "closed": "Resolved May 14",
        "days": 7,
        "resolution": "The invite was sent May 11. It was unread.",
        "court": "Varun's inbox",
        "folderLabel": "@HumanitariansAI"
      }
    }
  },
  "estimated_duration_s": 18
}
```

### Authoring laws that bind every beat

- **SHOW-DON'T-TELL.** Author the `show` block first. A beat with no `show` block is a script, not a beat. If a beat could be exported as a static slide with a voice over it, it is not done.
- **Evidence on screen, judgment in the voice.** Dates, filenames, hour counts, and the reports' own phrasings land as cards and counters. The narration reacts to them.
- **Narration budget 45–70 words** for body beats. Bookends (B00, the your-turn read, the verdict) are exempt.
- **ILLUSTRATE LAW.** The Claude UI appears only at B00, the ASK micro-beat, the verdict, the your-turn, and the outro. Never two consecutive beats on the same visual scheme — check the spine tables; they already alternate.
- **HANDOFF LAW.** Second-to-last beat is the your-turn composer; the narration reads the prompt aloud verbatim and then spends a line or two on what it does and why it's worth running.
- **One terracotta moment per beat.**

---

## Task 1: Enable the `am_michael` voice

**Files:**
- Modify: `runtime/scripts/generate_audio_kokoro.py:51`
- Modify: `runtime/scripts/generate_audio_kokoro.py:6-9` (the header comment that claims two voices)

**Interfaces:**
- Consumes: nothing.
- Produces: `generate_audio_kokoro.py` accepts `metadata.voice_kokoro = "am_michael"` and `beat["voice"] = "am_michael"` without exiting.

- [ ] **Step 1: Write the failing check**

Create the scratch fixture that proves the allowlist currently rejects the voice:

```bash
mkdir -p /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/voicecheck
cd /home/nayya/brutalist.art
cat > /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/voicecheck/beat_sheet.json <<'JSON'
{
  "metadata": {"slug": "voicecheck", "engine": "kokoro", "voice_kokoro": "am_michael"},
  "beats": [
    {"beat_id": "B00", "narration_text": "In week two, the extraction pipeline came together.", "estimated_duration_s": 4}
  ]
}
JSON
printf 'VERDICT: PASS\n' > /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/voicecheck/PEDAGOGY.md
```

- [ ] **Step 2: Run it to verify it fails**

Run:
```bash
cd /home/nayya/brutalist.art && python3 runtime/scripts/generate_audio_kokoro.py \
  /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/voicecheck --dry-run
```
Expected: exits non-zero with `[kokoro] B00 asks for voice 'am_michael' — this toolkit ships exactly two voices…`

- [ ] **Step 3: Make the minimal change**

In `runtime/scripts/generate_audio_kokoro.py`, replace line 51:

```python
ALLOWED_VOICES = {"am_onyx", "af_bella"}   # the only two voices in this toolkit
```

with:

```python
# am_michael added 2026-07-30 for the Medhavy OPT monthly recaps (user-directed).
# Still Kokoro-only and still free — the voices-v1.0.bin bundle already contains
# all 54 voices; this allowlist is the only thing that gates them.
ALLOWED_VOICES = {"am_onyx", "af_bella", "am_michael"}
```

Then update the module docstring at lines 6–9 so it no longer claims exactly two voices — change the `THE HOUSE VOICES — exactly two, both Kokoro:` heading to `THE HOUSE VOICES — all Kokoro:` and add a line for `am_michael` alongside the existing two.

- [ ] **Step 4: Run the dry run again to verify it passes**

Run:
```bash
cd /home/nayya/brutalist.art && python3 runtime/scripts/generate_audio_kokoro.py \
  /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/voicecheck --dry-run
```
Expected: `[kokoro] (dry-run) B00  voice=am_michael  …`, exit 0.

- [ ] **Step 5: Synthesize for real and listen to the duration**

Run:
```bash
cd /home/nayya/brutalist.art && python3 runtime/scripts/generate_audio_kokoro.py \
  /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/voicecheck
ffprobe -v error -show_entries format=duration -of csv=p=0 \
  /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/voicecheck/mp3/beat-B00.mp3
```
Expected: an mp3 is written; duration is between 2.5 and 6.0 seconds for that one sentence. If the file is 0 bytes or the duration is under 1s, the voice tensor did not load — stop and investigate before going further.

- [ ] **Step 6: Record, do not commit**

Do NOT run `git commit`. Append one line to `medhavy-opt/BUILD-LOG.md` (create the file and its parent directory if absent):

```
2026-07-30  Task 1  am_michael added to ALLOWED_VOICES in generate_audio_kokoro.py (user-directed). Smoke test: <duration>s for one sentence.
```

---

## Task 2: `OptWeekMarker` Remotion scene

**Files:**
- Create: `runtime/remotion/src/scenes/OptWeekMarker.tsx`
- Modify: `runtime/remotion/src/Root.tsx` (import + Composition registration)

**Interfaces:**
- Consumes: `CLAUDE`, `CLAUDE_FONT` from `../tokens/claude`; `SAFE`, `safeX`, `safeY` from `../tokens/layout`.
- Produces: Composition id `OptWeekMarker`, props
  `{ week: number; weeks: number; dates: string; thesis: string; bullets: string[]; folderLabel: string }`.
  Tasks 5, 9, and 12 author beats against exactly these prop names.

- [ ] **Step 1: Write the component**

Create `runtime/remotion/src/scenes/OptWeekMarker.tsx`:

```tsx
import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';
import { SAFE, safeX, safeY } from '../tokens/layout';

/**
 * OptWeekMarker — the spine beat of the Medhavy OPT monthly recaps.
 *
 * Marks WHERE in the month we are (a pip timeline across the top), WHICH week
 * (giant serif numeral + date range), and WHAT that week was (a thesis line and
 * up to four evidence bullets that wipe in one at a time).
 *
 * The one terracotta moment is the active pip and the numeral's rule.
 */

export const optWeekMarkerSchema = z.object({
  week: z.number().default(1),
  weeks: z.number().default(4),
  dates: z.string().default('May 1–7, 2026'),
  thesis: z.string().default('Two workstreams, from day one.'),
  bullets: z.array(z.string()).default([]),
  folderLabel: z.string().default('@HumanitariansAI'),
});
export type OptWeekMarkerProps = z.infer<typeof optWeekMarkerSchema>;

const SERIF = CLAUDE_FONT.serif;
const SANS = CLAUDE_FONT.ui;
const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

export const OptWeekMarker: React.FC<OptWeekMarkerProps> = ({
  week, weeks, dates, thesis, bullets, folderLabel,
}) => {
  const frame = useCurrentFrame();
  const inAt = (start: number) => clamp(interpolate(frame, [start, start + 12], [0, 1]), 0, 1);

  const pipW = 120;
  const pipGap = 18;
  const railW = weeks * pipW + (weeks - 1) * pipGap;

  return (
    <AbsoluteFill style={{ background: CLAUDE.PAGE }}>
      {/* timeline rail */}
      <div style={{ position: 'absolute', left: safeX(0), top: safeY(0), display: 'flex', gap: pipGap, width: railW }}>
        {Array.from({ length: weeks }, (_, i) => (
          <div key={i} style={{
            width: pipW, height: 10, borderRadius: 5,
            background: i + 1 === week ? CLAUDE.SPARK : CLAUDE.PILL,
            opacity: i + 1 <= week ? 1 : 0.45,
            transform: `scaleX(${i + 1 === week ? inAt(6) : 1})`,
            transformOrigin: 'left center',
          }} />
        ))}
      </div>

      {/* week numeral + dates */}
      <div style={{ position: 'absolute', left: safeX(0), top: safeY(90), opacity: inAt(0) }}>
        <div style={{ fontFamily: SANS, fontSize: 30, letterSpacing: '0.16em', color: CLAUDE.INK_SOFT }}>
          WEEK {week} OF {weeks}
        </div>
        <div style={{ fontFamily: SERIF, fontSize: 132, lineHeight: 1.02, color: CLAUDE.INK, marginTop: 4 }}>
          {dates}
        </div>
        <div style={{ width: 260, height: 6, background: CLAUDE.SPARK, marginTop: 22, transform: `scaleX(${inAt(10)})`, transformOrigin: 'left center' }} />
      </div>

      {/* thesis */}
      <div style={{
        position: 'absolute', left: safeX(0), top: safeY(400), maxWidth: SAFE.w,
        fontFamily: SERIF, fontSize: 58, lineHeight: 1.25, color: CLAUDE.INK, opacity: inAt(18),
      }}>
        {thesis}
      </div>

      {/* evidence bullets */}
      <div style={{ position: 'absolute', left: safeX(0), top: safeY(540), maxWidth: SAFE.w, display: 'flex', flexDirection: 'column', gap: 26 }}>
        {bullets.slice(0, 4).map((b, i) => (
          <div key={i} style={{ display: 'flex', gap: 22, alignItems: 'baseline', opacity: inAt(30 + i * 14) }}>
            <div style={{ width: 22, height: 22, flexShrink: 0, borderRadius: 11, border: `3px solid ${CLAUDE.INK_SOFT}` }} />
            <div style={{ fontFamily: SANS, fontSize: 38, lineHeight: 1.34, color: CLAUDE.INK, maxWidth: SAFE.w - 60 }}>{b}</div>
          </div>
        ))}
      </div>

      {/* channel chip */}
      <div style={{
        position: 'absolute', left: safeX(0), top: safeY(SAFE.h - 34),
        fontFamily: SANS, fontSize: 26, color: CLAUDE.GHOST, letterSpacing: '0.06em',
      }}>
        {folderLabel}
      </div>
    </AbsoluteFill>
  );
};
```

- [ ] **Step 2: Register the Composition**

In `runtime/remotion/src/Root.tsx`, add the import beside the other scene imports:

```tsx
import { OptWeekMarker, optWeekMarkerSchema } from './scenes/OptWeekMarker';
```

and add this registration immediately after the `ClaudeTitleOutro` Composition (search for `id="ClaudeTitleOutro"`):

```tsx
      {/* ── medhavy-opt — OPT monthly recaps ── */}
      <Composition id="OptWeekMarker" component={OptWeekMarker}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={optWeekMarkerSchema}
        defaultProps={{
          week: 2, weeks: 4, dates: 'May 8–14, 2026',
          thesis: 'The first working clinical-data pipeline.',
          bullets: [
            'Extracted test patient IDs and the Bulk FHIR Group ID.',
            'get_patient_demographics.py → patient_demographics.csv',
            'Six clinical categories, each to its own CSV.',
          ],
          folderLabel: '@HumanitariansAI',
        }} />
```

- [ ] **Step 3: Verify it appears in the composition list**

Run:
```bash
cd /home/nayya/brutalist.art/runtime/remotion && npx remotion compositions src/index.ts 2>&1 | grep -i optweekmarker
```
Expected: a line containing `OptWeekMarker`. If nothing prints, the import or registration is wrong — fix before rendering.

- [ ] **Step 4: Render a still and LOOK at it**

Run:
```bash
cd /home/nayya/brutalist.art/runtime/remotion && npx remotion still src/index.ts OptWeekMarker \
  /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/optweekmarker.png \
  --frame=90 --image-format=png
```
Then `Read` the PNG. Audit against the rubric and fix the scene source until all pass:
- Nothing crosses the safe inset (x 96–1824, y 54–1026).
- The date-range serif does not overflow or clip; the thesis wraps rather than running off.
- Bullets do not collide with the channel chip at the bottom.
- Exactly one terracotta element is prominent (the active pip and the rule read as one accent moment).
- Content occupies the safe area — no large dead band. If more than ~40% of the safe area is empty, scale type up.

- [ ] **Step 5: Render the longest realistic content and LOOK again**

The May B09 beat has the longest bullets. Render with overridden props:

```bash
cd /home/nayya/brutalist.art/runtime/remotion && cat > /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/wm-long.json <<'JSON'
{"week":4,"weeks":4,"dates":"May 22–28, 2026",
 "thesis":"The workstream ended on the strength of his own reporting.",
 "bullets":["Prof. Sridhar discontinued the EPIC integration workstream, citing the accumulated blockers already documented.",
            "Sparse sandbox data, OAuth friction, an unclear API-versus-database access model.",
            "Same day: reassigned to Manim instructional video production for the physics mechanics textbook.",
            "Access requested same day."],
 "folderLabel":"@HumanitariansAI"}
JSON
npx remotion still src/index.ts OptWeekMarker \
  /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/optweekmarker-long.png \
  --frame=120 --image-format=png --props=/tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/wm-long.json
```
`Read` the PNG. Expected: four bullets fit inside the safe area with no overlap and no clipping. If they overflow, reduce the bullet font size to 34 and the gap to 20, re-render, and look again. Do not proceed with an overflowing card.

- [ ] **Step 6: Record, do not commit**

Append to `medhavy-opt/BUILD-LOG.md`. No `git commit`.

---

## Task 3: `OptHoursCard` Remotion scene

**Files:**
- Create: `runtime/remotion/src/scenes/OptHoursCard.tsx`
- Modify: `runtime/remotion/src/Root.tsx`

**Interfaces:**
- Consumes: same tokens as Task 2.
- Produces: Composition id `OptHoursCard`, props
  `{ heading: string; rows: {label: string; hours: number}[]; total: number; caption: string; folderLabel: string }`.

- [ ] **Step 1: Write the component**

Create `runtime/remotion/src/scenes/OptHoursCard.tsx`:

```tsx
import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';
import { SAFE, safeX, safeY } from '../tokens/layout';

/**
 * OptHoursCard — the month's documented OPT hours, one row per week.
 *
 * Bars grow to their value as the narration lands on the figure. The total is
 * the one terracotta moment. Figures are DOCUMENTED hours quoted from the
 * weekly reports, never restated as measured — the caption prop must say so.
 */

export const optHoursCardSchema = z.object({
  heading: z.string().default('Documented hours'),
  rows: z.array(z.object({ label: z.string(), hours: z.number() })).default([]),
  total: z.number().default(80),
  caption: z.string().default('Reconstructed from task descriptions, not session-logged.'),
  folderLabel: z.string().default('@HumanitariansAI'),
});
export type OptHoursCardProps = z.infer<typeof optHoursCardSchema>;

const SERIF = CLAUDE_FONT.serif;
const SANS = CLAUDE_FONT.ui;
const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

export const OptHoursCard: React.FC<OptHoursCardProps> = ({
  heading, rows, total, caption, folderLabel,
}) => {
  const frame = useCurrentFrame();
  const inAt = (start: number) => clamp(interpolate(frame, [start, start + 14], [0, 1]), 0, 1);
  const max = Math.max(1, ...rows.map((r) => r.hours));
  const barMaxW = 900;

  return (
    <AbsoluteFill style={{ background: CLAUDE.PAGE }}>
      <div style={{
        position: 'absolute', left: safeX(0), top: safeY(10),
        fontFamily: SANS, fontSize: 30, letterSpacing: '0.16em', color: CLAUDE.INK_SOFT, opacity: inAt(0),
      }}>
        {heading.toUpperCase()}
      </div>

      <div style={{ position: 'absolute', left: safeX(0), top: safeY(90), display: 'flex', flexDirection: 'column', gap: 30 }}>
        {rows.map((r, i) => {
          const p = inAt(10 + i * 10);
          return (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 28 }}>
              <div style={{ width: 300, fontFamily: SANS, fontSize: 38, color: CLAUDE.INK, opacity: p }}>{r.label}</div>
              <div style={{ width: barMaxW, height: 44, background: CLAUDE.PILL, borderRadius: 4 }}>
                <div style={{
                  width: (r.hours / max) * barMaxW * p, height: 44,
                  background: CLAUDE.INK_SOFT, borderRadius: 4,
                }} />
              </div>
              <div style={{ fontFamily: SERIF, fontSize: 46, color: CLAUDE.INK, opacity: p }}>
                {Math.round(r.hours * p)}
              </div>
            </div>
          );
        })}
      </div>

      <div style={{
        position: 'absolute', left: safeX(0), top: safeY(SAFE.h - 250),
        display: 'flex', alignItems: 'baseline', gap: 26, opacity: inAt(10 + rows.length * 10 + 8),
      }}>
        <div style={{ fontFamily: SERIF, fontSize: 150, lineHeight: 1, color: CLAUDE.SPARK }}>{total}</div>
        <div style={{ fontFamily: SANS, fontSize: 40, color: CLAUDE.INK }}>hours documented</div>
      </div>

      <div style={{
        position: 'absolute', left: safeX(0), top: safeY(SAFE.h - 74), maxWidth: SAFE.w,
        fontFamily: SANS, fontSize: 27, lineHeight: 1.35, color: CLAUDE.INK_SOFT,
        opacity: inAt(10 + rows.length * 10 + 18),
      }}>
        {caption}
      </div>

      <div style={{
        position: 'absolute', left: safeX(SAFE.w - 240), top: safeY(SAFE.h - 34), width: 240, textAlign: 'right',
        fontFamily: SANS, fontSize: 26, color: CLAUDE.GHOST, letterSpacing: '0.06em',
      }}>
        {folderLabel}
      </div>
    </AbsoluteFill>
  );
};
```

- [ ] **Step 2: Register the Composition**

In `runtime/remotion/src/Root.tsx`, add the import:

```tsx
import { OptHoursCard, optHoursCardSchema } from './scenes/OptHoursCard';
```

and register directly after the `OptWeekMarker` Composition:

```tsx
      <Composition id="OptHoursCard" component={OptHoursCard}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={optHoursCardSchema}
        defaultProps={{
          heading: 'Documented hours — May 2026',
          rows: [
            { label: 'Week 1 · May 1–7', hours: 20 },
            { label: 'Week 2 · May 8–14', hours: 20 },
            { label: 'Week 3 · May 15–21', hours: 20 },
            { label: 'Week 4 · May 22–28', hours: 20 },
          ],
          total: 80,
          caption: 'Every week meets the 20-hour OPT floor. Breakdowns are reconstructed from task descriptions, not session-logged.',
          folderLabel: '@HumanitariansAI',
        }} />
```

- [ ] **Step 3: Verify registration**

Run:
```bash
cd /home/nayya/brutalist.art/runtime/remotion && npx remotion compositions src/index.ts 2>&1 | grep -i opthourscard
```
Expected: a line containing `OptHoursCard`.

- [ ] **Step 4: Render a still at the end state and LOOK at it**

Run:
```bash
cd /home/nayya/brutalist.art/runtime/remotion && npx remotion still src/index.ts OptHoursCard \
  /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/opthourscard.png \
  --frame=180 --image-format=png
```
`Read` the PNG. Check: all four bars are at full extent with `20` beside each; the terracotta `80` does not collide with the caption; the caption wraps inside `SAFE.w`; the chip sits bottom-right inside the safe inset.

- [ ] **Step 5: Render the five-row June case and LOOK again**

Run:
```bash
cd /home/nayya/brutalist.art/runtime/remotion && cat > /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/hours-june.json <<'JSON'
{"heading":"Documented hours — June 2026",
 "rows":[{"label":"Week 5 · May 29–Jun 4","hours":20},
         {"label":"Week 6 · Jun 5–11","hours":20},
         {"label":"Week 7 · Jun 12–18","hours":20},
         {"label":"Week 8 · Jun 19–25","hours":20},
         {"label":"Week 9 · Jun 26–Jul 2","hours":20}],
 "total":100,
 "caption":"Every week meets the 20-hour OPT floor. Breakdowns are reconstructed from task descriptions, not session-logged.",
 "folderLabel":"@HumanitariansAI"}
JSON
npx remotion still src/index.ts OptHoursCard \
  /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/opthourscard-june.png \
  --frame=220 --image-format=png --props=/tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/hours-june.json
```
`Read` the PNG. Expected: five rows fit above the total block with no overlap. If row 5 collides with the terracotta total, reduce the row gap to 22 and re-render. Do not proceed with a collision.

- [ ] **Step 6: Record, do not commit**

Append to `medhavy-opt/BUILD-LOG.md`. No `git commit`.

---

## Task 4: `OptBlockerCard` Remotion scene

**Files:**
- Create: `runtime/remotion/src/scenes/OptBlockerCard.tsx`
- Modify: `runtime/remotion/src/Root.tsx`

**Interfaces:**
- Consumes: same tokens as Task 2.
- Produces: Composition id `OptBlockerCard`, props
  `{ label: string; opened: string; closed: string; days: number; resolution: string; court: string; folderLabel: string }`.
  These are the exact prop names used in the worked example beat above.

- [ ] **Step 1: Write the component**

Create `runtime/remotion/src/scenes/OptBlockerCard.tsx`:

```tsx
import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';
import { SAFE, safeX, safeY } from '../tokens/layout';

/**
 * OptBlockerCard — the candor register of the OPT recaps.
 *
 * A blocker gets its own visual treatment so honesty reads as a deliberate
 * choice rather than something buried in narration: a heavy rule, the two
 * dates that bound it, a span bar that fills as the days count up, whose
 * court the ball was in, and how it resolved.
 *
 * `closed` may be empty for a blocker still open at the video's end; then the
 * span bar stops short and no resolution line renders.
 */

export const optBlockerCardSchema = z.object({
  label: z.string().default('Repo access'),
  opened: z.string().default('Requested May 7'),
  closed: z.string().default('Resolved May 14'),
  days: z.number().default(7),
  resolution: z.string().default('The invite was sent May 11. It was unread.'),
  court: z.string().default("Varun's inbox"),
  folderLabel: z.string().default('@HumanitariansAI'),
});
export type OptBlockerCardProps = z.infer<typeof optBlockerCardSchema>;

const SERIF = CLAUDE_FONT.serif;
const SANS = CLAUDE_FONT.ui;
const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

export const OptBlockerCard: React.FC<OptBlockerCardProps> = ({
  label, opened, closed, days, resolution, court, folderLabel,
}) => {
  const frame = useCurrentFrame();
  const inAt = (start: number) => clamp(interpolate(frame, [start, start + 14], [0, 1]), 0, 1);
  const spanW = SAFE.w - 120;
  const fill = inAt(22);
  const open = closed.trim() === '';

  return (
    <AbsoluteFill style={{ background: CLAUDE.FOOTER }}>
      {/* the heavy rule that marks this register */}
      <div style={{
        position: 'absolute', left: safeX(0), top: safeY(0), height: 14, width: SAFE.w,
        background: CLAUDE.INK, transform: `scaleX(${inAt(0)})`, transformOrigin: 'left center',
      }} />

      <div style={{
        position: 'absolute', left: safeX(0), top: safeY(44),
        fontFamily: SANS, fontSize: 28, letterSpacing: '0.2em', color: CLAUDE.INK_SOFT, opacity: inAt(2),
      }}>
        BLOCKER
      </div>

      <div style={{
        position: 'absolute', left: safeX(0), top: safeY(96), maxWidth: SAFE.w,
        fontFamily: SERIF, fontSize: 96, lineHeight: 1.1, color: CLAUDE.INK, opacity: inAt(6),
      }}>
        {label}
      </div>

      {/* span bar */}
      <div style={{ position: 'absolute', left: safeX(60), top: safeY(300), width: spanW }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontFamily: SANS, fontSize: 32, color: CLAUDE.INK, opacity: inAt(16) }}>
          <span>{opened}</span>
          <span style={{ opacity: open ? 0 : 1 }}>{closed}</span>
        </div>
        <div style={{ marginTop: 16, width: spanW, height: 30, background: CLAUDE.PILL, borderRadius: 4 }}>
          <div style={{
            width: spanW * fill * (open ? 0.72 : 1), height: 30,
            background: CLAUDE.SPARK, borderRadius: 4,
          }} />
        </div>
        <div style={{ marginTop: 18, fontFamily: SERIF, fontSize: 60, color: CLAUDE.INK, opacity: inAt(24) }}>
          {Math.round(days * fill)} days{open ? ' — and counting' : ''}
        </div>
      </div>

      <div style={{
        position: 'absolute', left: safeX(60), top: safeY(560), maxWidth: SAFE.w - 120,
        fontFamily: SANS, fontSize: 30, color: CLAUDE.INK_SOFT, opacity: inAt(30),
      }}>
        Ball in: {court}
      </div>

      <div style={{
        position: 'absolute', left: safeX(60), top: safeY(630), maxWidth: SAFE.w - 120,
        fontFamily: SERIF, fontSize: 50, lineHeight: 1.3, color: CLAUDE.INK, opacity: inAt(36),
      }}>
        {resolution}
      </div>

      <div style={{
        position: 'absolute', left: safeX(0), top: safeY(SAFE.h - 34),
        fontFamily: SANS, fontSize: 26, color: CLAUDE.GHOST, letterSpacing: '0.06em',
      }}>
        {folderLabel}
      </div>
    </AbsoluteFill>
  );
};
```

- [ ] **Step 2: Register the Composition**

In `runtime/remotion/src/Root.tsx`, add the import:

```tsx
import { OptBlockerCard, optBlockerCardSchema } from './scenes/OptBlockerCard';
```

and register directly after the `OptHoursCard` Composition:

```tsx
      <Composition id="OptBlockerCard" component={OptBlockerCard}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={optBlockerCardSchema}
        defaultProps={{
          label: 'Repo access',
          opened: 'Requested May 7',
          closed: 'Resolved May 14',
          days: 7,
          resolution: 'The invite was sent May 11. It was unread.',
          court: "Varun's inbox",
          folderLabel: '@HumanitariansAI',
        }} />
```

- [ ] **Step 3: Verify registration**

Run:
```bash
cd /home/nayya/brutalist.art/runtime/remotion && npx remotion compositions src/index.ts 2>&1 | grep -i optblockercard
```
Expected: a line containing `OptBlockerCard`.

- [ ] **Step 4: Render the resolved case and LOOK at it**

Run:
```bash
cd /home/nayya/brutalist.art/runtime/remotion && npx remotion still src/index.ts OptBlockerCard \
  /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/optblockercard.png \
  --frame=180 --image-format=png
```
`Read` the PNG. Check: the `#F1EFE7` ground is visibly distinct from the `#FAF9F5` of the week markers (this is what makes the register legible); the span bar fills fully; `7 days` reads; the resolution line wraps inside the safe area; only the span bar is terracotta.

- [ ] **Step 5: Render the still-open case and LOOK again**

The July B07 blocker (awaiting Sridhar's review) is open. Run:

```bash
cd /home/nayya/brutalist.art/runtime/remotion && cat > /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/blocker-open.json <<'JSON'
{"label":"Awaiting review","opened":"Submitted Jul 23","closed":"","days":0,
 "resolution":"Work complete on his end. Progress now depends on someone else's response time.",
 "court":"Prof. Sridhar","folderLabel":"@HumanitariansAI"}
JSON
npx remotion still src/index.ts OptBlockerCard \
  /tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/optblockercard-open.png \
  --frame=180 --image-format=png --props=/tmp/claude-1000/-home-nayya-brutalist-art/22b2036d-18f9-4a54-81ba-be929c08dfb4/scratchpad/blocker-open.json
```
`Read` the PNG. Expected: no closing date renders, the bar stops short of the right edge, and the day count reads `0 days — and counting`. If `0 days — and counting` reads awkwardly, change the July beat to pass `days: 7` (Jul 23 → Jul 30) rather than changing the component.

- [ ] **Step 6: Record, do not commit**

Append to `medhavy-opt/BUILD-LOG.md`. No `git commit`.

---

## Task 5: May — scaffold, beat sheet, and PEDAGOGY

**Files:**
- Create: `medhavy-opt/youtube/2026-05-medhavy-may/beat_sheet.json`
- Create: `medhavy-opt/youtube/2026-05-medhavy-may/PEDAGOGY.md`
- Create: `medhavy-opt/youtube/2026-05-medhavy-may/SOURCES.md`
- Read: `hai_reports_weeks_1-12.md` lines 1–222 (Weeks 1–4)

**Interfaces:**
- Consumes: Compositions `OptWeekMarker`, `OptHoursCard`, `OptBlockerCard` (Tasks 2–4), and the stock `ClaudeComposerAsk`, `ClaudeCodeBeat`, `ClaudeVerdictArtifact`, `ClaudeTitleOutro`.
- Produces: a valid 14-beat `beat_sheet.json` whose metadata block is the template every later video copies.

- [ ] **Step 1: Read the source weeks in full**

`Read` `hai_reports_weeks_1-12.md` lines 1–222. Every claim in the beat sheet must trace to a line in that range. Do not work from the summaries in this plan — they are a map, not the territory.

- [ ] **Step 2: Author the beat sheet**

Create `medhavy-opt/youtube/2026-05-medhavy-may/beat_sheet.json` with the shared metadata block (May row of the overrides table) and the 14 beats of the May spine. For each body beat, in this order:
1. Write the `show` block — the ordered visual events.
2. Write `narration_text` as the voice reacting to those events, 45–70 words, third person, Pragmatist register.
3. Fill `shot.remotion.props` from the component's prop contract in Tasks 2–4.
4. Set `estimated_duration_s` to `round(words / 2.3)` — measured in Task 1: Kokoro `am_michael` produced 8 words in 3.48s. This is only a pre-audio estimate; the measured duration replaces it. At that rate a 45–70 word body beat runs 20–30s, so the 14-beat May spine lands near 4 minutes rather than 3 — that is the content's length, and the spec forbids trimming to a target.

B00's `ClaudeComposerAsk` props: `command` (the ask, also the `narration_text`), `topic: "MEDHAVY · MAY 2026"`, `segment: "Two Fronts"`, `greeting: "Hej, HAI"`, `runningText: "reading the weekly reports…"`, `folderLabel: "@HumanitariansAI"`, `output` (three one-line month headlines).

B12's your-turn props: `greeting: "Your turn."`, `runningText: "paste this into Claude…"`, `command` = the prompt, and `narration_text` must contain that prompt verbatim followed by one or two lines on what it does and why it is worth running.

B13's `ClaudeTitleOutro` props: `title: "Two Fronts."`, `handle: "@HumanitariansAI"`, `subline: "Medhavy · OPT month one"`.

- [ ] **Step 3: Validate the sheet mechanically**

Run:
```bash
cd /home/nayya/brutalist.art && python3 - <<'PY'
import json, pathlib, re
p = pathlib.Path("medhavy-opt/youtube/2026-05-medhavy-may/beat_sheet.json")
s = json.loads(p.read_text())
m, beats = s["metadata"], s["beats"]
assert m["voice_kokoro"] == "am_michael", m["voice_kokoro"]
assert m["channel_title"] == "@HumanitariansAI"
assert m["aspect_ratio"] == "16:9"
ids = [b["beat_id"] for b in beats]
assert ids == [f"B{i:02d}" for i in range(len(beats))], ids
prev = None
for b in beats:
    sh = b["shot"]
    pat = (sh.get("remotion") or {}).get("pattern")
    assert pat, f"{b['beat_id']} has no remotion.pattern"
    assert "916" not in pat, f"{b['beat_id']} uses a 9:16 composition"
    assert sh.get("show"), f"{b['beat_id']} has no show block"
    assert pat != prev or b["beat_id"] in ("B00",), f"{b['beat_id']} repeats {pat} back-to-back"
    prev = pat
    w = len(b["narration_text"].split())
    if b["act"] not in ("ASK", "VERDICT", "YOUR TURN", "OUTRO"):
        assert 40 <= w <= 75, f"{b['beat_id']} narration is {w} words"
blob = json.dumps(s).lower()
for bad in ("week 13", "jul 24", "july 24", "in progress"):
    assert bad not in blob, f"forbidden phrase present: {bad}"
print(f"OK — {len(beats)} beats, patterns: {sorted({(b['shot']['remotion']['pattern']) for b in beats})}")
PY
```
Expected: `OK — 14 beats, patterns: [...]`. Every assertion failure is a real defect — fix the sheet, do not weaken the check.

- [ ] **Step 4: Confirm every pattern is renderable**

Run:
```bash
cd /home/nayya/brutalist.art && python3 runtime/scripts/remotion_scenes.py medhavy-opt/youtube/2026-05-medhavy-may --list
```
Expected: 14 lines, each `SLATE`, each naming a pattern. Cross-check each pattern name against `npx remotion compositions src/index.ts` output — a typo here surfaces as a slate later, not as an error.

- [ ] **Step 5: Write SOURCES.md**

Create `medhavy-opt/youtube/2026-05-medhavy-may/SOURCES.md` recording: the source file (`hai_reports_weeks_1-12.md`, Weeks 1–4), the compiler credit ("Addams — OPT Volunteer Documentation System"), the Substack URLs published in Weeks 1–4, and a "Corrections applied" section listing anything you softened or declined to state because the report did not support it.

- [ ] **Step 6: Write PEDAGOGY.md WITHOUT the verdict line**

Create `medhavy-opt/youtube/2026-05-medhavy-may/PEDAGOGY.md`:

```markdown
# PEDAGOGY — 2026-05-medhavy-may ("Two Fronts.")

**Reviewer:** Varun Nayyar
**Date:** <fill at review>

## What this video claims
<one paragraph: the month's thesis in plain language>

## Beat-by-beat narration
<the full narration_text of all 14 beats, in order, each under its beat id and act>

## Checks
- [ ] Every factual claim traces to a line in hai_reports_weeks_1-12.md, Weeks 1-4
- [ ] No invented metric; hours are stated as DOCUMENTED, not measured
- [ ] Third person throughout; the narrator never speaks as Varun
- [ ] No mention of Week 13 or any date after Jul 23, 2026
- [ ] Blockers are present and stated plainly
- [ ] Body beats are 45-70 words
- [ ] The your-turn prompt is read aloud verbatim and then discussed

VERDICT: <PENDING — a human writes PASS here after reading the above>
```

Leave the verdict as `PENDING`. Task 6 does not begin until a human replaces it.

- [ ] **Step 7: Record, do not commit**

Append to `medhavy-opt/BUILD-LOG.md`. No `git commit`.

---

## Task 6: May — GATE P, audio, and the review cut

**Files:**
- Modify: `medhavy-opt/youtube/2026-05-medhavy-may/PEDAGOGY.md` (human writes PASS)
- Generated: `medhavy-opt/youtube/2026-05-medhavy-may/mp3/`, `media/`, `_qc/`, `2026-05-medhavy-may-slate.mp4`

**Interfaces:**
- Consumes: the beat sheet from Task 5.
- Produces: `actual_duration_s` on every beat; `media/B*.mp4` for all 14 beats; a compiled review cut.

- [ ] **Step 1: STOP for the human gate**

Present the PEDAGOGY.md narration to the user and ask them to sign it. GATE P is a hard stop — do not generate audio, and never pass `--no-gate`. Verify the signature landed:

```bash
cd /home/nayya/brutalist.art && grep -c "VERDICT: PASS" medhavy-opt/youtube/2026-05-medhavy-may/PEDAGOGY.md
```
Expected: `1`. If `0`, wait.

- [ ] **Step 2: Generate the narration**

Run:
```bash
cd /home/nayya/brutalist.art && python3 runtime/scripts/generate_audio_kokoro.py medhavy-opt/youtube/2026-05-medhavy-may
```
Expected: 14 lines of `[kokoro] B..` output, one mp3 per beat.

- [ ] **Step 3: Check the runtime the audio actually produced**

Run:
```bash
cd /home/nayya/brutalist.art && python3 - <<'PY'
import json, pathlib
s = json.loads(pathlib.Path("medhavy-opt/youtube/2026-05-medhavy-may/beat_sheet.json").read_text())
d = [(b["beat_id"], b.get("actual_duration_s")) for b in s["beats"]]
assert all(v for _, v in d), [k for k, v in d if not v]
total = sum(v for _, v in d)
for k, v in d:
    print(f"  {k}  {v:6.2f}s")
print(f"TOTAL {total:.1f}s = {total/60:.2f} min")
PY
```
Expected: every beat has a measured duration; total lands roughly 2.5–4.0 minutes. Duration is an output — do not trim narration to hit 3:00. Only act if a beat is absurd (under 3s or over 40s), and then by rewriting that beat's narration and re-running Step 2 with `--only B0X`, never by editing durations.

- [ ] **Step 4: Render the Remotion beats**

Run in the foreground:
```bash
cd /home/nayya/brutalist.art && python3 runtime/scripts/remotion_scenes.py medhavy-opt/youtube/2026-05-medhavy-may
```
Expected: `ok: <Pattern> -> media/B..mp4 (extended to N.Ns)` for all 14. Any `FAIL:` line names a bad prop or an unregistered composition — fix and re-run with `--only B0X --force`.

- [ ] **Step 5: Compile the review cut**

Run:
```bash
cd /home/nayya/brutalist.art && python3 runtime/scripts/compile.py medhavy-opt/youtube/2026-05-medhavy-may --review --height 1080
```
Expected: `2026-05-medhavy-may-slate.mp4` is written.

- [ ] **Step 6: Visual QC — sample frames and LOOK at them**

Run:
```bash
cd /home/nayya/brutalist.art/medhavy-opt/youtube/2026-05-medhavy-may && mkdir -p _qc/frames && \
ffmpeg -y -i 2026-05-medhavy-may-slate.mp4 -vf fps=2 _qc/frames/%05d.png 2>&1 | tail -2 && \
ls _qc/frames | wc -l
```
Then `Read` a spread of those PNGs — at minimum one frame from each beat's span (compute spans from the `actual_duration_s` values; sample near 15%, 50%, and 85% of each). Audit all nine points: edge bleed/clipping, title-safe margins, container overflow, collision, offscreen anchors, legibility, brand bug placement, aspect (must be 16:9), and canvas fill.

Write `_qc/REPORT.md` listing every defect with severity (BLOCKER / MAJOR / MINOR), the beat, and the fix. Fix root causes in the scene source or the beat props — never by hand-editing the mp4 — and re-run Steps 4–6 until zero BLOCKER and zero MAJOR remain.

- [ ] **Step 7: Confirm no slates survived**

Run:
```bash
cd /home/nayya/brutalist.art && python3 runtime/scripts/todo.py medhavy-opt/youtube/2026-05-medhavy-may --open
```
Expected: no open beats. A remaining slate means a beat never rendered — go back to Step 4.

- [ ] **Step 8: Record, do not commit**

Append the QC outcome and total runtime to `medhavy-opt/BUILD-LOG.md`. No `git commit`.

---

## Task 7: May — final master

**Files:**
- Generated: `medhavy-opt/youtube/2026-05-medhavy-may/2026-05-medhavy-may.mp4`

**Interfaces:**
- Consumes: the QC-clean review cut from Task 6.
- Produces: the May master. June and July copy this reel's metadata block and component usage verbatim.

- [ ] **Step 1: Render the master**

Run:
```bash
cd /home/nayya/brutalist.art && ./art final medhavy-opt/youtube/2026-05-medhavy-may
```
This calls `compile.py … --height 2160`. Expected: `2026-05-medhavy-may.mp4` (no `-slate` suffix). If compile refuses, unfilled slates remain — return to Task 6 Step 4.

- [ ] **Step 2: Verify the file, then verify the frames**

Run:
```bash
cd /home/nayya/brutalist.art/medhavy-opt/youtube/2026-05-medhavy-may && \
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,nb_frames \
  -show_entries format=duration -of default=nw=1 2026-05-medhavy-may.mp4
```
Expected: `width=3840 height=2160`, duration matching the sum from Task 6 Step 3 within a second.

Then sample and `Read` three frames from the master itself — the cold open, one week marker, and the outro — to confirm the 4K upscale did not clip anything the 1080 pass showed clean.

- [ ] **Step 3: Confirm the master stays put**

Do not upload, publish, or move the file. Confirm it sits in the reel folder and stop.

- [ ] **Step 4: Record, do not commit**

Append to `medhavy-opt/BUILD-LOG.md`. No `git commit`.

---

## Task 8: June — scaffold, beat sheet, Manim scenes, and paperwork

**Files:**
- Create: `medhavy-opt/youtube/2026-06-medhavy-june/beat_sheet.json`
- Create: `medhavy-opt/youtube/2026-06-medhavy-june/scenes.py`
- Create: `medhavy-opt/youtube/2026-06-medhavy-june/PEDAGOGY.md`
- Create: `medhavy-opt/youtube/2026-06-medhavy-june/SOURCES.md`
- Create: `medhavy-opt/youtube/2026-06-medhavy-june/FACTCHECK.md`
- Create: `medhavy-opt/youtube/2026-06-medhavy-june/SHOTLIST.md`
- Create: `medhavy-opt/youtube/2026-06-medhavy-june/PROMPTS.md`
- Read: `hai_reports_weeks_1-12.md` lines 223–482 (Weeks 5–9)

**Interfaces:**
- Consumes: the three Opt* Compositions and the May metadata block.
- Produces: a 17-beat sheet (B00–B16) plus two Manim scene classes named `B05_ObservableUniverse` and `B06_MilkyWay` — `run.sh` derives the beat id from the text before the first underscore, so those names are load-bearing.

- [ ] **Step 1: Read the source weeks in full**

`Read` `hai_reports_weeks_1-12.md` lines 223–482.

- [ ] **Step 2: Author the beat sheet**

Same procedure as Task 5 Step 2, following the June spine table. Metadata takes the June row of the overrides table. Two June-specific points:

- B04 is the ASK half of an ASK→RESULT pair — `ClaudeComposerAsk` with the actual Manim generation prompt typed in and `runningText: "rendering Manim…"`. B05 is its RESULT. The pair reads as a receipt; do not separate them.
- B05 and B06 are Manim beats, so their `shot` has **no** `shot.remotion` block. Use:

```json
"shot": {
  "type": "GRAPHIC",
  "source": "manim",
  "motion": "build",
  "scene_type": "manim-fragment",
  "show": [
    {"at": "0.0", "event": "black field; stars seed outward from center on a corrected radial distribution"},
    {"at": "0.5", "event": "glow ring expands to the observable-universe boundary"},
    {"at": "0.8", "event": "scale label settles beneath"}
  ]
}
```

- [ ] **Step 3: Write the Manim scenes**

Create `medhavy-opt/youtube/2026-06-medhavy-june/scenes.py` with exactly two `Scene` subclasses, `B05_ObservableUniverse` and `B06_MilkyWay`. Requirements:
- Class names must match `^[A-Z][A-Za-z0-9]*_\w+$` — `run.sh` extracts them with that regex and slots `B05_*.mp4` to `manim/B05.mp4`.
- These recreate what Varun built in Week 6: the corrected radial star distribution with a glow ring, and logarithmic spiral arms with a galactic bulge. The point is that the math is right — a radial distribution that clusters at the center is the exact bug the report says he solved, so the star radii must be drawn as `r = R * sqrt(uniform(0,1))` for uniform areal density, and the arms must follow `r = a * exp(b * theta)`.
- Palette: match the Claude stage — ink `#3D3929` marks, one terracotta `#D97757` accent, cream `#F2F0E9` or a dark field if the astronomy subject demands it; pick one and state the choice in `SOURCES.md`.
- Seed every random draw and record the seed in `SOURCES.md`; same seed must give the same render.
- Keep all content inside a 5% inset — `run.sh` Gate B (`manim_layout_audit.py`) fails the build otherwise.

- [ ] **Step 4: Write the paperwork set that Gate F requires**

`run.sh` refuses to render Manim unless all three exist:
- `FACTCHECK.md` — every on-screen claim in the June video with the report line that supports it.
- `SHOTLIST.md` — one row per beat: beat id, what fills it, who fills it (machine or human), status.
- `PROMPTS.md` — beat-prefixed generation prompts for the two Manim beats, matching the prompt shown in B04's composer verbatim.

- [ ] **Step 5: Validate the sheet mechanically**

Run the Task 5 Step 3 validator with the path changed to `2026-06-medhavy-june`, and these two June amendments: allow beats whose `shot.source == "manim"` to have no `remotion.pattern`, and expect 17 beats. Then:

```bash
cd /home/nayya/brutalist.art && python3 -c "
import re,pathlib
src = pathlib.Path('medhavy-opt/youtube/2026-06-medhavy-june/scenes.py').read_text()
found = re.findall(r'class ([A-Z][A-Za-z0-9]*_\w+)\(Scene\)', src)
assert found == ['B05_ObservableUniverse','B06_MilkyWay'], found
print('OK', found)
"
```
Expected: `OK ['B05_ObservableUniverse', 'B06_MilkyWay']`. If the regex finds nothing, `run.sh` will silently render zero scenes.

- [ ] **Step 6: Write PEDAGOGY.md with `VERDICT: PENDING`**

Same template as Task 5 Step 6, retitled for June, with the checks list extended by one line: `- [ ] The two Manim beats show the actual mathematics described in Week 6, not decorative space art`.

- [ ] **Step 7: Record, do not commit**

Append to `medhavy-opt/BUILD-LOG.md`. No `git commit`.

---

## Task 9: June — GATE P, audio, render, and QC

**Files:**
- Modify: `medhavy-opt/youtube/2026-06-medhavy-june/PEDAGOGY.md` (human writes PASS)
- Generated: `mp3/`, `manim/`, `media/`, `_qc/`, `2026-06-medhavy-june-slate.mp4`

**Interfaces:**
- Consumes: Task 8's outputs.
- Produces: a QC-clean June review cut.

- [ ] **Step 1: STOP for the human gate**

As Task 6 Step 1, for June. Verify:
```bash
cd /home/nayya/brutalist.art && grep -c "VERDICT: PASS" medhavy-opt/youtube/2026-06-medhavy-june/PEDAGOGY.md
```
Expected: `1`.

- [ ] **Step 2: Generate the narration**

Run:
```bash
cd /home/nayya/brutalist.art && python3 runtime/scripts/generate_audio_kokoro.py medhavy-opt/youtube/2026-06-medhavy-june
```
Expected: 17 mp3s.

- [ ] **Step 3: Check the measured runtime**

Run the Task 6 Step 3 script with the June path. Expected: every beat measured; total roughly 3–4.5 minutes.

- [ ] **Step 4: Run the full machine pass**

June has Manim, so use `run.sh` — it gates the Manim scenes (A, W, B), renders them, then calls `remotion_scenes.py` and compiles:

```bash
cd /home/nayya/brutalist.art && ./art run medhavy-opt/youtube/2026-06-medhavy-june --height 1080
```
Expected: both Manim scenes render and slot to `manim/B05.mp4` and `manim/B06.mp4`; the Remotion pass fills the rest; a slate cut and then a clean cut are compiled; Gate V runs.

If Gate A/W/B fails, the message names the scene and the defect — fix `scenes.py` and re-run. Do not set `ART_QC=0` or `ART_STRICT=0` to get past a gate; those exist for previz, and this is a deliverable.

- [ ] **Step 5: Visual QC — sample frames and LOOK at them**

As Task 6 Step 6, for June. Pay particular attention to the two Manim beats: confirm the star field is areally uniform rather than center-clustered, and that the spiral arms are logarithmic. If they are wrong, the video is claiming a skill it is not demonstrating — fix `scenes.py`.

Write `_qc/REPORT.md`; iterate until zero BLOCKER and zero MAJOR.

- [ ] **Step 6: Confirm no slates survived**

Run:
```bash
cd /home/nayya/brutalist.art && python3 runtime/scripts/todo.py medhavy-opt/youtube/2026-06-medhavy-june --open
```
Expected: no open beats.

- [ ] **Step 7: Record, do not commit**

Append to `medhavy-opt/BUILD-LOG.md`. No `git commit`.

---

## Task 10: June — final master

**Files:**
- Generated: `medhavy-opt/youtube/2026-06-medhavy-june/2026-06-medhavy-june.mp4`

**Interfaces:**
- Consumes: the QC-clean June review cut.
- Produces: the June master.

- [ ] **Step 1: Render the master**

Run:
```bash
cd /home/nayya/brutalist.art && ./art final medhavy-opt/youtube/2026-06-medhavy-june
```

- [ ] **Step 2: Verify the file, then verify the frames**

As Task 7 Step 2, with the June path. Additionally `Read` one frame from each Manim beat at 4K — Manim renders at `3840,2160` natively here, so a defect that was invisible at 1080 can surface.

- [ ] **Step 3: Record, do not commit**

Append to `medhavy-opt/BUILD-LOG.md`. No `git commit`.

---

## Task 11: July — scaffold, beat sheet, and PEDAGOGY

**Files:**
- Create: `medhavy-opt/youtube/2026-07-medhavy-july/beat_sheet.json`
- Create: `medhavy-opt/youtube/2026-07-medhavy-july/PEDAGOGY.md`
- Create: `medhavy-opt/youtube/2026-07-medhavy-july/SOURCES.md`
- Read: `hai_reports_weeks_1-12.md` lines 483–636 (Weeks 10–12 and the outstanding-items summary)

**Interfaces:**
- Consumes: the three Opt* Compositions and the May metadata block.
- Produces: a 12-beat sheet (B00–B11) containing no reference to Week 13.

- [ ] **Step 1: Read the source weeks in full**

`Read` `hai_reports_weeks_1-12.md` lines 483–636. Note that the closing summary discusses Week 13 — that section informs your understanding of the contract's state but **must not** produce any on-screen or spoken content.

- [ ] **Step 2: Author the beat sheet**

Same procedure as Task 5 Step 2, following the July spine table, with the July metadata row. July is Remotion-only — no `scenes.py`, no paperwork set, and it never calls `run.sh`.

B07's `OptBlockerCard` is the still-open case. Pass `closed: ""` and `days: 7` (Jul 23 → Jul 30) so the counter reads sensibly, with `court: "Prof. Sridhar"`.

- [ ] **Step 3: Validate the sheet mechanically, with the Week 13 check sharpened**

Run the Task 5 Step 3 validator with the July path and 12 beats, then this additional scan:

```bash
cd /home/nayya/brutalist.art && python3 - <<'PY'
import json, pathlib, re
blob = pathlib.Path("medhavy-opt/youtube/2026-07-medhavy-july/beat_sheet.json").read_text().lower()
bad = ["week 13", "week thirteen", "jul 24", "jul 25", "jul 26", "jul 27", "jul 28",
       "jul 29", "jul 30", "jul 31", "july 24", "july 31", "final week", "last week",
       "in progress", "still to come", "remains outstanding"]
hits = [b for b in bad if b in blob]
assert not hits, f"FORBIDDEN: {hits}"
print("OK — no Week 13 reference")
PY
```
Expected: `OK — no Week 13 reference`. Note `days: 7` in B07's props is a number, not a date string, so it does not trip this check.

- [ ] **Step 4: Write SOURCES.md and PEDAGOGY.md**

As Task 5 Steps 5–6, retitled for July, with the checks list extended by: `- [ ] Verified by search that no beat mentions Week 13, any date after Jul 23, or "in progress"`.

- [ ] **Step 5: Record, do not commit**

Append to `medhavy-opt/BUILD-LOG.md`. No `git commit`.

---

## Task 12: July — GATE P, audio, render, QC, and final master

**Files:**
- Modify: `medhavy-opt/youtube/2026-07-medhavy-july/PEDAGOGY.md` (human writes PASS)
- Generated: `mp3/`, `media/`, `_qc/`, `2026-07-medhavy-july-slate.mp4`, `2026-07-medhavy-july.mp4`

**Interfaces:**
- Consumes: Task 11's beat sheet.
- Produces: the July master — the third and last deliverable.

- [ ] **Step 1: STOP for the human gate**

As Task 6 Step 1, for July. Verify:
```bash
cd /home/nayya/brutalist.art && grep -c "VERDICT: PASS" medhavy-opt/youtube/2026-07-medhavy-july/PEDAGOGY.md
```
Expected: `1`.

- [ ] **Step 2: Generate the narration**

Run:
```bash
cd /home/nayya/brutalist.art && python3 runtime/scripts/generate_audio_kokoro.py medhavy-opt/youtube/2026-07-medhavy-july
```
Expected: 12 mp3s.

- [ ] **Step 3: Check the measured runtime**

Run the Task 6 Step 3 script with the July path. Expected: every beat measured; total roughly 2–3.5 minutes. July is the shortest month by documented volume and its video is allowed to be the shortest — do not pad it to match May.

- [ ] **Step 4: Render the Remotion beats and compile the review cut**

Run:
```bash
cd /home/nayya/brutalist.art && python3 runtime/scripts/remotion_scenes.py medhavy-opt/youtube/2026-07-medhavy-july && \
python3 runtime/scripts/compile.py medhavy-opt/youtube/2026-07-medhavy-july --review --height 1080
```

- [ ] **Step 5: Visual QC — sample frames and LOOK at them**

As Task 6 Step 6, for July. Additionally, while reading the frames, confirm with your own eyes that no frame carries a Week 13 reference — the mechanical check in Task 11 covers the beat sheet, but this covers what actually rendered.

Write `_qc/REPORT.md`; iterate until zero BLOCKER and zero MAJOR.

- [ ] **Step 6: Confirm no slates survived**

Run:
```bash
cd /home/nayya/brutalist.art && python3 runtime/scripts/todo.py medhavy-opt/youtube/2026-07-medhavy-july --open
```
Expected: no open beats.

- [ ] **Step 7: Render the master**

Run:
```bash
cd /home/nayya/brutalist.art && ./art final medhavy-opt/youtube/2026-07-medhavy-july
```

- [ ] **Step 8: Verify all three masters exist together**

Run:
```bash
cd /home/nayya/brutalist.art/medhavy-opt/youtube && for d in 2026-05-medhavy-may 2026-06-medhavy-june 2026-07-medhavy-july; do
  f="$d/$d.mp4"
  if [ -f "$f" ]; then
    printf '%s  ' "$f"
    ffprobe -v error -select_streams v:0 -show_entries stream=width,height \
      -show_entries format=duration -of csv=p=0 "$f" | tr '\n' ' '
    echo
  else
    echo "MISSING: $f"
  fi
done
```
Expected: three lines, each `3840,2160` with a duration. Any `MISSING` means that month is not done.

- [ ] **Step 9: Confirm the series reads as one set**

`Read` the outro frame and one week-marker frame from each of the three masters side by side. They must share type, palette, chip placement, and timeline treatment. If July drifted from May, fix the props — not the component — and re-render.

- [ ] **Step 10: Record, do not commit**

Append the final summary to `medhavy-opt/BUILD-LOG.md`: three masters, their paths, runtimes, and the GATE P signature dates. Then stop. Do not publish, do not upload, do not commit.

---

## Definition of Done

- Three masters at `medhavy-opt/youtube/<slug>/<slug>.mp4`, all 3840×2160.
- Each has a `PEDAGOGY.md` containing `VERDICT: PASS`, signed before its audio existed.
- Each has an `_qc/REPORT.md` with zero BLOCKER and zero MAJOR, produced by reading frames.
- Every factual claim traces to `hai_reports_weeks_1-12.md`.
- The July video contains no reference to Week 13.
- No slates remain in any final cut.
- Nothing was committed to git.
