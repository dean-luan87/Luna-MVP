# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Admission Gate v0（最终准入门：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ADMISSION_GATE_V0.md`  
**性质**：Phase-Next-99：冻结 `release_control first live guarded implementation minimal real-effect` 的 **最终准入门**（只定义准入边界，不落实现；可冻结、可回归）

基于（已具备）：
- implementation definition v0（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_DEFINITION_V0.md`
- implementation skeleton v0（冻结 + 落代码）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_V0.md`
- implementation dry-run execution v0（冻结 + 最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_DRY_RUN_EXECUTION_V0.md`
- minimal real-effect plan v0（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_PLAN_V0.md`
- minimal real-effect stub / wiring / dry-run execution（已落地）
- dry-effect simulation（已落地）
- approval/launch/live/side-effect release gates（已落地）
- standard objects：`execution_state_v0` / `result_v0`

---

## A. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation minimal real-effect` 的 **最终准入门（admission gate）** 设计冻结文档。
- 当前目标：冻结“从 implementation dry-run execution 到第一版真实最小写入实现”的最终准入边界：谁来准入、准入前必须满足什么、准入结果是什么、准入本身不能做什么。

并且（本轮写死边界）：

- 当前**不做 admission gate 代码实现**。
- 当前不做真实最小写入实现（不落真实 real-effect implementation）。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。
- 当前 `side_effects_released` 仍强制锁死为 `false`（不允许打开）。

---

## B. 为什么现在必须先定义 admission gate（写死理由）

- 当前已经有 implementation definition（定义未来真实写入层边界）。
- 当前已经有 implementation non-effect wiring（证明合法入口收束成立）。
- 当前已经有 implementation dry-run execution（证明未来实现层的调用顺序可在零副作用模式跑通）。
- 但还没有一个明确的“谁来最终准入第一版最小真实写入实现”的门。
- 如果不先定义 admission gate，后续很容易把 `implementation_dry_run_executed` 误当成“可以直接进入真实写入”，导致放权失控与语义混乱。

因此必须先冻结最终准入门，再考虑是否真的进入第一版最小真实写入实现。

---

## C. admission gate 的最小定义（写死）

`release_control first live guarded implementation minimal real-effect admission gate` 是：

- implementation dry-run execution 之后、真实第一版最小写入实现之前的最终准入门
- 只负责判断“是否准入第一版最小真实写入实现”

它不是：

- implementation definition 本身
- implementation dry-run execution 本身
- live release gate 本身
- side-effect release gate 本身
- 真实执行器本身
- rollback / interrupt 审批门

核心定义（写死一句）：

> admission gate 只决定“是否准入第一版最小真实写入实现”，不直接执行任何动作，也不直接打开 `side_effects_released`。

---

## D. 最小合法输入（写死；只允许标准化对象）

admission gate 只允许消费（只读）：

1) `first_live_enablement_approval_gate_v0`
   - 必须 `approval_status == "first_live_enablement_approved"`
2) `first_live_launch_dry_run_v0`
   - 必须 `launch_status == "first_live_launch_dry_run_ready"`
3) `live_release_gate_v0`
   - 必须 `live_release_status == "live_release_ready"`
4) `side_effect_release_gate_v0`
   - 必须 `side_effect_release_status == "side_effect_release_ready"`
5) `first_live_guarded_implementation_dry_effect_simulation_v0`
   - 必须 `simulation_status == "first_live_guarded_dry_effect_simulated"`
6) `first_live_guarded_implementation_minimal_real_effect_wiring_v0`
   - 必须 `wiring_status == "first_live_minimal_real_effect_wired_ready"`
7) `first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0`
   - 必须 `execution_status == "first_live_minimal_real_effect_implementation_dry_run_executed"`
8) `execution_state_v0` 与 `result_v0`
   - 回传面在位
9) `side_effects_released`
   - 必须仍为 `false`
10) 明确的准入主体 / 准入信号（语义在位）
   - 必须存在
   - 当前只做语义定义，不实现来源机制
11) implementation skeleton identity / capability
   - 本体在位与能力边界依据（必须保守、不可越权）

并明确（写死）：

- 缺任一主前提，admission gate 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata` 作为输入来源。

---

## E. 最小结果集合（写死；三态）

admission gate 的结果必须收敛成最小集合：

- `first_live_minimal_real_effect_admitted`
- `first_live_minimal_real_effect_not_admitted`
- `first_live_minimal_real_effect_blocked`

语义（写死）：

1) `first_live_minimal_real_effect_admitted`
- 仅表示：允许进入第一版最小真实写入实现
- 不表示真实写入已经发生
- 不表示副作用已经发生
- 不表示 `side_effects_released` 已经变成 `true`

2) `first_live_minimal_real_effect_not_admitted`
- 当前准入信号缺失或条件未满足
- 不允许进入真实最小写入实现

3) `first_live_minimal_real_effect_blocked`
- 当前存在硬阻断 / 身份问题 / 一致性问题
- 明确不允许进入真实最小写入实现

---

## F. 明确禁止（写死）

admission gate 不允许直接：

- 打开 `side_effects_released`
- 执行真实 `release_control`
- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback` / `interrupt`
- 越过标准对象吐散字段

---

## G. 与现有链路的关系（写清；不能混用）

与 implementation dry-run execution：

- dry-run execution 负责演练未来真实实现层的调用顺序（零副作用）。
- admission gate 负责最终判断是否允许进入第一版最小真实写入实现。
- 两者不能混用。

与 live release gate / side-effect release gate：

- 它们负责资格与放权资格（就绪/放权门控）。
- admission gate 负责“是否准入真实最小写入实现”。
- `live_release_ready` 或 `side_effect_release_ready` 都不等于 `admitted`。

与 implementation definition / plan：

- definition 定义真实实现层边界（进入前提/允许面/禁止面/顺序）。
- plan 定义第一版最小真实副作用如何落地（仍需受控）。
- admission gate 只负责“是否准入这一层”，不替代 definition / plan。

---

## H. 当前仍然不能做什么（写死）

- 不允许现在就把 `side_effects_released` 打开。
- 不允许真实 `release_control`。
- 不允许真实 `rollback` / `interrupt`。
- 不允许 route / voice / memory / migration。
- 不允许把 `first_live_minimal_real_effect_admitted` 当作真实写入已发生。

---

## I. 当前不做（写死）

- 不做 admission gate 代码实现。
- 不做真实最小写入实现。
- 不做地图接入。
- 不做语音/记忆联动。
- 不做中台真实迁移。

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - minimal real-effect admission gate 的 minimal implementation
- 再之后才考虑：
  - 第一版最小真实写入实现方案
- 当前不直接落真实实现。

补充链接（最终放行门：设计冻结）：

- Phase-Next-102：Minimal Real-Effect Guarded Launch Gate v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_GUARDED_LAUNCH_GATE_V0.md`

---

## K. 未来样例（仅说明，不落代码）

```json
{
  "release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0",
  "admission_status": "first_live_minimal_real_effect_admitted|first_live_minimal_real_effect_not_admitted|first_live_minimal_real_effect_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

