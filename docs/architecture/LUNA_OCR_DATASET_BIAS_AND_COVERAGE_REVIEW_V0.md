# LUNA — OCR Dataset Bias and Coverage Review v0

## Phase

- **Phase-ModelOCR-006**

## Distribution summary (n=30)

- expected_text_type: `department_sign=5`, `doorplate=1`, `english_text=9`, `floor_sign=7`, `mixed=1`, `screen_text=7`
- language_type: `digit=6`, `en=11`, `mixed=8`, `zh=5`
- difficulty_level: `easy=10`, `medium=10`, `hard=10`
- visual_condition: `clear=6`, `distant=7`, `occluded=1`, `reflective=7`, `tilted=9`

## Imbalance risks

- `exit_sign` missing
- `warning_text` missing
- zh samples fewer than en samples
- doorplate count is low

## Output refs

- `dataset_distribution_summary.json`
- `imbalance_risk_register.json`
