# Luna — Navigation Governance Action Release Control Side-Effect Release Contract v0（副作用放权合同：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_CONTRACT_V0.md`  
**性质**：Phase-Next-77：冻结 `side_effects_released` 从默认锁死到未来受控打开的放权合同（不落代码、不触发真实动作）

基于（已具备）：
- live release gate（冻结/最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_IMPLEMENTATION_V0.md`
- guarded live stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_GUARDED_LIVE_STUB_V0.md`
- minimal live execution definition：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_LIVE_EXECUTION_DEFINITION_V0.md`
- minimal runtime contract / stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_STUB_V0.md`
- executor input bridge（冻结/最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_IMPLEMENTATION_V0.md`
- execution state / result（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 第一版真实最小执行前的 **side-effect release 合同**文档。
- 当前目标：冻结“何时允许从 gate ready 走到真实 side effect 放开”的规则。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为（不改 route/proposal）。

---

## B. 为什么现在必须先定义 side-effect release contract

- 当前已有 live release gate minimal implementation，但 `side_effects_released` 仍被锁死为 `false`。
- `live_release_ready` 只代表“最后一道放行门判断通过”，**不等于**“真实副作用已允许”。
- 若不单独定义 release contract，后续很容易把 gate ready 误当成 side effect 已经可以放开，导致越权与不可回归。
- 因此必须先冻结“从 ready 到真正 release 的合同”。

---

## C. side-effect release contract 的最小定义（写死）

`release_control side-effect release contract` 是：

- 约束 `side_effects_released` 何时允许从 `false` 变为未来受控 `true` 的最小放权合同
- 只负责定义放权条件与允许 side effect 范围

它不是（写死）：

- live release gate 本身
- runtime contract 本身
- minimal executor 本身
- 真正的 `release_control` 实现
- `rollback` / `interrupt` 放权合同

核心定义（建议写死一句）：

> live release gate 决定“是否具备进入真实执行线的资格”，side-effect release contract 决定“是否允许真正放开副作用”。

---

## D. 最小进入前提（写死）

建议最小进入前提至少包括：

1) `navigation_governance_action_release_control_live_release_gate_v0.live_release_status == "live_release_ready"`  
2) guarded live stub 已 `entered candidate`  
3) `side_effects_released == false`（仍处锁死态）  
4) `execution_state_v0` 在位  
5) `result_v0` 在位  
6) minimal executor identity / capability 合法且保守  
7) runtime contract 已定义  

并写清（写死）：

- 少任一项，不得打开 `side_effects_released`。
- 当前阶段只是冻结规则，不允许真的打开。

---

## E. 最小允许放开的 side effect 范围（写死极克制）

未来若允许放开 side effect，第一版最多只允许：

1) `execution state` 的真实推进  
2) `result object` 的真实写入  
3) `exception / failure path` 的真实写入  

并写死：

- 任何超出范围的 side effect 仍然禁止。

---

## F. 明确永久禁止或当前阶段禁止的 side effect（必须写死）

即使未来 `side_effects_released` 打开，当前阶段仍禁止：

- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback`
- 自动触发 `interrupt`
- 越过标准对象吐散字段
- 读取地图 / 路径规划字段作为执行副作用来源

---

## G. 最小放权结果集合（写死最小集合）

最小放权结果集合（建议写死为 3 态）：

- `side_effect_release_ready`
- `side_effect_release_not_ready`
- `side_effect_release_blocked`

并写清（写死）：

- `ready` 只表示“允许进入第一版真实 side-effect 验证线”，不表示业务完成，也不表示控制权交还已完成。

---

## H. 放权后的最小顺序（写死）

一旦未来允许打开 side effect，顺序必须仍然是：

1) 先推进 `execution state`  
2) 再写 `result object`  
3) 再走 `exception / failure path`  
4) 再交还治理链  

并写死：

- 不允许反过来。
- 不允许先做迁移、再补状态。

---

## I. 与现有链路的关系（写清）

与 live release gate：
- gate 决定“最后一道门是否 ready”  
- release contract 决定“ready 之后是否允许真正放开 side effect”  
- `live_release_ready` **不等于** `side_effects_released=true`

与 runtime contract：
- runtime contract 规定 runtime 内顺序与禁止面  
- release contract 规定是否允许真正启用 runtime side effect  
- 两者不能混用

与 execution state / result object：
- 这两个是未来放开 side effect 后，唯一允许被真实写入的标准面  
- release contract 不允许绕过它们

---

## J. 当前仍然不能做什么（必须写死）

- 不允许现在就把 `side_effects_released` 打开
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许改路线
- 不允许语音/记忆/中台迁移
- 不允许把合同当实现

---

## K. 当前不做（必须写死）

- 不做 release contract 代码实现
- 不做真实 `release_control`
- 不做 `rollback` / `interrupt`
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## L. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - side-effect release contract 的 minimal implementation
- 再之后才考虑：
  - 第一版真实 live implementation
- 当前不跨这两步

补充（已进入下一步）：
- Phase-Next-78：`side-effect release gate minimal implementation`：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_GATE_IMPLEMENTATION_V0.md`

下一步（启用方案冻结）：
- Phase-Next-79：`first live enablement plan`（第一次真实放权试运行启用方案冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_PLAN_V0.md`

下一步（干跑承载位）：
- Phase-Next-80：`first live enablement dry-run stub`（试运行启用流程干跑 stub）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_DRY_RUN_STUB_V0.md`

下一步（最终批准门冻结）：
- Phase-Next-81：`first live enablement approval gate`（第一次真实放权试运行最终批准门冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_V0.md`

下一步（最终批准门最小实现）：
- Phase-Next-82：`first live enablement approval gate minimal implementation`（第一次真实放权试运行最终批准门最小非动作实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_IMPLEMENTATION_V0.md`

下一步（最终发车演练层）：
- Phase-Next-83：`first live launch dry-run`（批准通过后的最终发车演练层冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_LAUNCH_DRY_RUN_V0.md`
- Phase-Next-83：`first live launch dry-run minimal implementation`（最终发车演练层最小非动作实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_LAUNCH_DRY_RUN_IMPLEMENTATION_V0.md`

