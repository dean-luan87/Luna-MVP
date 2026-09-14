# LUNA — OCR GT Expansion and Stratified Eval Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-005A**

## GO

- sample_count >= 30
- expected_text_type coverage >= 6
- language coverage includes `zh/en/digit/mixed`
- difficulty coverage includes `easy/medium/hard`
- stratified metrics generated
- governance leakage = 0
- trace/replay/whitebox complete

## CONDITIONAL_GO

- sample_count in [10, 29]
- stratified metrics generated
- coverage improved over seed set, but not complete
- provider status is honest and legal

## NO_GO

- sample_count <= 5
- GT includes semantic/navigation fields
- manifest lacks stratified fields
- provider failure faked as success
- governance leakage > 0
- missing observability artifacts
