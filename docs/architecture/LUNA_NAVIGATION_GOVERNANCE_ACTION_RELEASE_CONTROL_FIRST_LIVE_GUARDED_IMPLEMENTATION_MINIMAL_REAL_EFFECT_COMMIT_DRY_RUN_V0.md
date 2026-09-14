# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Commit Dry-Run v0（最终 commit 放行后干跑层：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_COMMIT_DRY_RUN_V0.md`  
**性质**：Phase-Next-108：冻结 `minimal real-effect` 在 `commit_admission_status == commit_admitted` 之后、真实最小写入实现之前的 **最终 commit 级干跑层（commit dry-run）**（只预演、不执行；可冻结、可回归）

基于（已具备）：
- admission gate implementation（已具备）
- guarded launch dry-run implementation（已具备）
- guarded launch gate implementation（已具备）
- pre-commit dry-run implementation（已具备）
- commit gate implementation（已具备）
- implementation definition / skeleton / wiring / implementation dry-run execution（已具备）
- standard objects：`execution_state_v0` / `result_v0`

---

## 1. 文档定位（写死）

这份文档定义：

- `release_control first live guarded implementation minimal real-effect` 在 **commit gate 通过之后**、进入第一版真实最小写入实现之前的 **最终 commit 级 dry-run 层**。
- 当前目标：冻结“最终 commit 放行后、真实写入前最后一次按真实提交顺序预演但不落真实副作用”的边界：输入是什么、输出是什么、不能做什么、与相邻层如何区分。

并且（本轮写死边界）：

- 当前不做真实写入。
- 当前不做真实 `release_control`。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不触发中台真实迁移。
- 当前不改变现有主线行为。
- 当前 `side_effects_released` 仍强制锁死为 `false`（不允许打开）。

---

## 2. 为什么现在必须先定义 commit dry-run（写死理由）

- commit gate implementation 已存在，系统已经可以产出 `first_live_minimal_real_effect_commit_admitted`。
- 如果没有 commit dry-run，后续链路很容易从 `commit_admitted` **直接跳到** 真实最小写入实现。
- 这会缺失：最终放行后、真实写入前最后一次“按真实提交顺序预演”的统一承载位，以及失败如何保守收口的标准化出口。

因此必须先冻结并尽量实现 commit 级最后一次顺序预演检查层，但当前仍不能触发任何真实治理动作与副作用。

---

## 3. 最小定义（写死）

`minimal real-effect commit dry-run` 是：

- commit gate 之后、真实第一版最小写入实现之前的最终 commit 级干跑层
- 只负责检查是否具备最后 commit 预演条件，并产出统一结果对象

它不是：

- commit gate 本身
- pre-commit dry-run 本身
- 真实写入器本身
- rollback / interrupt 层

核心定义（写死一句）：

> commit dry-run 只做“commit 放行后进入真实写入前的最后一次干跑预演”，不执行任何真实写入，也不打开 `side_effects_released`。

---

## 4. 最小合法输入（写死；只允许标准化对象）

commit dry-run 只允许消费（只读）：

- `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0`
  - 必须 `commit_admission_status == "first_live_minimal_real_effect_commit_admitted"`
- `first_live_guarded_implementation_minimal_real_effect_admission_gate_v0`
  - 必须 admitted
- `first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0`
  - 必须 launch_admitted
- `first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0`
  - 必须 pre_commit_ready
- `first_live_enablement_approval_gate_v0` / `first_live_launch_dry_run_v0` / `live_release_gate_v0` / `side_effect_release_gate_v0`
  - 仍必须 ready/approved
- `first_live_guarded_implementation_dry_effect_simulation_v0`
  - 必须 simulated
- `first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0`
  - 必须 executed
- `implementation skeleton identity / capability`
  - 必须在位且仍为 conservative / dry-run mode
- `execution_state_v0` 与 `result_v0`
  - 回传面在位
- `side_effects_released`
  - 必须仍为 `false`

并明确（写死）：

- 缺任一主前提，commit dry-run 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata`。

---

## 5. 最小结果集合（写死；三态）

commit dry-run 的结果必须收敛成最小集合：

- `first_live_minimal_real_effect_commit_ready`
- `first_live_minimal_real_effect_commit_not_ready`
- `first_live_minimal_real_effect_commit_blocked`

语义（写死）：

- `commit_ready`：仅表示 commit 放行后，系统具备最后一次进入真实最小写入前的干跑条件  
  不表示真实写入已开始、不表示副作用已发生、不表示 `side_effects_released == true`
- `commit_not_ready`：条件未满足或上游未通过
- `commit_blocked`：硬阻断 / 身份问题 / 一致性问题（保守阻断）

---

## 6. 明确禁止（写死）

commit dry-run 不允许直接：

- 打开 `side_effects_released`
- 执行真实 `release_control`
- 执行真实写入
- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback` / `interrupt`
- 越过标准对象吐散字段

---

## 7. 与现有链路的关系（写清；不能混用）

与 commit gate：

- commit gate 负责最终 commit 放行（`commit_admitted|not_admitted|blocked`）
- commit dry-run 负责放行后的最后一次顺序预演（`commit_ready|not_ready|blocked`）
- `commit_admitted != commit_ready`

与 pre-commit dry-run：

- pre-commit dry-run 负责最终放行前检查
- commit dry-run 负责最终放行后的最后干跑
- 两者不能混用

与 implementation definition / plan：

- definition 定边界
- plan 定真实写入策略
- commit dry-run 只做“进入真实写入前最后一次干跑”，不替代 definition / plan

---

## 8. 当前仍然不能做什么（写死）

- 不允许把 `side_effects_released` 打开
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 `commit_ready` 当作真实写入已开始

---

## 9. 当前不做（写死）

- 不做 commit dry-run 代码实现
- 不做真实最小写入实现
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 10. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - minimal real-effect commit dry-run 的 minimal implementation
- 再之后才考虑：
  - 第一版最小真实写入实现方案
- 当前不直接落真实实现

