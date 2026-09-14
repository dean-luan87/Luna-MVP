# LUNA — WorldModel Commit Audit Envelope v0

## Phase

- **Phase-WorldModel-WriteReadiness-002**

## Purpose

定义每次 commit / revision / rollback / quarantine 操作必须记录的“审计信封”（envelope），确保未来真实写入可回放、可复核、可回滚。

本阶段只定义，不实现 runtime。

## CommitAuditEnvelope（v0）

```json
{
  "commit_id": "commit_0001",
  "operation_type": "create | update | supersede | expire | contradict | rollback | quarantine | restore",

  "source_evidence_ref": "world_ctx_0001",
  "write_readiness_check_ref": "wrc_0001",

  "previous_memory_ref": null,
  "new_memory_ref": "wm_0001",

  "spatiotemporal_binding_snapshot": {
    "spatiotemporal_anchor_ref": null,
    "spatial_signature": null,
    "carrier_signature": null,
    "valid_from": null,
    "valid_until": null,
    "binding_status": "bound | weakly_bound | unresolved | expired | contradicted"
  },

  "decision_reason": "...",
  "operator": "system | human_review | user_feedback",
  "policy_version": "WriteReadiness-001",

  "trace_ref": "...",
  "replay_ref": "...",
  "whitebox_ref": "..."
}
```

## Hard rules

- 所有操作必须有 envelope
- `operator` 必须明确（系统/人工/用户反馈）
- `policy_version` 必须可追溯
- committed/revision/rollback 必须记录 `spatiotemporal_binding_snapshot`（避免世界事实错位）

