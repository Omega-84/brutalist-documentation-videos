# BUILD-LOG — Medhavy OPT monthly recaps

2026-07-30  Task 1  am_michael added to ALLOWED_VOICES in runtime/scripts/generate_audio_kokoro.py
                    (user-directed; still Kokoro-only, still free). Module docstring updated to
                    match. Smoke test: "In week two, the extraction pipeline came together."
                    -> 3.48s, voice=am_michael. Rate ~2.3 words/sec.
                    NOTE: system python3 lacks kokoro-onnx — must use venv/bin/python.

2026-07-30  Task 2  OptWeekMarker.tsx created + registered in Root.tsx (id=OptWeekMarker).
                    QC by reading frames: first render underfilled the canvas (~250px dead band
                    above the chip) -> restructured to flex space-between across full SAFE height.
                    Verified 3 cases: default (3 bullets), 4 long bullets (May B09 worst case,
                    wraps clean), 5-pip rail (June). No clipping, no collision, margins hold.

2026-07-30  Task 3  OptHoursCard.tsx created + registered (id=OptHoursCard).
                    QC by reading frames: first render used bars, but every week in the reports
                    is exactly 20h -> four identical full-width bars implied variance that does
                    not exist (decoration, banned). Rebuilt as a typographic ledger with ruled
                    rows. Verified 4-row (May, total 80) and 5-row (June, total 100) cases.

2026-07-31  4K   Fixed two stock components before re-rendering, so the expensive pass ran once:
                 ClaudeCodeBeat  — font was pinned at height*0.022; now sizes to the listing,
                                   bounded by card height, card width vs longest line (mono
                                   advance ~0.6em), and a hard cap at height*0.046.
                 ClaudeVerdictArtifact — card 84%/1560 -> 90%/1740; heading 46->68,
                                   lines 28->40, padding scaled to match.
                 Then all 33 beats re-rendered at ART_SCALE=2 (3840x2160) and all three
                 months compiled at --height 2160. Verified: 0 non-4K beats, all masters
                 3840x2160, 33/33 slots filled, 0 slates. QC sheets in each _qc/.
