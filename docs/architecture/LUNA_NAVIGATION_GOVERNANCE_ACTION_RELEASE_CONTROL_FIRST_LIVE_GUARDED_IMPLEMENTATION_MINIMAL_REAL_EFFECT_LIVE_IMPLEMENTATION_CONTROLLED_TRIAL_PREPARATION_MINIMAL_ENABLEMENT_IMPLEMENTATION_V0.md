# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation Minimal Enablement Implementation v0（准备态最小启用承接位最小实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_MINIMAL_ENABLEMENT_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-149：把 preparation minimal enablement plan 落成最小 enablement runner（运行时承接位；placeholder-safe；不启用；默认不开；不进默认路径）

---

## 1. 文档定位（写死）

这是第一版 controlled trial preparation minimal enablement 的实现文档。当前目标是冻结：

- 从 `preparation minimal enablement plan` 到未来“preparation 最小启用实现”的运行时承接边界

本轮边界写死：

- 本轮只做 controlled trial preparation minimal enablement implementation（承接位 + placeholder-safe）
- 不做真实 preparation 启用
- 不做真实 trial 启用
- 不做默认路径启用
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## 2. 为什么现在必须先做 enablement implementation（写死理由）

当前已经具备：

- controlled trial preparation minimal enablement plan（策略已冻结）
- preparation go/no-go gate（最终启动门已在位）

但仍缺：

- 一个正式 runner / adapter 去承接未来 preparation 最小启用入口（入口放哪、消费哪些对象、最后检查顺序是什么、如何保持非默认/非扩面/可回退）

如果不先做 implementation，后续最容易把 plan 直接当成“可以启用”。

因此必须先单独占住 enablement implementation 层。

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial preparation minimal enablement implementation` 是：

- future preparation 最小启用的运行时承接实现
- 当前只负责占位、校验、返回 placeholder-safe 结果
- **不直接执行真实 preparation**

---

## 4. 最小合法输入（写死；只允许标准对象）

只允许消费（只读）：

- `controlled_trial_preparation_go_no_go_status == first_live_minimal_real_effect_controlled_trial_preparation_go`
- `controlled_trial_preparation_shadow_eval_status == first_live_minimal_real_effect_controlled_trial_preparation_shadow_eval_go`
- `controlled_trial_preparation_status == first_live_minimal_real_effect_controlled_trial_preparation_admitted`
- `controlled_trial_preparation_dry_run_status == first_live_minimal_real_effect_controlled_trial_preparation_dry_run_executed`
- `controlled_trial_go_no_go_status == first_live_minimal_real_effect_controlled_trial_go`
- `controlled_trial_status == first_live_minimal_real_effect_controlled_trial_admitted`
- `real_write_go_no_go_status == first_live_minimal_real_effect_real_write_go`
- runtime activation stub / runtime implementation stub 在位
- `side_effects_released == false`
- **显式 preparation enablement signal / approval 在位**
- 默认开关仍为 false

并明确（写死）：

- 缺任一主前提，enablement implementation 不成立（不得输出 ready）
- 禁止读取 `request_* / approved_* / raw metadata`

---

## 5. 必须提供的最小接口（写死）

至少包括：

- `get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_enablement_identity()`
- `accept_first_live_minimal_real_effect_controlled_trial_preparation_enablement_input(...)`
- `enter_first_live_controlled_trial_preparation_enablement_placeholder(...)`
- `perform_first_live_controlled_trial_preparation_enablement_checks_placeholder(...)`
- `exit_first_live_controlled_trial_preparation_enablement_placeholder(...)`
- `raise_first_live_controlled_trial_preparation_enablement_exception(...)`

---

## 6. 当前接口共同约束（写死）

- 所有接口当前都必须返回 `inactive/not_implemented/placeholder-safe`
- 所有接口当前都必须保持 `side_effects_released == false`
- 不允许声称真实 preparation 已开始
- 不允许触发真实写入 / 真实 release_control
- 不允许 route / voice / memory / migration
- 不允许 rollback / interrupt

---

## 7. 与现有链路关系（写清）

- 与 preparation minimal enablement plan：plan 定启用策略；implementation 定运行时承接位
- 与 preparation go/no-go gate：gate 定“本次能不能开始 preparation”；implementation 定“若未来允许开始，入口放哪、怎么校验”
- 与真实 minimal preparation code：真实代码已存在；enablement implementation **不直接调用真实写入**
- 与 preparation minimal implementation / preparation dry-run：它们偏准备态承接与演练；本 implementation 是启用策略的运行时承接位

---

## 8. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - controlled trial preparation minimal enablement dry-run
- 再之后才考虑：
  - 第一阶段真实 preparation 的最小启用实现
- 当前不直接启用真实 preparation

