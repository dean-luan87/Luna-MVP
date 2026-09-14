# LUNA — MapAnchorEvidence Schema v0

## Phase

- **Phase-WorldModel-MapAnchor-001**

## Purpose

定义 `MapAnchorEvidence`：Map / GPS / POI 作为空间锚点来源的候选证据对象（candidate-only）。

## Schema（v0）

```json
{
  "map_anchor_evidence_id": "map_anchor_001",
  "candidate_only": true,

  "source_type": "gps | map_poi | offline_map | indoor_map | user_corrected_location | visual_map_alignment | unknown",

  "observed_at": {
    "timestamp_ms": 0,
    "time_source": "midplatform_clock | gps_time | system_clock | unknown"
  },

  "location": {
    "geo_location": {
      "lat": null,
      "lng": null,
      "accuracy_m": null
    },
    "altitude_m": null,
    "floor_level": null,
    "heading_deg": null,
    "speed_mps": null
  },

  "poi_context": {
    "poi_id": null,
    "poi_name": null,
    "poi_type": null,
    "building_id": null,
    "road_segment_id": null,
    "entrance_id": null,
    "indoor_zone_id": null,
    "distance_to_poi_m": null,
    "poi_confidence": 0.0
  },

  "spatial_scope": {
    "scope_type": "point | region | route_segment | indoor_zone | storefront | building | unknown",
    "radius_m": null,
    "polygon_ref": null,
    "scope_confidence": 0.0
  },

  "anchor_status": "bound | weakly_bound | unresolved | contradicted | stale",

  "spatial_anchor_grade": "grade_A_precise_bound | grade_B_probable_bound | grade_C_weak_bound | grade_D_unresolved | grade_E_contradicted",

  "freshness": {
    "observed_at": 0,
    "source_updated_at": null,
    "ttl_policy": "gps_short | poi_medium | indoor_map_versioned | user_correction_requires_validation",
    "expires_at": null,
    "requires_revalidation": true
  },

  "trust": {
    "gps_confidence": 0.0,
    "map_confidence": 0.0,
    "poi_confidence": 0.0,
    "cross_validation_status": "single_source | visual_confirmed | user_confirmed | contradicted | unknown"
  },

  "source_attribution": {
    "provider": "unknown | amap | apple_map | offline_map | user | local_cache",
    "provider_version": null,
    "query_ref": null,
    "raw_response_ref": null
  },

  "governance": {
    "navigation_action": null,
    "recommendation_invoked": false,
    "world_model_write_invoked": false,
    "hive_upload_invoked": false,
    "real_tts_invoked": false
  },

  "trace_ref": "...",
  "replay_ref": "...",
  "whitebox_ref": "..."
}
```

## Hard rules（强制）

- `candidate_only=true`
- 无 gps 输入不得填 `lat/lng`（no fabricated GPS）
- 不得产生 `navigation_action`
- 不得写世界模型（world_model_write_invoked=false）
- POI/地图信息只能作为“定位锚点候选”，不得当作现场事实

