# Luna MidPlatform — Scene Delta Write Candidate from OCR v0

**Phase**: `Phase-MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001`

## 目的

定义 **`scene_delta_write_candidate_from_ocr_v0`**：在 **不落库、不写 Scene Delta、不写事实层、不写 WorldModel、不调用 AI** 的前提下，将 **OCR read-only event payload**（及关联几何矩阵）整理为 **Scene Delta 写操作候选载荷**，供后续 **闸门评估** 与 **显式采纳流程** 使用。

## 核心边界

- **候选 ≠ 事实**：OCR 文本仅为 **`observed_text`**，**`fact_status=not_fact`**；不得出现 **`confirmed_fact`**、**`world_model_fact`**、**`scene_delta_written`** 等语义。
- **不写**：Scene Delta 执行体、MidPlatform 事实、WorldModel；**不**调用 AI 解释；**不**调用 OCR provider；**不**改 OCR routing；**不**连真实外部总线；**不**做数据库写入。
- **`write_allowed=false`**，**`requires_gate_approval=true`**，**`candidate_scope=write_candidate_only`**。

## 闸门占位（Gate Stub）

独立文件 **`scene_delta_write_candidate_gate_stub.json`**：`gate_required=true`，`gate_status=not_evaluated`，`gate_reason_codes` 至少包含：

- `ocr_evidence_requires_scene_delta_gate`  
- `no_ai_interpretation`  
- `no_world_fact_write`  

## 禁止字段（解释层）

载荷中 **不得** 出现以下键名（任意嵌套）：`semantic_summary`、`inferred_meaning`、`object_meaning`、`business_meaning`、`environment_interpretation`、`user_facing_explanation`。

## 评测入口

见 [LUNA_EVALUATION_SCENE_DELTA_WRITE_CANDIDATE_FROM_OCR_SMOKE_V0.md](../evaluation/LUNA_EVALUATION_SCENE_DELTA_WRITE_CANDIDATE_FROM_OCR_SMOKE_V0.md)。
