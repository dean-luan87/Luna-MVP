# Luna — Navigation Governance Action Release Control Status Object Implementation v0（子动作状态对象：正式实现版）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-55：将 `navigation_governance_action_release_control_status_v0` 从 placeholder 推进为 **implemented object**（可合法回传/识别，仍不表示真实 release_control 已执行）

关联：
- 状态对象边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_V0.md`
- 状态对象只读占位：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_PLACEHOLDER_V0.md`
- release_control skeleton：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SKELETON_V0.md`
- 输入契约占位：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_PLACEHOLDER_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 子动作标准化状态对象的**正式实现版文档**。
- 当前目标：把状态对象从 placeholder 推进到 `object_kind: implemented_v0` 的统一对象。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不改变现有主线执行行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在要先实现状态对象

- `release_control` skeleton 已存在。
- `release_control` input contract 已有占位对象。
- `release_control` 状态对象定义已存在（冻结）。
- 若无正式状态对象实现版，后续真实动作只能回 placeholder 或散字段，难以单独观察与回归。
- 因此必须先把子动作状态对象正式实现出来。
- 但当前仍不能让 `release_control` 回传**真实动作事实**（completed/failed 等运行时真值）。

---

## C. implemented status object 的最小定义（写死）

- 它不是 placeholder（`consume_mode` 为 `implemented_object`，`object_kind` 为 `implemented_v0`）。
- 也不是 `release_control` 已完成事件。
- 它是 `release_control` 子动作未来唯一合法回传对象的正式实现版。
- 作用：把上游合法依据收束为可被治理链合法观察/消费的标准化对象（当前仍表达非运行时事实）。

---

## D. 当前最小输入依据（写死）

1) `navigation_governance_action_release_control_input_v0`（主依据；无则不生成）  
- 且其中动作类型必须明确为 `release_control`

2) `navigation_governance_action_executor_wiring_v0`（一致性依据；无则不生成）  

可选只读（仅辅助一致性校验，不得扩权）：

- `navigation_governance_action_status_v0`
- `navigation_governance_action_executor_readiness_gate_v0`

要求：relevant-only；不脑补；这些只是对象实现依据，不代表真实 `release_control` 已运行。

---

## E. 输出位（写死）

- `result.metadata["navigation_governance_action_release_control_status_v0"]`
- 本轮为 implementation：以 `object_kind` / 分类字段表达，不再以 `*_placeholder` 作为主体表达。

---

## F. 最小字段类别（实现）

至少实现（最小可用表达）：

- 子动作状态类（例如 `release_control_state_fact = not_started`）
- 动作类型确认类（`action_type_confirmed = release_control`）
- 异常/阻断状态类（`exception_fact/block` 最小表达）

允许最小占位：

- 结果影响状态类
- 回传绑定/路由类

---

## G. 当前最小语义（写死）

产出 implemented 对象只表示：上游控制链已能把 `release_control` 子动作所需最小状态信息整理成正式对象，供观察与消费；**不表示**真实 `release_control` 已执行、不表示控制权已真实交还、不表示路线已改或中台已迁移。

---

## H. 当前不允许做什么（写死）

- 不允许把 implemented `release_control status` 伪装成真实动作已生效事实
- 不允许触发真实 `release_control`
- 不允许触发真实 `rollback` / `interrupt`
- 不允许改路线
- 不允许触发语音播报
- 不允许触发中台真实迁移
- 不允许把 implemented status 当动作已执行

---

## I. 实现落点

- Builder：`capabilities/governance/runtime/navigation_governance_action_release_control_status_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`
- skeleton 识别-only：`capabilities/governance/runtime/navigation_governance_action_release_control_v0.py`（`accept_release_control_status_object`）

