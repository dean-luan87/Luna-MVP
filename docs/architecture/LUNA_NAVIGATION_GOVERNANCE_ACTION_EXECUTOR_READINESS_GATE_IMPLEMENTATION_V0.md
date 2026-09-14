# Luna — Navigation Governance Action Executor Readiness Gate Minimal Implementation v0（就绪门控：最小非动作实现）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-46：把 readiness gate 从设计冻结推进到“统一结果对象”的最小非动作实现（只读、可观察、可回归）

关联：
- readiness gate 冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_V0.md`
- 治理动作执行器本体最小定义：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 治理动作执行器模块骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`
- 执行器输入对象（正式实现版）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`
- 治理动作状态对象（正式实现版）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- 批准边界状态对象（正式实现版）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_STATUS_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是治理动作执行器就绪门控的**正式实现版文档**（最小非动作实现）。
- 当前目标：把 readiness gate 从冻结文档推进到最小非动作实现，产出统一门控结果对象。
- 当前不做真实批准链执行。
- 当前不做真实治理动作实现。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在要先实现 readiness gate

- `navigation_governance_action_executor_input_v0` 已有 implemented object。
- `navigation_governance_action_status_v0` 已有 implemented object。
- `navigation_governance_action_approval_status_v0` 已有 implemented object。
- readiness gate 的门控类别与结果集合已冻结（ready_candidate / not_ready / blocked）。
- 若无最小实现，后续治理动作层会回到各模块各自判断“能不能执行”，导致边界漂移与越权风险。
- 因此必须先把 readiness gate 的统一结果对象实现出来。
- 但当前仍**不能触发任何真实治理动作**。

---

## C. implemented readiness gate 的最小定义（写死）

- 它不是真实治理动作执行器。
- 不是真实批准链。
- 它是“治理动作执行器进入未来动作层前的最小统一门控对象”的最小实现版。
- 作用：把输入对象、批准状态、回传状态承载位、执行器本体在位性收束成一个 `ready_candidate / not_ready / blocked` 结果。

---

## D. 当前最小输入依据（写死：只允许消费标准化对象）

必须输入：

1) implemented `navigation_governance_action_executor_input_v0`（主输入）  
2) implemented `navigation_governance_action_status_v0`（回传承载面在位性依据）  
3) implemented `navigation_governance_action_approval_status_v0`（批准一致性依据）  
4) governance action executor skeleton 的 identity / capability（执行器在位与仍为 skeleton 的可观察依据）  

可选只读：

5) implemented `navigation_governance_action_approval_boundary_v0`（仅作一致性校验，不得扩权）  

写死禁止：

- 没有合法 executor input object 时，不得产出 `ready_candidate`。
- 禁止直接读取 `request_* / approved_* / raw metadata` 作为门控主输入。
- 必须只消费标准化对象。

---

## E. 当前最小输出位（写死）

写入：

- `result.metadata["navigation_governance_action_executor_readiness_gate_v0"]`

最小结构（不加时间/空间字段，不膨胀复杂对象）：

```json
{
  "governance_action_executor_readiness_attempted": true,
  "governance_action_executor_readiness_scope": "navigation_governance_action_executor_readiness_gate_v0",
  "governance_action_executor_readiness_status": "ready_candidate|not_ready|blocked",
  "reason": "..."
}
```

实现口径（写死）：

- **relevant-only**：若主输入对象（executor input object）缺失/不合法，则不写 readiness gate 对象。
- 一旦主输入对象存在且合法，则必输出三态之一（attempted=true）。

---

## F. 当前最小判断规则（克制）

至少支持（写死）：

规则 1：主输入对象缺失  
→ relevant-only 不写（或在更高层统一输出 not_ready；本实现选择 relevant-only）  

规则 2：executor skeleton 不在位 / identity 不匹配  
→ `blocked`

规则 3：批准状态与输入对象不一致  
→ `blocked`

规则 4：状态回传面未就绪  
→ `not_ready`

规则 5：对象齐备但约束仍明确不允许进入动作层  
→ `not_ready`

并写死：

- 当前默认偏保守。
- `ready_candidate` 只在极窄条件下出现。
- 不做复杂评分模型。

---

## G. 当前最小语义（写死）

当 `navigation_governance_action_executor_readiness_gate_v0` 被产出时，只表示：

- 系统已能统一判断治理动作执行器是否具备进入未来动作层候选条件。
- 上游治理链未来可合法消费该门控结果。

不表示：

- 真实回退/中断/释放控制权已执行
- 路线已改变
- 中台已真实迁移
- 治理动作已开始

---

## H. 当前不允许做什么（必须写死）

- 不允许真实回退动作
- 不允许真实中断动作
- 不允许真实释放控制权动作
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 `ready_candidate` 当动作已开始

---

## I. 实现落点（最小连续）

- Builder：`capabilities/mid_platform/runtime/navigation_governance_action_executor_readiness_gate_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`（在既有 governance 对象聚合之后写入）

