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
