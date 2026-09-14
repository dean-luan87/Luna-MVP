# LUNA — Commercial Context Text → CommercialActivityEvidence Mapping v0

## Phase

- Phase-WorldModel-ContextEvidence-001-Fix
- Commercial Evidence Mapping Alignment v0

## Purpose

定义 MidPlatform 的商业/促销/广告类视觉文本如何映射为世界合同中的商业证据语义：
- `WorldContextEvidence.content.entity_type`
- `WorldContextEvidence.content.entity_name`
- `WorldContextEvidence.content.discount_or_promotion / valid_time_text`
- 并与 `CommercialActivityEvidence` 的占位策略一致。

本阶段只做映射，不实现 runtime。

## Mapping（可执行语义表）

| MidPlatform visual_text_relevance_class | Ambient/Context type（中台） | WorldContextEvidence.content.entity_type（占位枚举） | content.entity_name | content.valid_time_text | content.details/discount_or_promotion | default lifecycle.ttl_policy | default trust.fraud_risk_status |
|---|---|---|---|---|---|---|---|
| commercial_context_text | commercial_context_text | store_business_hours / store_business_promo（占位） | 店名（若可抽取） | 营业时间/活动时间（若可抽取） | 折扣/促销文本 | short_ttl | unknown |
| promotional_text | promotional_text | store_promotion | 店名（若可抽取） | 活动时间 | 促销规则/满减/会员价文本 | short_ttl | suspected |
| advertisement_like_text | ambient_context_text | store_ambient_ad | 店名或品牌名（若可抽取） | 活动时间（若文本包含） | 广告语/轮播屏内容 | short_ttl | unknown |
| world_context_text（店名/品牌） | world_context_text | store_business_info | 品牌/店名 | 公共信息时间（若可得） | 相关说明 | scene_local_ttl | unknown |
| user_requested_text（商业询问时） | user_requested_text | store_promotion/store_business_hours（由内容决定） | 店名（若可得） | 从原文提取 | 从原文提取 | short_ttl（默认）或需复核持久化 | unknown |

## Default constraints（关键约束）

1) 商业证据默认不用于主任务规划
- `WorldContextEvidence.world_model_policy.task_planning_impact=none`（占位），并保持 `requires_revalidation=true`。

2) 过期/冲突必须可表达
- 商业证据进入 `stale/expired/contradicted` 由后续观察更新；本阶段只定义字段与状态集。

3) 欺诈风险必须单独标记，不得传播为事实
- `trust.fraud_risk_status` 默认 `unknown`。
- 若跨模态/上下文冲突则可标记为 `suspected/suspected_fraud`（占位）。

