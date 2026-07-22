---
name: nbb
description: >
  NikBearBrown brand spec — Teardown register (Feynman × MKBHD), ElevenLabs
  NIKBEARBROWN voice (paid, no Kokoro fallback), teardown palette (white /
  ink / one red). Used by the audience-preset skill when brand=nbb. For the
  first-class nbb command (directory convention, LLM exercise beat, outro),
  see skills/make/nbb/SKILL.md.
---

# nbb — NikBearBrown brand spec

Brand specification used by `audience-preset` when `<brand>=nbb`. The
**first-class `nbb` command** (directory convention, LLM exercise beat, and
NikBearBrown outro) is documented in `skills/make/nbb/SKILL.md`.

## Register — Teardown (Feynman × MKBHD)

Take it apart, explain how each piece works, judge the design choices.

- **Explain the machinery**: not the name — the actual mechanism.
- **Reveal design philosophy**: what was this optimized for? what did it sacrifice?
- **Judge the choices**: do they succeed on their own terms? name the trade-offs.
- Intellectual honesty: admit limits ("I don't fully understand why…"), think in
  ecosystems ("nothing exists in isolation").
- Design-critic lens: "They optimized for X at the expense of Y."
- Nik Bear Brown speaks in **first person** when the content is his.

Forbidden: "One could argue…" / "innovative" without saying what changed / specs
without context. Use: "Here's what's actually happening…" / "This works if you
value X; it fails if you need Y."

Voice reference: `voices/teardown/VOICE.md`

## Voice

| Engine | Setting |
|---|---|
| ElevenLabs | `ELEVENLABS_VOICE_NIKBEARBROWN` env var — the **only** option |
| Kokoro | **NOT used** — nbb is the paid brand; there is no free fallback |

`brand_variant.py` writes `engine: "elevenlabs"` and reads `voice_id` from
`ELEVENLABS_VOICE_NIKBEARBROWN`. GATE P applies before any audio spend.

## Palette — `teardown`

Minimalist, single accent. Tokens: `runtime/remotion/src/tokens/vox.ts`
(exported as `TEARDOWN`).

| Role | Hex |
|---|---|
| CREAM / ground | `#FFFFFF` — flat white |
| INK | `#2A1A0E` — all body text / marks |
| CRIMSON (the one accent) | `#C8102E` — bad / lost / emphasis |
| SLATE (structure) | `#545454` |
| GOLD (fill only) | `#F6D8DC` — ~14% wash of accent |
| HAIRLINE | `#D4D4D4` |

**Color law:** one accent only. Good/kept = plain INK (label + position carry
the meaning, not a second hue). Gold is fill-only, never text.

Typography: **Montserrat** (display/titles) + **EB Garamond** (serif/editorial)
+ **PT Mono** (data numbers/math).

## Outro

Content from the **NikBearBrown** section of the book's `AUTHOR.MD`
(default channel: `www.brutalist.art`). Renders via Remotion `OutroSeries` /
`OutroCTA` in the teardown palette.

## LLM exercise flavor

The second-to-last beat is an **LLM exercise** (not a CLI command): a
paste-ready prompt for Claude / ChatGPT / Gemini + a "go deeper" follow-up
question. The prompt must produce a useful output on its own. The follow-up
must be genuinely explorable, not a summary.
