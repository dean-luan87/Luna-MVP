# LUNA — WriteReadinessCheck Schema v0

## Phase

- **Phase-WorldModel-WriteReadiness-001**

## Purpose

定义 `WriteReadinessCheck` 的结构化检查记录：它是写入评估的“审计对象”，用于回放、复核、回滚与防污染。

本阶段只定义，不实现 runtime。

## Schema（v0）

```json
{
  "write_readiness_check_id": "wrc_001",
  "source_world_context_evidence_id": "world_ctx_0001",
  "candidate_only": true,

  "input_evidence_type": "text_context | commercial_activity | world_change | ambient_context | visual_symbol | unknown",

  "anchor_check": {
    "has_observed_at": true,
    "has_observed_where": true,
    "has_spatial_anchor": true,
    "spatial_anchor_type": "visual_landmark | map_poi | gps | indoor_scene | unknown",
    "anchor_status": "present | missing_or_unresolved",
    "spatial_anchor_confidence": 0.0,
    "no_fabricated_gps": true
  },

  "spatiotemporal_binding_check": {
    "has_observed_at": true,
    "has_observed_where": true,
    "has_temporal_scope": true,
    "has_spatial_scope": true,
    "binding_status": "bound | weakly_bound | unresolved | expired | contradicted",
    "binding_confidence": 0.0,
    "allowed_world_memory_level": "no_write | audit_only | provisional_world_memory | scene_local_memory | persistent_world_memory"
  },

  "source_check": {
    "source_evidence_refs_non_empty": true,
    "source_reference_chain_present": true,
    "source_ref_integrity_status": "complete | partial | broken"
  },

  "trust_check": {
    "trust_score": 0.0,
    "cross_validation_status": "single_source | multi_source_confirmed | contradicted | unknown",
    "fraud_risk_status": "unknown | suspected | suspected_fraud | verified_safe"
  },

  "lifecycle_check": {
    "ttl_policy": "short_ttl | scene_local_ttl | persistent_requires_revalidation | no_persistent_write",
    "requires_revalidation": true,
    "evidence_status": "active_candidate | expired_candidate | uncertain_candidate | contradicted_candidate"
  },

  "policy_check": {
    "requested_write_level": "no_write | audit_only | ephemeral_scene_cache | scene_local_memory | persistent_world_candidate | committed_world_memory | quarantine_store",
    "allowed_write_level": "no_write",
    "requires_user_confirmation": false,
    "requires_multi_source_validation": false,
    "requires_human_review": false
  },

  "decision": {
    "write_readiness_status": "not_ready | ready_low_priority | ready_scene_local | ready_persistent_candidate | rejected | quarantine",
    "decision_reason": "...",
    "hard_blockers": [],
    "soft_followups": []
  },

  "audit": {
    "trace_ref": "...",
    "replay_ref": "...",
    "whitebox_ref": "..."
  }
}
```

## Hard rules（v0 约束）

- `candidate_only` 必须为 true（WriteReadiness-001 不接真实写入）
- `source_evidence_refs_non_empty=false` → 必须 `rejected`
- `no_fabricated_gps=false` → 必须 `quarantine` 或 `rejected`
- `has_observed_at=false` → 只能 `audit_only` 或 `rejected`
- `has_observed_where=false` → 不得进入事实世界模型层（最多 provisional/audit_only）
- `commercial_activity` 不得 `committed_world_memory`
- `visual_symbol` 未确认含义不得进入事实写入等级
- `metaphorical/emotional` 用户反馈不得进入事实写入等级（参见 Human Interaction Validation Layer）

