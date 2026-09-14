# LUNA — Scene Delta Input and State Contract v0

## Phase

- **Phase-MidPlatform-SceneDelta-001**

## Purpose

冻结 Scene Delta 的输入对象 `SceneDeltaInput` 与历史状态对象 `SceneProcessedState` 的 contract（schema v0）。

本阶段只定义，不实现。

## SceneDeltaInput（冻结 schema）

```json
{
  "delta_input_id": "scene_delta_input_001",
  "input_type": "ocr_evidence | yolo_detection | yolo_ocr_bridge_result | world_context_candidate | ambient_context_candidate | visual_symbol_candidate",
  "source_evidence_id": "...",
  "frame_id": "...",
  "timestamp_ms": 0,
  "source_frame_window_id": "...",

  "spatiotemporal_anchor": {
    "observed_at": { "timestamp_ms": 0, "time_source": "unknown", "date_confidence": "unknown" },
    "observed_where": {
      "geo_location": { "lat": null, "lng": null, "accuracy_m": null },
      "place_hint": "unknown",
      "spatial_anchor_type": "unknown",
      "relative_position": { "distance_estimate_m": null, "direction_hint": null }
    }
  },

  "spatiotemporal_delta_anchor_ref": null,

  "source_attribution": { "source": "unknown", "provider_id": null, "pipeline_stage": "scene_delta", "notes": null },

  "content_signature": {
    "text_signature": null,
    "object_signature": null,
    "layout_signature": null,
    "crop_signature": null,
    "symbol_signature": null,
    "scene_signature": null
  },

  "content_payload_ref": "...",

  "confidence": {
    "source_confidence": 0.0,
    "modality_confidence": 0.0,
    "trust_score": 0.0
  },

  "candidate_only": true,
  "allows_execute_now": false
}
```

### Contract invariants（必须满足）

- `candidate_only=true`
- `allows_execute_now=false`
- `source_attribution` 必须存在（缺失视为治理越界输入）
- `content_payload_ref` 必须存在（否则不可 replay/复核）

## SceneProcessedState（冻结 schema）

```json
{
  "state_id": "scene_state_001",
  "state_scope": "frame_window | spatial_region | task_context | world_context",
  "source_evidence_refs": [],
  "last_processed_at": 0,
  "last_seen_at": 0,
  "seen_count": 1,

  "spatiotemporal_delta_anchor_ref": null,

  "signatures": {
    "text_signature": null,
    "object_signature": null,
    "layout_signature": null,
    "crop_signature": null,
    "symbol_signature": null,
    "scene_signature": null
  },

  "last_delta_decision": "reuse_previous | ignore_duplicate | partial_update | full_reprocess | hold_uncertain | expire_and_reprocess | block",

  "last_output_refs": {
    "text_candidate_ref": null,
    "world_context_ref": null,
    "ambient_candidate_ref": null,
    "filter_result_ref": null
  },

  "ttl_policy": "short_ttl | scene_local_ttl | persistent_requires_revalidation",
  "expires_at": null,
  "requires_revalidation": true
}
```

## RepeatedEvidenceCompression linkage（主机制引用）

为支持“重复证据压缩 / 增量存储”，Scene Delta 的 state 必须允许引用压缩记录（实现阶段可选字段；本阶段仅冻结接口）：

- `compression_record_ref`（可选）：指向 `RepeatedEvidenceCompression.compression_record_id`

参照：

- `LUNA_SCENE_DELTA_REPEATED_EVIDENCE_COMPRESSION_POLICY_V0.md`

### State invariants（必须满足）

- `requires_revalidation=true` 为默认（除非未来定义 user_confirmed_write 分支）
- `source_evidence_refs` 保留可追责引用（不可删除）

## SpatiotemporalDeltaAnchor linkage（主机制引用）

为支持“同一空间载体上的内容演替/下架/替换”，Scene Delta 需要显式引用：

- `spatiotemporal_delta_anchor_ref`（指向 `SpatiotemporalDeltaAnchor.spatiotemporal_anchor_id`）

该引用不得被当作真实世界模型写入，仅用于增量分流与变化分析候选。

参照：

- `LUNA_SCENE_DELTA_SPATIOTEMPORAL_ANCHOR_POLICY_V0.md`

