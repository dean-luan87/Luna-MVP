# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Shadow Evaluation Gate v0（trial 影子评估闸门冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_SHADOW_EVALUATION_GATE_V0.md`  
**性质**：Phase-Next-140：冻结“从 controlled trial shadow observe-only 结果 → 是否允许进入下一阶段真实 controlled trial 准备态”的标准化 gate（只定义/可最小实现；不启用真实 trial；不进默认路径）

---

## 1. 文档定位（写死）

这是第一版 controlled trial shadow observe-only 的评估 gate 设计文档。当前目标是冻结：

- 从 controlled trial shadow 结果到“是否允许进入下一阶段真实 controlled trial 准备态”的评估边界

本轮边界写死：

- 本轮只做 controlled trial shadow evaluation gate
- 不做真实 trial 启用
- 不做默认路径开启
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## 2. 为什么现在必须先定义 controlled trial shadow evaluation gate（写死理由）

当前已经具备：

- controlled trial real enablement code 已存在
- controlled trial shadow trial 已存在（主链 relevant-only 可产出 shadow 对象）

但仍缺：

- 一个统一 gate 去回答：“这些 shadow 结果是否足够稳定/一致，足以支持进入下一阶段真实 controlled trial 准备态”

如果不先冻结 evaluation gate，后续最容易把 shadow 已运行直接等同于可以进入真实 controlled trial。

因此必须先冻结 evaluation gate，再决定是否进入真实准备态。

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial shadow evaluation gate` 是：

- 基于 controlled trial shadow observe-only 结果与一致性信息的下一阶段资格判断门
- 只负责判断是否允许进入下一阶段真实 controlled trial 准备态
- 不直接执行任何真实启用

---

## 4. 最小合法输入（写死；只允许标准对象）

evaluation gate 只允许消费（只读）：

- `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0`
- controlled trial go/no-go == go
- controlled trial admission == admitted
- shadow eval == go
- real_write_go_no_go == go
- controlled trial enablement dry-run == executed
- controlled trial first minimal real enablement == ready
- `side_effects_released == false`
- controlled-trial shadow evaluation signal（默认不开；语义在位）
- 可选：现有 trial gate / dry-run 结果对象（用于一致性判断；仍只读）

并明确（写死）：

- 缺任一主前提，evaluation gate 不成立（不得输出 go）
- 禁止读取 `request_* / approved_* / raw metadata`

---

## 5. 最小结果集合（三态；写死）

evaluation gate 输出三态（写死）：

- `first_live_minimal_real_effect_controlled_trial_shadow_eval_go`
- `first_live_minimal_real_effect_controlled_trial_shadow_eval_no_go`
- `first_live_minimal_real_effect_controlled_trial_shadow_eval_blocked`

并明确（写死）：

- `...shadow_eval_go` 只表示：trial 影子结果足以支持进入下一阶段真实 controlled trial 准备态
- 不表示真实 trial 已发生
- 不表示默认路径已开启
- 不表示 `side_effects_released` 已打开

---

## 6. 最小评估依据（写死）

当且仅当以下条件满足时，允许 `shadow_eval_go`：

- `shadow_trial_status == shadow_trial_executed`
- `would_have_entered_real_trial_enablement == true`
- would-have 三类写入标记符合预期（至少 state/result 为 true；异常标记为 true 时必须可解释）
- `side_effects_released == false`
- blocked / not_ready 原因必须可解释
- 与现有 trial gate / dry-run 不冲突；若冲突必须可解释（冲突默认 no_go）

---

## 7. 明确禁止（写死）

evaluation gate 不允许：

- 打开 `side_effects_released`
- 执行真实启用
- 改变主链输出
- route / voice / memory / migration
- rollback / interrupt
- 默认开启 controlled trial
- 越过标准对象吐散字段

---

## 8. 与现有链路的关系（写清）

- 与 controlled trial shadow trial：shadow trial 负责 observe-only 接入；evaluation gate 负责判断 shadow 结果是否足以支持下一阶段
- 与 controlled trial admission/go-no-go gate：这些 gate 决定 trial 条件是否允许；shadow evaluation gate 定“trial 影子结果是否足以支持进入真实准备态”
- 与 controlled trial minimal enablement plan：plan 定真实 trial 启用策略；shadow evaluation gate 是真实启用前的影子评估门

---

## 9. 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实启用
- 不允许真实写入
- 不允许默认启用
- 不允许真实 rollback / interrupt
- 不允许 route / voice / memory / migration
- 不允许把 `...shadow_eval_go` 当作真实 trial 结果

---

## 10. 当前不做（写死）

- 不做真实 trial 启用
- 不做默认路径开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 11. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - controlled trial shadow evaluation gate minimal implementation（若本轮未落）
- 再之后才考虑：
  - 是否进入真实 controlled trial 准备态
- 当前不直接启用真实 trial

