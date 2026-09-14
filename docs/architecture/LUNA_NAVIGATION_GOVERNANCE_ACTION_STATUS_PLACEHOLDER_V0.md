# Luna — Navigation Governance Action Status Placeholder v0（治理动作状态对象：只读占位）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_PLACEHOLDER_V0.md`  
**性质**：Phase-Next-35：将已冻结的 `navigation_governance_action_status_v0` 落地为**统一、只读、可观测、不可执行**的占位输出（relevant-only）

关联：
- 治理动作状态对象正式实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- 治理动作状态对象边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_V0.md`
- 治理动作执行器本体最小定义：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 治理动作执行器模块骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`
- 治理动作边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_V0.md`
- 治理动作边界最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是治理动作标准化状态对象的**只读占位**设计。
- 当前目标：让系统真正产出统一的 `navigation_governance_action_status_v0` **占位实例**（可观测、可回归）。
- 当前不做真实治理动作实现。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不改变现有主线行为。

---

## B. 为什么现在要做 placeholder

- 治理动作状态对象边界已经冻结。
- 治理动作执行器 skeleton 已存在。
- 但系统里此前还没有**真正的统一治理动作状态输出位**。
- 若无 placeholder，后续真实治理动作接入时易回到散乱临时字段。
- 因此必须先把状态对象**实体化**为占位输出，验证收束路径，且保持不可执行。

---

## C. placeholder 的最小定义（写死）

- 它不是治理动作执行器。
- 不是动作完成事件。
- 不是控制权释放事实。
- 只是「治理动作标准化状态对象」的**只读占位实例**。
- 作用：验证系统未来能否把治理动作状态收束为统一回传对象；**不驱动**任何后续真实动作。

---

## D. 当前最小输入（写死）

只读：

1. `navigation_governance_action_boundary_v0`  
   - 至少提供当前理论动作边界类型（`governance_action_boundary_status`）的依据。
2. 治理动作执行器 skeleton  
   - 通过 `get_governance_action_executor_identity()` 提供 identity / placeholder capability 依据（模块级，不写入 metadata 作为伪造输入）。

可选只读：

3. `navigation_rollback_and_interruption_governance_decision_v0`  
   - 仅作辅助一致性上下文，**不得扩权**、不得改变占位映射。

并明确：

- **relevant-only**：若合法 action boundary 或 executor skeleton 校验不满足，则不写。
- 不允许脑补缺失上游对象。
- 上述仅为占位组装依据，**不代表**真实治理动作已运行。

---

## E. 当前最小输出位（写死）

固定写入：

- `result.metadata["navigation_governance_action_status_v0"]`

最小结构（示例，不新增时间/空间字段）：

```json
{
  "governance_action_status_present": true,
  "governance_action_status_scope": "navigation_governance_action_status_v0",
  "action_type": "interrupt|release_control|rollback_request|hold",
  "action_state": "idle_placeholder",
  "action_effect_state": "unknown_not_applied",
  "action_block_state": "not_blocked_placeholder|blocked_placeholder",
  "route_binding_ready": false,
  "consume_mode": "read_only"
}
```

---

## F. 当前最小字段组织原则（克制）

- **动作类型类**：从 action boundary 做最小映射；**不表示**动作已生效。
- **动作状态类**：仅 `idle_placeholder`；**不得**伪装 `action_executing` / `action_completed`。
- **异常/阻断状态类**：仅用 `*_placeholder`；**不得**伪装真实阻断已执行。
- **结果影响类**：`action_effect_state` 固定 `unknown_not_applied` 类占位。
- **回传绑定/路由类**：`route_binding_ready: false` 占位，不做真实绑定。

---

## G. 当前最小结果语义（写死）

当 `navigation_governance_action_status_v0` 被产出时，只表示：

- 系统已能为未来治理动作执行器预留**统一状态对象承载位**。
- 后续真实执行器可基于该对象设计正式回传。

不表示：

- 真实回退/中断/释放控制权已执行；路线已改；中台已迁移。

---

## H. 当前不允许做什么（写死）

- 不允许真实回退/中断/释放控制权动作。
- 不允许直接改路线、触发语音播报、触发中台真实迁移。
- 不允许把 `governance_action_status_present == true` 当治理动作已执行。

---

## I. 与现有链路的关系

- **与 action boundary**：boundary 表达理论动作类别边界；status placeholder 表达未来执行器侧状态承载位；**不能混用**。
- **与 executor skeleton**：skeleton 是未来动作本体壳子；status placeholder 是未来唯一应回传的状态对象占位；当前 skeleton 不执行真实动作。
- **与 decision / entry**：decision/entry 在治理动作前；status 占位在回传侧；当前占位**不反向替代**前置层。

---

## J. 实现落点（落地说明）

- Builder：`capabilities/governance/runtime/navigation_governance_action_status_placeholder_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`（在 `navigation_governance_action_boundary_v0` 写入之后）
