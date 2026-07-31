# PEDAGOGY — 2026-05-medhavy-may ("Two Fronts.")

**Reviewer:** Varun Nayyar  ·  **Date:** 2026-07-30
**Voice:** Kokoro am_michael  ·  **Register:** Pragmatist, third person

## Constraints applied

- Month-as-a-whole structure; not split week by week.
- Runtime capped under 3:30.
- No names except professors and Varun.
- No programme/visa terminology anywhere on screen or in voice.
- No meta narration about the video itself.
- Renders at 4K.

## Beat-by-beat narration

### B00 — ASK  (41 words · ClaudeComposerAsk)

Month one on the Medhavy project ran two technical duties at the same time. Prompt engineering on the electron-microscopy textbook, and healthcare systems integration research against a live clinical API. Both started in the first week. Neither waited for the other.

### B01 — DUTY I  (46 words · OptWeekMarker)

The first duty was the electron-microscopy textbook. Varun pushed prompt changes to a dedicated branch rather than straight to main, and repaired what was breaking in production: equation rendering, image handling, the cover page. That work later merged into the textbook repository as a pull request.

### B02 — DUTY I  (48 words · ClaudeCodeBeat)

Changing a prompt an entire textbook's tutor depends on is not a small edit, which is why it went to its own branch. The rendering repairs were the visible half: equations failing to typeset, image paths resolving wrong, a cover that would not build into the self-contained output.

### B03 — DUTY II  (46 words · OptWeekMarker)

The second duty was healthcare systems integration research, run against Epic's FHIR sandbox. Not a tutorial environment — a real API with real authentication. Varun built the extraction end to end: test patient identifiers, the bulk group identifier, and nested demographic records flattened into something analysable.

### B04 — DUTY II  (32 words · ClaudeCodeBeat)

Two scripts carry the pipeline. The first flattens nested demographic structures into a single file. The second pulls six clinical categories into six: problems, encounter diagnoses, labs, social history, encounters, diagnostic reports.

### B05 — FRICTION  (42 words · OptBlockerCard)

One piece of friction is worth naming. The repository access needed to open that pull request took a week to become usable — the invite had been sent, and sat unread. Once open, the fixes went in as a proper pull request.

### B06 — DUTY II  (48 words · ClaudeCodeBeat)

Retrieving the note text returned a four-oh-three Forbidden. The move that matters is not retry logic — it is reading what the server is refusing. A missing OAuth scope, system slash Binary dot read, resolved through the developer portal. Not a defect. A permission the token never had.

### B07 — FINDING  (51 words · OptBlockerCard)

Then the finding that mattered more than the fix. Across the whole sandbox, seven patient records were populated, and sparsely. That is not enough to build research on. Varun reported it in writing to Prof. Sridhar, with a summarised spreadsheet of the sandbox API and an offer to explore further endpoints.

### B08 — DECISION  (48 words · OptWeekMarker)

Prof. Sridhar ended the Epic integration workstream, citing accumulated blockers — sparse data, authorization friction, an unclear access model. Every one of them already documented from Varun's side. The same day brought a new assignment: Manim instructional video for the physics mechanics textbook, with access requested that day.

### B09 — HOURS  (15 words · OptHoursCard)

Four weeks, twenty hours documented in each. Eighty hours for the month. Status: in compliance.

### B10 — VERDICT  (42 words · ClaudeVerdictArtifact)

Month one, then. Two technical duties in parallel from the first week. Textbook repairs merged to the repository. A clinical-data pipeline built end to end against a live API, including a real authorization fix. And a data limitation found, evidenced, and escalated.

### B11 — OUTRO  (5 words · ClaudeTitleOutro)

Two Fronts. Medhavy, month one.

## Runtime

464 words at ~2.3 words/sec ≈ 202s (3:22). Under the 3:30 cap.

## Checks

- [ ] Every claim traces to hai_reports_weeks_1-12.md, Weeks 1-4
- [ ] Hours stated as "documented"; status reads In compliance
- [ ] No non-professor names; teammates referred to generically
- [ ] Nothing referenced after May 28, 2026

VERDICT: PASS — signed by Varun Nayyar, 2026-07-30.
