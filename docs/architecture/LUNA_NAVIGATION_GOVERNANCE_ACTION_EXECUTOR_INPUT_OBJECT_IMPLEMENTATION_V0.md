# Luna — Navigation Governance Action Executor Input Object Implementation v0（治理动作执行器输入对象：正式实现版）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-41：将 `navigation_governance_action_executor_input_v0` 从 placeholder 推进为 **implemented object**（可合法接收，仍不执行真实治理动作）

关联：
- 输入对象边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_V0.md`
- 输入对象只读占位：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_PLACEHOLDER_V0.md`
- 已批准治理动作边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_V0.md`
- 已批准治理动作边界最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_IMPLEMENTATION_V0.md`
- 治理动作执行器模块骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`

---

## A. 文档定位（写死）

- 这是治理动作执行器标准化输入对象的**正式实现版**文档。
- 当前目标：把输入对象从 placeholder 推进为 `object_kind: implemented_v0` 的统一对象。
- 当前不做真实治理动作；不接地图；不驱动语音/记忆；不改变现有主线执行行为。

---

## B. 为什么现在要先实现输入对象

- 治理动作执行器 skeleton 已存在。
- approval boundary implementation 已存在。
- 若无正式输入对象实现版，执行器后续只能面对 placeholder 或散字段，边界会变得不可回归。
- 因此必须先把输入对象正式实现出来。
- 但当前仍不能让执行器消费后产生真实动作。

---

## C. implemented input object 的最小定义（写死）

- 它不是 placeholder。
- 也不是治理动作执行命令。
- 它是治理动作执行器未来唯一合法输入对象的正式实现版。
- 作用：把上游合法依据收束为可被治理动作执行器 skeleton **合法接收**的标准化对象。

---

## D. 当前最小输入依据（写死）

1) implemented `navigation_governance_action_approval_boundary_v0`（主依据）  
- 且 `governance_action_approval_status` 必须为 `approved_*` 之一（不得为 `approval_blocked`）。

2) governance action executor skeleton identity / capability  
- 通过 `get_governance_action_executor_identity()` 进行最小一致性校验。

可选只读一致性校验（不得扩权）：

- implemented `navigation_governance_action_boundary_v0`
- implemented `navigation_rollback_and_interruption_governance_decision_v0`

要求：relevant-only；不脑补；这些只是对象实现依据，不代表真实治理动作已运行。

---

## E. 输出位（写死）

- `result.metadata["navigation_governance_action_executor_input_v0"]`

并明确：本轮是实现版对象，不是 placeholder；对象用 `object_kind/consume_mode` 与分类字段表达，不再以 `execution_prerequisites_ready=false + placeholder_minimal_constraints` 作为主体语义堆砌。

---

## F. 最小字段类别（实现）

至少实现以下类别的最小可用表达：

- 已批准动作类型类
- 执行前提类
- 执行约束类

允许保持最小占位：

- 作用目标类
- 回传绑定类

---

## G. 当前最小语义（写死）

产出 implemented 对象只表示：上游已把治理动作执行所需最小信息整理成正式对象，skeleton 可合法接收；不表示回退/中断/释权已执行，不表示路线改变或中台迁移。

---

## H. 当前不允许做什么（写死）

- 不允许治理动作执行器拿到对象后直接执行真实动作。
- 不允许触发真实回退/中断/释权；不允许改路线、语音播报、中台真实迁移。
- 不允许把 implemented input object 当治理动作已执行。

---

## I. 实现落点

- Builder：`capabilities/governance/runtime/navigation_governance_action_executor_input_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`（替换原 placeholder 写入路径）
- Skeleton 识别：`capabilities/governance/runtime/navigation_governance_action_executor_v0.py`（`accept_governance_action_executor_input_object`，非执行）

