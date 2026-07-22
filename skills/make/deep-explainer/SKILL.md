---
name: deep-explainer
description: >
  5–10 minute deep explainers on the ai-explainer chassis — Claude composer
  cold open, verdict recap, YOUR TURN handoff, title-restate outro — with a
  vox-style documentary BODY: roughly 20–25% of body beats are VOX beats
  animated from static stills waiting in pantry/ (greyscale/duotone cutout
  treatment, ease-out Ken Burns, spring pop-ins, film grain), and the rest are
  Manim fragments and Remotion patterns/illustrations chosen per beat.
  Frame-continuity chains ONLY within runs of consecutive vox beats (the
  vox-run handoff contract); hard cuts everywhere else. Two hard gates beyond
  the parents': the first compile is a full-length SLATE PREVIZ, and a
  tier-tagged, duration-locked SHOPPING LIST for pantry stills must exist
  before the review cut. Use when the user types `deep-explainer`,
  `deep explainer`, `deep reel`, or asks for a long / in-depth / documentary
  Claude-bookended explainer (5–10 min). Register: Teardown. Default channel
  claude-liam (Kokoro am_onyx, free). GATE P before any audio spend. Never
  publishes.
---

> **BRUTALIST (pared-down) EDITION.** This copy of the skill lives in the
> free-only `brutalist` toolkit. Kokoro is the ONLY TTS engine, with exactly
> two voices: **Onyx** (`am_onyx` — the nbb / Liam-in-for-Bear persona) and
> **Bella** (`af_bella` — the hai persona). The only channels are
> `claude-liam` (@NikBearBrown) and `claude-hai` (@HumanitariansAI); the only
> persona skills are `nbb` and `hai`. Any remaining reference in this file to
> ElevenLabs, Bear's voice clone, Suno, Higgsfield, the medhavy/musinique
> channels, or publishing machinery is inherited text from the full
> `brutalist-art` toolkit and does NOT apply here. GATE P remains in force as
> a QUALITY gate (narration review before audio), not a cost gate.

# deep-explainer — the long-form Claude-bookended documentary cut

A sibling of `ai-explainer` and `cli-explainer` on the same shared skeleton:
Claude bookends, different MIDDLE. Here the middle is a 5–10 minute
documentary-register vox body that leans on **human-supplied static stills in
`pantry/`** which the machine animates in the vox cutout grammar. Where
`ai-explainer` makes a tight reel, deep-explainer makes an episode.

## Lineage — what governs when

This skill EXTENDS `ai-explainer`, which extends `explainer`. Nothing below
repeals a parent law; this file only adds the genre's own contracts.

- **Bookends, brand, laws** → `../ai-explainer/SKILL.md` governs: COLD OPEN
  LAW (B00 is `ClaudeComposerAsk`, ask lands answered), ASK→RESULT LAW,
  ILLUSTRATE LAW, SHOW-DON'T-TELL LAW, SPARK-LINE LAW, REBUILD LAW,
  DOUBLE-CHECK LAW, FILL-THE-CANVAS, LOGO LAW, VISUAL QC LAW, HANDOFF LAW,
  OUTRO LAW, the channels table, IN-FOR-BEAR LAW, GATE P.
- **Closing block** → the `your-turn` skill's three-beat standard: VERDICT
  recap (`ClaudeVerdictArtifact`) → YOUR TURN prompt Liam reads in full
  (`ClaudeComposerAsk`, greeting `Your turn.`) → TITLE re-read
  (`ClaudeTitleOutro`).
- **How graphics are MADE** → `../explainer/` doctrine: MOTION.md,
  EQUATIONS.md (equation tangents), REMOTION.md, the two-axis shot system,
  the slot contract, the pantry law, the slate system, `manim/animated_graphics.py`.
- **Pacing** → `../duration-planner/` doctrine: duration is an OUTPUT.
  The 5–10 min band is the genre's natural landing zone for a multi-act
  concept, never a target to pad toward. If the arc lands at 4:40, ship 4:40.
