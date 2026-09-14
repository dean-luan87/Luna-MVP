# LUNA — World Model Write Audit Requirements v0

## Phase

- **Phase-WorldModel-WriteReadiness-001**

## Purpose

定义每一次写入评估（WriteReadinessCheck）必须记录的审计字段，以支持：

- 回放（replay）
- 复核（review）
- 回滚（rollback）
- 防污染（contamination guard）

本阶段只定义，不实现 runtime/写入。

## Audit record must include（必须包含）

- `write_readiness_check_id`
- `source_world_context_evidence_id`
- `requested_write_level`
- `allowed_write_level`
- `write_readiness_status`
- `decision_reason`
- `hard_blockers`
- `soft_followups`
- `source_reference_chain`
- `trust_score`
- `lifecycle_status`
- `contamination_guard_result`（reject/quarantine/downgrade/...）
- `rollback_policy_ref`（对应回滚策略/记录占位）
- `trace_ref`
- `replay_ref`
- `whitebox_ref`

## Non-governance boundary（再次强调）

- 不做真实写入
- 不上传蜂巢
- 不接推荐/导航/TTS

