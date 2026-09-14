# Luna — Navigation Governance Action Approval Boundary Status Object v0（批准边界状态对象：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_STATUS_OBJECT_V0.md`  
**性质**：Phase-Next-42：冻结批准边界层自身的标准化状态回传对象（可冻结、可回归；不落代码、不触发真实批准链/治理动作）  

关联：
- 批准边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_V0.md`
- 批准边界最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_IMPLEMENTATION_V0.md`
- 执行器输入对象冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_V0.md`
- 执行器输入对象正式实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`
- 治理动作状态对象冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_V0.md`
- 治理动作状态对象正式实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是“**已批准治理动作边界层标准化状态对象**”的最小设计文档。
- 当前目标：冻结批准边界状态回传对象边界（可冻结、可回归）。
- 当前不做真实治理动作实现。
- 当前不做真实批准执行链。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在要先定义批准边界状态对象

- 当前已有 approved boundary 结果对象（`navigation_governance_action_approval_boundary_v0`）。
- 当前已有 governance action executor input object（冻结 + 实现版对象已存在）。
- 但尚无“批准层自身当前状态如何被统一组织并回传”的正式对象。
- 若不先冻结状态对象，一旦批准链复杂化，容易退回散乱字段与临时判断，造成不可回归与越权风险。
- 因此必须先冻结 `navigation_governance_action_approval_status_v0` 的位置、类别与语义边界。

---

## C. 状态对象在系统中的位置（写死）

这个对象应位于：

- approval boundary 之后
- governance action executor input object 之前或并行观察面
- 中台/治理链消费层之前
- 不进入 entry / decision / action boundary / executor action status 层

并写清：

- 它不是 action boundary 对象。
- 不是 approved boundary 结果本身。
- 不是治理动作执行器输入对象。
- 它是“批准边界层自己唯一应回传的标准化状态对象”。

---

## D. 状态对象的最小字段类别（只定义类别与语义，不做过细字段表、不做实现）

建议至少包括这 5 类：

### 1) 批准状态类

用于表示：

- 当前批准边界是否处于 `approved` / `approval_blocked` / `pending_like` / `unresolved_like`
- 说明：这是语义分类，不要求复杂状态机

### 2) 批准动作类型类

用于表示：

- 当前涉及的是 interrupt / release_control / rollback_request / hold 中哪一类
- 只表达类型，不表达动作已生效

### 3) 阻断 / 异常状态类

用于表示：

- 是否被阻断
- 是否一致性校验失败
- 是否因前提不足不能继续升级

### 4) 结果影响状态类（扩展占位）

用于表示：

- 是否允许继续进入 executor input object 构建
- 是否建议退回上游治理链
- 当前只做语义占位，不做真实迁移

### 5) 回传绑定 / 路由类（扩展占位）

用于表示：

- 状态对象未来应回传到哪条治理链 / 中台链
- 当前只做绑定占位，不做真实路由实现

---

## E. 哪些是“最小必需字段类别”（写死）

最小必需类别（缺则对象不成立）：

- 批准状态类
- 批准动作类型类
- 阻断 / 异常状态类

并写清：

- 结果影响状态类、回传绑定 / 路由类当前可以占位，但未来真实接入必不可少。

---

## F. 明确哪些东西不能直接等同于状态对象（必须写死）

以下都不能直接等同于 `navigation_governance_action_approval_status_v0`：

- 任意单个 `approved_*`
- 任意单个 `approval_blocked`
- 任意单个 `request_*`
- 任意单个 executor input object
- 任意单个 governance decision / entry 对象
- 任意单个异常回调或一致性校验结果

解释（写死）：

- 它们只是状态对象的组成依据或单点事件。
- 不是治理链应消费的完整标准化状态对象。

---

## G. 状态对象的最小语义（写死）

当未来系统拿到这个对象时，只表示：

- 批准边界层已把自身当前状态整理成统一回传对象。
- 中台/治理链可基于该对象做观察、记录与后续判断。

它不表示：

- 真实治理动作已执行。
- 路线/控制权/中台状态已改变。

---

## H. 与现有链路的关系（写清）

### 与 governance action boundary

- action boundary 负责给出理论动作边界。
- approval status object 记录批准边界层自己的状态。
- 两者不能混用。

### 与 governance action approval boundary

- approval boundary 结果对象是前台结论。
- approval status object 是批准层回传观察面。
- 两者不能互相替代。

### 与 governance action executor input object

- input object 是执行前输入面。
- approval status object 是批准层状态回传面。
- 两者不能混用。

### 与 governance action status object

- governance action status object 发生在未来执行器之后。
- approval status object 发生在批准层。
- 不能跨层替代。

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
- 不做真实批准执行链
- 不做地图接入
- 不做语音/记忆联动
- 不做自动迁移 / 自动治理

---

## K. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - approval status object placeholder 或 implementation
- 再之后才考虑：
  - 真实治理动作最小实现
- 当前不跨这两步

---

## L. 未来状态对象样例（仅说明，不落代码）

```json
{
  "governance_action_approval_status_present": true,
  "governance_action_approval_status_scope": "navigation_governance_action_approval_status_v0",
  "approval_state": "approved|approval_blocked|pending_like|unresolved_like",
  "approved_action_type": "interrupt|release_control|rollback_request|hold",
  "approval_effect_state": "unknown_not_applied",
  "route_binding_ready": false
}
```

