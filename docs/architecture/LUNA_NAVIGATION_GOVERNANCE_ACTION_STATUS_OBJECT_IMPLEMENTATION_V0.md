# Luna — Navigation Governance Action Status Object Implementation v0（治理动作状态对象：正式实现版）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-36：将 `navigation_governance_action_status_v0` 从 placeholder 推进为 **implemented object**（可合法回传/识别，仍不表示真实治理动作已执行）

关联：
- 状态对象边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_V0.md`
- 状态对象只读占位：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_PLACEHOLDER_V0.md`
- 治理动作执行器本体定义：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 治理动作执行器模块骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`
- 治理动作边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_V0.md`
- 治理动作边界最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是治理动作标准化状态对象的**正式实现版**文档。
- 当前目标：把状态对象从 placeholder 推进为 **`object_kind: implemented_v0`** 的统一对象。
- 当前不做真实治理动作；不接地图；不驱动语音/记忆；不改变现有主线执行行为。

---

## B. 为什么现在要先实现状态对象

- 治理动作执行器 skeleton 已存在；action boundary implementation 已存在。
- 若无正式状态对象实现版，执行器后续只能回 placeholder 或散字段，无法稳定收口。
- 因此必须先把状态对象正式实现出来。
- 但当前仍不能让执行器回传**真实动作执行事实**（running/completed/failed 等运行时真值）。

---

## C. implemented status object 的最小定义（写死）

- 它不是 placeholder（`consume_mode` 为 `implemented_object`）。
- 也不是治理动作已完成事件。
- 它是治理动作执行器未来**唯一合法回传**对象的正式实现版形态（当前仍表达非运行时事实）。
- 作用：把上游合法依据收束为可被 skeleton **合法回传/识别**的标准化对象。

---

## D. 当前最小输入依据（写死）

1. `navigation_governance_action_boundary_v0`（必需；无则不生成）
2. governance action executor skeleton identity（模块内校验 `get_governance_action_executor_identity()`）

可选只读：

3. `navigation_rollback_and_interruption_governance_decision_v0`（仅一致性 echo，不得扩权）

要求：relevant-only；不脑补。

---

## E. 输出位（写死）

- `result.metadata["navigation_governance_action_status_v0"]`
- 本轮为 **implementation**，以 `object_kind` / 分类字段表达，不再以扁平 `idle_placeholder` 为主体。

---

## F. 最小字段类别（实现）

至少实现：动作状态类、动作类型类、异常/阻断状态类的最小可用表达（嵌套在 `action_state_class` / `action_type_class` / `anomaly_and_block_class`）。

结果影响、回传绑定类保持最小占位（`effect_and_upstream_class`、`route_and_return_class`）。

---

## G. 最小语义（写死）

产出 implemented 对象只表示：上游已能把最小信息整理为正式对象，skeleton 可识别；**不表示**回退/中断/释权已执行、路线已改、中台已迁移。

---

## H. 当前不允许做什么（写死）

- 不允许伪装 `action_executing` / `action_completed` / `action_failed` 真实事实。
- 不允许触发真实回退/中断/释权；不允许改路线、语音播报、中台真实迁移。
- 不允许把 implemented status 当治理动作已执行。

---

## I. 实现落点

- Builder：`capabilities/governance/runtime/navigation_governance_action_status_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`（替换原 placeholder 写入路径）
- Skeleton 识别：`capabilities/governance/runtime/navigation_governance_action_executor_v0.py`（`accept_governance_action_status_object`，非执行）
