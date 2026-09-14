# Luna — Navigation Governance Action Status Object v0（治理动作状态对象：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_V0.md`  
**性质**：Phase-Next-34：治理动作执行器向中台/治理链回传的**标准化状态对象**边界（冻结语义与字段类别，不落代码、不执行治理动作）

关联：
- 治理动作状态对象正式实现版（Phase-Next-36）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- 治理动作状态对象只读占位（Phase-Next-35）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_PLACEHOLDER_V0.md`
- 治理动作执行器本体最小定义（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 治理动作执行器模块骨架（不可执行）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`
- 治理动作边界层冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_V0.md`
- 治理动作边界层最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_IMPLEMENTATION_V0.md`
- release_control 子动作状态对象（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_V0.md`
- 治理决策层冻结：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_DECISION_V0.md`
- 治理决策最小非动作实现：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_DECISION_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是“**治理动作执行器标准化状态对象**”的最小设计文档。
- 当前目标：冻结治理动作状态回传对象边界（可冻结、可回归）。
- 当前不做真实治理动作实现。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在要先定义状态对象

- 当前已有治理动作执行器本体定义与 skeleton。
- 但还没有“治理动作状态如何被统一组织并回传”的正式对象。
- 若不先定义状态对象，后续真实治理动作会回传散乱字段，治理链无法稳定消费、不可回归。
- 因此必须先冻结 `navigation_governance_action_status_v0` 的语义与字段类别边界。

---

## C. 状态对象在系统中的位置（写死）

这个对象应位于：

- **治理动作执行器之后**
- **中台/治理链消费层之前**
- **不进入** governance entry / decision / action boundary 层

并写清：

- 它不是 entry 对象。
- 不是 decision 对象。
- 不是 action boundary 对象。
- 它是**治理动作执行器唯一应回传的标准化状态对象**（面向中台/治理链的统一回传面）。

---

## D. 状态对象的最小字段类别（只定义类别与语义，不做过细字段表、不做实现）

建议至少包括这 **5 类**：

### 1. 动作状态类

用于表示：

- 当前治理动作是否 ready
- 是否 executing
- 是否 completed
- 是否 failed
- 是否 blocked

### 2. 动作类型类

用于表示：

- 当前对应的是 interrupt / release control / rollback request 中哪一类动作
- **只表达动作类型，不表达动作已在外部世界生效**

### 3. 异常/阻断状态类

用于表示：

- 是否出现动作执行失败
- 是否被阻断
- 是否因前提不足无法继续

### 4. 结果影响状态类（扩展占位）

用于表示：

- 是否建议上游继续治理
- 是否需要再次打开治理入口
- 当前仅为语义占位，**不做真实迁移**

### 5. 回传绑定/路由类（扩展占位）

用于表示：

- 状态对象应回传到哪条治理链/中台链
- 当前只做绑定占位，**不做真实路由实现**

---

## E. 哪些是“最小必需字段类别”（写死）

最小必需类别（没有这些，状态对象不成立）：

- **动作状态类**
- **动作类型类**
- **异常/阻断状态类**

并写清：

- **结果影响状态类**、**回传绑定/路由类**当前可以是占位，但未来真实接入时**必不可少**（否则治理链无法闭环观测与路由）。

---

## F. 明确哪些东西不能直接等同于状态对象（必须写死）

以下都不能直接等同于 `navigation_governance_action_status_v0`：

- 任意单个 `request_*` 动作边界结果
- 任意单个动作执行回调
- 任意单个异常事件
- 任意中台迁移状态
- 任意语音播报状态
- 任意 UI 展示状态

解释（写死）：

- 它们只是状态对象的**组成依据**或**单点事件**。
- 不是治理链应消费的**完整标准化状态对象**。

---

## G. 状态对象的最小语义（写死）

当未来系统拿到这个对象时，只表示：

- 治理动作执行器已把自身当前治理动作相关状态整理成**统一回传对象**。
- 中台/治理链可基于该对象做观察、记录、后续治理判断。

它不表示：

- 治理动作一定已在外部世界真正生效。
- 路线/控制权/中台状态一定已改变。

---

## H. 与现有链路的关系（写清）

### 与 governance action executor

- 治理动作执行器未来应通过该对象回传状态。
- skeleton 当前不实现真实状态，但未来必须收口到该对象。

### 与 governance action boundary

- action boundary 负责限制理论动作边界。
- status object 记录治理动作执行器侧的状态整理结果。
- 两者不能混用。

### 与 governance decision / entry

- decision 与 entry 发生在治理动作前。
- status object 发生在治理动作执行器之后。
- 不得反向替代前置层。

### 与中台/治理链

- 状态对象未来应由中台/治理链消费。
- 当前不接线实现。

---

## I. 当前仍然不能做什么（必须写死）

- 不允许真实回退动作
- 不允许真实中断动作
- 不允许真实释放控制权动作
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把状态对象定义当状态对象已实现

---

## J. 当前不做（必须写死）

- 不做状态对象代码实现
- 不做真实治理动作实现
- 不做地图接入
- 不做语音/记忆联动
- 不做自动迁移/自动治理

---

## K. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - 治理动作状态对象 placeholder 或 implementation
- 再之后才考虑：
  - 真实治理动作最小实现
- 当前不跨这两步

---

## L. 未来状态对象样例（仅说明，不落代码）

```json
{
  "governance_action_status_present": true,
  "governance_action_status_scope": "navigation_governance_action_status_v0",
  "action_type": "interrupt|release_control|rollback_request",
  "action_state": "idle|action_ready|action_executing|action_failed|action_completed|action_blocked",
  "action_effect_state": "unknown_not_applied",
  "route_binding_ready": false
}
```

说明：

- 仅为未来样例；当前不落代码；当前不改现有链路行为。
