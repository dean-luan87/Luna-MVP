# Luna — Navigation Governance Action Release Control Executor Input Bridge Minimal Implementation v0（最终执行输入桥接对象：最小非动作实现）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-70：把 `release_control executor input bridge` 从设计冻结推进为统一对象的最小非动作实现（落代码；不触发真实动作）

关联：
- bridge 边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_V0.md`
- minimal executor（冻结/骨架）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_SKELETON_V0.md`
- input / execution state / result（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`
- readiness / wiring（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_IMPLEMENTATION_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control executor input bridge` 的最小非动作实现文档。
- 当前目标：把 bridge 从冻结文档推进到最小非动作实现（统一对象）。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不改变现有主线行为。

---

## B. 为什么现在要先实现 bridge

- `release_control input / execution state / result / readiness / wiring` 已在位（均为标准化对象）。
- `minimal executor skeleton` 已存在，但“最终唯一合法消费面”仍缺少**主链可观测的统一对象**。
- 若不先做最小实现，后续执行器实现会回到直接拼读多个对象，bridge 只停留在文档层，无法形成实际约束与白盒观测。
- 因此必须先把 bridge 对象实现出来。
- 但当前仍不能触发任何真实治理动作。

---

## C. implemented bridge 的最小定义（写死）

- 它不是真实 `release_control` 执行器。
- 不是真实批准链。
- 它是“`release_control minimal executor` 唯一允许消费的最终执行输入桥接对象”的最小非动作实现。
- 作用：把 `input / execution_state / result / readiness / wiring / executor identity` 统一收束为 `ready/not_ready/blocked` 三态结果。

---

## D. 当前最小输入依据（写死：只允许标准化对象）

主输入（缺任一则 bridge 不成立或 not_ready/blocked）：

1) implemented `navigation_governance_action_release_control_input_v0`
2) implemented `navigation_governance_action_release_control_execution_state_v0`
3) implemented `navigation_governance_action_release_control_result_v0`
4) `navigation_governance_action_release_control_readiness_gate_v0`（必须 `ready_candidate`）
5) `navigation_governance_action_release_control_wiring_v0`（必须 `wired_inactive|wired_action_ready`）
6) `release_control minimal executor identity / capability`（本体在位与能力边界依据）

可选只读一致性（不得扩权）：
- implemented `navigation_governance_action_approval_status_v0`
- implemented `navigation_governance_action_executor_wiring_v0`

禁止（写死）：
- 禁止直接读取 `request_* / approved_* / raw metadata` 作为 bridge 主输入。

---

## E. 当前最小输出位（写死）

写入：

- `result.metadata["navigation_governance_action_release_control_executor_input_bridge_v0"]`

最小结构：

```json
{
  "release_control_executor_input_bridge_attempted": true,
  "release_control_executor_input_bridge_scope": "navigation_governance_action_release_control_executor_input_bridge_v0",
  "bridge_status": "executor_input_bridge_ready|executor_input_bridge_not_ready|executor_input_bridge_blocked",
  "consumable_by_executor": false,
  "reason": "..."
}
```

写死：
- 不加时间/空间字段
- 不膨胀成复杂对象
- 只表达“最终执行输入包是否可形成”
- 即便 `bridge_status == executor_input_bridge_ready`，`consumable_by_executor` 也必须保持保守为 `false`

---

## F. 当前最小判断规则（写死克制）

- **规则 1（主来源对象缺失）**：`executor_input_bridge_not_ready`
- **规则 2（readiness != ready_candidate）**：`executor_input_bridge_not_ready`（保守口径）
- **规则 3（wiring 不在允许集合）**：`executor_input_bridge_blocked`
- **规则 4（minimal executor identity/capability 不合法）**：`executor_input_bridge_blocked`
- **规则 5（齐备但仍不允许真正消费）**：`consumable_by_executor=false`

---

## G. 当前最小语义（写死）

当 `navigation_governance_action_release_control_executor_input_bridge_v0` 被产出时，只表示：

- 系统已能统一判断 `release_control minimal executor` 的最终输入包是否已可形成
- 未来执行器只应消费该 bridge 输出

它不表示（写死）：
- 真实 `release_control` 已执行
- 控制权已真实交还
- 路线已改变
- 中台已真实迁移
- 动作已开始

---

## H. 当前不允许做什么（写死）

- 不允许真实 `release_control`
- 不允许借 bridge 顺手做 `rollback` / `interrupt`
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 `executor_input_bridge_ready` 当动作已开始
- 不允许把 `consumable_by_executor=false` 之外的状态伪装成可真实执行

---

## I. 代码落点（本轮落地）

- Builder：`capabilities/mid_platform/runtime/navigation_governance_action_release_control_executor_input_bridge_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`
- minimal executor skeleton recognize-only：`capabilities/governance/runtime/navigation_governance_action_release_control_minimal_executor_v0.py`

