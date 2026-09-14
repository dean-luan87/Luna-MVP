# LUNA — Visual Symbol → WorldContextEvidence Mapping v0

## Phase

- **Phase-WorldModel-VisualSymbolEvidence-001**

## Purpose

定义 `VisualSymbolEvidence` 如何映射到统一世界证据合同 `WorldContextEvidence`（参照既有 spatiotemporal/trust/lifecycle 口径），并写死“未确认不得污染世界事实”的边界。

本阶段只做映射定义，不接真实世界模型写入。

## Mapping overview

### 1) 未确认（unknown / suspected）

当：

- `meaning_status in {unknown, suspected}` 或 `confirmation_method=none`

映射策略：

- 只允许进入 `WorldContextEvidence` 的 **candidate-only** 形态（或以 `world_model_policy.write_policy=no_write` 表达）
- 必须 `requires_revalidation=true`
- `task_planning_impact="none"`
- 不得作为“事实性实体/机构/授权”写入

### 2) 已确认（confirmed）

当：

- `meaning_status=confirmed` 且 `confirmation_method != none`

映射策略：

- 允许生成 `WorldContextEvidence` 候选，`write_policy` 仍默认为 `low_priority_candidate` 或 `scene_local_candidate`
- `requires_revalidation=true`（高风险类别强制）
- 仍不得生成导航动作

### 3) 被否定/冲突（contradicted）

映射策略：

- 仅保留证据引用，不写事实
- 触发 revalidation/冲突标记（占位）

## Field mapping（字段对齐）

建议映射到 `WorldContextEvidence` 的字段：

- `observed_at` ← `VisualSymbolEvidence.observed_at`
- `observed_where` ← `VisualSymbolEvidence.observed_where`
- `trust` ← 映射/复制 `trust_score`、`fraud_risk_status`、`visual_confidence/context_confidence`
- `lifecycle.requires_revalidation` ← `memory_policy.requires_revalidation`（默认 true）
- `content`：
  - `entity_type`：根据 `symbol_type`/`confirmed_meaning.entity_type` 映射（如 `institution_mark` / `brand_mark` / `document_authority_mark` 占位）
  - `details`：保留 `symbol_type` + `symbol_visual_signature.feature_hash` + `confirmation_method`（可追责）
- `source_evidence_refs`：包含 `source_image_ref`（以及 `visual_symbol_evidence_id` 的引用）

## 禁止项（强制）

- 禁止把 `seal_or_stamp/signature/certificate_mark` 在 `meaning_status != confirmed` 时映射为世界事实
- 禁止仅凭 `ocr_auxiliary_text` 映射为确认含义

