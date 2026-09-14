# Luna 评测 — MidPlatform Vision ReadOnly Ingest Candidate GO / NO_GO Pack v0

**Verifier**：`tools/evaluation/midplatform/verify_midplatform_vision_recognition_evidence_readonly_ingest_candidate_v0.py`  
**Phase**：`Phase-MidPlatform-Vision-Recognition-Evidence-ReadOnly-Ingest-Candidate-001`

## GO

- **`midplatform_vision_recognition_ingest_candidate.json`** 存在；`schema_version=midplatform_vision_recognition_ingest_candidate_v0`。  
- `ingest_scope=read_only_candidate`；`evidence_count > 0`。  
- `provider=vision_stub`，`provider_level=stub`。  
- `fact_status_summary.not_fact == evidence_count`；`synthetic_summary` 两项均等于 `evidence_count`。  
- `evidence_by_frame`、`evidence_by_roi_type`、`geometry_summary` 非空。  
- `forbidden_actions` 六键齐全且值为 **true**（表示禁止）。  
- audit：`midplatform_vision_ingest_candidate_generated=true`；所有写 / 模型 / 解释 / 导航类字段为 **false**。  
- ingest matrix、source_chain_summary 文件存在。

## CONDITIONAL_GO

- 无 **NO_GO** blockers，但存在 **soft_notes**（例如 ingest 矩阵行数与 `evidence_count` 轻微不一致等）。

## NO_GO

- 写 MidPlatform fact / Scene Delta / WorldModel；调用 AI interpretation / 导航 / 真实视觉 / YOLO / Supervision 主线 / VLM / OCR。  
- 将 stub 标为 **confirmed fact**；`forbidden_actions` 缺失；**audit** 缺失；candidate 缺失。

## 一句话

本 smoke **只**生成 Vision 证据的 **中台只读 ingest 候选**；**不**落库、**不**写事实层。
