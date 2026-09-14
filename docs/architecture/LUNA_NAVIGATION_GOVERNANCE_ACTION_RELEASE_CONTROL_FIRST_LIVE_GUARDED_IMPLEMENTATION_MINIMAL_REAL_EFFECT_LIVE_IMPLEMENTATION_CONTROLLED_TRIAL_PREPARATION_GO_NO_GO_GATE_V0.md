# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation Go/No-Go Gate v0（准备态最终启动闸门冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_GO_NO_GO_GATE_V0.md`  
**性质**：Phase-Next-147：在 `preparation shadow evaluation == go` 之后，冻结“本次是否允许真正开始第一阶段真实 preparation”的最终启动门（只决策、不执行；默认不开；不进默认路径）

---

## 1. 文档定位（写死）

这是第一版 controlled trial preparation shadow evaluation 进入真实 preparation start 前的最终 go/no-go gate 设计文档。当前目标是冻结：

- 从 `preparation shadow evaluation` 到“本次 preparation 是否真正启动”的**边界**

本轮边界写死：

- 本轮只做 controlled trial preparation go/no-go gate
- 不做真实 preparation 启用
- 不做默认路径启用
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## 2. 为什么现在必须先定义 preparation go/no-go gate（写死理由）

当前已经具备：

- preparation shadow evaluation gate 已存在（影子结果是否足够好）
- preparation admission gate / dry-run / real code 已存在（承接与真实代码都闭合）

但仍缺：

- 一个正式 gate 去回答：“影子评估通过后，这一次是否真的允许开始真实 preparation”

写死核心：

- `preparation_shadow_eval_go != preparation_go`
- 即使 `preparation_go` 也不等于默认路径已开启

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial preparation go/no-go gate` 是：

- 从 preparation shadow evaluation 进入真实 preparation start 前的最终启动闸门
- 只负责判断本次是否允许真正开始第一阶段真实 preparation
- 不直接执行真实启用，不直接开启默认路径

---

## 4. 最小合法输入（写死；只允许标准对象）

只允许消费（只读）：

- `...controlled_trial_preparation_shadow_evaluation_gate_v0`
  - 必须 `first_live_minimal_real_effect_controlled_trial_preparation_shadow_eval_go`
- `...controlled_trial_preparation_admission_gate_v0`
  - 必须 `first_live_minimal_real_effect_controlled_trial_preparation_admitted`
- `controlled_trial_go_no_go == first_live_minimal_real_effect_controlled_trial_go`
- `controlled_trial_admission == first_live_minimal_real_effect_controlled_trial_admitted`
- `real_write_go_no_go == first_live_minimal_real_effect_real_write_go`
- `controlled_trial_preparation_dry_run == first_live_minimal_real_effect_controlled_trial_preparation_dry_run_executed`
- `controlled_trial_first_minimal_real_enablement == first_live_minimal_real_effect_controlled_trial_real_enablement_ready`
- runtime activation stub / runtime implementation stub 在位
- `side_effects_released == false`
- **显式 preparation go/no-go approval / signal 在位**
- 默认开关仍为 false

并明确（写死）：

- 缺任一主前提，preparation go/no-go gate 不成立（不得输出 go）
- 禁止读取 `request_* / approved_* / raw metadata`

---

## 5. 最小结果集合（三态；写死）

输出三态（写死）：

- `first_live_minimal_real_effect_controlled_trial_preparation_go`
- `first_live_minimal_real_effect_controlled_trial_preparation_no_go`
- `first_live_minimal_real_effect_controlled_trial_preparation_blocked`

并明确（写死）：

- `...preparation_go` 只表示本次允许开始第一阶段真实 preparation
- 不表示真实 preparation 已完成
- 不表示默认路径已启用
- 不表示 `side_effects_released` 已打开

---

## 6. 最小评估依据（写死）

- `controlled_trial_preparation_shadow_eval_status == ..._go`
- `controlled_trial_preparation_status == ..._admitted`
- `controlled_trial_go_no_go == ..._go`
- `controlled_trial_admission == ..._admitted`
- `controlled_trial_preparation_dry_run == ..._executed`
- `side_effects_released == false`
- preparation go/no-go approval / signal 明确存在
- blocked / no_go 原因必须可解释

---

## 7. 明确禁止（写死）

go/no-go gate 不允许：

- 打开 `side_effects_released`
- 执行真实 preparation 启用
- 开启默认路径
- route / voice / memory / migration
- rollback / interrupt
- 越过标准对象吐散字段
- 把 `preparation_go` 直接等同于真实启用已发生

---

## 8. 与现有链路的关系（写清）

- 与 preparation shadow evaluation gate：shadow evaluation 判影子结果是否足够好；go/no-go 判在此基础上“本次是否真正放行”
- 与 preparation admission gate：admission 定“能不能进入准备态”；go/no-go 定“这一次 preparation 是否真正开始”
- 与 preparation dry-run：dry-run 证明入口零副作用可走通；go/no-go 是启动前最终决策门
- 与真实 preparation code：真实代码已存在；go/no-go 不直接执行真实代码

---

## 9. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - controlled trial preparation 最小启用方案（或 preparation real execution runner 的受控接入）
- 当前不直接启用真实 preparation

