# PEDAGOGY — 2026-06-medhavy-june ("Learning to Render.")

**Reviewer:** Varun Nayyar  ·  **Date:** 2026-07-30
**Voice:** Kokoro am_michael  ·  **Register:** Pragmatist, third person

## Scope

Month two (June 2026)

## Constraints applied

- Month-as-a-whole structure; not split week by week.
- No names except professors and Varun; teammates referred to generically.
- No vendor/tool brand names on screen.
- No programme terminology anywhere.
- No meta narration.
- Renders at 4K.

## Beat-by-beat narration

### B00 — ASK  (41 words · ClaudeComposerAsk)

Month two was a standing start on a new toolchain. In five weeks Varun went from an empty environment to animated physics scenes a professor approved and asked him to continue — with one genuine animation bug solved along the way.

### B01 — SETUP  (52 words · OptWeekMarker)

The first week produced no visible deliverable, and that is worth stating accurately. Standing up a rendering toolchain on Windows Subsystem for Linux means system libraries, a package manager that resolves paths correctly, and a filesystem that will not fight you. All of it has to work before a single frame exists.

### B02 — SETUP  (46 words · ClaudeCodeBeat)

Two failures had to be diagnosed before anything rendered. The package manager was resolving against the wrong environment, fixed with the active flag. And the Windows filesystem rejected the hardlinks the installer wanted, fixed by telling it to copy instead. Then the first scene rendered clean.

### B03 — THE SCENES  (46 words · OptWeekMarker)

With the environment working, the actual animation began. Two scenes: the observable universe, and the Milky Way. Both started as naive approximations and both were rebuilt, because the first versions were geometrically wrong in ways an audience would feel even if they could not name it.

### B04 — THE SCENES  (54 words · ClaudeCodeBeat)

The star field is the clearest example. Scattering points uniformly in radius clusters them at the centre, because area grows with the square of the radius. The correct sampling takes the square root of a uniform draw. That one substitution is the difference between a diagram that looks plausible and one that is right.

### B05 — THE BUG  (46 words · OptWeekMarker)

Then a real animation bug. In a scene cycling through SI base quantities, the static headings were vanishing after the first iteration. Not a rendering fault, and not a timing problem — a structural one. Something was clearing elements that were never meant to be cleared.

### B06 — THE BUG  (48 words · ClaudeCodeBeat)

The fade-out call was inside the loop that cycled the units, so every pass cleared the headings along with the values. Moving it outside fixed it. The second change was subtler: swapping the transform so fixed phrases stay stationary while only the variable unit symbols morph between iterations.

### B07 — APPROVAL  (65 words · OptWeekMarker)

On June fifteenth the completed videos went to Prof. Sridhar. He approved them and asked Varun to continue — in writing, and again verbally in the standing meeting. Later that month Prof. Nik directed a move to a new tool, with an instruction to build visualisations only for topics that genuinely warrant one. Varun submitted a scoped topic list for review rather than deciding alone.

### B08 — DEPENDENCY  (50 words · OptBlockerCard)

Videos were produced on the new tool against that approved list. The narration layer was the one piece that did not land: the API key provided for voice was disabled. Not a configuration error and not a usage limit — an inactive credential, resolvable only by whoever administers the account.

### B09 — HOURS  (16 words · OptHoursCard)

Five weeks, twenty hours documented in each. One hundred hours for the month. Status: in compliance.

### B10 — VERDICT  (47 words · ClaudeVerdictArtifact)

Month two, then. A rendering toolchain stood up from nothing on an awkward platform. Two physics scenes rebuilt until the geometry was correct. A real animation bug traced to its structural cause and fixed. Professor approval to continue, in writing. And production scoped collaboratively rather than unilaterally.

### B11 — OUTRO  (6 words · ClaudeTitleOutro)

Learning to Render. Medhavy, month two.

## Runtime

517 words at ~2.3 words/sec ≈ 225s.

VERDICT: PASS — signed by Varun Nayyar, 2026-07-30.
