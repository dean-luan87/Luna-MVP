# LUNA — World Model Rollback & Revision Policy v0

## Phase

- **Phase-WorldModel-WriteReadiness-001**

## Purpose

定义写入后的回滚/修订机制（只定义，不实现写入）：

- 写入必须可回滚
- 回滚不是删除，而是**状态迁移** + **保留 previous_state**
- 冲突证据不得直接覆盖，只能触发 `rollback_required / revalidation / quarantine`

## Rollback record schema（v0）

```json
{
  "rollback_record_id": "rollback_001",
  "target_world_memory_ref": "...",
  "rollback_reason": "expired | contradicted | superseded | fraud_risk | source_invalid | user_correction | policy_violation",
  "trigger_evidence_ref": "...",
  "previous_state": "...",
  "new_state": "expired | superseded | quarantined | reverted",
  "requires_revalidation": true,
  "trace_ref": "...",
  "whitebox_ref": "..."
}
```

## Principles（硬约束）

1. 回滚必须可审计：保留触发证据引用与原因
2. 回滚必须可追溯：保留 previous_state（不可“直接抹除”）
3. 回滚必须可复核：回滚后的对象默认 `requires_revalidation=true`
4. 冲突处理：不允许“新证据直接覆盖旧事实”，只能触发：
   - `contradicted` → `rollback_required` 或 `quarantined`

