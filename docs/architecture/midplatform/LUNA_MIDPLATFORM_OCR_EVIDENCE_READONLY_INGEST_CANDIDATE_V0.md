# Luna MidPlatform — OCR Evidence Read-Only Ingest Candidate v0

**Phase**: `Phase-MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001`

## 目的

定义中台侧 **`midplatform_ocr_evidence_ingest_candidate_v0`**：在 **不写事实层** 的前提下，将 **OCR read-only consumer** 已归一化的视图（`consumer_view`、`evidence_by_roi`、几何矩阵、`source_chain_summary`、`provider_summary`）封装为 **只读 ingest 候选**，供后续人工评审或 **远期** Scene Delta / AI 解释链路 **显式闸门** 消费。

## 边界

**允许**：订阅/读取上述 JSON 产物；生成 `midplatform_ocr_evidence_ingest_candidate`；保留 text / ROI / geometry / source chain / provider summary；写 **ingest audit**（全部为 false 的只读声明）。

**禁止**：AI 解释、语义总结、Scene Delta 写入、WorldModel 写入、MidPlatform **事实**写入、改变 OCR routing、调用 OCR provider。

## 契约摘要

- **schema_version**：`midplatform_ocr_evidence_ingest_candidate_v0`
- **ingest_scope**：`read_only_candidate`
- **forbidden_actions**：声明 `write_midplatform_fact` / `write_scene_delta` / `write_world_model` / `invoke_ai_interpretation` 等为 **禁止**（载荷内为 `true` 表示该项被标记为禁止，见评测产物 JSON）。
- **Audit**（`midplatform_ocr_evidence_ingest_audit_report.json`）：`midplatform_fact_written=false`、`scene_delta_written=false`、`world_model_written=false`、`ai_interpretation_invoked=false`、`ocr_provider_invoked=false`、`ocr_routing_changed=false`。

## 评测入口

见 [LUNA_EVALUATION_MIDPLATFORM_OCR_EVIDENCE_READONLY_INGEST_CANDIDATE_SMOKE_V0.md](../evaluation/LUNA_EVALUATION_MIDPLATFORM_OCR_EVIDENCE_READONLY_INGEST_CANDIDATE_SMOKE_V0.md)。
