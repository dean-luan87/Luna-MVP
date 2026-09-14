# LUNA — World Model Spatiotemporal Binding Constitution v0

## Phase

- **Phase-WorldModel-WriteReadiness-003**

## Status

- 宪法级原则（长期约束）
- 本阶段只做 definition closure，不实现 runtime、不写真实世界模型

## Core claim（宪法级定义）

世界模型中的任何内容（无论是店铺、海报、广告、服务台、路线、风险点、人的行为、商业活动、视觉符号、用户反馈），只要进入世界模型并可被读取/复用，就必须回答三个问题：

1) **它是什么？**  
2) **它在哪里？**  
3) **它在什么时候成立？**

缺少时空间信息的内容，不得称为“世界模型信息”；最多只能是 **未定位证据** / **待复核碎片** / **审计片段**。

## Constitution rules（硬规则）

1. 世界模型中任何可读取、可复用、可推荐、可规划的信息，必须具备**时空间绑定**。
2. 无 `observed_at` 的信息，不得进入世界模型。
3. 无 `observed_where` 的信息，不得进入世界模型事实层。
4. 时空锚点弱或未知的信息，只能进入 `audit_only` / `provisional` / `uncertain candidate`。
5. 所有 `CommittedWorldMemoryRecord` 必须携带 `spatiotemporal_binding`。
6. 所有 revision / rollback / supersede / expire 必须基于同一或可证明相关的时空锚点发生。
7. 所有 read visibility 必须受 `spatial_scope + temporal_scope` 限制（读取请求必须检查当前上下文是否落在 scope 内）。
8. 没有时空间信息的内容，不允许被任务链/推荐/导航/蜂巢资料包当作事实使用。

## Minimal binding fields（v0 必备字段）

任何 `world_model_item`（含 committed/provisional）至少具备：

- `observed_at`（first/last/valid_from/valid_until/time_source/temporal_confidence）
- `observed_where`（spatiotemporal_anchor_ref/spatial_anchor_type/geo_location/place_hint/relative_position/spatial_signature/carrier_signature/spatial_confidence）
- `scope`（scope_type + scope_confidence）
- `binding_status`（bound/weakly_bound/unresolved/expired/contradicted）

## Definition consequence（系统性声明）

**World model information is only meaningful when bound to time and space.**  
Unbound information is not world knowledge; it is unresolved evidence.