- **This file** governs: the beat-mix quota, the vox-beat treatment on the
  Claude stage, the vox-run continuity contract, the shopping-list gate, and
  the deep act structure.

## When this skill (and when not)

Use deep-explainer when the concept is **multi-act** — several linked
mechanisms that each need their own instances and evidence (the source is a
long research doc, a chapter, a framework with 4+ parts). If the source is one
insight, it's an `ai-explainer`; if it's mostly math, it's a `math-explainer`;
if it's mostly a build, it's a `cli-explainer`.

## The spine (fixed)

```
B00 cold open (ClaudeComposerAsk, ask answered, Liam signs in)
  ACT I   … ACT N        the documentary body (this skill's subject)
VERDICT recap (ClaudeVerdictArtifact)
YOUR TURN (ClaudeComposerAsk, prompt read aloud + discussed)
TITLE re-read outro (ClaudeTitleOutro)
```

Acts are 4–8 beats each. Every act opens with a one-line segment card or a
spark-line beat naming the act (Title Case serif) — the viewer always knows
where they are in a 5–10 minute film.

## THE BEAT-MIX CONTRACT (the quota this genre exists for)

Count only **body beats** (bookends, ask micro-beats, and the closing block
are exempt). Target mix, linted at the plan gate:

| Lane | Share of body | What it is |
|---|---|---|
| **VOX** | **~20–25%** | A pantry still animated in the vox cutout grammar (below). `shot.type: STILL` or `COMPOSITE`, `shot.source: archive` or `ai`. |
| **MANIM** | ~25–40% | Fragments from `animated_graphics.py`: isotype grids, state cards, quote cards, equation tangents. `shot.source: own`. |
| **REMOTION** | ~30–45% | C2 rhetorical patterns, C3 concept illustrations, Onda `code-block` for anything code, segment cards. `shot.source: own`. |
| **CARD** | remainder | Act cards, kicker, sources card. |

