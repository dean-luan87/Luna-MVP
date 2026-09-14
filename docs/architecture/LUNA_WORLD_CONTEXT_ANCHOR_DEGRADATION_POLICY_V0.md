# LUNA — WorldContextEvidence Anchor Degradation Policy v0

## Phase

- **Phase-WorldModel-ContextEvidence-003**

## Purpose

当 `observed_where` / `spatiotemporal_anchor_ref` 缺失或不可解析时，定义离线候选必须采取的降级策略，防止候选“看起来很像事实”。

## Degradation rules（必须）

### A) observed_where 缺失或 unknown

当 `observed_where.spatial_anchor_type="unknown"`：

- `lifecycle.requires_revalidation=true`（强制）
- `world_model_policy.task_planning_impact="none"`（强制）
- `world_model_policy.write_policy` 保守为 `no_write` 或 `low_priority_candidate`
- `trust.trust_score` 保守降权（占位即可，但必须存在）

### B) spatiotemporal_anchor_ref 缺失

当 `observed_where.spatiotemporal_anchor_ref=null`：

- 允许生成 candidate（candidate-only）
- `anchor_status="missing_or_unresolved"`
- `observed_where_source="fallback_unknown"`
- `spatial_anchor_confidence=0.0`

### C) source chain 缺失

- 若 `source_evidence_refs` 也缺失：视为 **hard blocker**（NO_GO）
- 若 direct refs 存在但链不完整：`source_ref_integrity_status="partial"` 并记录 `missing_source_refs`

## Forbidden（强禁止）

- 不得伪造 GPS（lat/lng）
- 不得把处理层（scene_delta/midplatform）当作感知来源写入 `source_modalities`

