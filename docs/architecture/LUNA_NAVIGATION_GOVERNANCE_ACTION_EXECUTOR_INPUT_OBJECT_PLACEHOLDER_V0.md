# Luna — Navigation Governance Action Executor Input Object Placeholder v0（治理动作执行器输入对象：只读占位）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_PLACEHOLDER_V0.md`  
**性质**：Phase-Next-40：将已冻结的 `navigation_governance_action_executor_input_v0` 落地为统一、只读、可观测、不可执行的占位输出（relevant-only）

关联：
- 输入对象边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_V0.md`
- 输入对象正式实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`
- 已批准治理动作边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_V0.md`
- 已批准治理动作边界最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_IMPLEMENTATION_V0.md`
- 治理动作执行器模块骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`
- 治理动作状态对象冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_V0.md`
- 治理动作状态对象正式实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是治理动作执行器标准化输入对象的**只读占位**设计。
- 当前目标：让系统真正产出统一的 `navigation_governance_action_executor_input_v0` 占位实例。
- 当前不做真实治理动作实现；不接地图；不驱动语音/记忆；不改变现有主线行为；不触发中台真实迁移。

---

## B. 为什么现在要做 placeholder

- 输入对象边界已经冻结。
- 治理动作执行器 skeleton 已存在。
- approval boundary implementation 已存在。
- 但系统里还没有真正统一的治理动作执行器输入输出位。
- 若无 placeholder，后续真实治理动作接入时易回到临时输入字段与越权消费。
- 因此必须先把输入对象**实体化**为占位输出，验证收束路径，但保持不可执行。

---

## C. placeholder 的最小定义（写死）

- 它不是治理动作执行器。
- 不是动作执行命令。
- 不是批准动作已执行事实。
- 只是「治理动作执行器标准化输入对象」的只读占位实例。
- 作用：验证系统未来能否把 approved action boundary 收束成统一输入对象。

---

## D. 当前最小输入（写死）

只读：

1) `navigation_governance_action_approval_boundary_v0`  
- 提供“当前已批准动作类型”的依据（`approved_*`）。

2) governance action executor skeleton identity / capability  
- 通过 `get_governance_action_executor_identity()` 提供“未来谁来消费该对象”的最小一致性依据。

可选只读：

3) `navigation_governance_action_boundary_v0`  
- 仅作辅助一致性上下文，不得扩权。

并明确：

- relevant-only：缺少主输入或 skeleton 校验不满足则不写。
- 不允许脑补；以上仅为占位组装依据，不代表真实治理动作已运行。

---

## E. 当前最小输出位（写死）

固定写入：

- `result.metadata["navigation_governance_action_executor_input_v0"]`

最小结构建议：

```json
{
  "governance_action_executor_input_present": true,
  "governance_action_executor_input_scope": "navigation_governance_action_executor_input_v0",
  "approved_action_type": "interrupt|release_control|rollback_request|hold",
  "execution_prerequisites_ready": false,
  "constraint_profile": "placeholder_minimal_constraints",
  "return_binding_ready": false,
  "consume_mode": "read_only"
}
```

约束（写死）：

- 不加时间/空间字段
- 不膨胀成复杂对象
- 只表达“统一输入对象占位实例已形成”

---

## F. 当前最小字段组织原则（克制）

- 已批准动作类型类：从 approval boundary 做最小映射，但不表示动作已生效。
- 执行前提类：固定占位 `execution_prerequisites_ready=false`，不得伪装可立即执行。
- 执行约束类：固定占位 profile，不展开真实约束树。
- 作用目标类：当前只做语义占位（可留空或 minimal echo，不扩权）。
- 回传绑定类：固定 `return_binding_ready=false`，不做真实绑定。

---

## G. 当前最小结果语义（写死）

当 `navigation_governance_action_executor_input_v0` 被产出时，只表示：

- 系统已能为未来治理动作执行器预留统一输入对象承载位。
- 后续真实治理动作执行器可基于该对象设计正式消费。

不表示：

- 真实回退/中断/释放控制权已执行；路线已改变；中台已迁移。

---

## H. 当前不允许做什么（必须写死）

- 不允许真实回退动作
- 不允许真实中断动作
- 不允许真实释放控制权动作
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 `governance_action_executor_input_present == true` 当治理动作已执行或可立即执行

---

## I. 与现有链路的关系（写清）

- 与 approval boundary：approval boundary 表达“已批准动作边界”；input placeholder 表达“未来执行器唯一合法输入对象占位”；两者不能混用。
- 与 executor skeleton：skeleton 是未来动作执行本体壳子；input placeholder 是它未来唯一应消费的输入对象占位；当前不执行真实动作。
- 与 status object：input 是执行前输入面；status 是执行后回传面；两者不能混用。

---

## J. 实现落点（落地说明）

- Builder：`capabilities/governance/runtime/navigation_governance_action_executor_input_placeholder_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`（在 `navigation_governance_action_approval_boundary_v0` 之后）

