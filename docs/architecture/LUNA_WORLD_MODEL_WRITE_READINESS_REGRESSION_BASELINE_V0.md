# LUNA — WorldModel Write Readiness Closure Baseline v0

## Phase

- **Phase-WorldModel-WriteReadiness-003**

## Baseline（文档基线）

本闭包以“文档/定义完整性”为基线（静态检查），允许措辞变化，但不允许删除硬约束。

## Required docs（必须存在）

- `docs/architecture/LUNA_WORLD_MODEL_WRITE_READINESS_DEFINITION_V0.md`
- `docs/architecture/LUNA_WORLD_MODEL_WRITE_LEVEL_AND_STATE_POLICY_V0.md`
- `docs/architecture/LUNA_WORLD_MODEL_WRITE_READINESS_CHECK_SCHEMA_V0.md`
- `docs/architecture/LUNA_WORLD_MODEL_CONTAMINATION_GUARD_POLICY_V0.md`
- `docs/architecture/LUNA_WORLD_MODEL_ROLLBACK_AND_REVISION_POLICY_V0.md`
- `docs/architecture/LUNA_WORLD_MODEL_WRITE_AUDIT_REQUIREMENTS_V0.md`
- `docs/architecture/LUNA_WORLD_MODEL_COMMIT_LAYER_CONTRACT_V0.md`
- `docs/architecture/LUNA_COMMITTED_WORLD_MEMORY_RECORD_SCHEMA_V0.md`
- `docs/architecture/LUNA_WORLD_MEMORY_REVISION_SEMANTICS_V0.md`
- `docs/architecture/LUNA_WORLD_MEMORY_QUARANTINE_STORE_POLICY_V0.md`
- `docs/architecture/LUNA_WORLD_MEMORY_READ_VISIBILITY_POLICY_V0.md`
- `docs/architecture/LUNA_WORLD_MODEL_COMMIT_AUDIT_ENVELOPE_V0.md`
- `docs/architecture/LUNA_PROVISIONAL_WRITE_AND_SUSPICION_FIRST_COMMIT_POLICY_V0.md`

## Hard gates（不允许波动）

- 缺 provisional-first（占位优先、事实提交滞后）
- 缺 rollback/revision/contamination/audit/read_visibility/quarantine 任一核心机制
- 允许真实写入/上传蜂巢/推荐/导航/TTS/下游执行
- 允许覆盖式更新（无 revision 记录）
- 允许 quarantined 可任务读取
- 允许未通过 WriteReadinessCheck 也能 commit

## Allowed fluctuations（允许波动）

- 文档措辞与组织结构
- schema 字段顺序
- future branches 顺序

