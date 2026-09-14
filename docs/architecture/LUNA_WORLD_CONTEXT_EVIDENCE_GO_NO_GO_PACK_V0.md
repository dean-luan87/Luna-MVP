# LUNA — World Context Evidence Contract GO/NO-GO Pack v0

## Phase

- Phase-WorldModel-ContextEvidence-001

## Scope

本阶段只定义合同，不接 runtime。

此处给出本阶段的 GO/NO-GO 验收判据，用于后续实现阶段复核。

## GO 条件

1) 时空字段定义完整
- `observed_at.timestamp_ms`
- `observed_where.spatial_anchor_type` 与 `place_hint`（至少占位可读）

2) 信任度与验证状态定义完整
- `trust.trust_score`
- `trust.cross_validation_status`

3) 生命周期与有效期定义完整
- `lifecycle.ttl_policy`
- `lifecycle.expires_at`（允许为 null 但必须存在字段）
- `lifecycle.requires_revalidation`
- `lifecycle.evidence_status`

4) 商业/活动证据策略定义完整（占位）
- 使用 `short_ttl` 与 `requires_revalidation=true`
- 欺诈风险独立标记（fraud_risk_status 或 fraud signal）

5) 世界变化观察事件定义完整（占位）
- `WorldChangeEvent.change_type` 枚举
- 事件必须绑定 `observed_at` 与 `observed_where`

6) rating/fraud signal 占位合同存在

7) 不实现 runtime / 不接推荐执行

## NO-GO 条件

1) 把 OCR/YOLO 单次结果直接当世界事实

2) 缺少时空锚点（无法判断过期与变化）

3) 缺少信任度/验证状态字段

4) 缺少 TTL 或 revalidation 规则（导致旧信息污染）

5) 允许广告/欺诈信息直接影响任务规划或默认共享（没有 share/安全门控）

6) 接入推荐/导航/任务执行 runtime

