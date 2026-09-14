# LUNA — OCR Raw Text Length and Segmentation Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-001-Patch-002**

## GO

- hard length thresholds are explicitly defined
- segment schema is explicitly defined
- over-limit split/truncate policy is explicitly defined
- no-summary/no-semantic/no-navigation constraints are explicitly frozen
- line reference rule (`line_ids`) is frozen
- this phase does not modify runtime and does not connect downstream

## NO_GO

- OCR allowed to output long summary
- OCR allowed semantic compression
- `raw_text_joined` has no max limit
- segmentation has no line references
- runtime/downstream integration changed in this patch phase
