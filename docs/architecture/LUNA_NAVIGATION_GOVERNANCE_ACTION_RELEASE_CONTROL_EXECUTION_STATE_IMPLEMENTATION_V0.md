# Luna — Navigation Governance Action Release Control Execution State Implementation v0（子动作执行过程状态对象：正式实现版）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-66：把 `navigation_governance_action_release_control_execution_state_v0` 从 placeholder 推进到 implemented object（落代码；仍为非动作）

关联：
- execution state 边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_V0.md`
- execution state 占位输出：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_PLACEHOLDER_V0.md`
- release_control skeleton：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SKELETON_V0.md`
- 状态对象实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- 结果对象实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`
- 子动作 wiring（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 子动作标准化 execution state 的**正式实现版**文档。
- 当前目标：把 execution state 从 placeholder 推进到 implemented object。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不改变现有主线执行行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在要先实现 execution state

- `release_control skeleton` 已存在。
- `release_control status object` 已是 implemented object。
- `release_control result object` 已是 implemented object。
- `release_control execution state` 定义已存在。
- `release_control execution state placeholder` 已存在（主链已占位）。
- 如果没有正式 execution state 实现版，后续真实动作只能回到 placeholder 或散字段，过程面会再次失控并与 result object 混写。
- 因此必须先把 execution state 正式实现出来。
- 但当前仍不能让 `release_control` 回传真实执行过程事实（不能把“对象实现”误当“已执行”）。

---

## C. implemented execution state 的最小定义（写死）

- 它不是 placeholder。
- 也不是 `release_control` 已进入真实执行事件。
- 它是 `release_control` 子动作未来唯一合法“执行过程回传对象”的实现版。
- 作用：把上游合法依据收束为可被治理链合法观察/消费的标准化对象。

---

## D. 当前最小输入依据（写死：只读）

必须只读（缺一则 relevant-only 不写）：

1) `navigation_governance_action_release_control_status_v0`  
- 主依据  
- 要求：对象存在且合法，且动作类型明确为 `release_control`

2) `navigation_governance_action_release_control_wiring_v0`  
- 一致性依据：仍处在合法接线链路内

可选只读（仅辅助一致性校验，不得扩权）：

- `navigation_governance_action_release_control_result_v0`
- `navigation_governance_action_release_control_readiness_gate_v0`

写死：不允许脑补；这些只是对象实现依据，不代表真实 `release_control` 已运行。

---

## E. 当前最小输出位（写死）

继续写入：

- `result.metadata["navigation_governance_action_release_control_execution_state_v0"]`

但对象语义为 implemented object（不是 placeholder），因此不再以 `*_placeholder` 作为主体表达。

---

## F. 当前最小字段类别（按冻结文档收敛）

至少实现 **3 类** 的最小可用表达：

1) 执行状态类  
2) 动作类型确认类  
3) 异常/阻断状态类  

说明（写死）：
- 执行影响类可以仍保持最小占位（但不能声称已生效）
- 回传绑定/路由类可以仍保持最小占位（不做真实绑定）

---

## G. 当前最小语义（写死）

当 implemented `navigation_governance_action_release_control_execution_state_v0` 被产出时，只表示：

- 上游控制链已能把 `release_control` 子动作所需最小执行过程信息整理成正式对象
- 治理链/中台未来可合法观察和消费该对象

它不表示（写死）：

- 真实 `release_control` 已执行
- 控制权已真实交还
- 路线已改变
- 中台已真实迁移
- 最终结果对象已成立

---

## H. 当前不允许做什么（写死）

- 不允许把 implemented execution state 伪装成真实动作已生效事实
- 不允许触发真实 `release_control`
- 不允许触发真实 `rollback` / `interrupt`
- 不允许改路线
- 不允许触发语音播报
- 不允许触发中台真实迁移
- 不允许把 implemented execution state 当动作已执行

---

## I. 代码落点（本轮落地）

- Builder：`capabilities/governance/runtime/navigation_governance_action_release_control_execution_state_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`
- skeleton 识别位（recognize-only）：`capabilities/governance/runtime/navigation_governance_action_release_control_v0.py`

