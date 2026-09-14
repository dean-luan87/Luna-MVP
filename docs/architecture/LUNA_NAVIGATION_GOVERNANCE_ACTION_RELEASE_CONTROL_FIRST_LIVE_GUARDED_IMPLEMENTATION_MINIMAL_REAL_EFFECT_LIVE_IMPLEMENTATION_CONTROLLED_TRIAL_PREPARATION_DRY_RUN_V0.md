# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation Dry-Run v0（准备态入口最后一次 runtime 干跑冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_DRY_RUN_V0.md`  
**性质**：Phase-Next-143：把 controlled trial preparation runner 串成“进入真实 preparation 前最后一次零副作用 runtime 干跑链”（只演练、不启用；默认不开；不进默认路径）

---

## 1. 文档定位（写死）

这是第一版 `controlled trial preparation minimal implementation` 的 dry-run 设计文档。当前目标是冻结：

- 从 preparation implementation 到未来真实 preparation 启用之前的**最后 runtime 演练边界**

本轮边界写死：

- 本轮只做 controlled trial preparation dry-run
- 不做真实 preparation 启用
- 不做真实 trial 启用
- 不做默认路径开启
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## 2. 为什么现在必须先做 preparation dry-run（写死理由）

当前已经具备：

- controlled trial preparation admission gate（真实准备态准入门）
- controlled trial preparation minimal implementation（准备态运行时承接位）

但仍缺：

- 一个对象明确回答：“preparation 启用入口是否已在 runtime 上按固定顺序零副作用走通”

如果不先做 dry-run，后续最容易从 `preparation ready` 直接跳到真实 preparation / 真实 trial。

因此必须先冻结 preparation dry-run。

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial preparation dry-run` 是：

- future controlled trial preparation 启用前的最后 runtime 级零副作用演练层
- 只负责判断 preparation 入口顺序是否可走通
- 不执行任何真实启用

---

## 4. 最小合法输入（写死；只允许标准对象）

只允许消费（只读）：

- `controlled_trial_preparation_status == first_live_minimal_real_effect_controlled_trial_preparation_admitted`
- `controlled_trial_go_no_go == first_live_minimal_real_effect_controlled_trial_go`
- `controlled_trial_admission == first_live_minimal_real_effect_controlled_trial_admitted`
- `controlled_trial_shadow_eval == first_live_minimal_real_effect_controlled_trial_shadow_eval_go`
- `real_write_go_no_go == first_live_minimal_real_effect_real_write_go`
- `controlled_trial_enablement_dry_run == first_live_minimal_real_effect_controlled_trial_enablement_dry_run_executed`
- `controlled_trial_first_minimal_real_enablement == first_live_minimal_real_effect_controlled_trial_real_enablement_ready`
- controlled trial preparation minimal implementation 在位（runner 可导入且接口存在）
- `side_effects_released == false`
- **显式 preparation dry-run signal / approval 在位**
- 默认开关仍为 false

并明确（写死）：

- 缺任一主前提，preparation dry-run 不成立
- 禁止读取 `request_* / approved_* / raw metadata`

---

## 5. 最小结果集合（三态；写死）

输出三态（写死）：

- `first_live_minimal_real_effect_controlled_trial_preparation_dry_run_executed`
- `first_live_minimal_real_effect_controlled_trial_preparation_dry_run_not_ready`
- `first_live_minimal_real_effect_controlled_trial_preparation_dry_run_blocked`

并明确（写死）：

- `...executed` 只表示 preparation 入口已能零副作用走通
- 不表示真实 preparation 已开始
- 不表示默认路径已启用
- 不表示 `side_effects_released` 已打开

---

## 6. 最小演练顺序（写死；固定顺序）

preparation dry-run 的固定顺序（不得倒序、不得跳步、不得夹带副作用）：

1) `accept_first_live_minimal_real_effect_controlled_trial_preparation_input`  
2) `enter_first_live_controlled_trial_preparation_placeholder`  
3) `perform_first_live_controlled_trial_preparation_checks_placeholder`  
4) `exit_first_live_controlled_trial_preparation_placeholder`

---

## 7. 明确禁止（写死）

preparation dry-run 不允许：

- 打开 `side_effects_released`
- 启用真实 preparation
- 启用真实 trial
- 开启默认路径
- 执行真实写入
- route / voice / memory / migration
- rollback / interrupt
- 越过标准对象吐散字段

---

## 8. 与现有链路的关系（写清）

- 与 preparation minimal implementation：implementation 是运行时承接位；dry-run 是对承接位的顺序演练
- 与 preparation admission gate：gate 决定能不能进入 preparation 准备态；dry-run 决定开始前入口是否已可演练
- 与 controlled trial enablement dry-run：enablement dry-run 更上游；preparation dry-run 更接近真实 preparation 启动
- 与未来真实 preparation 启用：dry-run 不替代真实启用

---

## 9. 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实 preparation 启用
- 不允许真实 trial 启用
- 不允许默认路径启用
- 不允许真实 rollback / interrupt
- 不允许 route / voice / memory / migration
- 不允许把 `...dry_run_executed` 当作真实 preparation 已开始

---

## 10. 当前不做（写死）

- 不做真实 preparation 启用
- 不做真实 trial 启用
- 不做默认路径开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 11. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - controlled trial preparation first minimal real code
- 当前不直接启用真实 preparation

