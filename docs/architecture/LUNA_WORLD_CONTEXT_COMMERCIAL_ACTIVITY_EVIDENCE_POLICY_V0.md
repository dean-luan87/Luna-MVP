# LUNA — World Context Commercial Activity Evidence Policy v0

## Phase

- Phase-WorldModel-ContextEvidence-001

## Purpose

定义：当商业信息（店铺活动、折扣、促销、营业时间、开业/关店、招商、施工围挡提示等）被观测时，
如何在世界证据层形成 `CommercialActivityEvidence`（或等价结构）并进入/更新 `WorldContextEvidence`。

本合同强调三点：
1) 商业信息默认低信任，不是世界事实；
2) 商业信息必须短 TTL + requires_revalidation，避免旧信息污染；
3) 欺诈风险必须单独标记，默认不传播为事实。

参照：`LUNA_MIDPLATFORM_TO_WORLD_CONTEXT_FIELD_MAPPING_V0.md`（字段口径对齐映射）

## Non-governance boundary

- 不实现 runtime，不接真实世界模型写入。
- 不接推荐系统/任务执行/导航/播报。

## CommercialActivityEvidence（扩展字段）

建议以“商业证据体”形式填入 `WorldContextEvidence.content` 或作为子结构：

```json
{
  "entity_type": "store_promotion | store_business_hours | store_opening_closing | store_construction_notice | store_tenant_change",

  "store_name": "...",
  "activity_text": "...",
  "discount_or_promotion": "...",

  "valid_time_text": "活动时间以门店为准",

  "observed_time_source": "midplatform_clock",
  "observed_time": 0,

  "observed_location_ref": "world_observed_where_ref",

  "expiry_policy": "short_ttl | scene_local_ttl",
  "confidence": 0.0,
  "requires_revalidation": true,

  "allowed_for_experience_enrichment": true,
  "allowed_for_task_planning": false
}
```

## Mapping rules（世界证据层约束）

### 1) 默认不用于主任务规划
- `allowed_for_task_planning=false`，对应 `world_model_policy.task_planning_impact=none | weak`（占位）。

### 2) 默认短 TTL
- 商业/活动证据：`ttl_policy=short_ttl`
- `requires_revalidation=true`

### 3) 跨源与用户确认可提升 trust_score（占位）
- 若满足任一条件，则可将 `cross_validation_status` 从 `single_source` 升级：
  - OCR+YOLO 多源一致
  - 多时间窗口重复观测一致
  - 用户明确确认“确实如此”

### 4) 复核与过期
- TTL 到期后证据进入 `stale/expired` 分支，不得继续驱动任务规划。
- 若出现冲突观测：`evidence_status=contradicted`，并触发下一次复核路径。

## Fraud & safety placeholder（欺诈风险占位）

- 对疑似欺诈信息：设置 `trust.fraud_risk_status=suspected | suspected_fraud`。
- 若疑似欺诈，`requires_user_confirmation=true` 或将 `shareable_to_hive=false`（至少占位其一）。

