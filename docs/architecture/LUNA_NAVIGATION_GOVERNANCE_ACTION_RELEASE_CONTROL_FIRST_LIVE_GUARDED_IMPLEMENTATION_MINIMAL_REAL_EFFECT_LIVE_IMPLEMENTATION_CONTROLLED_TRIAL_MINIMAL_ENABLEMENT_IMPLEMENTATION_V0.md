# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Minimal Enablement Implementation v0（启用承接位最小实现）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_MINIMAL_ENABLEMENT_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-135：把 Phase-Next-134 enablement plan 落成最小 enablement implementation（运行时承接位；placeholder-safe；不启用 trial；不进默认路径）

---

## 1) 文档定位（写死）

这是第一版 `live implementation minimal real-effect` 的 `controlled trial minimal enablement` **实现文档**。当前目标是冻结并落地：

- 从 `controlled trial minimal enablement plan` 到未来 trial 最小启用实现之间的 **运行时承接边界**

本轮边界写死：

- 本轮只做 enablement implementation（承接位 + placeholder-safe）
- 不做真实 trial 启用
- 不做默认路径启用
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## 2) 为什么现在必须先做 enablement implementation（写死理由）

当前已经具备：

- enablement plan（Phase-Next-134）
- controlled trial admission/go-no-go gates（Phase-Next-132/133）
- shadow evaluation gate（Phase-Next-131）
- 真实最小写入代码存在但不接默认路径

但仍缺：

- 一个正式 runner/adapter 承接未来 trial 的“最小启用入口”，回答“入口放哪、最小接口是什么、当前如何继续保持非默认/非扩面/可回退”

如果不先占住 implementation 层，后续最容易把 plan 当作“已可启用”。

因此必须先单独占住 enablement implementation 层。

---

## 3) 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial minimal enablement implementation` 是：

- future controlled trial 最小启用的运行时承接实现
- 当前只负责占位、校验与返回 placeholder-safe 结果
- **不直接执行真实 trial**

---

## 4) 最小合法输入（写死；只允许标准对象）

只允许消费（只读）：

- controlled trial go/no-go gate == go
- controlled trial admission gate == admitted
- shadow evaluation gate == go
- real-write go/no-go gate == go
- live code path dry-run == executed
- live implementation wiring == wired_ready
- live implementation dry-run execution == executed
- rollout plan 已冻结
- first real code activation definition 已冻结
- runtime activation stub / runtime implementation stub 在位
- activation / commit / pre-commit / launch / admission 全链路 admitted/ready
- `side_effects_released == false`
- 显式 controlled-trial enablement approval/signal 存在
- 默认开关仍为 false

并明确（写死）：

- 缺任一主前提，enablement implementation 不成立
- 禁止读取 `request_* / approved_* / raw metadata`

---

## 5) 必须提供的最小接口（写死）

实现必须至少提供：

- `get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_identity()`
- `accept_first_live_minimal_real_effect_controlled_trial_enablement_input(...)`
- `enter_first_live_controlled_trial_enablement_placeholder(...)`
- `perform_first_live_controlled_trial_enablement_checks_placeholder(...)`
- `exit_first_live_controlled_trial_enablement_placeholder(...)`
- `raise_first_live_controlled_trial_enablement_exception(...)`

---

## 6) 当前接口共同约束（写死）

- 所有接口当前都必须返回 `inactive/not_implemented/placeholder-safe`
- 所有接口当前都必须保持 `side_effects_released == false`
- 不允许声称真实 trial 已开始
- 不允许触发真实写入 / 真实 release_control
- 不允许 route/voice/memory/migration
- 不允许 rollback/interrupt

---

## 7) 与现有链路关系（写清）

- 与 enablement plan：plan 定启用策略；implementation 定运行时承接位
- 与 controlled trial go/no-go gate：gate 定“本次能不能开始 trial”；implementation 定“如果未来允许开始，运行时入口放哪”
- 与真实最小写入代码：真实代码已存在；enablement implementation 不直接调用真实写入
- 与 runtime activation/runtime implementation stub：它们更下游；enablement implementation 位于其上游

---

## 8) 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实 trial 启用
- 不允许真实默认启用
- 不允许真实 rollback / interrupt
- 不允许 route / voice / memory / migration
- 不允许把 enablement implementation 当作 trial 已开始

---

## 9) 当前不做（写死）

- 不做真实 trial 启用
- 不做默认路径开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 10) 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - controlled trial minimal enablement dry-run
- 再之后才考虑：
  - 第一阶段受控真实 trial 的最小启用实现（含是否允许短时受控开启 side_effects_released 的讨论）
- 当前不直接启用真实 trial

