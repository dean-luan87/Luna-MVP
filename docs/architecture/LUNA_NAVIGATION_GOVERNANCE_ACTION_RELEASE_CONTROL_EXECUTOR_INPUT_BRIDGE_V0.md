# Luna — Navigation Governance Action Release Control Executor Input Bridge v0（最小执行器最终输入桥接层：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_V0.md`  
**性质**：Phase-Next-69：冻结 `release_control minimal executor` 未来唯一允许消费的最终执行输入桥接层（不落代码、不触发真实动作）

基于（已具备）：
- minimal executor 定义/骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_SKELETON_V0.md`
- input contract（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`
- readiness / wiring（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_IMPLEMENTATION_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_IMPLEMENTATION_V0.md`
- execution state（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`
- result object（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`
- minimal runtime contract（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control minimal executor` 的**执行输入桥接层**设计文档。
- 当前目标：冻结“执行器最终输入消费面”的边界（可冻结、可回归）。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在必须先定义 executor input bridge

- 当前已经有：input contract / readiness / wiring / execution state / result object / minimal executor skeleton。
- 但还没有一个明确的“最小执行器最终消费输入包”边界。
- 如果不先定义 bridge，后续 minimal executor 很容易直接读取多个对象并自行拼装输入，导致职责重新混掉（桥接、门控、执行混为一体）。
- 因此必须先冻结 `executor input bridge`：明确“执行器只认一个收束后的最终输入包”。

---

## C. executor input bridge 的最小定义（写死）

`release_control executor input bridge` 是：

- 把 `release_control` 前置对象链收束成 `minimal executor` **唯一允许消费**的最终执行输入包的桥接层

它不是（写死）：

- input contract 本身
- readiness gate 本身
- wiring 本身
- execution state 本身
- result object 本身
- minimal executor 本身
- 真实执行器

核心定义（建议写死一句）：

> `release_control minimal executor` **只允许消费 bridge 收束后的最终输入包**，不允许直接拼读上游多个对象。

---

## D. 最小合法输入来源（写死：只允许桥接这些来源）

bridge 只允许桥接以下来源（缺任一主前提，bridge 不成立）：

1) **implemented** `navigation_governance_action_release_control_input_v0`
2) **implemented** `navigation_governance_action_release_control_execution_state_v0`
3) **implemented** `navigation_governance_action_release_control_result_v0`
4) `navigation_governance_action_release_control_readiness_gate_v0`（必须 `ready_candidate`）
5) `navigation_governance_action_release_control_wiring_v0`（必须 `wired_inactive|wired_action_ready`）
6) `release_control minimal executor identity / capability`（本体在位与能力边界依据）

可选只读一致性来源（不得扩权）：

- **implemented** `navigation_governance_action_approval_status_v0`
- **implemented** `navigation_governance_action_executor_wiring_v0`

写死：
- 这些是 bridge 的合法输入来源，**不是执行器直接读取来源**。

---

## E. 最小桥接结果集合（写死最小集合）

bridge 最小桥接结果集合（建议写死为最小 3 态）：

- `executor_input_bridge_ready`
- `executor_input_bridge_not_ready`
- `executor_input_bridge_blocked`

语义（写死）：

1) `executor_input_bridge_ready`
- 仅表示：最终执行输入包已可形成，未来 minimal executor 可合法消费  
- **不表示**动作已开始

2) `executor_input_bridge_not_ready`
- 当前仍有前提不足  
- 不允许进入真实执行

3) `executor_input_bridge_blocked`
- 当前存在硬阻断 / 一致性问题 / identity 问题  
- 明确不允许进入真实执行

---

## F. bridge 最小输出语义（写死）

- bridge 输出的不是最终结果
- 不是执行状态
- 不是动作本身
- 只是“最终执行输入包是否已可形成”的判断与桥接结果

---

## G. 明确禁止（必须写死）

`release_control minimal executor` **不得直接读取**：

- 任意 `request_*`
- 任意 `approved_*` 散字段
- 任意 raw metadata
- 任意地图 / 路径规划字段
- 任意语音输出字段
- 任意记忆写入字段
- 任意 `rollback` / `interrupt` 专属字段
- 任意中台迁移执行字段

并写清（写死）：

- 这些都必须被 bridge 层挡在外面
- 执行器只认 bridge 收束后的最终输入包

---

## H. 与现有链路的关系（写清）

与 input contract：
- input contract 是前置输入面  
- bridge 是执行器最终消费输入面  
- 两者不能混用

与 readiness / wiring：
- readiness / wiring 提供进入执行前的一致性与接线依据  
- bridge 负责把它们收束进最终执行输入包  
- 它们不直接等于 executor input bridge

与 execution state / result object：
- 这两个是回传面  
- bridge 只负责保证这些回传面在位且一致  
- bridge 不替代回传面

与 minimal executor skeleton：
- minimal executor skeleton 未来只应消费 bridge 输出  
- 当前 skeleton 不执行真实动作

---

## I. 当前仍然不能做什么（必须写死）

- 不允许真实 `release_control`
- 不允许借 bridge 顺手做 `rollback` / `interrupt`
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 `executor_input_bridge_ready` 当动作已开始

---

## J. 当前不做（必须写死）

- 不做 bridge 代码实现
- 不做真实 `release_control`
- 不做 `rollback` / `interrupt`
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## K. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - `release_control executor input bridge` placeholder / implementation
- 再之后才考虑：
  - `release_control minimal executor` 最小真实实现
- 当前不跨这两步

---

## L. 未来 bridge 样例（仅说明，不落代码）

```json
{
  "release_control_executor_input_bridge_scope": "navigation_governance_action_release_control_executor_input_bridge_v0",
  "bridge_status": "executor_input_bridge_ready|executor_input_bridge_not_ready|executor_input_bridge_blocked",
  "consumable_by_executor": false,
  "reason": "..."
}
```

