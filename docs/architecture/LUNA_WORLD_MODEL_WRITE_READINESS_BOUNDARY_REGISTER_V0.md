# LUNA — WorldModel Write Readiness Boundary Register v0

## Phase

- **Phase-WorldModel-WriteReadiness-003**

## Purpose

登记并冻结 WriteReadiness / Commit Layer 定义层的硬禁止项，防止“定义阶段”误触 runtime 或越权写入。

## Hard boundaries（强制禁止）

- 不实现 runtime
- 不真实写入世界模型（commit layer 仅合同）
- 不上传蜂巢
- 不接推荐系统
- 不执行导航动作
- 不真实播报
- 不进入 SceneTask/Fusion/Output

## Governance invariants（关键底线）

- candidate ≠ fact
- 通过 WriteReadinessCheck ≠ committed fact
- 默认 `provisional_world_memory`（占位优先、事实提交滞后）
- 修订不是覆盖（append-only revision）
- 回滚不是删除（state transition + audit）
- 隔离区默认不可任务读取
- 未通过 WriteReadinessCheck 不得 commit

