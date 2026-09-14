# LUNA — WorldModel Commit Layer Contract v0

## Phase

- **Phase-WorldModel-WriteReadiness-002**

## Purpose

定义未来“真正写入世界模型”的 Commit Layer 的输入/输出合同、边界与修订语义承载对象。

本阶段只定义，不实现 runtime、不执行真实写入。

## Non-governance boundary（强制）

- 不实现 runtime
- 不真实写入世界模型
- 不上传蜂巢
- 不接推荐系统
- 不执行导航动作
- 不真实播报
- 不进入 SceneTask/Fusion/Output

## Positioning（分层定位）

- SceneDelta：判断变化，不写世界模型
- WorldContextEvidence（ContextEvidence-closed_v0）：生成候选，不写世界模型
- WriteReadiness：判断是否具备写入资格，仍不写世界模型
- **Commit Layer**：未来真实写入层（本阶段只定义合同）

## Inputs（只允许的输入）

Commit Layer 未来只消费：

- 已通过 `WriteReadinessCheck` 的 evidence（`allowed_write_level != no_write` 且非 quarantine/rejected）
- 以及明确的 `operation_request`（create/update/supersede/expire/rollback/quarantine/restore）

禁止：

- 未经过 WriteReadinessCheck 的 candidate 直接 commit

## Outputs（对象）

Commit Layer 的对象输出（schema 在各文档定义）：

- `CommittedWorldMemoryRecord`
- `WorldMemoryRevisionRecord`
- `QuarantineWorldEvidenceRecord`
- `CommitAuditEnvelope`

## Core invariants（硬约束）

- 修订不是覆盖：必须追加版本，并保留 previous_state/ref
- 回滚不是删除：必须状态迁移 + 可审计
- 隔离默认不可用于任务读取/推荐/播报
- 所有 commit/revision/rollback 必须有 audit envelope（trace/replay/whitebox 可追溯）

## Default principle（默认原则：占位优先、事实提交滞后）

即使通过了 `WriteReadinessCheck`，也不代表可以直接写成“世界事实/稳定记忆”。

Commit Layer 默认策略应为：

1. **先占位（provisional）**
2. **再标疑（suspicion-first）**
3. **再复核（multi-source / repeated observation / user confirmation / time recheck）**
4. **再升级（verified scene-local）**
5. **最后才持久（persistent stable memory）**

对应的默认状态链（概念性）：

`candidate_only → write_evaluation_pending → provisional_world_memory → verified_scene_local_memory → persistent_world_memory`

