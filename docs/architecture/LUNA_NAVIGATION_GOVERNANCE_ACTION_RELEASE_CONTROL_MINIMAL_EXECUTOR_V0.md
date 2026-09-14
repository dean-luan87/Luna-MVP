# Luna — Navigation Governance Action Release Control Minimal Executor v0（子动作最小真实执行器：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_V0.md`  
**性质**：Phase-Next-67：冻结 `release_control` 子动作未来第一类最小真实执行器边界（不落代码、不触发真实动作）

基于（已具备）：
- `release_control` 最小定义冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_DEFINITION_V0.md`
- `release_control` skeleton：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SKELETON_V0.md`
- 输入契约（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`
- 状态对象（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- readiness / wiring（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_IMPLEMENTATION_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_IMPLEMENTATION_V0.md`
- execution state（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`
- result object（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`
- executor input bridge（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_V0.md`
- executor input bridge（最小非动作实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_IMPLEMENTATION_V0.md`
- minimal runtime contract（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`
- minimal runtime stub（不可执行占位）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_STUB_V0.md`
- minimal live execution definition（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_LIVE_EXECUTION_DEFINITION_V0.md`
- guarded live stub（准 live 态受控 stub）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_GUARDED_LIVE_STUB_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 子动作**最小真实执行器**的设计文档。
- 当前目标：冻结 `release_control` 第一类真实动作执行器边界（可冻结、可回归）。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在必须先定义 minimal executor

- 当前已经有：`release_control input / status / readiness / wiring / execution state / result object`。
- 但还没有一个明确的“谁来真正执行 `release_control`”的边界定义。
- 如果不先定义 executor，后续很容易把 skeleton、status、result、wiring 混成一个模糊执行体，导致职责漂移与越权扩张。
- 因此必须先冻结 `release_control minimal executor` 的职责边界与输入输出面。

---

## C. minimal executor 的最小定义（写死）

`release_control minimal executor` 是：

- 未来第一类真实治理动作的**最小执行单元**
- 只负责“控制权交还上游控制面”这一件事的执行边界

它不是（写死）：

- `rollback` 执行器
- `interrupt` 执行器
- 路线改写器
- 语音播报器
- 记忆写入器
- 中台迁移逻辑本身
- 总治理动作执行器本体

核心定义（建议写死一句）：

> `release_control minimal executor` 只负责执行“控制权交还”这一类最小动作，并通过 `execution state / result object / exception path` 回传其执行过程与结果。

---

## D. 在系统中的位置（写死）

它应位于：

- `release_control input / readiness / wiring` 之后
- `release_control execution state / result object` 的产出责任位之前
- 治理链 / 中台消费层之前

并写清（写死）：

- 它不是 input contract
- 不是 readiness gate
- 不是 wiring
- 不是 execution state 本身
- 不是 result object 本身
- 它是“未来产生这些回传面的最小执行单元”

---

## E. 最小合法输入（写死：只允许消费标准化对象）

只允许消费（缺任何一个主前提都不应进入真实执行）：

1) **implemented** `navigation_governance_action_release_control_input_v0`  
- 主输入  
- 动作类型必须明确为 `release_control`

2) **implemented** `navigation_governance_action_release_control_execution_state_v0`  
- 执行过程回传面在位性依据（对象边界必须在位）

3) **implemented** `navigation_governance_action_release_control_result_v0`  
- 最终结果回传面在位性依据（对象边界必须在位）

4) `navigation_governance_action_release_control_readiness_gate_v0`  
- 必须为 `ready_candidate`

5) `navigation_governance_action_release_control_wiring_v0`  
- 必须为 `wired_inactive` 或 `wired_action_ready`

6) `release_control executor/skeleton identity / capability`  
- 本体在位性与能力边界依据（必须可证明“只做 release_control、且不具备其它真实动作能力”）

可选只读（仅一致性观测；不得扩权）：

- **implemented** `navigation_governance_action_approval_status_v0`
- **implemented** `navigation_governance_action_executor_wiring_v0`

禁止（写死）：

- 禁止直接读取 `request_* / approved_* / raw metadata` 作为执行主输入。

---

## F. 最小输出 / 回传面（写死）

minimal executor 的最小输出不是“随便返回一个结果”，而应至少包括：

1) **execution state**（执行过程回传面）  
2) **result object**（最终结果回传面）  
3) **exception / failure reporting path**（异常/失败上报通道）  

并写清（写死）：

- 未来真实执行时，`execution state` 与 `result object` 都必须走标准化对象。
- 不允许只吐散字段。

---

## G. 最小执行结果集合（仅语义定义；写死克制）

建议最小执行结果集合（仅语义，不落代码）：

- `execution_started`
- `execution_blocked`
- `execution_failed`
- `execution_completed`

并写清（写死）：

- 这是 executor 自身的最小执行结果语义，不等于最终中台迁移已完成。
- `execution_completed` 不等于路线改变或其它动作发生。

---

## H. 最小状态约束（写清）

- `execution_started` 不等于控制权已完成交还。
- `execution_completed` 不等于中台迁移已完成。
- `execution_failed` 不等于 `rollback` / `interrupt` 自动补偿已发生。

---

## I. 不负责什么（必须写死）

- 不负责 `rollback`
- 不负责 `interrupt`
- 不负责改路线
- 不负责语音播报
- 不负责记忆写入
- 不负责中台迁移逻辑本身
- 不负责批准逻辑
- 不负责 readiness / wiring 判断本身

---

## J. 当前仍然不能做什么（必须写死）

- 不允许直接做真实 `release_control minimal executor` 实现
- 不允许借 executor 顺手做 `rollback` / `interrupt`
- 不允许触发地图、语音、记忆、中台真实迁移
- 不允许把定义文档当成执行器已实现

---

## K. 与现有链路的关系（写清）

与 `release_control skeleton`：
- skeleton 是当前不可执行壳子  
- minimal executor 是未来真实执行单元定义  
- 两者不能混用

与 `release_control input contract`：
- input contract 是执行前输入面  
- minimal executor 只应消费其定义好的最小输入面

与 `release_control readiness / wiring`：
- readiness / wiring 是进入执行前的门与接线  
- minimal executor 不替代它们

与 `release_control execution state / result object`：
- 这两个是未来执行器的标准回传面  
- minimal executor 应通过它们回传  
- 不允许跳过它们直接吐散字段

---

## L. 当前不做（必须写死）

- 不做 minimal executor 代码实现
- 不做真实 `release_control`
- 不做 `rollback` / `interrupt`
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## M. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - `release_control minimal executor` skeleton / placeholder / implementation
- 当前不直接跨到真实执行

补充（已进入下一步）：
- Phase-Next-68：`release_control minimal executor skeleton`（不可执行骨架）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_SKELETON_V0.md`

---

## N. 未来 minimal executor 责任样例（仅说明，不落代码）

```json
{
  "release_control_executor_scope": "navigation_governance_action_release_control_minimal_executor_v0",
  "consumes": [
    "navigation_governance_action_release_control_input_v0",
    "navigation_governance_action_release_control_execution_state_v0",
    "navigation_governance_action_release_control_result_v0"
  ],
  "produces": [
    "execution_state",
    "result_object",
    "exception_path"
  ]
}
```

