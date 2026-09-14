# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation Shadow Evaluation Gate v0（准备态 shadow 评估门冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_SHADOW_EVALUATION_GATE_V0.md`  
**性质**：Phase-Next-146：把 preparation shadow observe-only 结果收束为正式评估 gate（只评估、不启用；默认不开；不进默认路径）

---

## 1. 文档定位（写死）

这是第一版 controlled trial preparation shadow observe-only 的评估 gate 设计文档。当前目标是冻结：

- 从 `preparation shadow` 结果到“是否允许进入下一阶段真实 preparation”的**边界**

本轮边界写死：

- 本轮只做 preparation shadow evaluation gate
- 不做真实 preparation 启用
- 不做默认路径开启
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## 2. 为什么现在必须先定义 preparation shadow evaluation gate（写死理由）

当前已经具备：

- preparation shadow integration 已存在
- preparation 旁路观察已能产出 shadow 对象（含 would-have 与 observe-only 执行结果）

但仍缺：

- 一个统一 gate 去回答“这些 shadow 结果是否足够稳定，是否足以支持进入下一阶段真实 preparation”

如果不先定义 evaluation gate，后续最容易把 shadow 已运行直接等同于可以进入真实 preparation。

因此必须先冻结 evaluation gate，再决定是否进入真实 preparation 下一阶段。

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial preparation shadow evaluation gate` 是：

- 基于 preparation shadow observe-only 结果与一致性信息的下一阶段资格判断门
- 只负责判断是否允许进入下一阶段真实 preparation
- 不直接执行任何真实启用

---

## 4. 最小合法输入（写死；只允许标准对象）

只允许消费（只读）：

- `...controlled_trial_preparation_shadow_v0`（shadow 对象）
- `controlled_trial_preparation_status == ...preparation_admitted`
- `controlled_trial_preparation_dry_run == ...preparation_dry_run_executed`
- `controlled_trial_go_no_go == ...controlled_trial_go`
- `controlled_trial_admission == ...controlled_trial_admitted`
- `controlled_trial_shadow_eval == ...controlled_trial_shadow_eval_go`
- `controlled_trial_first_minimal_real_enablement == ...controlled_trial_real_enablement_ready`
- `real_write_go_no_go == ...real_write_go`
- `side_effects_released == false`
- **preparation shadow evaluation signal 在位**
- 可选但推荐：现有 preparation / trial gate 与 dry-run 结果对象，用于一致性判断

并明确（写死）：

- 缺任一主前提，evaluation gate 不成立
- 禁止读取 `request_* / approved_* / raw metadata`

---

## 5. 最小结果集合（三态；写死）

输出三态（写死）：

- `first_live_minimal_real_effect_controlled_trial_preparation_shadow_eval_go`
- `first_live_minimal_real_effect_controlled_trial_preparation_shadow_eval_no_go`
- `first_live_minimal_real_effect_controlled_trial_preparation_shadow_eval_blocked`

并明确（写死）：

- `...shadow_eval_go` 只表示 preparation 影子结果足以支持进入下一阶段真实 preparation
- 不表示真实 preparation 已发生
- 不表示默认路径已开启
- 不表示 `side_effects_released` 已打开

---

## 6. 最小评估依据（写死）

至少满足：

- `preparation_shadow_status == preparation_shadow_executed`
- `would_have_entered_real_preparation_enablement == true`
- would-have 三类写入标记符合预期（state/result 为 true；exception_or_failure 默认期望为 false）
- `side_effects_released == false`
- blocked / not_ready 原因必须可解释
- 与现有 preparation gate / dry-run / controlled trial gate 结果不冲突，或冲突必须可解释

---

## 7. 明确禁止（写死）

evaluation gate 不允许：

- 打开 `side_effects_released`
- 执行真实 preparation 启用
- 改变主链输出
- route / voice / memory / migration
- rollback / interrupt
- 默认开启 preparation
- 越过标准对象吐散字段

---

## 8. 与现有链路的关系（写清）

- 与 preparation shadow：shadow 负责 observe-only 接入；evaluation gate 负责判断其结果是否足以支持下一阶段
- 与 preparation admission/dry-run：它们是更上游门与演练；shadow evaluation gate 是基于真实 preparation 代码旁路结果的评估门
- 与 controlled trial shadow/evaluation 链：它们更上游；preparation shadow evaluation gate 更下游、更接近真实 preparation 启用

---

## 9. 当前不做（写死）

- 不做真实 preparation 启用
- 不做默认路径开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 10. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - preparation shadow evaluation gate minimal implementation（若本轮未实现）
- 再之后才考虑：
  - 是否进入真实 preparation 的下一阶段
- 当前不直接启用真实 preparation

