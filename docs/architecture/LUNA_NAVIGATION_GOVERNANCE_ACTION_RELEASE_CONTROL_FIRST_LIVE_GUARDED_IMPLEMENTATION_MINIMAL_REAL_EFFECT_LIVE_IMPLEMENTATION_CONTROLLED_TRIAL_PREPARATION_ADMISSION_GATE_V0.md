# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation Admission Gate v0（真实准备态准入门冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_ADMISSION_GATE_V0.md`  
**性质**：Phase-Next-141：冻结“从 controlled trial shadow evaluation 阶段进入真实 controlled trial 准备态”的 admission gate（只决策、不执行；默认不开；不进默认路径）

---

## 1. 文档定位（写死）

这是第一版 controlled trial shadow evaluation 进入真实准备态的 admission gate 设计文档。当前目标是冻结：

- 从 `controlled_trial_shadow_eval_go` 到“是否允许进入真实 controlled trial 准备态”的边界

本轮边界写死：

- 本轮只做 controlled trial preparation admission gate
- 不做真实 trial 准备实现
- 不做真实 trial 启用
- 不做默认路径启用
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## 2. 为什么现在必须先定义 preparation admission gate（写死理由）

当前已经具备：

- controlled trial shadow evaluation gate（影子评估已存在）
- controlled trial minimal enablement plan（启用策略已冻结）

但仍缺：

- 一个正式 gate 去回答：“影子评估通过后，是否允许进入真实准备态”

如果不先定义该 gate，后续最容易把 `shadow_eval_go` 直接等同于“可以开始真实 trial 准备/甚至启用”。

因此必须先冻结 preparation admission gate，再决定是否进入真实准备实现。

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial preparation admission gate` 是：

- 从 controlled trial shadow evaluation 阶段进入真实 controlled trial 准备态的正式准入门
- 只负责判断是否允许进入 trial 准备态
- 不直接执行任何真实启用，也不直接开启默认路径

---

## 4. 最小合法输入（写死；只允许标准化对象）

只允许消费（只读）：

- `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_evaluation_gate_v0`
  - 必须 `controlled_trial_shadow_eval_status == first_live_minimal_real_effect_controlled_trial_shadow_eval_go`
- `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0`
- controlled trial go/no-go == go
- controlled trial admission == admitted
- real-write go/no-go == go
- controlled trial enablement dry-run == executed
- controlled trial first minimal real enablement == ready
- `side_effects_released == false`
- **显式 preparation admission signal / approval 存在**
- 默认开关仍为 false

并明确（写死）：

- 缺任一主前提，preparation admission gate 不成立（不得输出 admitted）
- 禁止读取 `request_* / approved_* / raw metadata`

---

## 5. 最小结果集合（三态；写死）

输出三态（写死）：

- `first_live_minimal_real_effect_controlled_trial_preparation_admitted`
- `first_live_minimal_real_effect_controlled_trial_preparation_not_admitted`
- `first_live_minimal_real_effect_controlled_trial_preparation_blocked`

并明确（写死）：

- `...preparation_admitted` 只表示允许进入真实 controlled trial 准备态
- 不表示真实 trial 已开始
- 不表示默认路径已启用
- 不表示 `side_effects_released` 已打开

---

## 6. 最小评估依据（写死）

当且仅当以下条件满足时，允许 `...preparation_admitted`：

- `controlled_trial_shadow_eval_status == ..._go`
- `shadow_trial_status == shadow_trial_executed`
- `would_have_entered_real_trial_enablement == true`
- `controlled_trial_go_no_go == ..._go`
- `controlled_trial_admission == ..._admitted`
- `side_effects_released == false`
- preparation admission signal 明确存在
- blocked / not_admitted 原因必须可解释

---

## 7. 明确禁止（写死）

preparation admission gate 不允许：

- 打开 `side_effects_released`
- 执行真实 trial 启用
- 开启默认路径
- route / voice / memory / migration
- rollback / interrupt
- 越过标准对象吐散字段
- 把 `...preparation_admitted` 直接等同于真实 trial 已开始

---

## 8. 与现有链路的关系（写清）

- 与 controlled trial shadow evaluation gate：shadow evaluation 判影子结果是否足够好；preparation admission gate 判是否允许从影子阶段跨入真实准备态
- 与 controlled trial admission/go-no-go gate：它们是 trial 启动前门；preparation admission gate 是影子阶段后的真实准备态准入门
- 与 minimal enablement plan：plan 定启用策略；preparation admission gate 定是否允许先进入准备态
- 与真实最小试运行启用代码：真实代码已存在；preparation admission gate 不直接调用真实启用

---

## 9. 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实 trial 启用
- 不允许默认路径启用
- 不允许真实 rollback / interrupt
- 不允许 route / voice / memory / migration
- 不允许把 `...preparation_admitted` 当作真实 trial 已开始

---

## 10. 当前不做（写死）

- 不做真实准备实现
- 不做真实 trial 启用
- 不做默认路径开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 11. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - controlled trial preparation admission gate minimal implementation（若本轮未落）
- 再之后才考虑：
  - controlled trial preparation minimal implementation
- 当前不直接启用真实 trial

