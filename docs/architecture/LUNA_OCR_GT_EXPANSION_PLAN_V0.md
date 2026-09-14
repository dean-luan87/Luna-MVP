# LUNA — OCR GT Expansion Plan v0

## Phase

- **Phase-ModelOCR-005A**
- Scope: expand OCR raw-text GT only.

## Target

- v0.1 target: >=30 samples (current round is expansion-in-progress).
- Keep strict raw-text-only annotation.

## Stratified dimensions

- `expected_text_type`
- `difficulty_level` (`easy|medium|hard`)
- `visual_condition` (`clear|blurred|tilted|distant|reflective|occluded|low_light|screen`)
- `language_type` (`zh|en|digit|mixed`)

## Guardrails

- no semantic labels
- no navigation labels
- no downstream linkage
- no GT backfilled from OCR prediction
