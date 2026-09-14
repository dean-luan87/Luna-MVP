# LUNA — OCR GT 30+ Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-005B**

## GO

- sample_count >= 30
- expected_text_type >= 6
- language_type covers zh/en/digit/mixed
- difficulty covers easy/medium/hard
- visual_condition >= 5
- stratified metrics complete
- governance leakage = 0
- trace/replay/whitebox complete

## CONDITIONAL_GO

- sample_count in [20, 29]
- expected_text_type >= 6
- hard_blockers = []

## NO_GO

- sample_count <= 12
- expected_text_type < 6
- GT/manifest has forbidden semantic/navigation fields
- benchmark leaks downstream or governance checks fail
