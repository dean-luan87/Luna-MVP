# Luna — Navigation Governance Action Approval Status Placeholder v0（批准边界状态对象：只读占位）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_STATUS_PLACEHOLDER_V0.md`  
**性质**：Phase-Next-43：将已冻结的 `navigation_governance_action_approval_status_v0` 落地为统一、只读、可观测、不可执行的占位输出（relevant-only）

关联：
- 批准边界状态对象冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_STATUS_OBJECT_V0.md`
- 批准边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_V0.md`
- 批准边界最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_IMPLEMENTATION_V0.md`
- 执行器输入对象冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_V0.md`
- 执行器输入对象正式实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是批准边界标准化状态对象的**只读占位**设计。
- 当前目标：让系统真正产出统一的 `navigation_governance_action_approval_status_v0` 占位实例。
- 当前不做真实批准链实现。
- 当前不做真实治理动作实现。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在要做 placeholder

- 批准边界状态对象边界已经冻结。
- approval boundary implementation 已存在。
- 但系统里还没有真正的统一批准边界状态输出位。
- 若无 placeholder，后续真实批准链接入时易回到临时状态字段与散乱判断。
- 因此必须先把批准边界状态对象**实体化**为占位输出，验证收束路径，但保持不可执行。

---

## C. placeholder 的最小定义（写死）

- 它不是 approval boundary 结果本身。
- 不是 input object。
- 不是批准已生效事实。
- 只是「批准边界标准化状态对象」的只读占位实例。
- 作用：验证系统未来能否把批准边界状态收束成统一回传对象。

---

## D. 当前最小输入（写死）

只读：

1) `navigation_governance_action_approval_boundary_v0`  
- 提供 approved/blocked 类别与动作类型映射依据。

可选只读（仅一致性上下文，不得扩权）：

- `navigation_governance_action_boundary_v0`
- `navigation_governance_action_executor_input_v0`

并明确：

- relevant-only：缺少主输入则不写。
- 不允许脑补；上述仅为占位组装依据，不代表真实批准链已运行。

---

## E. 当前最小输出位（写死）

固定写入：

- `result.metadata["navigation_governance_action_approval_status_v0"]`

最小结构建议：

```json
{
  "governance_action_approval_status_present": true,
  "governance_action_approval_status_scope": "navigation_governance_action_approval_status_v0",
  "approval_state": "approved_placeholder|approval_blocked_placeholder|pending_like_placeholder|unresolved_like_placeholder",
  "approved_action_type": "interrupt|release_control|rollback_request|hold",
  "approval_effect_state": "unknown_not_applied",
  "route_binding_ready": false,
  "consume_mode": "read_only"
}
```

约束（写死）：

- 不加时间/空间字段
- 不膨胀成复杂对象
- 只表达“统一批准边界状态对象占位实例已形成”

---

## F. 当前最小字段组织原则（克制）

- 批准状态类：只能占位，不得伪装真实批准链已执行完成。
- 批准动作类型类：允许从 approval boundary 做最小映射，但不表示动作已生效。
- 阻断/异常状态类：当前只能占位，不得伪装真实失败处理已发生。
- 结果影响类：固定 `unknown_not_applied` 占位。
- 回传绑定/路由类：固定 `route_binding_ready=false` 占位，不做真实绑定。

---

## G. 当前最小结果语义（写死）

当 `navigation_governance_action_approval_status_v0` 被产出时，只表示：

- 系统已能为未来批准边界层预留统一状态对象承载位。
- 后续真实批准链可基于该对象设计正式回传。

不表示：

- 真实批准已执行。
- 真实治理动作已执行。
- 路线已改变或中台已迁移。

---

## H. 当前不允许做什么（必须写死）

- 不允许真实批准链执行
- 不允许真实回退/中断/释放控制权动作
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 `governance_action_approval_status_present == true` 当批准链已运行

---

## I. 与现有链路的关系（写清）

- 与 approval boundary：approval boundary 表达“已批准边界结果”；approval status placeholder 表达“批准边界层自身状态承载位”；两者不能混用。
- 与 executor input object：input object 是执行前输入面；approval status placeholder 是批准层状态回传面；两者不能混用。
- 与 action status object：action status object 发生在未来执行器之后；approval status placeholder 发生在批准层；两者不能跨层替代。

---

## J. 实现落点（落地说明）

- Builder：`capabilities/governance/runtime/navigation_governance_action_approval_status_placeholder_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`（在 `navigation_governance_action_approval_boundary_v0` 之后）

