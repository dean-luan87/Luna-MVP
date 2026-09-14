# LUNA — CommittedWorldMemoryRecord Schema v0

## Phase

- **Phase-WorldModel-WriteReadiness-002**

## Purpose

定义未来写入世界模型后持久对象的最小结构：`CommittedWorldMemoryRecord`。

本阶段只定义，不实现写入。

## Schema（v0）

```json
{
  "world_memory_id": "wm_0001",

  "source_world_context_evidence_id": "world_ctx_0001",
  "source_write_readiness_check_id": "wrc_0001",

  "memory_type": "text_context | commercial_activity | world_change | ambient_context | visual_symbol | unknown",
  "memory_scope": "scene_local | persistent",

  "spatiotemporal_binding": {
    "observed_at": {
      "first_observed_at": null,
      "last_observed_at": null,
      "valid_from": null,
      "valid_until": null,
      "time_source": "midplatform_clock | gps_time | system_clock | unknown",
      "temporal_confidence": 0.0
    },
    "observed_where": {
      "spatiotemporal_anchor_ref": null,
      "spatial_anchor_type": "visual_landmark | map_poi | gps | indoor_scene | unknown",
      "geo_location": null,
      "place_hint": null,
      "relative_position": null,
      "spatial_signature": null,
      "carrier_signature": null,
      "spatial_confidence": 0.0
    },
    "scope": {
      "scope_type": "point | region | route_segment | indoor_zone | storefront | poster_board | unknown",
      "scope_confidence": 0.0
    },
    "binding_status": "bound | weakly_bound | unresolved | expired | contradicted",
    "requires_revalidation": true
  },

  "content": {
    "canonical_text": null,
    "structured_payload": null,
    "raw_refs": []
  },

  "observed_at": {},
  "observed_where": {},

  "trust": {},
  "lifecycle": {},

  "revision_state": {
    "revision_status": "active | superseded | expired | contradicted | quarantined | rollback_required",
    "current_revision_id": "rev_0001",
    "previous_revision_id": null
  },

  "read_visibility": {
    "visibility": "task_readable | weak_readable | audit_only | hidden",
    "forbidden_consumers": ["recommendation", "tts", "navigation_output"]
  },

  "rollback_policy": {
    "rollback_supported": true,
    "rollback_required_on": ["contradicted", "fraud_risk", "source_invalid", "policy_violation"]
  },

  "audit_refs": {
    "commit_audit_envelope_id": "commit_0001",
    "trace_ref": "...",
    "replay_ref": "...",
    "whitebox_ref": "..."
  }
}
```

## Hard rules

- 必须引用 `source_write_readiness_check_id`
- 必须保留 `source_world_context_evidence_id`
- committed memory **不允许缺** `spatiotemporal_binding`
- 缺 `observed_where`：只能进入 provisional / audit_only，不能 committed
- 缺 `observed_at`：只能进入 audit_only 或 rejected
- `spatial_anchor_type=unknown`：不能进入 `committed_persistent`（最多 scene_local/provisional）
- 商业活动必须有 `valid_from/valid_until` 或短 TTL（short_ttl）策略
- 不允许没有审计 envelope 的 committed record
- `commercial_activity` 默认不允许进入 `persistent + task_readable`

