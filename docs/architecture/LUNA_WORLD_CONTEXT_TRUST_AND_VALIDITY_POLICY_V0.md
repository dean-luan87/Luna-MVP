# LUNA — World Context Trust & Validity Policy v0

## Phase

- Phase-WorldModel-ContextEvidence-001

## Purpose

定义 WorldContextEvidence 的 trust / validity / revalidation 规则，使得世界证据具备：
- 可解释的信任度（trust_score）
- 可追踪的验证状态（cross_validation_status）
- 可更新的有效期与生命周期（evidence_status / ttl_policy / expires_at）
- 明确的复核触发（requires_revalidation）

本阶段只定义合同，不实现 runtime。

## Non-governance boundary

- 不实现真实写入/共享/推荐/导航/播报。

## trust_score（信任度占位体系）

`trust.trust_score` 建议取值范围：`0.0 ~ 1.0`。

信任度用于约束：
- 是否可共享到跨个体（share_policy / shareable_to_hive）
- 是否可用于任务规划（world_model_policy.task_planning_impact）

## cross_validation_status（交叉验证状态冻结）

取值必须来自：
- `single_source`：仅单一来源模态（如单次 OCR 或单次视觉）支持
- `multi_source_confirmed`：多源一致（例如 OCR+YOLO、或多次观测一致）
- `contradicted`：证据冲突（同空间锚点下文本/实体出现互斥）
- `expired`：证据已过期但仍有历史记录
- `unknown`：无法判断验证状态（默认保守）

## fraud_risk_status（欺诈风险占位）

取值必须来自：
- `unknown`：未评估
- `suspected`：疑似欺诈/误导（例如文本风格异常、上下文不一致）
- `verified_safe`：已验证安全
- `suspected_fraud`：疑似欺诈且更强风险信号

欺诈风险用于约束：
- `world_model_policy.requires_user_confirmation`
- `world_model_policy.shareable_to_hive`

## Validity lifecycle（有效期与生命周期冻结）

`lifecycle.evidence_status` 取值：
- `active`：在有效期内，可信度满足最低可用阈值（阈值占位由后续阶段定义）
- `stale`：仍未过期，但信任度下降或时间接近失效
- `expired`：过期
- `contradicted`：被观测到与旧信息冲突
- `superseded`：被更可信/更新状态的证据替代

`ttl_policy` 取值：
- `short_ttl`：默认给商业/活动类证据（促销、营业时间、临时信息等）
- `scene_local_ttl`：给场景局部环境信息（店铺名称、楼层导视等）
- `persistent_requires_revalidation`：可持久化但必须复核门控（例如长期公共标识）

## requires_revalidation（复核触发冻结）

`lifecycle.requires_revalidation`：
- 对短 TTL 商业信息：默认 `true`
- 对可持久化信息：默认 `true`
- 对用户确认或多源确认：可下降为 `false`（但是否允许由后续 governance 决策）

## Revalidation policy（复核规则，合同层占位）

复核触发条件（占位）：
1) 同空间锚点在新时间窗口再次被观察到（last_seen_at 更新）
2) 内容文本出现明显变化（evidence_status 变为 stale/contradicted）
3) 用户明确请求读取/确认（requires_user_confirmation 分支产生更高信任路径）

复核动作仅定义“状态如何更新”，不定义 runtime。

