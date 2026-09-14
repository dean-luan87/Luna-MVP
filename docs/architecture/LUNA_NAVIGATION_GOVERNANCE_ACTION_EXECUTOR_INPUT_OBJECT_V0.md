# Luna — Navigation Governance Action Executor Input Object v0（治理动作执行器标准化输入对象：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_V0.md`  
**性质**：Phase-Next-39：冻结治理动作执行器**唯一合法输入对象**边界（`navigation_governance_action_executor_input_v0`；不落代码、不执行治理动作）

关联：
- 已批准治理动作边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_V0.md`
- 已批准治理动作边界最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_IMPLEMENTATION_V0.md`
- 批准边界状态对象（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_STATUS_OBJECT_V0.md`
- 批准边界状态对象只读占位：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_STATUS_PLACEHOLDER_V0.md`
- 治理动作执行器本体最小定义：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 治理动作执行器模块骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`
- 输入对象正式实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`
- 治理动作执行器就绪门控（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_V0.md`
- 治理动作执行器就绪门控最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_IMPLEMENTATION_V0.md`
- 治理动作：Release Control 动作级输入契约冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_V0.md`
- 治理动作：Release Control 输入契约占位输出：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_PLACEHOLDER_V0.md`
- 治理动作状态对象冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_V0.md`
- 治理动作状态对象正式实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是「**治理动作执行器标准化输入对象**」的最小设计文档。
- 当前目标：冻结治理动作执行器输入对象边界（可冻结、可回归）。
- 当前不做真实治理动作实现。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在必须先定义输入对象

- 当前已有 approved action boundary（含最小非动作实现）。
- 当前也有 governance action executor skeleton。
- 但 skeleton **未来不应**直接消费「散落的 `approved_*` 字段或对象碎片」作为执行器输入。
- 若不先冻结统一输入对象，后续极易把 **approval boundary 结果直接当执行器输入**，造成边界混乱与越权消费。
- 因此必须先冻结「治理动作执行器唯一合法输入对象」。

---

## C. 输入对象在系统中的位置（写死）

这个对象应位于：

- **approval boundary 之后**
- **governance action executor 之前**
- 处于 **action boundary / approval boundary** 与 **executor 本体** 之间

并写清：

- 它不是 action boundary。
- 不是 approved boundary 本身。
- 它是**治理动作执行器唯一应消费的标准化输入对象**（`navigation_governance_action_executor_input_v0`）。

---

## D. 与 approved_* / approval 对象的关系（写清）

- **`governance_action_approval_status` 的 `approved_*` 语义**表达「已批准动作类别/边界」，是上游结论，但**不是**执行器输入面的完整封装。
- **输入对象**应在合法上游依据齐备的前提下，把「已批准动作类型 + 执行前提 + 约束」等**收口为一个对象**，供执行器**唯一**消费。
- 执行器未来**不直接**以「只吃 approved_* 枚举」替代该对象（除非后续显式废弃本对象并另行冻结，不在本轮）。

---

## E. 输入对象的最小字段类别（只定义类别与语义，不做过细字段表、不做实现）

建议至少包括这 **5 类**：

### 1. 已批准动作类型类

用于表示：

- 当前被批准的是 interrupt / release_control / rollback_request / hold 里的哪一类  
- 这是**主输入语义**（与 approval 结论对齐，但以对象内统一字段承载）

### 2. 执行前提类

用于表示：

- 当前是否满足进入治理动作执行器的**最小前提**  
- **不表示**动作已执行

### 3. 作用目标类（语义占位）

用于表示：

- 该治理动作主要作用于什么对象/控制面（例如导航执行器控制权、执行状态、保持态等）  
- 当前只做语义级占位

### 4. 执行约束类

用于表示：

- 该治理动作受哪些硬约束限制  
- 当前只做最小约束语义，不做真实执行链约束展开

### 5. 回传绑定类（占位）

用于表示：

- 未来治理动作执行后，状态应回传到哪条治理链/中台链  
- 当前只做绑定占位

---

## F. 哪些是「最小必需字段类别」（写死）

最小必需类别：

- **已批准动作类型类**
- **执行前提类**
- **执行约束类**

并写清：

- 没有这些，输入对象**不成立**。
- **作用目标类**与**回传绑定类**当前可以是占位，但未来真实接入时**必不可少**。

---

## G. 明确哪些东西不能直接等同于输入对象（必须写死）

以下都不能直接等同于 `navigation_governance_action_executor_input_v0`：

- 任意单个 `approved_*`（枚举或片段）
- 任意单个 `request_*`
- 任意单个治理决策对象
- 任意单个治理入口对象
- 任意 executor status 对象
- 任意 monitoring status 对象

解释（写死）：

- 它们只是输入对象的**依据**或**前置层结果**。
- 不是治理动作执行器应直接消费的**完整标准化输入对象**。

---

## H. 输入对象的最小语义（写死）

当未来系统拿到这个对象时，只表示：

- 上游治理链已经把治理动作执行所需**最小信息**整理成**统一输入对象**。
- 治理动作执行器未来可以**合法消费**该对象。

它不表示：

- 真实回退/中断/释权已执行；路线已改；中台已迁移。

---

## I. 与现有链路的关系（写清）

### 与 action boundary

- action boundary 表达理论允许的动作类别；**不直接**成为执行器输入。

### 与 approval boundary

- approval boundary 表达已批准动作边界；**仍不直接等于**执行器输入对象。
- input object 位于其后。

### 与 governance action executor

- 治理动作执行器未来**只应消费**该输入对象。
- **不应**直接消费 `approved_*` 作为唯一输入面。

### 与 governance action status object

- status object 是**执行后回传面**。
- input object 是**执行前输入面**。
- 两者不能混用。

---

## J. 当前仍然不能做什么（必须写死）

- 不允许真实回退/中断/释权动作
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 input object 定义当作 input object 已实现

---

## K. 当前不做（必须写死）

- 不做 input object 代码实现
- 不做真实治理动作实现
- 不做地图接入
- 不做语音/记忆联动
- 不做自动迁移/自动治理

---

## L. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - governance action executor input object placeholder 或 implementation
- 再之后才考虑：
  - 真实治理动作最小实现
- 当前不跨这两步

---

## M. 未来输入对象样例（仅说明，不落代码）

```json
{
  "governance_action_executor_input_present": true,
  "governance_action_executor_input_scope": "navigation_governance_action_executor_input_v0",
  "approved_action_type": "interrupt|release_control|rollback_request|hold",
  "execution_prerequisites_ready": false,
  "constraint_profile": "minimal_safe_constraints",
  "return_binding_ready": false
}
```

说明：仅为未来样例；当前不落代码；当前不改现有链路行为。
