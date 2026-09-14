# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation Minimal Enablement Dry-Run v0（启用入口最后一次 runtime 干跑冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_MINIMAL_ENABLEMENT_DRY_RUN_V0.md`  
**性质**：Phase-Next-150：把 preparation minimal enablement runner 串成“进入真实 preparation 启用前最后一次零副作用 runtime 干跑链”（只演练、不启用；默认不开；不进默认路径）

---

## 1. 文档定位（写死）

这是第一版 `controlled trial preparation minimal enablement implementation` 的 dry-run 设计文档。当前目标是冻结：

- 从 preparation minimal enablement implementation 到未来真实 preparation 启用之前的**最后 runtime 演练边界**

本轮边界写死：

- 本轮只做 controlled trial preparation minimal enablement dry-run
- 不做真实 preparation 启用
- 不做真实 trial 启用
- 不做默认路径开启
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## 2. 为什么现在必须先做 preparation minimal enablement dry-run（写死理由）

当前已经具备：

- controlled trial preparation minimal enablement implementation（运行时承接位）
- preparation go/no-go gate（最终启动门）

但仍缺：

- 一个对象明确回答：“preparation enablement 入口是否已在 runtime 上按固定顺序零副作用走通”

如果不先做 dry-run，后续最容易从 enablement ready 直接跳到真实 preparation。

因此必须先冻结 preparation minimal enablement dry-run。

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial preparation minimal enablement dry-run` 是：

- future preparation enablement 启用前的最后 runtime 级零副作用演练层
- 只负责判断 enablement 入口顺序是否可走通
- 不执行任何真实启用

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
- controlled trial preparation minimal enablement implementation 在位（runner 可导入且接口存在）
- `side_effects_released == false`
- **显式 preparation minimal enablement dry-run signal / approval 在位**
- 默认开关仍为 false

并明确（写死）：

- 缺任一主前提，dry-run 不成立
- 禁止读取 `request_* / approved_* / raw metadata`

---

## 5. 最小结果集合（三态；写死）

输出三态（写死）：

- `first_live_minimal_real_effect_controlled_trial_preparation_minimal_enablement_dry_run_executed`
- `first_live_minimal_real_effect_controlled_trial_preparation_minimal_enablement_dry_run_not_ready`
- `first_live_minimal_real_effect_controlled_trial_preparation_minimal_enablement_dry_run_blocked`

并明确（写死）：

- `...executed` 只表示 enablement 入口已能零副作用走通
- 不表示真实 preparation 已开始
- 不表示默认路径已启用
- 不表示 `side_effects_released` 已打开

---

## 6. 最小演练顺序（写死；固定顺序）

preparation minimal enablement dry-run 的固定顺序（不得倒序、不得跳步、不得夹带副作用）：

1) `accept_first_live_minimal_real_effect_controlled_trial_preparation_enablement_input`  
2) `enter_first_live_controlled_trial_preparation_enablement_placeholder`  
3) `perform_first_live_controlled_trial_preparation_enablement_checks_placeholder`  
4) `exit_first_live_controlled_trial_preparation_enablement_placeholder`

---

## 7. 明确禁止（写死）

enablement dry-run 不允许：

- 打开 `side_effects_released`
- 启用真实 preparation / trial
- 开启默认路径
- 执行真实写入
- route / voice / memory / migration
- rollback / interrupt
- 越过标准对象吐散字段

---

## 8. 与现有链路关系（写清）

- 与 enablement implementation：implementation 是运行时承接位；dry-run 是对承接位的顺序演练
- 与 preparation go/no-go gate：gate 决定本次能不能开始 preparation；dry-run 决定开始前 enablement 入口是否已可演练
- 与 preparation shadow evaluation gate：shadow evaluation 是更上游证据；enablement dry-run 更接近真实启用
- 与未来真实 preparation 启用：dry-run 不替代真实启用

---

## 9. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - controlled trial preparation minimal enablement 的真实启用实现（或更细分的真实启用定义/runner）
- 当前不直接启用真实 preparation

