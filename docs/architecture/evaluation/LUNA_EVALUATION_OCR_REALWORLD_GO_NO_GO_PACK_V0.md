# LUNA Evaluation — OCR Real-World Samples Go/No-Go Pack v0

## GO

- `manifest.jsonl`、`taxonomy_coverage_report.json`、逐条 `annotations/*.json`、human_review 三件套齐全。  
- `verify_ocr_realworld_difficult_samples_v0.py` **GO**。  
- `constraints` 表明未调 OCR provider、无 runtime/白盒/主线/中台副作用。  
- **placeholder** 均 `sample_source=placeholder`，且 `has_ground_truth` 不为 true。

## CONDITIONAL_GO

- 五类齐全但 **多为 placeholder**（`readiness_posture: CONDITIONAL_GO_pending_human_capture`）。  
- 人工标注仍为 `pending`。

## NO_GO

- 占位被标为 `user_fixture` / `manual_import` 等 **非 placeholder**。  
- 缺 annotation 或 human review 包。  
- 工具调用 OCR provider 或接入 runtime / 白盒 / 改 routing。
