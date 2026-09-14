# LUNA — World Context Field Alignment GO/NO-GO Pack v0

## Phase

- Phase-WorldModel-ContextEvidence-001-Fix
- Field Mapping Alignment v0

## Purpose

给出字段对齐阶段的验收判据，确保后续 `Phase-ModelOCR-MidPlatform-Bridge-002` skeleton 不会因为字段漂移而返工。

本阶段只定义合同，不实现 runtime。

## GO conditions

1) 目标合同一致
- `WorldContextEvidence` 作为唯一世界证据 schema 名称被使用（允许旧命名别名存在，但必须映射）。

2) 时空字段对齐
- `observed_at.timestamp_ms` 存在
- `observed_where.spatial_anchor_type` 与 `observed_where.place_hint` 存在（允许为占位，但字段必须存在）

3) 信任与验证字段对齐
- `trust.trust_score` 存在
- `trust.cross_validation_status` 存在
- `trust.fraud_risk_status` 存在（或通过占位合同存在）

4) 生命周期与有效期对齐
- `lifecycle.ttl_policy` 存在
- `lifecycle.requires_revalidation` 存在
- `lifecycle.expires_at` 字段存在（可为 null，但字段必须存在）

5) 策略与共享对齐
- `world_model_policy.write_policy` 存在
- `world_model_policy.shareable_to_hive` 存在

6) MidPlatform → World 映射完整
- `trace_ref/whitebox_ref` 从中台候选保留到世界合同。
- `expiry_policy/short_ttl/scene_local_ttl` 与 `lifecycle.ttl_policy` 枚举可一一对应。

7) 禁止错误越界
- MidPlatform 的商业/广告信息在默认情况下不得驱动导航主路径（通过 `task_planning_impact=none` 或 `allowed_for_primary_task_decision=false` 的映射体现）。
- 不实现 runtime / 不写真实世界模型 / 不接推荐系统 / 不接任务执行 / 不做播报。

## NO-GO conditions

1) 出现“两个并列世界证据 schema”且无映射

2) 缺少 TTL / revalidation 对应关系

3) 缺少 trust 或 observed_at/observed_where

4) 将 OCR/广告结果当世界事实用于任务规划或默认共享（没有 share/安全门控）

