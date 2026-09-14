# Luna — Navigation Governance Action Release Control Wiring Minimal Implementation v0（子动作接线：最小非动作实现）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-60：把 `release_control wiring` 从设计冻结推进到统一结果对象的最小非动作实现（只读、可观察、可回归）

关联：
- 接线边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_V0.md`
- readiness gate（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_IMPLEMENTATION_V0.md`
- 输入契约实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`
- 状态对象实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- release_control skeleton：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SKELETON_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 子动作接线边界的正式实现版文档（最小非动作实现）。
- 当前目标：把 wiring 从冻结文档推进到最小非动作实现，产出统一接线结果对象。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在要先实现 wiring

- `release_control readiness gate` 已有 implemented object。
- `release_control input contract / status object` 都已有 implemented object。
- `release_control skeleton` 已存在。
- wiring 的最小前提与结果集合已冻结。
- 若无最小实现，后续实验线会回到各模块各自判断“能不能接到 skeleton”，边界易漂移。
- 因此必须先把 wiring 对象实现出来。
- 但当前仍不能触发任何真实治理动作。

---

## C. implemented wiring 的最小定义（写死）

- 它不是真实 `release_control` 执行器。
- 不是真实批准链。
- 它是“`release_control` 子动作从 readiness 到 skeleton 的最小统一接线对象”的最小实现版。
- 作用：把 input contract、status object、readiness、子动作本体在位性收束成 `wired_inactive/wired_action_ready/blocked/not_applicable`。

---

## D. 当前最小输入依据（写死：只允许标准化对象）

必须输入：

1) implemented `navigation_governance_action_release_control_input_v0`  
2) implemented `navigation_governance_action_release_control_status_v0`  
3) `navigation_governance_action_release_control_readiness_gate_v0`（且为 `ready_candidate` 才进入接线分支）  
4) release_control skeleton identity / capability（在位且仍为 skeleton）  

可选只读一致性（不得扩权）：

5) `navigation_governance_action_executor_wiring_v0`  
6) `navigation_governance_action_approval_status_v0`  

写死：

- 没有合法 input object 时，不得进入接线正路径（实现口径：输出 `not_applicable` 或 relevant-only）。
- 禁止直接读取 `request_* / approved_* / raw metadata` 作为接线主输入。

---

## E. 当前最小输出位（写死）

写入：

- `result.metadata["navigation_governance_action_release_control_wiring_v0"]`

最小结构：

```json
{
  "release_control_wiring_attempted": true,
  "release_control_wiring_scope": "navigation_governance_action_release_control_wiring_v0",
  "release_control_wiring_status": "wired_inactive|wired_action_ready|blocked|not_applicable",
  "reason": "..."
}
```

---

## F. 当前最小判断规则（与实现对齐）

- 核心对象缺失 → `not_applicable`
- readiness gate 不是 `ready_candidate` → `not_applicable`
- skeleton identity/capability 不合法 → `blocked`
- 输入对象/状态对象不一致（动作类型不匹配）→ `blocked`
- 默认保守 → `wired_inactive`
- 仅在可选一致性（executor wiring + approval status）同时在位时，极窄升级 → `wired_action_ready`

---

## G. 当前最小语义（写死）

产出 wiring 对象只表示：系统已能统一判断 `release_control` 子动作是否被合法接到 skeleton；不表示真实 `release_control` 已执行、不表示控制权已交还、不表示路线改变或中台迁移、不表示动作已开始。

---

## H. 当前不允许做什么（写死）

- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许直接改路线/语音播报/中台真实迁移
- 不允许把 `wired_action_ready` 当 `release_control` 已开始

---

## I. 实现落点

- Builder：`capabilities/mid_platform/runtime/navigation_governance_action_release_control_wiring_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`
- skeleton 识别-only：`capabilities/governance/runtime/navigation_governance_action_release_control_v0.py`（`wire_release_control`）

