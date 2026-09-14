# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Activation Dry-Run v0（最终 activation 级零副作用演练层：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_DRY_RUN_V0.md`  
**性质**：Phase-Next-112：冻结 `minimal real-effect` 在 `activation_admission_status == activation_admitted` 之后、真实最小写入实现之前的 **最终 activation 级零副作用演练层（activation dry-run）**（只演练、不执行；可冻结、可回归）

基于（已具备）：
- activation gate implementation（已具备）
- activation contract（冻结）
- commit gate / commit dry-run / pre-commit / launch / admission 链路（冻结 + 最小实现）
- implementation definition / skeleton / wiring / implementation dry-run execution（冻结 + 最小实现）
- standard objects：`execution_state_v0` / `result_v0`

---

## 1. 文档定位（写死）

这份文档定义：

- `release_control first live guarded implementation minimal real-effect` 的最终 **activation 级零副作用演练层**。
- 当前目标：冻结“从 activation gate 到第一版真实最小写入实现”的最后 activation dry-run 边界：演练前必须满足什么、演练结果是什么、演练本身不能做什么。

并且（本轮写死边界）：

- 当前不做真实代码实现（不落 activation dry-run minimal implementation）。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。
- 当前 `side_effects_released` 仍强制锁死为 `false`（不允许打开）。

---

## 2. 为什么现在必须先定义 activation dry-run（写死理由）

- 当前已经有 activation gate implementation。
- 当前已经有 activation contract（定义未来唯一允许的 side effects 受控激活范围与顺序）。
- 但还没有一个明确的“activation 放行之后、真实写入之前的最后零副作用演练层”。
- 如果不先定义 activation dry-run，后续很容易把 `activation_admitted` 误当成可以直接进入真实写入，造成缺失最后一次 activation 级干跑与失败收口承载位。

因此必须先冻结最后 activation dry-run，再考虑是否真的进入第一版最小真实写入实现。

---

## 3. activation dry-run 的最小定义（写死）

`release_control first live guarded implementation minimal real-effect activation dry-run` 是：

- activation gate 之后、真实第一版最小写入实现之前的最后 activation 级零副作用演练层
- 只负责判断“是否具备进入真实最小写入实现前的最后 activation 级演练条件”

它不是：

- activation gate 本身
- activation contract 本身
- commit dry-run 本身
- 真实执行器本身
- rollback / interrupt 演练层

核心定义（写死一句）：

> activation dry-run 只决定“是否具备进入真实最小写入实现前的最后 activation 级演练条件”，不直接执行任何真实动作，也不直接打开 `side_effects_released`。

---

## 4. 最小合法输入（写死；只允许标准化对象）

activation dry-run 只允许消费（只读）：

- `first_live_guarded_implementation_minimal_real_effect_admission_gate_v0`（必须 admitted）
- `first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0`（必须 launch_admitted）
- `first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0`（必须 pre_commit_ready）
- `first_live_guarded_implementation_minimal_real_effect_commit_gate_v0`（必须 commit_admitted）
- `first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0`（必须 commit_ready）
- `first_live_guarded_implementation_minimal_real_effect_activation_gate_v0`（必须 activation_admitted）
- approval / launch / live release / side-effect release（仍必须 ready/approved）
- `first_live_guarded_implementation_dry_effect_simulation_v0`（必须 simulated）
- `first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0`（必须 executed）
- `execution_state_v0` / `result_v0`（在位）
- `side_effects_released`（必须仍为 false）
- implementation skeleton identity / capability（必须在位且仍为 conservative / dry-run mode）

并明确（写死）：

- 缺任一主前提，activation dry-run 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata`。

---

## 5. 最小结果集合（写死；三态）

activation dry-run 的结果必须收敛成最小集合：

- `first_live_minimal_real_effect_activation_ready`
- `first_live_minimal_real_effect_activation_not_ready`
- `first_live_minimal_real_effect_activation_blocked`

语义（写死）：

- `activation_ready`：仅表示 activation 放行后，系统具备最后一次进入真实最小写入前的干跑条件  
  不表示真实写入已开始、不表示副作用已发生、不表示 `side_effects_released == true`
- `activation_not_ready`：条件未满足或上游未通过
- `activation_blocked`：硬阻断 / 身份问题 / 一致性问题（保守阻断）

---

## 6. 明确禁止（写死）

activation dry-run 不允许直接：

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

与 activation gate：

- activation gate 负责进入受控激活的判断门
- activation dry-run 负责放行后的最后一次零副作用演练
- `activation_admitted != activation_ready`

与 activation contract：

- activation contract 定义未来唯一允许的受控激活范围与顺序
- activation dry-run 负责在不真实打开 side effects 的前提下演练这条链

与 commit dry-run：

- commit dry-run 负责 commit 级最后干跑
- activation dry-run 负责 activation 级最后干跑
- 两者不能混用

---

## 8. 当前仍然不能做什么（写死）

- 不允许把 `side_effects_released` 打开
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 `activation_ready` 当作真实写入已开始

---

## 9. 当前不做（写死）

- 不做 activation dry-run 代码实现
- 不做真实最小写入实现
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 10. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - minimal real-effect activation dry-run 的 minimal implementation
- 补充链接：
  - Phase-Next-114：Minimal Real-Effect Live Implementation Definition v0（第一版真实最小写入实现本体：定义冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_DEFINITION_V0.md`
- 再之后才考虑：
  - 第一版最小真实写入实现方案
- 当前不直接落真实实现

