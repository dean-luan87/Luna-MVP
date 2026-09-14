# Luna — Navigation Governance Action Release Control Minimal Definition v0（治理动作：Release Control 最小真实动作定义冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_DEFINITION_V0.md`  
**性质**：Phase-Next-49：治理动作执行器未来第一类真实动作 `release_control` 的最小定义（设计冻结；不落代码、不触发真实动作）

基于（已具备）：
- 治理动作执行器本体最小定义：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 治理动作执行器模块骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`
- 执行器输入对象（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`
- 就绪门控（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_IMPLEMENTATION_V0.md`
- 接线边界（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_IMPLEMENTATION_V0.md`
- 治理动作边界（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_V0.md`
- 已批准治理动作边界（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_V0.md`
- release_control 动作级输入契约（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_V0.md`
- release_control 子动作状态对象（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_V0.md`
- release_control 子动作就绪门控（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_V0.md`
- release_control 子动作结果对象（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_V0.md`
- release_control 子动作结果占位输出：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_PLACEHOLDER_V0.md`
- release_control 子动作执行过程状态面（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_V0.md`
- release_control 子动作执行过程状态占位输出：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_PLACEHOLDER_V0.md`
- release_control 子动作执行过程状态正式实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`
- release_control 子动作最小真实执行器（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_V0.md`
- release_control 子动作最小真实执行器骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_EXECUTOR_SKELETON_V0.md`

---

## A. 文档定位（写死）

- 这是治理动作执行器**第一类真实动作** `release_control` 的最小定义文档。
- 当前目标：冻结 `release_control` 动作边界。
- 当前不做真实动作实现。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么先做 release_control（写清）

- 相比 `rollback`：`release_control` 不直接改路径、不承诺回退效果，风险更低。
- 相比 `interrupt`：`release_control` 更接近“收权/交权”，而不是强打断执行链。
- 因此它更适合作为治理动作执行器“第一类最小真实动作”的定义起点（先把边界钉死，再谈实现）。

---

## C. release_control 的最小定义（写死）

`release_control` 是：

- 在已批准动作边界、输入对象、readiness、wiring 都成立后，把当前控制权从治理动作执行器链路**交还**上游治理链/中台控制面的动作类型。

它不是（写死）：

- `rollback`
- `interrupt`
- 路线改写
- 语音播报
- 中台迁移本身

---

## D. 最小合法输入（写死：只允许标准化对象）

仅允许在以下前提全部成立时进入 `release_control`（缺一不可）：

1) **已合法接线**的治理动作执行器输入对象  
- 只能来自 `navigation_governance_action_executor_input_v0`（implemented object），并已通过 wiring 进入安全接线态（见后续第 3 点）。

2) `approved_release_control` 对应的动作类型依据  
- 输入对象内部的 `approved_action_type` 必须明确为 `release_control`（或 `release_control` 的标准化等价名），且来源链路为 approval boundary → input object（不允许从散字段“推断”）。

3) readiness / wiring 结果为允许进入第一真实动作实验线的前提  
- readiness gate：`ready_candidate`  
- wiring：至少为 `wired_inactive`（更保守）或 `wired_action_ready`（更窄更强的安全接线态）

4) 状态回传面已在位  
- `navigation_governance_action_status_v0`（implemented object）作为未来执行后的回传承载面必须在位。

并写死：

- 没有这些，不允许进入 `release_control` 动作。
- 不能直接消费普通 `request_release_control`（它只是 action boundary 的类别边界，不是可执行输入面）。

---

## E. 最小结果集合（只定义语义，不实现）

建议最小结果集合（写死仅语义，不落代码）：

- `release_control_requested`
- `release_control_blocked`
- `release_control_completed`
- `release_control_failed`

说明（写死）：

- 这些结果是未来真实实现的“最小状态/结果集合”。
- 当前只冻结语义与边界，不代表系统能产出这些真实结果。

---

## F. 最小状态约束（写清）

- `release_control_completed` **不等于**路线已改变。
- `release_control_completed` **不等于**中台已迁移完成。
- `release_control_completed` 只表示：控制权已按定义交还上游控制面（语义定义层面）。

---

## G. 不负责什么（必须写死）

- 不负责 `rollback`
- 不负责 `interrupt`
- 不负责改路线
- 不负责语音播报
- 不负责记忆写入
- 不负责中台迁移逻辑本身

---

## H. 当前仍然不能做什么（必须写死）

- 不允许直接做真实 `release_control` 实现
- 不允许借 `release_control` 顺手做 `rollback` / `interrupt`
- 不允许触发地图、语音、记忆、中台真实迁移
- 不允许把定义文档当成动作已实现

---

## I. 与 request_/approved_/wiring 的关系（写清）

- `request_release_control`：action boundary 层的“理论动作类别边界”；不等于可执行输入。
- `approved_release_control`：approval boundary 层的“已批准动作边界”；仍不等于可执行输入。
- executor input object：执行器唯一合法输入面；`release_control` 必须以它为主输入依据。
- readiness gate：判断进入动作层候选条件；不等于动作授权或动作已开始。
- wiring：把候选条件安全接到 skeleton；不等于动作执行。
- executor skeleton：未来动作执行载体；当前仍为 recognize-only / non-action。

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - `release_control` 的最小 skeleton / placeholder / implementation 方案
- 当前不跨这一步（不落代码、不触发真实动作）。

