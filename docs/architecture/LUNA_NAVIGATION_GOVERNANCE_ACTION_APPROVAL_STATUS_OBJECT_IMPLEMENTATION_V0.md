# Luna — Navigation Governance Action Approval Status Object Implementation v0（批准边界状态对象：正式实现版）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_STATUS_OBJECT_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-44：将 `navigation_governance_action_approval_status_v0` 从 placeholder 推进为 **implemented object**（可合法回传/观察，仍不表示真实批准链已执行）

关联：
- 批准边界状态对象冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_STATUS_OBJECT_V0.md`
- 批准边界状态对象只读占位：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_STATUS_PLACEHOLDER_V0.md`
- 批准边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_V0.md`
- 批准边界最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_IMPLEMENTATION_V0.md`
- 执行器输入对象冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_V0.md`
- 执行器输入对象正式实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是批准边界标准化状态对象的**正式实现版**文档。
- 当前目标：把状态对象从 placeholder 推进为 `object_kind: implemented_v0` 的统一对象。
- 当前不做真实批准链执行；不做真实治理动作；不接地图；不驱动语音/记忆；不改变现有主线执行行为。

---

## B. 为什么现在要先实现状态对象

- approval boundary implementation 已存在。
- approval status object 定义已存在，placeholder 已存在。
- 若无正式实现版，后续批准链只能回 placeholder 或散字段，难以回归与统一消费。
- 因此必须先把状态对象正式实现出来。
- 但当前仍不能回传“真实批准链已执行完成”的事实。

---

## C. implemented status object 的最小定义（写死）

- 它不是 placeholder。
- 也不是批准链已完成事件。
- 它是批准边界层未来唯一合法回传对象的正式实现版。
- 作用：把上游合法依据收束为可被治理链/中台合法观察与消费的标准化对象。

---

## D. 当前最小输入依据（写死）

1) implemented `navigation_governance_action_approval_boundary_v0`（主依据；缺则 relevant-only 不写）  

可选只读一致性上下文（不得扩权）：

- implemented `navigation_governance_action_boundary_v0`
- implemented `navigation_governance_action_executor_input_v0`

要求：不脑补；relevant-only 成立；这些只是对象实现依据，不代表真实批准链已运行。

---

## E. 输出位（写死）

- `result.metadata["navigation_governance_action_approval_status_v0"]`

并明确：本轮为实现版对象，不再以 `*_placeholder` 作为主体表达；通过 `object_kind/consume_mode` 与分类字段表达语义。

---

## F. 最小字段类别（实现）

至少实现：

- 批准状态类（`approval_state_class`）
- 批准动作类型类（`approved_action_type_class`）
- 阻断/异常状态类（`block_and_exception_class`）

允许最小占位：

- 结果影响状态类（`effect_and_upstream_class`）
- 回传绑定/路由类（`route_and_return_class`）

---

## G. 当前最小语义（写死）

产出 implemented 对象只表示：上游已能把批准边界层所需最小信息整理成正式对象供观察；不表示真实批准链已执行，也不表示任何治理动作已执行、路线已改或中台已迁移。

---

## H. 当前不允许做什么（写死）

- 不允许把 implemented approval status 伪装成真实批准已生效事实。
- 不允许触发真实批准链或任何治理动作。
- 不允许改路线、语音播报、中台真实迁移。
- 不允许把 implemented status 当批准链已执行。

---

## I. 实现落点

- Builder：`capabilities/governance/runtime/navigation_governance_action_approval_status_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`（替换原 placeholder 写入路径）

