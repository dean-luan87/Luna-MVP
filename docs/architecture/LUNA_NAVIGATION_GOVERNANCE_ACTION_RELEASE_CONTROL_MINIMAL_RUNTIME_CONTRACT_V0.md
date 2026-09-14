# Luna — Navigation Governance Action Release Control Minimal Runtime Contract v0（最小运行时合同：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`  
**性质**：Phase-Next-71：冻结 `release_control minimal executor` 进入运行态后的最小运行时合同（不落代码、不触发真实动作）

基于（已具备）：
- minimal executor（冻结/骨架）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_SKELETON_V0.md`
- executor input bridge（冻结/最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_IMPLEMENTATION_V0.md`
- input contract（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`
- status object（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- readiness / wiring（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_IMPLEMENTATION_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_IMPLEMENTATION_V0.md`
- execution state（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`
- result object（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control minimal executor` 的最小运行时合同文档。
- 当前目标：冻结第一类真实治理动作进入 runtime 前后的边界。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在必须先定义 runtime contract

- 当前已经有：bridge / input / execution state / result / readiness / wiring / minimal executor skeleton。
- 但还没有一份明确约束“真正开始执行的那一刻到底意味着什么”的运行时合同。
- 如果不先冻结 runtime contract，后续真实实现会把执行起点、状态推进、失败收口、允许 side effect 混在一起，导致不可回归。
- 因此必须先写死 runtime contract，再考虑第一版真实最小实现。

---

## C. runtime contract 的最小定义（写死）

`release_control minimal runtime contract` 是：

- 约束 `release_control minimal executor` 进入运行态、推进执行态、回传结果态、异常收口的最小运行时合同

它不是（写死）：

- input contract 本身
- readiness gate 本身
- wiring 本身
- execution state 本身
- result object 本身
- executor input bridge 本身
- 真正的业务动作实现代码

核心定义（建议写死一句）：

> runtime contract 只规定“何时允许进入 runtime、runtime 中可做什么、结束后必须回什么”，不直接替代执行器实现。

---

## D. 进入 runtime 的最小前提（写死）

进入 runtime 的最小前提建议至少包括：

1) `navigation_governance_action_release_control_executor_input_bridge_v0.bridge_status == "executor_input_bridge_ready"`  
2) `consumable_by_executor` 在未来真实实现线中才允许从 `false` 打开；**当前 v0 仍不打开**  
3) `release_control minimal executor identity / capability` 合法  
4) `navigation_governance_action_release_control_execution_state_v0` 在位  
5) `navigation_governance_action_release_control_result_v0` 在位  

并写清（写死）：

- 这些前提不成立，不得进入 runtime。
- 当前阶段只是冻结规则，不允许把这些门控真的打开。

---

## E. runtime 最小状态推进顺序（只定义合同顺序，不实现）

建议最小状态推进顺序（合同）：

- `not_started`
- `execution_started`
- `execution_completed`
- `execution_failed`

并写清（写死）：

- `execution_started` 不等于控制权已完成交还。
- `execution_completed` 不等于中台迁移完成。
- 不允许跳过 `execution state` 直接写最终 `result object`。

---

## F. runtime 内最小允许动作面（写死极克制）

runtime 内最小允许动作面只允许：

1) 更新 `execution state`  
2) 更新 `result object`  
3) 进入 `exception / failure reporting path`  

并写清（写死）：

- 这是最小运行时允许面，其余都先禁止。

---

## G. runtime 内明确禁止动作面（必须写死）

当前 runtime 不允许直接：

- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback`
- 自动触发 `interrupt`
- 越过标准对象直接吐散字段

---

## H. 失败收口合同（写死顺序）

当 runtime 失败时，最小收口顺序必须是：

1) 先写 `execution state`  
2) 再写 `result object`  
3) 再走 `exception / failure path`  
4) 再把处置权交还治理链  

并写清（写死）：

- 失败后不允许执行器自行决定 `rollback` / `interrupt`。
- 不允许跳过标准化回传对象直接结束。

---

## I. 最小真实实现的定义（写死）

`release_control` 的“最小真实实现”只允许验证：

- executor 是否能在合同约束下进入 runtime
- `execution state` 是否能按顺序推进
- `result object` 是否能按顺序写出
- `failure path` 是否能按顺序收口

并写清（写死）：

- 不允许把“最小真实实现”扩成完整业务动作。
- 不允许顺手接入地图/语音/记忆/中台迁移。

---

## J. 与现有链路的关系（写清）

与 input contract / bridge：
- input contract / bridge 负责执行前输入成立与收口  
- runtime contract 负责真正进入执行后的行为边界

与 readiness / wiring：
- readiness / wiring 负责进入执行前的门与接线  
- runtime contract 负责进入执行后的状态推进与收口

与 execution state / result object：
- 它们是 runtime 中必须使用的标准化回传面  
- runtime contract 规定必须通过它们回传  
- 不允许绕过它们

与 minimal executor skeleton：
- skeleton 是未来 executor 的骨架  
- runtime contract 是未来 executor 的运行时约束  
- 两者不能混用

---

## K. 当前仍然不能做什么（必须写死）

- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 runtime contract 当成 runtime 已实现

---

## L. 当前不做（必须写死）

- 不做 runtime contract 代码实现
- 不做真实 `release_control`
- 不做 `rollback` / `interrupt`
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## M. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - `release_control minimal runtime` skeleton / stub
- 再之后才考虑：
  - `release_control` 第一版最小真实实现
- 当前不跨这两步

补充（已进入下一步）：
- Phase-Next-72：`release_control minimal runtime stub`（不可执行占位）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_STUB_V0.md`

下一步（定义冻结之后的下一层）：
- Phase-Next-73：`release_control minimal live execution definition`（第一版真实最小执行定义冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_LIVE_EXECUTION_DEFINITION_V0.md`
- Phase-Next-74：`release_control guarded live stub`（准 live 态受控 stub）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_GUARDED_LIVE_STUB_V0.md`

---

## N. 未来 runtime contract 样例（仅说明，不落代码）

```json
{
  "release_control_runtime_contract_scope": "navigation_governance_action_release_control_minimal_runtime_contract_v0",
  "runtime_entry_conditions": [
    "executor_input_bridge_ready",
    "execution_state_present",
    "result_object_present",
    "executor_identity_valid"
  ],
  "allowed_runtime_surfaces": [
    "execution_state",
    "result_object",
    "exception_path"
  ],
  "forbidden_runtime_surfaces": [
    "route_change",
    "voice_output",
    "memory_write",
    "mid_platform_real_migration"
  ]
}
```

