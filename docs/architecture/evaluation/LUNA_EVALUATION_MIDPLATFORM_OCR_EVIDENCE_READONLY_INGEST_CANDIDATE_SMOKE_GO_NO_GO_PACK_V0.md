# LUNA Evaluation — MidPlatform OCR Evidence Read-Only Ingest Candidate Smoke GO / NO-GO Pack v0

**Phase**: `Phase-MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001`

## GO

- `midplatform_ocr_evidence_ingest_candidate.json` **存在**，且 `schema_version` = **`midplatform_ocr_evidence_ingest_candidate_v0`**。
- `evidence_count` **≥ 1**；`text_joined` **非空**。
- `evidence_by_roi`、`geometry_matrix`、`source_chain_summary`、`provider_summary` **均存在且非空**（在类型语义下：`evidence_by_roi` 非空对象；`geometry_matrix` 非空数组；`source_chain_summary` 含 `chain` 或 `chain_item_count`）。
- `ingest_scope` = **`read_only_candidate`**。
- **Audit** 全为 **false**：`midplatform_fact_written`、`scene_delta_written`、`world_model_written`、`ai_interpretation_invoked`、`ocr_provider_invoked`、`ocr_routing_changed`。

## CONDITIONAL_GO

- `source_chain_summary.chain_item_count == 0`（链缺失或空），但其余硬条件满足；须在 `soft_notes` 披露。

## NO_GO

- 任何 **事实写入**、**Scene Delta 写入**、**WorldModel 写入**、**AI 解释调用**、**OCR provider 调用**、**OCR routing 变更**（由 audit 或实现侧证实）。
- **丢失 ROI 归属**（`evidence_by_roi` 不可用）、**丢失 source chain 摘要结构**、**audit 缺失或门禁字段非 false**。
- Candidate **缺失**或 **schema 不匹配**。

## 一句话

本阶段只验证中台能够以 **只读 ingest 候选** 接收 OCR evidence，并保留 **文本、ROI、几何与 source chain**；**不写事实层、不写 Scene Delta、不写 WorldModel、不调用 AI 解释**。
