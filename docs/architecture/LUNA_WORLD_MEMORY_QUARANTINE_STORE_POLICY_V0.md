# LUNA — World Memory Quarantine Store Policy v0

## Phase

- **Phase-WorldModel-WriteReadiness-002**

## Purpose

定义隔离区对象与语义：对疑似污染/欺诈/冲突/来源缺失的证据与已写入对象进行隔离，防止其被任务/推荐/播报消费。

本阶段只定义，不实现 runtime。

## Quarantine reasons（分类）

- `suspected_fraud`
- `contradicted`
- `missing_source_chain`
- `unconfirmed_symbol`
- `metaphor_as_fact`
- `low_confidence_pollution`
- `fabricated_anchor_risk`

## QuarantineWorldEvidenceRecord（v0）

```json
{
  "quarantine_id": "q_0001",
  "source_world_context_evidence_id": "world_ctx_0007",
  "source_write_readiness_check_id": "wrc_0007",
  "target_world_memory_ref": "wm_0001",
  "quarantine_reason": "suspected_fraud",
  "status": "quarantined | released | expired",
  "read_visibility": "hidden",
  "allowed_consumers": ["audit", "human_review"],
  "forbidden_consumers": ["task", "recommendation", "tts", "navigation_output"],
  "requires_multi_source_validation": true,
  "requires_user_confirmation": false,
  "audit_refs": {
    "commit_audit_envelope_id": "commit_0007",
    "trace_ref": "...",
    "whitebox_ref": "..."
  }
}
```

## Hard rules（强制）

- 隔离区默认 **不可任务读取**、不可推荐、不可播报
- 隔离解除必须通过多源验证/人工复核（后续阶段实现）

