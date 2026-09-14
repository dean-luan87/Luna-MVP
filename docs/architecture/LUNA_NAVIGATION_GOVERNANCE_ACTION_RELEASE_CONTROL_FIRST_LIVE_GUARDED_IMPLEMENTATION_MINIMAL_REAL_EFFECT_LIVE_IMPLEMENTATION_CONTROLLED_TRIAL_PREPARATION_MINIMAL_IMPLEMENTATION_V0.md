# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation Minimal Implementation v0（准备态承接位最小实现）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_MINIMAL_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-142：把 preparation admission 之后的“真实准备态入口”落成 minimal implementation（运行时承接位；placeholder-safe；不启用 preparation；不进默认路径）

---

## 1) 文档定位（写死）

这是第一版 controlled trial preparation 的 minimal implementation 文档。当前目标是冻结并落地：

- 从 `preparation admission gate` 到未来真实 preparation 运行时入口之间的 **承接边界**

本轮边界写死：

- 本轮只做 controlled trial preparation minimal implementation（承接位 + placeholder-safe）
- 不做真实 preparation 启用
- 不做真实 trial 启用
- 不做默认路径启用
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## 2) 为什么现在必须先做 preparation minimal implementation（写死理由）

当前已经具备：

- preparation admission gate 已存在（允许进入真实准备态的准入门）

但仍缺：

- 一个正式 runner/adapter 承接 preparation 运行时入口，回答“准备态入口由谁承接、最小接口是什么、当前如何保持非默认/非扩面/可回退”

如果不先做 implementation，后续最容易把 admission gate 直接等同于可以进入真实 preparation。

因此必须先单独占住 preparation implementation 层。

---

## 3) 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial preparation minimal implementation` 是：

- future controlled trial preparation 的运行时承接实现
- 当前只负责占位、校验与返回 placeholder-safe 结果
- **不直接执行真实 preparation**

---

## 4) 最小合法输入（写死；只允许标准对象）

只允许消费（只读）：

- `controlled_trial_preparation_status == first_live_minimal_real_effect_controlled_trial_preparation_admitted`
- `controlled_trial_go_no_go == first_live_minimal_real_effect_controlled_trial_go`
- `controlled_trial_admission == first_live_minimal_real_effect_controlled_trial_admitted`
- `controlled_trial_shadow_eval == first_live_minimal_real_effect_controlled_trial_shadow_eval_go`
- `real_write_go_no_go == first_live_minimal_real_effect_real_write_go`
- `controlled_trial_enablement_dry_run == first_live_minimal_real_effect_controlled_trial_enablement_dry_run_executed`
- `controlled_trial_first_minimal_real_enablement == first_live_minimal_real_effect_controlled_trial_real_enablement_ready`
- runtime activation stub / runtime implementation stub 在位
- `side_effects_released == false`
- **显式 preparation implementation signal / approval 存在**
- 默认开关仍为 false

并明确（写死）：

- 缺任一主前提，preparation implementation 不成立
- 禁止读取 `request_* / approved_* / raw metadata`

---

## 5) 必须提供的最小接口（写死）

实现必须至少提供：

- `get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_identity()`
- `accept_first_live_minimal_real_effect_controlled_trial_preparation_input(...)`
- `enter_first_live_controlled_trial_preparation_placeholder(...)`
- `perform_first_live_controlled_trial_preparation_checks_placeholder(...)`
- `exit_first_live_controlled_trial_preparation_placeholder(...)`
- `raise_first_live_controlled_trial_preparation_exception(...)`

---

## 6) 当前接口共同约束（写死）

- 所有接口当前都必须返回 `inactive/not_implemented/placeholder-safe`
- 所有接口当前都必须保持 `side_effects_released == false`
- 不允许声称真实 preparation 已开始
- 不允许触发真实写入/真实 release_control
- 不允许 route/voice/memory/migration
- 不允许 rollback/interrupt

---

## 7) 与现有链路关系（写清）

- 与 preparation admission gate：gate 定“能不能进入准备态”；implementation 定“进入准备态后运行时入口放哪”
- 与 controlled trial enablement implementation：enablement implementation 是 trial 启用承接位；preparation implementation 是 trial 准备态专用承接位
- 与真实 minimal trial enablement code：真实代码已存在；preparation implementation 不直接调用真实启用
- 与 runtime activation/runtime implementation stub：更下游；preparation implementation 位于其上游

---

## 8) 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实 preparation 启用
- 不允许真实 trial 启用
- 不允许默认路径启用
- 不允许真实 rollback / interrupt
- 不允许 route / voice / memory / migration
- 不允许把 preparation implementation 当作 trial 已开始

---

## 9) 当前不做（写死）

- 不做真实 preparation 启用
- 不做真实 trial 启用
- 不做默认路径开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 10) 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - controlled trial preparation dry-run
- 再之后才考虑：
  - controlled trial preparation first minimal real code
- 当前不直接启用真实 trial

