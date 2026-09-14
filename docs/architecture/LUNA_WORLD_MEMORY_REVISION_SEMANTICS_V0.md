# LUNA — World Memory Revision Semantics v0

## Phase

- **Phase-WorldModel-WriteReadiness-002**

## Purpose

定义世界记忆的修订语义：**修订不是覆盖，而是追加版本**。

本阶段只定义，不实现 runtime。

## Operations（v0）

- `create`
- `update`
- `supersede`
- `expire`
- `contradict`
- `rollback`
- `quarantine`
- `restore`

## Rules（硬约束）

1. **追加版本**：每次变更必须生成 `WorldMemoryRevisionRecord`，并链接 previous_revision
2. **保留旧版本**：旧版本不可删除，至少保留 `previous_state_ref` 与触发证据
3. **冲突不覆盖**：`contradict` 只能触发 `rollback_required` / `quarantine` / `requires_revalidation`
4. **回滚不删除**：`rollback` 必须生成新的 revision，将状态迁移为 `reverted/superseded/expired/quarantined` 之一
5. **隔离优先**：疑似污染/欺诈/来源链缺失/伪造锚点 → `quarantine`
6. **时空绑定约束**：
   - revision/supersede/rollback 必须在 **同一** 或 **可证明相关** 的 `spatiotemporal_anchor_ref` 下发生
   - `content_replaced/content_removed` 必须引用同一 `spatiotemporal_anchor_ref` 的 carrier/anchor（避免 A 板内容误写到 B 板）
   - rollback/supersede 必须携带 `spatiotemporal_binding_snapshot`（用于审计与回放）

## WorldMemoryRevisionRecord（v0）

```json
{
  "revision_id": "rev_0002",
  "world_memory_id": "wm_0001",
  "operation_type": "update",

  "trigger_evidence_ref": "world_ctx_0009",
  "write_readiness_check_ref": "wrc_0009",

  "spatiotemporal_anchor_ref": "sta_...",
  "spatiotemporal_binding_snapshot_ref": "binding_snapshot_0002",

  "previous_revision_id": "rev_0001",
  "new_revision_snapshot_ref": "wm_snapshot_0002",

  "reason": "...",
  "policy_version": "WriteReadiness-001",

  "audit_refs": {
    "commit_audit_envelope_id": "commit_0009",
    "trace_ref": "...",
    "replay_ref": "...",
    "whitebox_ref": "..."
  }
}
```

