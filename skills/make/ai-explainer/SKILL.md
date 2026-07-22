---
name: ai-explainer
description: >
  Full-fledged Brutalist explainer reels in the CLAUDE brand — the Claude
  desktop app's own look (cream #FAF9F5 page, warm ink #3D3929, terracotta
  #D97757 spark as the ONE accent, EB Garamond serif + UI sans). Default
  working channel is claude-liam (Liam in for Bear, Kokoro am_onyx "Onyx",
  free); the alternate voice is Kokoro af_bella "Bella" (the hai persona) —
  Kokoro is the only engine in this toolkit. Beat-sheet driven
  and phase-gated; visuals mix the
  Claude Remotion scenes, Onda code-block for code, Manim fragments for math
  beats, and human-added media via the per-beat slot convention. ILLUSTRATE
  LAW: middles are concept-illustrated — the Claude UI appears only where
  the UI is the subject. Use when the user types `claude-explainer`, `claude
  reel`, `claude style`, `claude cut`, or asks for a Claude-branded
  explainer or "Claude, oversimplified"-style walkthrough. A SKILL.md
  source (or `skill teardown`) arms the skill-teardown modifier: same
  bookends, body breaks the skill down and demos it live. Register:
  Teardown. GATE P before audio spend. Never publishes.

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

# ai-explainer — the Claude cut (formerly `claude-explainer`)

> Renamed from `claude-explainer` (reserved word in installable skill names;
> also the Phase 2 naming policy — vendor names never as identity). The old
> name still resolves via the `art` alias map and remains a trigger word.

## The shared skeleton (claude-explainer AND claude-cli are siblings)

Both skills produce the SAME Claude-branded bookends; only the MIDDLE differs.

1. **Beat 1 — the Claude terminal, `[Hello], [Name]`** (`ClaudeComposerAsk`:
   world-language hello + persona). Always beat 0.
2. **Middle — the ONLY part that differs:**
   - **claude-explainer** → a **vox-style explainer**: any media that fits the
     concept (archival, isotype, Manim, illustrations — and terminals/code where
     they earn the beat). The bookends frame it; the middle teaches.
   - **claude-cli** → the **build-with-Claude loop**, each step discussed: CLI
     prompt (Claude template) + *why this prompt* → show code + discuss → show
     output + discuss; at least one revision.
3. **Second-to-last — "Your Turn"**: the composer with a suggested prompt typed in
   for the viewer to explore (`greeting: "Your turn."`).
4. **Last — the channel brand card**: `@NikBearBrown` or `@HumanitariansAI`
   (title restate + channel handle).

