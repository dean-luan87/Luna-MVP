# Luna — Navigation Governance Action Release Control Input Contract Implementation v0（输入契约：正式实现版）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-56：将 `navigation_governance_action_release_control_input_v0` 从 placeholder 推进为 **implemented object**（可合法接收/识别，仍不执行真实 release_control）

关联：
- 输入契约冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_V0.md`
- 输入契约占位输出：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_PLACEHOLDER_V0.md`
- release_control skeleton：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SKELETON_V0.md`
- release_control 状态对象实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- 执行器总输入对象实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`
- wiring（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 子动作标准化输入契约的**正式实现版文档**。
- 当前目标：把输入契约从 placeholder 推进到 `object_kind: implemented_v0` 的统一对象。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不改变现有主线执行行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在要先实现输入契约

- `release_control` skeleton 已存在。
- `release_control` 输入契约定义已存在（冻结）。
- `release_control` 状态对象已是 implemented object。
- 若无正式输入契约实现版，后续真实动作仍会依赖 placeholder 或散字段，容易打穿动作级边界。
- 因此必须先把输入契约正式实现出来。
- 但当前仍不能让 skeleton 消费后产生真实动作。

---

## C. implemented input contract 的最小定义（写死）

- 它不是 placeholder。
- 也不是 `release_control` 执行命令。
- 它是 `release_control` 子动作未来唯一合法输入对象的正式实现版。
- 作用：把上游合法依据收束为可被 `release_control` skeleton 接收的标准化对象（当前仍表达非可执行语义）。

---

## D. 当前最小输入依据（写死）

必须输入：

1) `navigation_governance_action_executor_input_v0`（implemented）  
- 主来源，且动作类型必须明确为 `release_control`

2) `navigation_governance_action_executor_readiness_gate_v0`  
- 执行前提一致性依据（不等于可执行）

3) `navigation_governance_action_executor_wiring_v0`  
- 接线一致性依据

可选只读（仅辅助一致性校验，不得扩权）：

- `navigation_governance_action_approval_status_v0`
- `navigation_governance_action_status_v0`

要求：relevant-only；不脑补；这些只是对象实现依据，不代表真实 `release_control` 已运行。

---

## E. 输出位（写死）

- `result.metadata["navigation_governance_action_release_control_input_v0"]`
- 本轮为 implementation：以 `object_kind` / 分类字段表达；不再以 placeholder 语义作为主体表达。

---

## F. 最小字段类别（实现）

至少实现：

1) 动作类型确认类  
2) 执行前提确认类（仍保守：不声明 ready）  
3) 约束确认类  
4) 目标控制面类（仅 upstream_control_handover_only）  

并写死：不扩展到路线/播报/记忆/迁移。

---

## G. 当前最小语义（写死）

产出 implemented 输入对象只表示：上游已能把 `release_control` 子动作所需最小输入信息整理成正式对象，skeleton 可合法接收；不表示真实 `release_control` 已执行，不表示控制权已交还，不表示路线改变或中台迁移。

---

## H. 当前不允许做什么（写死）

- 不允许 skeleton 拿到对象后直接执行真实动作
- 不允许触发真实 `release_control`
- 不允许触发真实 `rollback` / `interrupt`
- 不允许改路线
- 不允许触发语音播报
- 不允许触发中台真实迁移
- 不允许把 implemented input contract 当动作已执行

---

## I. 实现落点

- Builder：`capabilities/governance/runtime/navigation_governance_action_release_control_input_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`
- skeleton 识别-only：`capabilities/governance/runtime/navigation_governance_action_release_control_v0.py`（`accept_release_control_input_object`）

