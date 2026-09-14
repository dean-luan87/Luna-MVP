# Luna — Navigation Governance Action Release Control Readiness Gate Minimal Implementation v0（子动作就绪门控：最小非动作实现）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-58：把 `release_control readiness gate` 从冻结推进到最小非动作实现（只读、可观察、可回归）

关联：
- readiness gate 冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_V0.md`
- release_control 输入契约实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`
- release_control 状态对象实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- release_control skeleton：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SKELETON_V0.md`
- 总执行器 readiness gate（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_IMPLEMENTATION_V0.md`
- 执行器接线（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 子动作就绪门控的正式实现版文档（最小非动作实现）。
- 当前目标：把 readiness gate 从冻结文档推进到最小非动作实现，产出统一门控结果对象。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在要先实现 readiness gate

- `release_control input contract` 已有 implemented object。
- `release_control status object` 已有 implemented object。
- `release_control skeleton` 已存在。
- readiness gate 的门控类别与结果集合已冻结（ready_candidate/not_ready/blocked）。
- 若无最小实现，后续 `release_control` 实验线会回到各模块各自判断“能不能进入动作层”，边界易脏。
- 因此必须先把子动作 readiness gate 对象实现出来。
- 但当前仍不能触发任何真实治理动作。

---

## C. implemented readiness gate 的最小定义（写死）

- 它不是真实 `release_control` 执行器。
- 不是真实批准链。
- 它是“`release_control` 子动作进入未来动作层前的最小统一门控对象”的最小实现版。
- 作用：把 input contract、status object、上游 wiring/readiness、子动作本体在位性收束成一个 `ready_candidate/not_ready/blocked` 结果。

---

## D. 当前最小输入依据（写死：只允许标准化对象）

必须输入：

1) implemented `navigation_governance_action_release_control_input_v0`（主输入）  
2) implemented `navigation_governance_action_release_control_status_v0`（承载面在位性）  
3) `navigation_governance_action_executor_wiring_v0`（接线一致性）  
4) `navigation_governance_action_executor_readiness_gate_v0`（总 gate 一致性）  
5) release_control skeleton identity / capability（在位且仍为 skeleton）  

可选只读：

6) implemented `navigation_governance_action_approval_status_v0`（仅一致性观察，不得扩权）  

写死：

- 没有合法 release_control input object 时，不得产出 `ready_candidate`（实现口径：relevant-only 不写）。
- 禁止直接读取 `request_* / approved_* / raw metadata` 作为门控主输入。

---

## E. 当前最小输出位（写死）

写入：

- `result.metadata["navigation_governance_action_release_control_readiness_gate_v0"]`

最小结构：

```json
{
  "release_control_readiness_attempted": true,
  "release_control_readiness_scope": "navigation_governance_action_release_control_readiness_gate_v0",
  "release_control_readiness_status": "ready_candidate|not_ready|blocked",
  "reason": "..."
}
```

---

## F. 当前最小判断规则（克制、默认保守）

- 主输入对象缺失 → relevant-only 不写（或在更高层统一 not_ready；本实现选择 relevant-only）  
- release_control skeleton 不在位 / identity 不匹配 → `blocked`  
- 上游 wiring/readiness 缺失或不一致 → `blocked`  
- 子动作状态承载面未就绪 → `not_ready`  
- 对象齐备但约束仍不允许进入动作层 → `not_ready`  
- 仅在极窄条件下 → `ready_candidate`  

---

## G. 当前最小语义（写死）

产出该 gate 对象只表示：系统已能统一判断 `release_control` 是否具备进入未来动作层候选条件；不表示真实 `release_control` 已执行、不表示控制权已交还、不表示路线改变或中台迁移、不表示动作已开始。

---

## H. 当前不允许做什么（写死）

- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许直接改路线/语音播报/中台真实迁移
- 不允许把 `ready_candidate` 当动作已开始

---

## I. 实现落点

- Builder：`capabilities/mid_platform/runtime/navigation_governance_action_release_control_readiness_gate_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`
- skeleton 识别-only：`capabilities/governance/runtime/navigation_governance_action_release_control_v0.py`（`accept_release_control_readiness_gate`）

