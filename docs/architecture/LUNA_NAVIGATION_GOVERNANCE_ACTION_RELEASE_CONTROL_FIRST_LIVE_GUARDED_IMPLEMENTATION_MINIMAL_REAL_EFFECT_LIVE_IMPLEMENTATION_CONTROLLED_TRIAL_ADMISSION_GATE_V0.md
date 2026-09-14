# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Admission Gate v0（受控试运行准入门冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_ADMISSION_GATE_V0.md`  
**性质**：Phase-Next-132：冻结“从 shadow 观察阶段进入第一阶段受控真实试运行”的准入 gate（只决策、不执行；默认不开；不进入任何默认路径）

---

## A. 文档定位（写死）

这是第一版 `live implementation minimal real-effect` 从 shadow 阶段进入 **controlled trial** 的 admission gate 设计文档。当前目标是冻结：

- 从 `shadow_eval_go` 到“是否允许进入第一阶段受控真实试运行准备态”的边界
- 最小输入、三态输出、评估依据、禁止项、链路关系

本轮边界写死：

- 本轮只做 controlled trial admission gate（定义冻结）
- 不做真实 trial 启用
- 不做真实默认启用
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## B. 为什么现在必须先定义 controlled trial admission gate（写死理由）

当前已经具备：

- shadow integration（旁路观察）已存在
- shadow evaluation gate 已存在
- rollout plan 已冻结
- real-write go/no-go gate 已冻结（且真实最小写入代码已存在但不接默认路径）

但仍缺：

- 一个正式 gate 去回答：“现在这一次是否允许进入 controlled trial（受控真实试运行准备态）”

如果不先冻结该 gate，后续最容易把 `shadow_eval_go` 直接等同于“可以开始真实试运行”，从而绕过“受控试运行准入门”。

因此必须先冻结 controlled trial admission gate，再决定是否真正开启 trial。

---

## C. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial admission gate` 是：

- 从 shadow evaluation 阶段进入第一阶段受控真实试运行的正式准入门
- 只负责判断是否允许进入 controlled trial（准备态）
- 不直接执行任何真实写入，也不直接开启默认路径

核心定义（写死一句）：

> controlled trial admission gate 只决定“是否允许进入第一阶段受控真实试运行”，不直接执行真实 trial。

---

## D. 最小合法输入（写死；只允许标准化对象）

只允许消费（只读）：

- `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0`
- `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_gate_v0`
  - 必须 `shadow_eval_status == first_live_minimal_real_effect_shadow_eval_go`
- real-write go/no-go gate == go：
  - `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0`
  - 必须 `real_write_status == first_live_minimal_real_effect_real_write_go`
- live code path dry-run == executed：
  - `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0`
  - 必须 `dry_run_status == first_live_minimal_real_effect_live_code_path_dry_run_executed`
- live implementation wiring == wired_ready：
  - `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0`
  - 必须 `wiring_status == first_live_minimal_real_effect_live_wired_ready`
- live implementation dry-run execution == executed：
  - `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0`
  - 必须 `execution_status == first_live_minimal_real_effect_live_dry_run_executed`
- live implementation definition / skeleton / stub / minimal code skeleton / runtime activation stub / runtime implementation stub 在位（只读身份对象或占位对象）
- rollout plan 已冻结（语义在位）
- activation / commit / pre-commit / launch / admission 全链路 admitted/ready
- `side_effects_released == false`
- **显式 controlled-trial approval / admission signal 存在**（默认不开；语义在位即可）
- **默认开关仍为 false**

并明确（写死）：

- 缺任一主前提，controlled trial admission gate 不成立（不得输出 admitted）
- 禁止读取 `request_* / approved_* / raw metadata`

---

## E. 最小结果集合（三态；写死）

输出三态（写死）：

- `first_live_minimal_real_effect_controlled_trial_admitted`
- `first_live_minimal_real_effect_controlled_trial_not_admitted`
- `first_live_minimal_real_effect_controlled_trial_blocked`

并明确（写死）：

- `controlled_trial_admitted` 只表示允许进入第一阶段受控真实试运行准备态
- 不表示真实 trial 已开始
- 不表示默认路径已启用
- 不表示 `side_effects_released` 已打开

---

## F. 最小评估依据（写死）

当且仅当以下条件同时满足时，才允许输出 `controlled_trial_admitted`：

- `shadow_eval_status == first_live_minimal_real_effect_shadow_eval_go`
- shadow 输出 would-have 指标符合预期（至少 would-have state/result 为 true 且可解释）
- `side_effects_released == false`
- real-write go/no-go 仍为 go
- code path dry-run 仍为 executed
- rollout plan 在位且未被绕过（语义在位；本 gate 不实现 rollout）
- controlled-trial admission signal 明确存在
- blocked / not_admitted 原因必须可解释

---

## G. 明确禁止（写死）

controlled trial admission gate 不允许：

- 打开 `side_effects_released`
- 执行真实写入
- 开启默认路径
- route / voice / memory / migration
- rollback / interrupt
- 越过标准对象吐散字段
- 把 trial admission 直接等同于真实启用或试运行已开始

---

## H. 与现有链路的关系（写清）

- 与 shadow evaluation gate：shadow evaluation gate 判 shadow 结果是否足够好；controlled trial admission gate 判“是否允许从 shadow 阶段进入真实 trial 阶段”
- 与 rollout plan：rollout plan 定试运行策略；controlled trial admission gate 定“这一次能不能进入试运行准备态”
- 与 real-write go/no-go gate：go/no-go gate 定未来能否开始真实写入；controlled trial admission gate 定是否允许先进入第一阶段受控 trial
- 与真实最小写入代码：真实代码已存在；controlled trial admission gate **不直接调用真实写入**

---

## I. 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实写入
- 不允许真实默认启用
- 不允许真实 rollback / interrupt
- 不允许 route / voice / memory / migration
- 不允许把 `controlled_trial_admitted` 当作 trial 已经开始

---

## J. 当前不做（写死）

- 不做 controlled trial admission gate 代码实现（除非边界足够稳定且同轮落最小实现）
- 不做真实 trial 启用
- 不做默认路径开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## K. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - controlled trial admission gate minimal implementation
- 再之后才考虑：
  - 第一阶段受控真实试运行
- 当前不直接启用真实写入

