# CLAUDE.md — brutalist/

The pared-down, free-only video toolkit. **Start with `HOW-TO.md`** — it is
the operating manual (what Brutalist is, install, the three skills, the six
worked examples). This file adds only the session rules.

## What this toolkit is

Three builder skills — `ai-explainer`, `cli-explainer`, `deep-explainer` —
plus two personas (`nbb` = Teardown/Onyx, `hai` = Pragmatist/Bella) on a
shared runtime (`runtime/`). Entry point: `./art` (`--list`, `todo`, `run`,
`shorts`, `final`, `doctor`). Kokoro is the ONLY TTS engine; the only voices
are `am_onyx` ("Onyx") and `af_bella` ("Bella"). No API keys exist anywhere
in this folder.

## Rules

1. **Read the whole SKILL.md before building.** The three builders inherit
   doctrine from `skills/make/explainer/`, `your-turn/`, and
   `duration-planner/` — those are reference law, not entry points.
2. **Audio-first.** Narration MP3s are generated and measured first
   (`runtime/scripts/generate_audio_kokoro.py`); their durations are the
   master clock. Never fix timing by hand — regenerate audio, recompile.
3. **GATE P binds.** A human signs `PEDAGOGY.md` ("VERDICT: PASS") before
   audio is generated. It is a quality gate, not a cost gate — audio here is
   free.
4. **Videos travel with their book.** Build into `<book>/youtube/<slug>/`,
   never into this toolkit folder. `examples/` holds study copies only.
5. **Verify renders by LOOKING at frames** (`_qc/` + qc-sheet), never by the
   mp4 probe alone. Render Remotion only via
   `runtime/scripts/remotion_scenes.py` (foreground) — never hand-roll
   `npx remotion render`.
6. **Never publish.** There is no publishing machinery here at all; the
   master stays in the reel folder.
7. **No money, ever.** If any step appears to require a key or a paid
   service, stop — that's a bug in this toolkit, not a missing credential.
   The full-fat toolkit (paid voices, publishing, the other 35 skills) is
   `books/brutalist-art/`.
