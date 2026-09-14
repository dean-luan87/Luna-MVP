# Luna — Navigation Governance Action Approval Boundary v0（已批准治理动作边界：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_V0.md`  
**性质**：Phase-Next-37：冻结「普通 action boundary → 已批准动作边界」的升级边界（不执行治理动作、不实现批准链）

关联：
- 已批准治理动作边界最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_IMPLEMENTATION_V0.md`
- 治理动作边界层冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_V0.md`
- 治理动作边界最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_IMPLEMENTATION_V0.md`
- 治理动作执行器本体最小定义：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 治理动作执行器模块骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`
- 治理动作状态对象冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_V0.md`
- 治理动作状态对象正式实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- 治理动作执行器标准化输入对象（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_V0.md`
- 治理动作执行器输入对象只读占位：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_PLACEHOLDER_V0.md`
- 批准边界状态对象（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_STATUS_OBJECT_V0.md`
- 批准边界状态对象只读占位：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_STATUS_PLACEHOLDER_V0.md`

---

## A. 文档定位（写死）

- 这是「**治理动作批准边界层**」的设计文档。
- 当前目标：冻结 action boundary → **approved action boundary** 的升级边界与语义。
- 当前不做真实治理动作实现。
- 当前不做真实批准执行链。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在必须先定义批准边界层

- 当前系统已有 implemented `navigation_governance_action_boundary_v0`。
- 但普通 `request_*` / `hold_*` / `action_blocked` 只表达「理论允许进入的动作类别边界」，**不等于**「已批准可进入执行器输入面」。
- 若不先定义批准边界，后续极易把 `request_rollback` / `request_interrupt` / `request_release_control` **直接误当**可执行动作。
- 因此必须先冻结「已批准边界」这一层，与「理论边界」显式区分。

---

## C. 批准边界层的最小定义（写死）

批准边界层是：

- 在 action boundary 已形成的前提下，对其是否可升级为「**已批准动作边界**」、并进入未来治理动作执行器输入面，进行**最小批准判断**的层。

它不是：

- governance entry  
- governance decision  
- governance action boundary 本身  
- 真实治理动作执行器  
- formal decision  
- readiness gate  
- takeover authorization  

核心一句（写死）：

**批准边界层负责限定「哪些 action boundary 结果可以升级为已批准边界」，但不直接执行治理动作。**

---

## D. 当前最小合法输入（写死）

只允许消费：

1) implemented `navigation_governance_action_boundary_v0`（**主输入**）

可选只读一致性校验（不得扩权）：

2) implemented `navigation_rollback_and_interruption_governance_decision_v0`  
3) implemented `navigation_rollback_and_interruption_governance_entry_v0`  
4) implemented `navigation_real_executor_status_v0`  
5) implemented `navigation_execution_monitoring_status_v0`  

并写死：

- action boundary 是主输入。
- 其它对象最多用于一致性校验，不得扩权。
- 没有合法 action boundary 对象时，不得形成 approved action boundary 结果。

---

## E. 最小批准结果集合（写死）

最小集合（不发散）：

- `approved_hold_executor_state`
- `approved_interrupt`
- `approved_release_control`
- `approved_rollback`
- `approval_blocked`

语义（写死「意味着什么 / 不意味着什么」）：

1) `approved_hold_executor_state`  
- 表示：允许进入「维持当前执行器状态」的**已批准**动作边界。  
- 不表示：动作已执行。

2) `approved_interrupt`  
- 表示：允许进入「中断」相关治理动作执行器输入面的**已批准**边界。  
- 不表示：中断已执行。

3) `approved_release_control`  
- 表示：允许进入「释放控制权」相关治理动作执行器输入面的**已批准**边界。  
- 不表示：控制权已释放。

4) `approved_rollback`  
- 表示：允许进入「回退」相关治理动作执行器输入面的**已批准**边界。  
- 不表示：回退已执行。

5) `approval_blocked`  
- 表示：虽然存在 action boundary 结果，但**不允许**升级为已批准边界，**不允许**进入后续治理动作执行器输入面。

---

## F. 当前最小判断原则（克制写死）

> 说明：这是「边界 → 已批准边界」的映射规则草案；**默认偏保守**，不激进批准；不做复杂批准流程树。

规则 1：`request_rollback` → `approved_rollback` **或** `approval_blocked`  
规则 2：`request_release_control` → `approved_release_control` **或** `approval_blocked`  
规则 3：`request_interrupt` → `approved_interrupt` **或** `approval_blocked`  
规则 4：`hold_executor_state` → `approved_hold_executor_state` **或** `approval_blocked`  
规则 5：`action_blocked` → `approval_blocked`  

并明确（写死）：

- 当前只是「边界到已批准边界」的映射规则占位；**未来**具体何时落 `approved_*` vs `approval_blocked` 由批准链/中台策略决定，**本轮不实现**。
- 不做复杂批准流程树。

---

## G. 批准边界层与现有链路的关系（写清）

### 与 governance action boundary

- action boundary 只表达「理论允许的动作类别」。
- approval boundary 决定其是否可升级为「已批准动作边界」。
- 两者不能混用。

### 与 governance action executor

- 治理动作执行器未来**只应消费** approved action boundary（正式对象形态由后续实现定义）。
- 不应直接消费普通 `request_*` 作为执行器输入。

### 与 governance decision / entry

- decision 与 entry 发生在更早层。
- approval boundary 发生在 action boundary 之后。
- 不得反向替代前置层。

### 与中台/治理链

- 当前批准边界仍只是设计冻结。
- 未来批准动作应由中台/治理链参与；**本轮不实现**。

---

## H. 当前仍然不能做什么（必须写死）

- 不允许真实回退动作
- 不允许真实中断动作
- 不允许真实释放控制权动作
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把任何 `approved_*` 当动作已执行

---

## I. 当前阶段结论（写死一句）

**当前阶段只适合冻结「已批准治理动作边界」；即使未来落最小实现，也只能先输出 `approved_*` / `approval_blocked` 类结果，不能直接执行真实治理动作。**

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - governance action approval boundary 的最小实现
- 再之后才考虑：
  - 治理动作执行器最小输入对象 / 真正最小动作实现
- 当前不跨这两步

---

## K. 未来批准边界结果样例（仅说明，不落代码）

```json
{
  "governance_action_approval_attempted": true,
  "governance_action_approval_scope": "navigation_governance_action_approval_boundary_v0",
  "governance_action_approval_status": "approved_hold_executor_state|approved_interrupt|approved_release_control|approved_rollback|approval_blocked",
  "reason": "..."
}
```

说明：仅为未来样例；当前不落代码；当前不改现有链路行为。
