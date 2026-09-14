# LUNA Evaluation — Scene Delta Write Candidate from OCR Smoke GO / NO-GO Pack v0

**Phase**: `Phase-MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001`

## GO

- `scene_delta_write_candidate_from_ocr.json` **存在**，`schema_version` = **`scene_delta_write_candidate_from_ocr_v0`**。
- **`candidate_scope=write_candidate_only`**，**`write_allowed=false`**，**`requires_gate_approval=true`**。
- **`evidence_count` ≥ 1**，**`evidence_items`** 非空；每条含 **非空 `text`**、**`roi_id` 或 `unit_id`**、**原图几何**（`original_bbox` 或 `original_polygon`）、**`fact_status=not_fact`**、**`evidence_role=observed_text`**。
- **`forbidden_actions`** 四键齐全且为 **true**（声明禁止写/解释）。
- **Gate stub**：`gate_required=true`，`gate_status=not_evaluated`，`gate_reason_codes` 含规范所列三条。
- **Audit**：`scene_delta_write_candidate_generated=true`；`scene_delta_written`、`midplatform_fact_written`、`world_model_written`、`ai_interpretation_invoked`、`database_write_invoked`、`external_bus_invoked`、`ocr_provider_invoked`、`ocr_routing_changed` 均为 **false**。
- 载荷树中 **无** AI 解释类禁止键名。

## CONDITIONAL_GO

- **`source_chain_summary`** 为空或不完整，但有 **gap 记录**（summary 或 notes）；**无写路径**。

## NO_GO

- **实际写入** Scene Delta / MidPlatform 事实 / WorldModel，或 **调用 AI / OCR provider**，或 **改 routing**，或 **连真实外部总线 / DB**。
- **`write_allowed=true`** 或 **`gate_status=approved`**（或等效已放行语义）。
- OCR 证据被标为 **`confirmed_fact`** 等禁止 **`fact_status`**。
- **缺 audit**、**缺 gate stub**、**schema 不匹配**、**forbidden_actions 不齐**。

## 一句话

本阶段只从 OCR ingest / 只读事件载荷 **生成 Scene Delta write candidate JSON**；**不写 Scene Delta、不写事实层、不写 WorldModel、不调用 AI 解释**。