Lint rules (checked when the plan is presented, reported as a histogram like
the parent's rhythm lint): vox share outside 15–30% is a WARN, outside 10–35%
is a FAIL; more than 2 consecutive beats of the same lane is a WARN (except
inside a vox run, where sameness is the point). The quota exists because the
genre's texture IS the mix — all-Remotion reads as a deck, all-vox reads as a
slideshow.

**Rhythm.** Denser than the parent explainer's ~28-word vox rhythm, lighter
than a lecture: ~7–14 s per beat, narration ~25–45 words. A 5–10 min episode
lands around 30–50 beats. The parent's 45–70-word budget applies only to the
exempt bookend beats (the ask, the verdict recap, the handoff
read-and-discuss). Estimate at ~2.9 words/second for planning; the measured
audio is the only clock that counts.

## VOX BEATS — pantry stills, machine-animated

A vox beat does not generate its own media. It **expects a static image** —
`pantry/[BID].png` → intake to `media/[BID].png` — and the compiler animates
it. That's the whole deal: the human supplies the plate, the machine supplies
the motion.

**Treatment — the vox laundering function on the CLAUDE stage.** This is a
FIDELITY brand (parent law), so vox beats do NOT import the newsprint ground.
The treatment is: desaturate ~80%, contrast ~1.15, seated on the Claude cream
stage (`#F2F0E9`), subtle film-grain overlay (screen/overlay blend, low
opacity), warm-ink vignette. Terracotta `#D97757` remains the ONE accent —
a hand-drawn ring, an underline, a highlight bar. One editor's-pen voice per
beat. Serif labels with hairline underlines, per the parent design tokens.
The result must still read as the Claude brand wearing a documentary texture,
not as a Vox clone dropped into a Claude reel.

**Motion menu per vox beat** (`shot.motion`):

- `kenburns` — the workhorse. Ease-out bias (`Easing.out(Easing.cubic)` —
  documentary, not bouncy). Set `shot.focus: [fx, fy]` toward the sentence's
  subject.
- `cutout` — the transparent-background subject rises/settles onto the stage
  with a spring (pop-in, damped); background layer holds or drifts. Requires
  a cut-out PNG (alpha) in the pantry; the shopping list says so.
- `parallax` — 2–3 layers (background plate, midground subject, foreground
  detail) drifting at different rates. Requires the layers as separate pantry
  files (`[BID]-bg.png`, `[BID]-mid.png`, `[BID]-fg.png`).
- `drawon` / `annotate` — the still holds; the terracotta ring/underline/X
  draws on, keyed to the spoken word.
- `hold` — legal for a portrait kicker; never twice in a row.

Reveals land ON the spoken word (parent MOTION.md doctrine; word clock from
the align step). Constant velocity for documentary moves; easing only for
elements that feel like UI.

**Provenance.** Parent rules bind unchanged: `archive` slots need the
`.source.txt` sidecar (URL, license, credit → auto-credits); generated media
of real people gets `source: ai` + the disclosure sidecar. Real people/events
→ real archives first.

## CONTINUITY — the vox-run contract (and its deliberate limit)

The documentary "one continuous shot" feel is scoped to **vox runs only**: a
run is 2–3 consecutive vox beats authored as one camera move. Everywhere else
— any boundary where the lane changes (vox→Manim, Remotion→vox, etc.) — is a
hard cut. Never attempt frame-continuity across the whole episode: chaining
40+ beats through prose prompts is exactly the fragility this rule exists to
kill.

Inside a run, continuity is a **serialized contract, not narrative trust**.
The run's beats share a `vox_run` id, and each beat but the last carries a
`handoff` block that the next beat's first frame MUST reproduce:

```jsonc
"shot": {
  "type": "STILL", "source": "archive", "motion": "kenburns",
  "vox_run": "R2",                    // same id across the run's beats
  "handoff": {                        // this beat's LAST frame, serialized
    "camera": { "x": 0.62, "y": 0.40, "scale": 1.8 },   // 0–1 frame coords
    "objects": [
      { "id": "portrait-hume", "x": 0.5, "y": 0.45, "scale": 1.0, "opacity": 1 }
    ]
  }
}
```

Rules: the run's beats render as ONE composition internally (one camera
spline, beat boundaries = narration boundaries), OR as separate clips whose
first/last frames are pinned to the handoff values — either implementation is
legal, but the handoff block is authored at plan time either way, so the
continuity survives any re-render. A run never crosses an act boundary. Max
run length 3 beats. Runs are where the pantry earns drama: zoom out from the
detail (beat 1) to reveal the whole plate (beat 2), pan to the consequence
(beat 3).

## THE TWO HARD GATES (beyond the parents')

### Gate D1 — the slate previz IS the first deliverable

