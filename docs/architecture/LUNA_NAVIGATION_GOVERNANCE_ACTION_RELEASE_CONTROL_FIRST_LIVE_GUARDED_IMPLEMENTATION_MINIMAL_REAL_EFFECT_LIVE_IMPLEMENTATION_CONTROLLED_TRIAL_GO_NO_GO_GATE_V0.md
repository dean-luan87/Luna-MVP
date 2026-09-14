# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Go/No-Go Gate v0（受控试运行最终启动闸门冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_GO_NO_GO_GATE_V0.md`  
**性质**：Phase-Next-133：冻结“从 controlled trial admission → 本次是否真正启动第一阶段受控真实 trial”的最终 go/no-go gate（只决策、不执行；默认不开；不进入任何默认路径）

---

## 1. 文档定位（写死）

这是第一版 `live implementation minimal real-effect` 从 `controlled trial admission` 进入真正 trial start 前的最终 go/no-go gate 设计文档。当前目标是冻结：

- 从 admission 到“本次 trial 是否真正启动”的边界
- 最小输入、三态输出、评估依据、禁止项、链路关系

本轮边界写死：

- 本轮只做 controlled trial go/no-go gate（定义冻结）
- 不做真实 trial 启用
- 不做默认路径启用
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## 2. 为什么现在必须先定义 controlled trial go/no-go gate（写死理由）

当前已经具备：

- controlled trial admission gate（admitted 只表示进入准备态）
- shadow evaluation gate（shadow_eval_go 只表示 shadow 质量足够）
- rollout plan（策略冻结）
- real-write go/no-go gate（真实写入启动闸门冻结）

但仍缺：

- 一个正式 gate 去回答：“这一次 trial admission 通过后，是否真的允许开始第一阶段受控真实 trial”

如果不先冻结该 go/no-go gate，后续最容易把：

- `controlled_trial_admitted` 直接等同于 “trial 已开始”

因此必须先冻结 controlled trial go/no-go gate，再决定是否真正开启真实 trial。

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial go/no-go gate` 是：

- 从 controlled trial admission 进入真实 trial start 前的最终启动闸门
- 只负责判断本次是否允许真正开始第一阶段受控真实 trial
- 不直接执行真实写入，不直接开启默认路径

核心定义（写死一句）：

> controlled trial go/no-go gate 只决定“本次是否允许真正开始第一阶段受控真实 trial”，不直接执行 trial。

---

## 4. 最小合法输入（写死；只允许标准化对象）

只允许消费（只读）：

- `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0`
  - 必须 `controlled_trial_status == first_live_minimal_real_effect_controlled_trial_admitted`
- `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_gate_v0`
  - 必须 `shadow_eval_status == first_live_minimal_real_effect_shadow_eval_go`
- real-write go/no-go gate == go：
  - `...real_write_go_no_go_gate_v0` 必须 `real_write_status == first_live_minimal_real_effect_real_write_go`
- live code path dry-run == executed：
  - `...live_code_path_dry_run_v0` 必须 `dry_run_status == first_live_minimal_real_effect_live_code_path_dry_run_executed`
- live implementation wiring == wired_ready：
  - `...live_implementation_wiring_v0` 必须 `wiring_status == first_live_minimal_real_effect_live_wired_ready`
- live implementation dry-run execution == executed：
  - `...live_implementation_dry_run_execution_v0` 必须 `execution_status == first_live_minimal_real_effect_live_dry_run_executed`
- live runtime activation stub / runtime implementation stub 在位
- rollout plan 已冻结（语义在位）
- activation / commit / pre-commit / launch / admission 全链路 admitted/ready
- `side_effects_released == false`
- **显式 controlled-trial go/no-go approval / signal 存在**
- **默认开关仍为 false**

并明确（写死）：

- 缺任一主前提，controlled trial go/no-go gate 不成立（不得输出 go）
- 禁止读取 `request_* / approved_* / raw metadata`

---

## 5. 最小结果集合（三态；写死）

输出三态（写死）：

- `first_live_minimal_real_effect_controlled_trial_go`
- `first_live_minimal_real_effect_controlled_trial_no_go`
- `first_live_minimal_real_effect_controlled_trial_blocked`

并明确（写死）：

- `controlled_trial_go` 只表示本次允许开始第一阶段受控真实 trial
- 不表示真实写入已发生
- 不表示默认路径已启用
- 不表示 `side_effects_released` 已打开

---

## 6. 最小评估依据（写死）

当且仅当以下条件同时满足时，才允许输出 `controlled_trial_go`：

- `controlled_trial_status == admitted`
- `shadow_eval_status == go`
- `real_write_go_no_go == go`
- `code path dry-run == executed`
- `side_effects_released == false`
- rollout plan 在位且未被绕过（语义在位；本 gate 不实现 rollout）
- go/no-go approval / signal 明确存在
- blocked / no_go 原因必须可解释

---

## 7. 明确禁止（写死）

controlled trial go/no-go gate 不允许：

- 打开 `side_effects_released`
- 执行真实写入
- 开启默认路径
- route / voice / memory / migration
- rollback / interrupt
- 越过标准对象吐散字段
- 把 trial go 直接等同于真实写入已发生

---

## 8. 与现有链路的关系（写清）

- 与 controlled trial admission gate：admission gate 定“能不能进入 trial 准备态”；go/no-go gate 定“这一次 trial 是否真正开始”
- 与 shadow evaluation gate：shadow evaluation gate 判影子结果是否足够好；go/no-go gate 判在此基础上这一次是否真正放行 trial
- 与 rollout plan：rollout plan 定 trial 策略；go/no-go gate 定本次 trial 启动决策
- 与真实最小写入代码：真实代码已存在；go/no-go gate 不直接执行真实写入

---

## 9. 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实写入
- 不允许真实默认启用
- 不允许真实 rollback / interrupt
- 不允许 route / voice / memory / migration
- 不允许把 `controlled_trial_go` 当作真实 trial 已经开始

---

## 10. 当前不做（写死）

- 不做 controlled trial go/no-go gate 代码实现（除非边界足够稳定且同轮落最小实现）
- 不做真实 trial 启用
- 不做默认路径开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 11. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - controlled trial go/no-go gate minimal implementation
- 再之后才考虑：
  - 第一阶段受控真实 trial 的最小启用方案
- 当前不直接启用真实写入

