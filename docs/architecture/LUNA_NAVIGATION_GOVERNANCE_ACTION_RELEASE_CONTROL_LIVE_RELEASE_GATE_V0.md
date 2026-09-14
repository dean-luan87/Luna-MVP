# Luna — Navigation Governance Action Release Control Live Release Gate v0（受控 live 候选 → 真实 live 执行：放行门冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_V0.md`  
**性质**：Phase-Next-75：冻结从 guarded live stub 到第一版真实 live execution 的最后一道放行门（不落代码、不触发真实动作）

基于（已具备）：
- guarded live stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_GUARDED_LIVE_STUB_V0.md`
- minimal live execution definition：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_LIVE_EXECUTION_DEFINITION_V0.md`
- minimal runtime contract / stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_STUB_V0.md`
- minimal executor（冻结/骨架）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_SKELETON_V0.md`
- executor input bridge（冻结/最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_IMPLEMENTATION_V0.md`
- execution state / result（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 的 **live release gate** 设计文档。
- 当前目标：冻结从 guarded live stub 到真实 live execution 的最后一道放行门。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在必须先定义 live release gate

- 当前已经有 guarded live stub，可进入 live candidate，但 side effects 仍被写死锁住。
- 若没有单独的 release gate，后续“谁来决定何时打开真实 side effect”会变得不清晰，且 `consumable_by_executor/entered_real_live_execution/side_effects_released` 会被不同模块各自解释，边界变脏。
- 因此必须先冻结最后一道放行门，再考虑是否真的打开 live execution。

---

## C. live release gate 的最小定义（写死）

`release_control live release gate` 是：

- guarded live stub 之后、真实 live execution 之前的最后一道放行门
- **只负责判断**是否允许放开真实 side effect（进入第一版真实最小执行线）

它不是（写死）：

- guarded live stub 本身
- minimal executor 本身
- runtime contract 本身
- 真实执行器本身
- `rollback` / `interrupt` gate

核心定义（建议写死一句）：

> live release gate 只决定“可否放行真实 live execution”，不直接执行任何动作。

---

## D. 最小合法输入（写死：只允许消费）

只允许消费（缺任一主前提，release gate 不成立）：

1) `navigation_governance_action_release_control_executor_input_bridge_v0`  
- 必须 `bridge_status == "executor_input_bridge_ready"`

2) guarded live stub 状态  
- 必须已进入 candidate  
- 且 `side_effects_released == false`

3) `navigation_governance_action_release_control_execution_state_v0`  
- 回传面在位

4) `navigation_governance_action_release_control_result_v0`  
- 回传面在位

5) minimal executor / guarded live stub identity / capability  
- 本体在位与能力边界依据

可选只读（仅一致性观测，不得扩权）：

- `navigation_governance_action_release_control_readiness_gate_v0`
- `navigation_governance_action_release_control_wiring_v0`

禁止（写死）：

- 禁止直接读取 `request_* / approved_* / raw metadata` 作为 gate 主输入。

---

## E. 最小结果集合（写死最小集合）

最小结果集合（建议写死为 3 态）：

- `live_release_ready`
- `live_release_not_ready`
- `live_release_blocked`

语义（写死）：

1) `live_release_ready`
- 仅表示：允许进入第一版真实最小执行线  
- 不表示动作已经执行  
- 不表示 side effect 已发生

2) `live_release_not_ready`
- 当前前提不足  
- 不允许放开真实执行

3) `live_release_blocked`
- 当前存在硬阻断 / identity 问题 / 一致性问题  
- 明确不允许进入真实执行

---

## F. 明确禁止（必须写死）

live release gate 不允许直接：

- 执行真实 `release_control`
- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback` / `interrupt`
- 越过标准对象吐散字段

---

## G. 与现有链路的关系（写清）

与 guarded live stub：
- guarded live stub 负责承载 live candidate  
- live release gate 负责决定是否允许放开真实 side effect  
- 两者不能混用

与 executor input bridge：
- bridge 负责形成最终执行输入包  
- live release gate 负责决定是否放行  
- bridge ready **不等于** release ready

与 runtime contract / live execution definition：
- runtime contract 规定运行态内边界  
- live execution definition 规定第一版真实执行边界  
- release gate 是进入这条真实执行线前的最后一道门

---

## H. 当前仍然不能做什么（必须写死）

- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许改路线
- 不允许语音/记忆/中台迁移
- 不允许把 `live_release_ready` 当动作已开始

---

## I. 当前不做（必须写死）

- 不做 live release gate 代码实现
- 不做真实 `release_control`
- 不做 `rollback` / `interrupt`
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - live release gate 的 minimal implementation
- 再之后才考虑：
  - 第一版真实 live implementation
- 当前不跨这两步

补充（已进入下一步）：
- Phase-Next-76：`live release gate minimal implementation`：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_IMPLEMENTATION_V0.md`

下一步（放权合同冻结）：
- Phase-Next-77：`side-effect release contract`（副作用放权合同冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_CONTRACT_V0.md`

