# LUNA — World Context Spatiotemporal & Trust Evidence Contract v0

## Phase

- Phase-WorldModel-ContextEvidence-001

## Purpose

定义 Luna **世界上下文证据（WorldContextEvidence）** 的统一合同：
- 时间（observed_at）
- 空间（observed_where / spatial_anchor）
- 信任与验证状态（trust）
- 生命周期与有效期（lifecycle）
- 写入与共享策略（world_model_policy / share_policy / privacy_policy）

核心原则：世界模型不是“我见过什么”的日志，而是一个“可过期、可复核、可对比变化、可共享”的动态证据层。

参照：`LUNA_MIDPLATFORM_TO_WORLD_CONTEXT_FIELD_MAPPING_V0.md`（字段口径对齐映射）

## Non-governance boundary

- 不实现 runtime：只定义字段与合规规则。
- 不接真实世界模型写入。
- 不接推荐/任务执行/导航动作。
- 不做最终语义提炼或实时播报。

## WorldContextEvidence（主 schema）

```json
{
  "world_context_evidence_id": "world_ctx_001",

  "source_modalities": ["yolo", "ocr"],
  "source_evidence_refs": ["ocr_evidence_001", "yolo_detection_001"],

  "observed_at": {
    "timestamp_ms": 0,
    "time_source": "midplatform_clock",
    "date_confidence": "system_confirmed"
  },

  "observed_where": {
    "geo_location": {
      "lat": null,
      "lng": null,
      "accuracy_m": null
    },
    "place_hint": "某商场一楼",
    "spatial_anchor_type": "gps | map_poi | visual_landmark | indoor_scene | unknown",
    "relative_position": {
      "distance_estimate_m": null,
      "direction_hint": null
    }
  },

  "content": {
    "text": "第二杯半价",
    "entity_type": "store_promotion",
    "entity_name": "星巴克",
    "details": "第二杯半价",
    "valid_time_text": "活动时间以门店为准",
    "extracted_from": "ocr_raw_text"
  },

  "trust": {
    "source_confidence": 0.82,
    "ocr_confidence": 0.76,
    "yolo_confidence": 0.81,
    "cross_validation_status": "single_source | multi_source_confirmed | contradicted | expired | unknown",
    "trust_score": 0.62,
    "fraud_risk_status": "unknown | suspected | verified_safe | suspected_fraud"
  },

  "lifecycle": {
    "evidence_status": "active | stale | expired | contradicted | superseded",
    "ttl_policy": "short_ttl | scene_local_ttl | persistent_requires_revalidation",
    "expires_at": null,
    "requires_revalidation": true,
    "last_seen_at": 0,
    "seen_count": 1
  },

  "world_model_policy": {
    "write_policy": "low_priority_candidate",
    "task_planning_impact": "none | weak | medium | strong",
    "shareable_to_hive": false,
    "requires_user_confirmation": false
  },

  "trace_ref": "...",
  "whitebox_ref": "..."
}
```

## Must-have invariants（必须满足的契约约束）

1) 时空锚点必须存在
- `observed_at.timestamp_ms` 必须可追溯到 MidPlatform clock 或明确的时间来源。
- `observed_where.spatial_anchor_type` 必须存在；`place_hint` 至少为可读文本占位。

2) Trust 与验证状态必须存在
- `trust.trust_score` 必须存在（即使是占位值，也必须记录）。
- `trust.cross_validation_status` 必须可解释其“来自单源/多源/冲突/过期/未知”的状态。

3) 生命周期与有效期必须存在
- `lifecycle.ttl_policy` 必须显式记录。
- 商业/活动类证据默认短 TTL，并设置 `requires_revalidation=true`。
- `lifecycle.evidence_status` 必须能从后续观察更新到 expired/contradicted/superseded。

4) 共享与隐私策略必须存在
- `world_model_policy.shareable_to_hive` 必须明确。
- `requires_user_confirmation` 必须明确（防止未确认的广告/欺诈信息扩散）。

5) 证据必须可审计
- 必须带 `trace_ref/whitebox_ref` 用于追溯来源与验证依据。

