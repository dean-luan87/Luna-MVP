# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Shadow Evaluation Gate v0（shadow 评估闸门冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_SHADOW_EVALUATION_GATE_V0.md`  
**性质**：Phase-Next-131：冻结“从 shadow observe-only 结果 → 是否允许进入下一阶段受控真实试运行前评估”的标准化 gate（只定义、不启用、不真实写入）

---

## 1. 文档定位（写死）

这是第一版 `live implementation shadow observe-only` 的 **评估 gate** 设计文档。当前目标是冻结：

- 如何基于 shadow 结果、would-have 写入信息、以及与既有 gate / dry-run 的一致性信息
- 判断是否 **允许进入下一阶段“受控真实试运行前评估”**

本轮边界写死：

- 只做 shadow evaluation gate（定义冻结）
- 不做真实 rollout 启用
- 不做真实写入
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## 2. 为什么现在必须先定义 shadow evaluation gate（写死理由）

当前已经具备：

- 真实最小写入代码（显式入口；不在默认路径）
- shadow observe-only adapter（no-op writers）
- dispatcher relevant-only 可挂 shadow 结果
- shadow verify 已通过，且主链回归验证通过
- `side_effects_released` 仍锁死为 `false`

但仍缺：

- 一个统一的 gate 去回答：“这些 shadow 结果是否足够稳定/一致，足以支持进入下一阶段受控真实试运行准备”

如果不先冻结 evaluation gate，后续最容易发生的错误是：

- “shadow 已接入且可观察”被误当成“可以试运行真实写入”

因此必须先冻结 evaluation gate，再决定是否进入下一阶段受控试运行准备。

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation shadow evaluation gate` 是：

- 基于 **shadow observe-only** 结果与一致性信息的 **下一阶段资格判断门**
- 只负责判断是否允许进入下一阶段“受控真实试运行前评估”
- **不直接执行任何真实写入**

---

## 4. 最小合法输入（写死；只允许标准对象）

evaluation gate 只允许消费（标准化对象）：

- `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0`
- real-write go/no-go gate（必须 == go）：
  - `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0`
- live code path dry-run（必须 == executed）：
  - `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0`
- live implementation non-effect wiring（必须 == wired_ready）：
  - `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0`
- live implementation dry-run execution（必须 == executed）：
  - `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0`
- activation / commit / pre-commit / launch / admission 全链路对象（必须 admitted/ready）
- `side_effects_released == false`
- shadow approval / evaluation signal（默认不开；语义在位）：
  - `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_signal_v0`
- 可选但推荐：现有 gate / dry-run 结果对象（用于一致性判断；仍只读）

并明确（写死）：

- 缺任一主前提，evaluation gate 不成立（不得输出 go）
- 禁止读取 `request_* / approved_* / raw metadata`

---

## 5. 最小结果集合（三态；写死）

evaluation gate 输出三态（写死）：

- `first_live_minimal_real_effect_shadow_eval_go`
- `first_live_minimal_real_effect_shadow_eval_no_go`
- `first_live_minimal_real_effect_shadow_eval_blocked`

并写死语义：

- `shadow_eval_go` 只表示：shadow 结果足以支持进入下一阶段“受控真实试运行前评估”
- 不表示真实写入已发生
- 不表示 rollout 已开启
- 不表示 `side_effects_released` 已打开

---

## 6. 最小评估依据（写死）

当且仅当以下条件满足时，才允许 `shadow_eval_go`：

- shadow 对象存在且：
  - `shadow_status == shadow_executed`
  - `side_effects_released == false`
  - `would_have_entered_real_write == true`
  - would-have 三类写入标记符合预期（至少 state/result 为 true；异常写入标记为 true 时必须可解释）
- blocked / not_ready 原因必须可解释（不得是“缺主前提仍执行”）
- 与现有 gate / dry-run 不冲突；若冲突必须可解释（例如上游已明确 no-go / not_ready）
- 上游关键前提同时满足：
  - go/no-go == go
  - live code path dry-run == executed
  - live implementation wiring == wired_ready
  - live implementation dry-run execution == executed
  - admission/launch/pre-commit/commit/activation 链路均 admitted/ready

---

## 7. 明确禁止（写死）

evaluation gate 不允许：

- 打开 `side_effects_released`
- 执行真实写入
- 改变主链输出
- route / voice / memory / migration
- rollback / interrupt
- 默认开启 rollout
- 越过标准对象吐散字段
- 将 `shadow_eval_go` 当作“真实试运行已开启/已执行”

---

## 8. 与现有链路关系（写清）

- 与 shadow integration：shadow integration 负责 observe-only 接入并产出 shadow 对象；evaluation gate 负责判断 shadow 结果是否足以支持进入下一阶段
- 与 rollout plan：rollout plan 定未来试运行策略；evaluation gate 是进入试运行准备前的 shadow 评估门
- 与 real-write go/no-go gate：go/no-go gate 定未来是否允许开始真实写入；evaluation gate 定 shadow 结果是否足以支持进入下一阶段试运行准备

---

## 9. 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实写入
- 不允许真实 rollout
- 不允许真实 rollback / interrupt
- 不允许 route / voice / memory / migration
- 不允许把 `shadow_eval_go` 当作真实试运行已开启

---

## 10. 当前不做（写死）

- 不做 evaluation gate 的代码实现（除非边界已足够清晰且同轮落最小实现）
- 不做真实试运行开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 11. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - shadow evaluation gate minimal implementation
- 再之后才考虑：
  - 是否进入受控真实试运行
- 当前不直接启用真实写入