**Scout → builder routing (the idea's SOURCE picks the skill):**
- `cli-ideas.md` (cli-scout) and `simulation-ideas.md` (sim-scout) cards → **claude-cli**
- video-idea cards (`vids/` scouts, `media-scout` video cards) → **claude-explainer**

Both are audio-first, phase-gated (GATE P before audio spend), fill-in-first, and
output `[slug].mp4` + `[slug]-slate.mp4`. See `docs/how-to-create-a-claude-explainer.md`.


## Lineage: an EXTENSION of `explainer`

claude-explainer is not a standalone pipeline — it extends
`skills/make/explainer` and inherits its whole chassis: the Manim doctrine
(`MOTION.md`, `EQUATIONS.md`), the Remotion scene rules (`REMOTION.md`), the
previz slate system, and the shared runtime belt (`runtime/scripts/*`). What
this skill adds is the Claude skin, the register, and the laws below. When in
doubt about how to MAKE a graphic, the parent explainer doctrine governs; when
in doubt about how it LOOKS or how the reel is framed, this skill governs.


Brutalist explainer reels wearing the Claude desktop app's skin. Same machinery
as every other brand (shared `beat_sheet.json` schema, audio-first, phase-gated,
conform-to-audio), different clothes: the app's cream page, its serif, its
terracotta spark — and the composer window as the recurring visual anchor.

**This is a FIDELITY brand.** The palette replicates the real product. Do not
retint it, theme it, or "improve" it — the moment it stops looking like the
actual Claude app it loses its reason to exist. Brand law: `CLAUDE-BRAND.md`.

## Trigger

```
claude-explainer [input]
```

`[input]` is a reel folder, a lecture folder, a book (batch), or a concept to
build fresh. Also triggers on `claude reel`, `claude style`, `claude cut`.

## Brand facts (the five decisions, pre-made)

| Slot | Value |
|---|---|
| Palette | `claude` — tokens in `runtime/remotion/src/tokens/claude.ts` (CLAUDE + CLAUDE_FONT). Shared by ALL channels — the look never changes per channel. |
| Accent law | Terracotta `#D97757` is the ONE accent: the spark, the send button, a summoned `/skill` token, one focal moment per beat. Everything else warm ink on cream. |
| Type | Serif for greetings + segment titles (`Tiempos → EB Garamond` — Tiempos is proprietary, so **EB Garamond is the effective default**; it's bundled in `runtime/fonts`). UI sans for chrome; mono for terminal/output lines only. Segment titles are **Title Case** (`Photoelectric Effect`) — never all caps, never sentence case. |
| Voice | Per channel — see the channels table. Working default: `claude-liam` (Kokoro `am_onyx` "Onyx", free). The other house voice is Kokoro `af_bella` "Bella" (the hai persona). Kokoro is the only engine. |
| Register | Per channel — default Teardown (Feynman × MKBHD). |

## Channels

One look, many voices. The Claude skin is shared; the channel sets voice,
register, greeting persona, and the footer folder chip:

| Brand key | Persona | Folder chip | Voice | Register |
|---|---|---|---|---|
| `claude-liam` **(working default)** | Liam (in for Bear) | `@NikBearBrown` | kokoro `am_onyx` ("Onyx") | Teardown |
| `claude-hai` | HAI | `@HumanitariansAI` | kokoro `af_bella` ("Bella") | Pragmatist |

Two channels, two voices, both free — that is the whole roster in this
toolkit. Scaffold: `python3 runtime/scripts/brand_variant.py [input] claude-liam`
(or `nbb` / `hai` for the persona cuts).
When authoring the beat sheet, set the scene's `greeting` persona and
`folderLabel` from this table.

**Audiences (bake into every episode — who the narration is FOR):**

- `claude-liam` — practitioners and makers following the channel's
  Claude workflows.
- `claude-hai` — **STUDENTS**: smart people open to learning AI who need some
  help getting started — some in schools that banned AI, some mid-career and
  needing to get proficient. The channel's spine question is **when to use AI
  and when NOT to** (crutch vs scaffold; fluency isn't mastery). HAI episodes
  never teach evading a ban or an integrity policy — they teach the ethical
  path and name the line plainly.

**Liam — the substitute narrator (IN-FOR-BEAR LAW).** `claude-liam` is not a
new channel: Liam is the nbb persona's stand-in voice on the SAME
@NikBearBrown channel — same Teardown register, same laws, same footer chip —
for every reel in this free-only toolkit (batch runs, high-volume
series, previz-grade uploads alike). Two rules whenever Liam narrates:

1. **Say it out loud.** B00's narration introduces the voice in its first
   breath — pattern: "… this is Liam, in for Bear." — and the outro signs
   off the same way ("Liam, in for Bear."). The greeting slot reads
   `[hello], Liam` (Bear's two-word cue budget; **Wagwan stays Bear's —
   Liam never takes it**). The viewer is never left guessing whose voice
   this is.
2. **A named voice, never a clone.** Liam does not imitate Bear's delivery
   or claim to be him. In this toolkit Liam IS the @NikBearBrown voice —
   Kokoro `am_onyx`, always.

## The greeting (the hello slot)

`ClaudeComposerAsk` renders the app-style serif greeting — spark + salutation —
above the composer: `[cue], [persona]`. All greeting choices are made at
**beat-sheet authoring time** — renders stay deterministic.

**Default: a world-language hello.** The cue slot defaults to "hello" in a
rotating world language, so the channel passively teaches viewers to greet in
languages from everywhere. Rotate by reel (don't repeat a language within a
batch); pick from the lexicon:

- **One word** (fits every persona): Hola (Spanish) · Olá (Portuguese) ·
  Bonjour (French) · Ciao (Italian) · Hallo (German) · Hej (Swedish) ·
  Hei (Norwegian) · Ahoj (Czech) · Cześć (Polish) · Privet (Russian) ·
  Yassou (Greek) · Merhaba (Turkish) · Shalom (Hebrew) · Salaam (Arabic/Farsi) ·
  Jambo (Swahili) · Habari (Swahili) · Sawubona (Zulu) · Selam (Amharic) ·
  Namaste (Hindi) · Vanakkam (Tamil) · Annyeong (Korean) · Sawadee (Thai) ·
  Halo (Indonesian) · Kumusta (Filipino) · Aloha (Hawaiian) · Talofa (Samoan) ·
  Bula (Fijian) · Konnichiwa (Japanese)
- **Two words** (Bear only — see word budget): Nǐ hǎo (Mandarin) ·
  Xin chào (Vietnamese) · Kia ora (Māori) · Dia dhuit (Irish)

**Word budget by persona.** The line must stay one comfortable serif line:
`Bear` is short, so the cue gets up to two words; `HAI` takes only the
shortest forms (Hi · Ola · Hej · Ciao).
Never spell out `HumanitariansAI` in the greeting — that's what the footer
chip (`@HumanitariansAI`) is for.

**Bear's Wagwan.** Roughly 1 reel in 10, Bear's hello is `Wagwan, Bear`
(Jamaican Patois). Authoring rule: if the reel slug's character-sum mod 10
is 0, use Wagwan — deterministic, no dice at render.

**Arc cues are the exception, not the default.** `The ask,` / `Watch this,` /
`The verdict,` (two words → Bear only) may replace the hello when the beat
genuinely earns it. If nothing earns it, hello. Day-greetings
(`Happy Tuesday, Bear`) stay reserved for channel-update reels. Empty
`greeting` shows the spark alone.

## The `profile` modifier (opt-in — NOT the default)

`profile` is an explicit MODIFIER on a claude-explainer, not a channel and not
the default behaviour. Invoke it only when the human asks for a profile (a
claude-explainer of a feature article ABOUT a person — a NortheasternISE
Substack piece, a Humanitarians AI Fellow profile, any "here's an engineer and
what they build" essay). A normal claude-explainer is unchanged; the modifier
only applies when explicitly requested. Trigger phrasing: "profile mode",
"claude-explainer profile", "profile of [name]", or pasting a profile article
and asking for a reel of it.

What the modifier changes (everything else — cold open → body → verdict →
handoff → title outro, ASK→RESULT, REBUILD LAW, ILLUSTRATE LAW — stays the
same):

1. **The greeting becomes the subject, not the persona.** Where a normal reel's
   `ClaudeComposerAsk` greeting reads `Hello, Liam` (`[cue], [persona]`), a
   profile reel reads **`Profile, [Subject Name]`** — the cue is the literal
   word "Profile" and the name takes the persona slot (e.g. `Profile, Aditi
   Deodhar`). This overrides the world-language hello lexicon and the Wagwan
   mod-10 rule for B00. The narrator is still Liam and still signs
   "Liam, in for Bear" out loud in B00 and the outro (IN-FOR-BEAR LAW is
   untouched) — the greeting names WHO the video is about, the sign-off names
   WHO is narrating.
2. **The name recurs throughout.** The subject's name appears on segment cards
   and spark lines across the body (not just the greeting) — the reel is about
   a person, so the person is named on screen repeatedly, and the outro title
   card carries the name too.
3. **Register: Teardown-warm, celebratory-but-honest.** The profile genre makes
   invisible work visible. Narrate the person's thesis and judge it the
   Teardown way, but the verdict lands ON THEIR SIDE — the skepticism points at
   the industry blind spot the article names, never at the subject.
4. **Find the ONE idea.** Every profile has a thesis sentence — extract it and
   build the whole reel to land it (Kaustubha Eluri: "trustworthiness is a
   system property, not a model property"; Aditi Deodhar: "the willingness to
   stop and discard working code is a learned discipline").
5. **Evidence beats are the person's PROJECTS as concept illustrations (C3)** —
   never headshots or lifted article images. REBUILD LAW governs.
6. **A PERSON CREDIT card is required, near the outro** — the subject's name,
   program/role, and their public links VERBATIM (LinkedIn `linkedin.com/in/…`,
   GitHub `github.com/…`) plus the article's own call-to-action; author of the
   article credited on the SOURCES card.
7. **HONESTY (DOUBLE-CHECK LAW, sharpened for people):** only claims the article
   makes — never invent an accomplishment, metric, quote, credential, or link.
   Keep soft attributions soft. Log the article URL + author + date in
   SOURCES.md.

**Channel / branding / publish.** Default voice claude-liam; NortheasternISE
and Humanitarians AI Fellow profiles carry the **@HumanitariansAI** folder chip
and HAI logo bug (a Bear-channel profile would carry @NikBearBrown). Build into
the owning series' `youtube/[slug]/` (e.g.
`humanitarians_html/youtube/claude-liam-profile-[name]/`). **Profiles publish to
the @humanitariansai YouTube "Profiles" playlist** (not Fellows Research —
that's the how-to series).

## The `skill-teardown` modifier (auto-armed when the source is a SKILL.md)

`skill-teardown` is the second explicit MODIFIER on a claude-explainer
(sibling of `profile`). Unlike `profile` it arms AUTOMATICALLY whenever the
reel's source is a skill: a SKILL.md file or a skill folder — an Anthropic
shipped skill under `../anthropics/**`, a house skill, a plugin skill.
Explicit triggers: "skill teardown", "skill explainer",
`claude-explainer [path-to-SKILL.md]`, or a scout card whose source field
points at a SKILL.md.

**Exemplar: `youtube/claude-liam-algorithmic-art/` — "Claude, Seeded —
Inside Anthropic's Algorithmic-Art Skill"** (build prompt:
`CLAUDE-CODE-ALGORITHMIC-ART-EXPLAINER.md` at the repo root). Copy its
moves, not just its shape: every major visual in that reel was generated by
FOLLOWING the skill it explains — seeded flow fields, the 3×3 seed grid,
the rebuilt viewer chrome. That is the standard this modifier enforces.

**The bookends do not change.** Cold open on `ClaudeComposerAsk`, verdict
artifact page, HANDOFF, title-restate outro, and every house and frame law
bind exactly as on any other claude-explainer. The modifier governs the
MIDDLE:

1. **Read the WHOLE skill first.** The SKILL.md plus everything it
   references — templates, reference files, scripts, licenses. The teardown
   explains the skill's actual mechanism, not its README summary.
2. **The body BREAKS THE SKILL DOWN.** Default act spine (adapt to the
   skill, never pad to it):
   - *what a skill is* — one beat for newcomers: a folder of instructions
     Claude reads before working (SKILL.md + assets). Skip or compress in a
     batch where the audience just heard it.
   - *the pipeline* — the skill's phases and contracts as a diagram beat
     (C3 / SourceFlow-style: what goes in, what each phase produces, what
     comes out).
   - *the mechanism acts* — the 2–4 design decisions that make this skill
     THIS skill (a two-phase order, a reproducibility contract, a fixed
     chrome vs. free interior, a hard ban), each carried by its own
     illustrated beat per ILLUSTRATE LAW — C2 pattern, C3 illustration,
     Manim fragment, Onda code-block for anything the skill renders as code.
   - *the design tell* — the Teardown moment: why the file is WRITTEN the
     way it is (a phrase repeated to steer the model's register, a
     constraint that encodes a lesson learned), judged honestly — what the
     design gets right, where it bites.
3. **SELF-DEMO LAW (mandatory when feasible).** The reel USES the skill to
   demo the skill: the build EXECUTES the skill's own instructions and
   shows the real output as native beats. Requirements:
   - Demo outputs render as native deterministic scenes (Remotion/Manim
     ports of what the skill produced) — seeded wherever the skill's medium
     allows, every seed logged in SOURCES.md; same seed → identical output
     every render.
   - Every demo lands as an ASK→RESULT pair: the composer micro-beat shows
     the ACTUAL invocation of the skill, the next beat shows what it made.
   - Never screen recordings, never screenshots, and never fabricated
     output passed off as generated — a faked demo is a DOUBLE-CHECK LAW
     violation, not a shortcut.
   - **Feasibility fallback:** if the skill cannot run inside the free
     pipeline (paid APIs, external services, credentials, human-in-the-loop
     steps), that demo beat renders as a PIPELINE slate naming exactly what
     is needed, the surrounding body falls back to REBUILD-LAW
     illustrations of the skill's *documented* outputs, and the fallback is
     logged in BUILD-LOG.md. Never silently skipped, never faked.
4. **VERBATIM QUOTE LAW.** The skill's own language is the evidence. Quotes
   shown on screen match the SKILL.md exactly, cited once per figure,
   small: "Source: Anthropic, [skill-name] SKILL.md" (or the actual
   publisher). DOUBLE-CHECK LAW still governs the narration — the script
   judges the skill in the episode's register; if it could have been read
   off the SKILL.md, the law was skipped.
5. **The Your Turn prompt INVOKES the skill.** The handoff prompt runs the
   skill on the viewer's own material (pattern: the exemplar's "Create
   algorithmic art about something I love. First write me the manifesto…").
   HANDOFF LAW's read-and-discuss requirement applies unchanged.
6. **Naming.** Series-style title when it fits — "Claude, [participle]"
   (Claude, Seeded · Claude, Scripted) — with the skill's name restated in
   the description. Slug: `claude-liam-[skill-name]` on the default
   channel. SOURCES.md records the skill's repo path and, for shipped
   skills, the upstream URL.

Channel, voice, and spend rules are unchanged: default `claude-liam`
(Kokoro, free), GATE P before audio, never publishes.

## Flow

### Step 1 — Scaffold (deterministic, no spend)

```bash
python3 runtime/scripts/brand_variant.py [INPUT_PATH] claude
```

Directory-isolated like nbb: writes `claude-[slug]/beat_sheet.claude.json`;
the canonical source is never modified. Metadata lands as:

```json
{
  "audience": "Claude",
  "engine": "kokoro",
  "voice_kokoro": "am_onyx",
  "palette": "claude",
  "typography": { "serif": "Tiempos/EB Garamond", "ui": "system sans", "mono": "SF Mono" },
  "register": "Teardown",
  "derived_from": "beat_sheet.json"
}
```

For a fresh build (no source reel), author `beat_sheet.json` directly in a new
kebab-case folder with the same metadata block.

### Step 2 — Narration (Teardown register) — SHOW first, words second

Before writing a single line of narration, sketch each beat's `show` block
(SHOW-DON'T-TELL LAW): what the viewer WATCHES, event by event. THEN write
the narration as the voice REACTING to what's on screen — pointing at it,
judging it — never as a self-sufficient essay read over wallpaper. Body
beats: ~45–70 words; the evidence (quotes, numbers, source lines) goes on
screen as cards/counters/sorts, not into the voice.

Rewrite/write every beat's narration in the Teardown register. The subject
matter for this brand is usually *workflows* — what to type, what Claude does,
where the output lands — so narrate the mechanism, then judge it: what this
design gets right, where it bites.

**GATE P — human signs off on the narration before any audio spend — reviewed
on an ANIMATED slate that plays the `show` events, never a page of text.**

### Step 3 — Audio (the master clock)

```bash
python3 runtime/scripts/generate_audio_kokoro.py [REEL_DIR]   # Kokoro — Onyx/Bella, free
```

Audio-first: per-beat MP3 durations become the clock everything conforms to.
Captions via the faster-whisper pipeline as usual.

### Step 4 — Visuals (the two-source mix)

One beat = one visual slot. Fill each slot from whichever source teaches best:

**A. Claude Remotion scenes** (`runtime/remotion`):
- `ClaudeComposerAsk` / `ClaudeComposerAsk916` — **the REQUIRED ask/intro
  beat.** The composer types the ask, send button arms, running indicator +
  output lines follow. Same prop contract as the legacy TerminalAsk (command /
  topic / segment / runningText / output) so old beat sheets convert by
  renaming the scene. This rule also applies to the nbb brand — the dark
  `NikBearBrownTerminalAsk` is legacy, kept only so historical reels re-render.
- `NikBearBrownOpen` / `NikBearBrownOutro` — brand open/outro stay as-is
  (channel identity beats; palette teardown is correct there).

**B. Bench components** (`runtime/remotion/src/scenes`, via the riff harness):
- `claude-composer` — the "Happy Tuesday" home screen; prompt types itself.
- `claude-window` — app frame; `composer` / `artifact` / `blank` views. Use
  `blank` as the stage when layering other media "inside the app."
- `claude-callout` — "oversimplified"-style annotation boxes + draw-on arrows;
  one callout per narration beat. This is the signature move of the brand:
  freeze the UI, annotate it while the voice explains.
- `code-block` (Onda) — code stays Onda's code-block; do not re-skin it.

**C. Manim fragments** — math/simulation beats render as Manim mp4s (white
canvas, ink strokes, terracotta accent to match) and drop into their slots.

**C2. Rhetorical patterns (animated-deck).** When a beat's narration argues
something that MOVES — a funnel, magnitudes on one axis, two readings
resolved, identical things splitting, a state change at a cutoff — render it
with the five-pattern library (`skills/animated-deck/assets/remotion/patterns.tsx`,
Remotion components, pure functions of progress; retint constants to the
claude stage: cream `#F2F0E9`, ink `#3D3929`, accent `#D97757`, warn
`#A44A32` — log the retint as a decision). Classification follows the
animated-deck gate: author `anim.json` per reel (beat → pattern → data drawn
from the narration's own numbers, nothing invented), present the pattern
table, human signs before build. Motion must earn its place — the no-fit
case gets a custom illustration or stays still.

**C3. Concept illustrations (Remotion).** Custom scenes on the cream stage
(`#F2F0E9`) in the fidelity palette — one terracotta accent, spark line
overlaid (top by default; bottom when the illustration owns the top). House
examples: books-from-the-server-to-Cowork, the commodity grid of drafting
windows, the predict card. These are pure functions of the beat's audio
clock, like everything else. **Start from the library:** `runtime/remotion/src/illustrations/` (see `ILLUSTRATIONS.md`) ships parameterized, annotated starter templates for the STRUCTURAL sub-family — `LayerStack` (N layers), `SourceFlow` (source→app; the merge of the teachers Standards→Cowork and medhavy Server→Cowork scenes), `ChipGrid` (a set of peer tools), and `PredictCard`. Adapt by changing props, not motion math; a genuinely new shape becomes a new component there. The five RHETORICAL patterns (attrition / divergence / scale / branch / threshold) stay in `deckPatterns.tsx` / `deck_anim.js` — a different family, chosen by the ILLUSTRATIONS.md decision tree.

**ASK → RESULT LAW (the signature of this brand).** Whenever the reel is
about to show a GENERATED visual — a Manim scene, a Remotion graphic, a D3
chart — it first shows the Claude prompt that makes it: a short composer
micro-beat (`ClaudeComposerAsk`, spark line allowed, runningText matching the
action — `rendering Manim…`, `building the chart…`) with the ACTUAL generation
prompt typed in. The NEXT beat is the result. The Claude interface is never
shown alone as decoration — it is always followed by what it produced. Ask
beats stay in the fixed Claude skin; RESULT graphics render in the episode's
CHANNEL palette (claude: ink + one terracotta on cream; nbb: teardown
white/ink/red; hai: the humanitarians token set). One reel may
contain several ask→result pairs; each pair reads as a receipt.

**PLACEHOLDER SLATES (inherited from explainer / the vox slot contract).**
A beat whose media is not yet made renders as a slate: beat id, the narration
line, and a terracotta pipeline pointer (`PIPELINE → fill media/B03.mp4`).
The first pass is always a watchable previz with slates standing in; any
slot's media swaps by filename and the reel rebuilds without touching the
edit. A slate is a request for media — from the pipeline or from the human.

**D. Human-added media** — screen recordings, product screenshots, B-roll.
The slot contract (vox-explainer doctrine) applies: every beat compiles to a
conformed per-beat mp4 named by beat id; swap any slot's media by filename
(png or mp4) and rebuild without touching the edit. First pass is always a
watchable previz with the Remotion scenes; upgrading slots to real
recordings is the human's call, beat by beat.

### Step 5 — Assemble

```bash
python3 runtime/scripts/compile.py [REEL_DIR]   # conform to audio, mux, captions
```

`greybox` previz is allowed at any point before the render for pacing review.

### Step 6 — The build prompt (always)

Every reel ships with `BUILD-PROMPT.md` in its folder: the single paste-ready
Claude Code prompt that builds the final cut end to end (gate check → audio →
conform → render → visual QC → report, never publish). QC here means the
frame-level VISUAL QC LAW pass (see Hard rules), not just the mp4 probe. Run from `books/` — typically
under `claude --dangerously-skip-permissions`, appropriate here BECAUSE the
pipeline meets the seatbelt rules (git-tracked, regenerable outputs, GATE P
still requires a human signature before spend). A reel without its build
prompt is unfinished.

## Hard rules

### House laws — standing for ALL claude explainers (every channel)

- **DEFAULT CHANNEL: claude-liam.** Unless the human names a channel or
  explicitly asks for Bear's own voice, build on `claude-liam` (Kokoro
  `am_onyx` "Onyx", free pipeline — IN-FOR-BEAR LAW applies). The hai channel
  uses Kokoro `af_bella` "Bella". GATE P (narration review) still binds.
- **LOGO LAW.** Every beat carries the channel's brand mark as a small,
  low-opacity corner bug (lower-right), inside the title-safe area, never
  covering content — the NBB logo for the `@NikBearBrown` channels
  (`claude`, `claude-liam`; source the mark from the nbb skill / runtime
  assets, e.g. the NikBearBrownOpen/Outro scene assets), the channel's own
  mark otherwise (e.g. the HAI logo for `@HumanitariansAI`). The outro brand
  card shows the mark FULL-SIZE. If no logo file exists, render the channel
  handle as a clean wordmark in the Claude serif — never skip the bug.
- **REBUILD LAW (animated graphics, never screenshots).** Every figure,
  chart, diagram, or infographic from a source is REBUILT as a native
  animated Remotion graphic in the fidelity palette — screenshots and lifted
  images are not visuals, they're placeholders. Honesty governs the rebuild:
  only numbers verifiable in the source may appear on screen (exact data when
  published; orderings/anchors only when not; never an invented figure), and
  a simplified rebuild is captioned "Redrawn (simplified) from …" once, small.
- **FILL-THE-CANVAS / TYPESIZE LAW.** The frame is 1920×1080 — use it. A
  graphic that occupies the top third and leaves the rest of the safe area
  empty is a defect, and so is timid type. Size content to FILL the safe
  area: scale the composition AND its type up until it comfortably occupies
  the vertical and horizontal span of `SAFE`, distributing elements down the
  abundant axis instead of clustering them at the top. Interrogate every font
  size — the legibility floor (~24px effective) is a FLOOR, not a target; a
  full-screen figure with several rows of data should read from across a
  room: headline type large, labels generous, numbers bold. The test: if you
  could shrink the whole graphic to half size and it would still fit with
  room to spare, it was built too small — scale it up. Two guards against
  overshoot: nothing crosses the `SAFE` inset (VISUAL QC LAW still binds —
  fill toward the edges, never past them), and one-idea-per-beat still holds
  (fill by making the ONE idea bigger and better-spaced, never by cramming a
  second idea in to use the room). Deliberate negative space for emphasis is
  legal as a design choice; accidental dead space under undersized content is
  the defect this law kills.
- **SHOW-DON'T-TELL LAW — the FIRST authoring question, not a render-time
  check.** This law binds at BEAT-SHEET TIME: author the SHOW first, the
  narration second. Every beat is a SHOT with stage directions, and the
  beat sheet records them — each body beat's `shot` carries a `show` block:
  an ordered list of visual events (`{"at": [fraction-or-phrase], "event":
  "[what appears/moves]"}`) naming exactly what the viewer WATCHES as each
  phrase lands. A beat authored without a `show` block is a script, not a
  beat.

  What showing means in practice:
  - **Evidence lives ON SCREEN, not in the voice.** Verbatim quotes land as
    comment/artifact cards the viewer READS while the voice reacts to them;
    numbers land as counters/bars that move to their value on the spoken
    figure; a source's own words appear as the source's own card. If the
    voice is reciting a list the viewer cannot see, the beat is a podcast.
  - **Motion enacts the sentence.** A number that grows → the bar grows AS
    the words land. A sequence → stages light in narration order. A
    comparison → the two sides visibly SORT/diverge at the spoken contrast.
    A reframe → the old words are struck through and the new words type in,
    on the spoken word. A mechanism → it performs itself while explained.
  - **THE PPT TEST (hard fail).** If a beat could be exported as a static
    slide — a headline plus a paragraph while the voice talks — it is not
    done. A spark line floating over narration is a slide. Two consecutive
    slide-beats is a slideshow, and a slideshow is a build failure, not a
    style choice.
  - **NARRATION BUDGET.** Body beats run ~45–70 words. The screen carries
    the evidence; the voice carries the judgment. If a body beat's narration
    is pushing 100+ words, the words are doing work the visuals should be
    doing — move the evidence on screen and cut the words. (Bookends are
    exempt: the ask, the handoff's read-and-discuss, the verdict's spoken
    artifact lines.)

  Reveals land ON the spoken word (signaling principle — parent doctrine in
  `skills/make/explainer/MOTION.md`); use the beat's `sub_beats` word-level
  timing when motion must hit mid-sentence. Telling-only beats are legal
  ONLY when nothing in the line can move — a pure judgment line or a
  breathing beat — and then SPARK-LINE LAW governs. Motion still must EARN
  its place: animation that enacts the narration is the point; animation
  that merely decorates it stays banned. The previz/slate is bound too: a
  slate that presents beats as static text pages misrepresents the reel —
  slates animate their `show` events at estimated timing so GATE P reviews
  the SHOW, not a deck of paragraphs.
- **DOUBLE-CHECK LAW.** The source is fact-checked and REWRITTEN in the
  episode's register (Teardown by default) — never parroted. Before
  scripting: verify the source's claims, strip anything that will date the
  video (model version numbers, counts that drift), separate the author's
  conventions from facts, and de-sensationalize rates and results to what the
  source actually supports. Corrections applied are logged in the reel's
  SOURCES.md. The register's value IS the rewrite — if the script could have
  been read off the source, the law was skipped.
- **VISUAL QC LAW.** Every build ends with a frame-level visual QC pass —
  after every `compile.py` render, and the mp4 probe (duration + frame
  count) is a FILE check that never counts as QC. Procedure (full spec:
  `CLAUDE-CODE-VISUAL-QC-CHECK.md` at repo root): sample frames with ffmpeg
  (≥2 fps — `ffmpeg -i [mp4] -vf fps=2 _qc/frames/%05d.png` — plus each
  beat at ~15/50/85% of its span from the beat sheet), actually **Read the
  PNGs**, and audit the 9-point rubric — edge bleed/clipping, title-safe
  margins, container overflow, collision, offscreen anchors, legibility,
  brand bug placement, aspect, and CANVAS FILL (content and type sized to
  occupy the safe area — undersized type or large dead space under a
  top-clustered graphic is a defect, per FILL-THE-CANVAS LAW). Log defects
  and fixes in `_qc/REPORT.md`.
  Fix root causes in scene source and re-render until zero BLOCKER and zero
  MAJOR defects remain — a build that was never visually inspected is not
  done. Standing layout rules that prevent the defects: all essential text,
  logos, and chips sit inside the 5% title-safe inset — the shared `SAFE`
  constant in `runtime/remotion/src/tokens/layout.ts` (`CANVAS`, `SAFE`,
  `safeX`/`safeY`/`safeCenterX` helpers; 16:9: x 96–1824, y 54–1026) —
  positioned from `SAFE`, never nudged by pixels; every text element that
  can hold variable-length copy gets `maxWidth` + wrap or auto-fit, never a
  bare fixed width; boxes size to content or clip by intent, never by
  accident.

### Frame laws

- **COLD OPEN LAW.** B00 opens directly on the Claude UI — `ClaudeComposerAsk`
  is always the first beat. Never a brand open card, never a channel ident
  before the UI appears. B00's composer always shows its RESULT output lines —
  the ask lands answered; ASK→RESULT begins at the cold open.
- **ILLUSTRATE LAW (the anti-wallpaper rule).** The UI earns its beats. The
  Claude interface appears ONLY where the interface is the subject: the cold
  open, the ask micro-beats of ask→result pairs, the verdict artifact page,
  the handoff, and the outro. Every OTHER inner beat ILLUSTRATES its concept —
  a rhetorical pattern (C2), a concept illustration (C3), a Manim fragment,
  an Onda code-block for anything code (real file contents, never prose
  restyled as code). The window-plus-callout move stays legal only when the
  UI itself is the thing being annotated ("Claude, oversimplified" on an
  actual interface). Two consecutive beats sharing the same visual scheme is
  the smell; seven videos of composer wallpaper is the failure this law exists
  to prevent.
- **SPARK-LINE LAW.** Inner beats never show a lonely asterisk. Wherever the
  spark appears mid-reel (the window's composer view, a breathing beat), it
  carries ONE short serif line summarizing the beat — the narration's key line,
  compressed (≤4 words: "The code exists." · "Librarian, not scanner."). B00's
  spark line is the hello greeting; typing belongs to B00 and the handoff beat only — inner beats
  show the command already typed. On illustration beats (ILLUSTRATE LAW) the
  spark + line overlays the stage: top by default, bottom when the
  illustration owns the top of the frame.
- **HANDOFF LAW.** The second-to-last beat of every reel is the Claude
  interface with a SUGGESTED PROMPT typed into the composer — directly relevant
  to the episode, ready for the viewer to paste into Claude to learn more or
  apply the lesson to their own work. Pattern: `ClaudeComposerAsk` with
  greeting fixed to `Your turn.` (viewer-addressed — the one greeting that
  drops the persona), runningText `paste this into Claude…`, command = the
  suggested prompt. This amends the typing rule: typing appears in EXACTLY two
  beats — the cold open and the handoff. The spine is therefore always:
  cold open → body → verdict page → HANDOFF → title-restate outro.
  **The prompt is READ and DISCUSSED, never just typed.** Two requirements,
  both mandatory: (1) the prompt must be an INTERESTING prompt — one that
  extends the episode's idea into the viewer's own work, not a bland
  "learn more about X"; (2) the narration reads the prompt ALOUD verbatim
  and then spends a line or two discussing it — what it does, why it's worth
  running, what the viewer should look for in Claude's answer — before
  inviting the pause ("take this prompt, run it on your own …"). A handoff
  where the prompt only appears on screen is a defect.
- **OUTRO LAW.** The outro RESTATES THE EPISODE TITLE, poster-style serif with
  the terracotta period, handle beneath (`ClaudeTitleOutro` pattern:
  title · handle · subline). Never a generic brand outro.

- **Never publish.** Output stays in the reel folder for human review.
- **GATE P** — narration reviewed on an animated slate before audio is generated.
- The intro/ask beat is `ClaudeComposerAsk` — no dark terminals in this brand.
- One terracotta moment per beat. If two things are orange, neither is the point.
- The footer chip reads `@NikBearBrown` unless the beat sheet overrides it.