The first compile is always a **full-length watchable previz**: every vox
beat renders as a slate (beat id + narration line + terracotta pipeline
pointer), Manim/Remotion beats render for real (they're free), audio is real
(post-GATE P). This is honest by design — at this genre's scale the pantry is
the bottleneck, and the previz is what the human reviews for pacing while
sourcing stills. Never present a previz as a finished cut.

### Gate D2 — the shopping list (duration-locked, tier-tagged)

`SHOPPING.md` is written **after audio lock** (never before — a card written
before the beat's real length is known can't state its duration requirement,
and conform is left stretching instead of trimming). One entry per missing
pantry asset. The review cut does not proceed while SHOPPING.md entries sit
unresolved without an explicit human "ship with slates" override.

Entry format and the three sourcing tiers: `reference/shopping-list.md`.
The short version:

- **Tier 1 — generic/illustrative** (no real referent): AI-generate or stock;
  no rights escalation.
- **Tier 2 — specific real object** (named building, document, artifact):
  prefer the real image; verify THE ITEM's stated rights, not the hosting
  institution's reputation; AI fallback is labeled.
- **Tier 3 — specific named real person**: archival photo first (the
  PHOTOGRAPH's rights govern — photographer's term, not the subject's);
  the rights check itself escalates to the human, every time.
- Motion assets state their minimum duration and ask for MORE than needed —
  conform trims (lossless) rather than stretches (lossy).

## Workflow (each gate is the human's)

1. **`plan`** — read the WHOLE source; act structure → beats (~20–35 words),
   lane per beat (the mix contract), vox runs + handoff blocks, `show` blocks
   (SHOW-DON'T-TELL binds at authoring time), viz data, equation tangents
   marked. Present the lane histogram + the act map. **GATE: approve.**
2. **`factcheck`** — parent explainer Gate F, sharpened for this genre:
   long sources are where fabricated-but-fluent claims hide. Verify every
   number and named claim against the source; strip what will date the
   episode (tool names, versions, "as of [month]"); anything the source
   itself flags as unverified either dies or is presented AS unverified.
   `FACTCHECK.md` in the reel folder. **GATE: claims hold.**
3. **GATE P** — narration reviewed on an animated slate. Then audio
   (Kokoro — Onyx or Bella; the only engine here).
4. **Audio lock** — measured mp3s become the clock; align writes the word
   clock.
5. **Gate D2** — write `SHOPPING.md` from the locked durations. Hand it over.
6. **Gate D1 previz** — `./art run [reel]`: full compile, slates in vox
   slots, Manim/Remotion rendered, `--review` burn-in. **GATE: watch it.**
7. **Pantry fill** — human drops stills into `pantry/`; the parent pantry
   law (`pantry` command word) intakes, treats, renames; set `shot.focus`;
   fill sidecars. Rerun — only changed slots recompile.
8. **Review cut → VISUAL QC LAW pass → `./art final`.** The closing block is
   the `your-turn` standard. `BUILD-PROMPT.md` ships in the folder (parent
   rule: a reel without its build prompt is unfinished).

## Output contract

```
[book]/youtube/[slug]/
  beat_sheet.json      the heart (schema: runtime/schema/beat_sheet.schema.json
                       + vox_run/handoff + the lane annotations above)
  BUILD-PROMPT.md      paste-ready end-to-end build prompt
  BUILD-LOG.md         decisions, MISSING: lines, gate signatures
  FACTCHECK.md         claim | verdict | source | fix
  SHOPPING.md          Gate D2 manifest (after audio lock)
  SOURCES.md           source doc(s), corrections, seeds, credits
  pantry/  media/  manim/  clips/  mp3/   (parent slot contract)
```

Slug convention: `[channel]-[concept]` (default `claude-liam-…`), built into
the OWNING BOOK's `youtube/` — never into the toolkit.

## Hard rules (the genre's own — parents' rules all still bind)

1. **The quota is real.** A "deep-explainer" with 5% vox beats is an
   ai-explainer that skipped its pantry; with 60% it's a slideshow. Fix the
   plan, not the label.
2. **No whole-film continuity.** The vox-run contract is the ONLY
   frame-continuity mechanism. A plan that chains runs across act boundaries
   or beyond 3 beats fails the plan gate.
3. **SHOPPING.md only after audio lock.** A shopping list with estimated
   durations is a defect, not a head start.
4. **Strip the datable.** This genre's episodes are long-lived; vendor tool
   lists, model names, and "as of" claims from sources are compressed to
   generic mechanisms or cut (DOUBLE-CHECK LAW, sharpened).
5. **Unverified-source caution.** When the source doc itself mixes verified
   and fabricated material (research-pass output often does), FACTCHECK.md
   must mark which claims were independently checked — inheriting the
   source's own confidence is the exact failure mode this genre's episodes
   tend to be ABOUT.
6. **Never publish.** Master stays in the reel folder; public is a human
   Studio flip.

## Reference files (this folder)

- `reference/vox-beats.md` — the cutout grammar in implementation terms:
  easing, springs, grain, screen-blend keying, layer compositing; what's
  verified vs. what to re-check.
- `reference/shopping-list.md` — the Gate D2 manifest format + tier law.
- `reference/continuity.md` — the vox-run handoff contract, worked example.
