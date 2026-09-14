# LUNA — WorldModel Commit Layer Contract Go/No-Go Pack v0

## Phase

- **Phase-WorldModel-WriteReadiness-002**

## GO conditions（必须）

- Commit Layer 定位、输入/输出与边界清晰（只定义，不写入）
- `CommittedWorldMemoryRecord` schema 完整
- revision semantics 完整（追加版本、保留 previous_state、冲突不覆盖）
- quarantine store policy 完整（默认不可任务读取）
- read visibility policy 完整（task/weak/audit_only/hidden）
- commit audit envelope 完整（每次操作可审计）
- 与 WriteReadiness-001 的接口关系清晰：**未通过 WriteReadinessCheck 不得 commit**
- 默认原则明确：占位优先、事实提交滞后（provisional → verified → persistent）
- 明确本阶段不实现 runtime、不写真实世界模型、不上传蜂巢、不推荐、不导航、不播报

## NO_GO（任意一条）

- 允许覆盖式更新（无 revision 记录）
- 无 rollback 机制或无状态迁移语义
- quarantined evidence 可被任务直接读取
- provisional 被当作 verified/persistent 事实使用（越权消费）
- 未通过 WriteReadinessCheck 也能 commit
- 本阶段实现真实写入/蜂巢上传/推荐/导航/TTS/下游执行

