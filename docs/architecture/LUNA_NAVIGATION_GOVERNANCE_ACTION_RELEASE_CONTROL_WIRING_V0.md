# Luna — Navigation Governance Action Release Control Wiring v0（Release Control 子动作接线边界：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_V0.md`  
**性质**：Phase-Next-59：冻结 `release_control readiness gate` 之后到 `release_control skeleton` 之前的接线边界（不落代码）

关联（已具备）：
- release_control readiness gate（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_IMPLEMENTATION_V0.md`
- release_control 输入契约实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`
- release_control 状态对象实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- release_control skeleton：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SKELETON_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 子动作接线边界的设计文档。
- 当前目标：冻结 `release_control readiness gate` 之后到 `release_control skeleton` 之前的接线边界。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在必须先定义 wiring 层

- 当前已经有 implemented `release_control readiness gate`。
- 当前已经有 implemented `release_control input contract` 与 implemented `release_control status object`。
- 当前已经有 `release_control skeleton`。
- 但还没有统一判断“何时合法接到 skeleton、接完后最多到什么状态”的接线层。
- 若不先冻结 wiring 层，后续很容易把 `ready_candidate` 误当成可执行动作。
- 因此必须先冻结“子动作就绪门之后的接线边界”。

---

## C. wiring 的最小定义（写死）

`release_control wiring` 是：

- 在 `release_control readiness gate` 已给出候选就绪的前提下，把 `release_control` 子动作最小合法接到 skeleton 的层。

它不是（写死）：

- 总治理动作执行器 wiring
- `release_control readiness gate`
- `release_control` 输入契约本身
- `release_control` 状态对象本身
- 真实 `release_control` 执行器本身
- 真实 `release_control` 动作执行

核心一句（写死）：

**release_control wiring 只负责把合格前提接到 release_control skeleton 的安全接线态，不直接执行任何动作。**

---

## D. 最小合法接线前提（写死，缺一不可）

1) implemented `navigation_governance_action_release_control_input_v0` 已存在  
2) implemented `navigation_governance_action_release_control_status_v0` 已存在  
3) `navigation_governance_action_release_control_readiness_gate_v0.release_control_readiness_status == "ready_candidate"`  
4) release_control skeleton identity / capability 正常（仍为 skeleton、不可真实执行）  

可选只读一致性校验（不得扩权）：

- `navigation_governance_action_executor_wiring_v0`
- `navigation_governance_action_approval_status_v0`

并写死：

- 少任一项都不允许接线。
- 这些只是接线前提，不是动作执行授权。

---

## E. 最小接线结果集合（写死）

- `wired_inactive`
- `wired_action_ready`
- `blocked`
- `not_applicable`

语义（写死）：

- `wired_inactive`：合法接到 skeleton，但保持保守静止态；不表示动作已开始  
- `wired_action_ready`：合法接到 skeleton，进入可进一步推进的安全接线态；不表示真实动作已开始  
- `blocked`：硬阻断/一致性/identity 问题；不允许接线  
- `not_applicable`：前提链不成立，不进入接线流程

---

## F. 当前最小判断原则（克制、默认保守）

- 核心对象缺失 → `not_applicable`
- readiness gate 不是 `ready_candidate` → `not_applicable`
- skeleton identity/capability 不合法 → `blocked`
- 输入对象 / 状态对象明显不一致 → `blocked`
- 前提齐备但仍需最保守接线态 → `wired_inactive`

并写死：

- 默认偏保守
- `wired_action_ready` 只在极窄条件下出现
- 不做复杂评分树

---

## G. 与现有链路的关系（写清）

- readiness gate 负责候选判断；wiring 负责把候选条件接到 skeleton；两者不能混用。
- input contract 是主输入面；wiring 不替代 input contract。
- status object 是回传承载面；wiring 只检查在位，不等于动作发生。
- 总执行器 wiring 负责总执行器接线；本 wiring 负责子动作接线；两者不能跨层替代。
- wiring 是 skeleton 的前置接线层，不等于 skeleton 自己执行动作。

---

## H. 当前仍然不能做什么（必须写死）

- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许直接改路线/语音播报/中台真实迁移
- 不允许把 `wired_action_ready` 当 `release_control` 已开始

---

## I. 当前阶段结论（写死一句）

**当前阶段只适合冻结 release_control 子动作接线边界；即使未来落最小实现，也只能先进入安全接线态，不能直接执行 release_control。**

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - release_control wiring 的最小非动作实现
- 再之后才考虑：
  - release_control 最小真实实现
- 当前不跨这两步

---

## K. 未来接线结果样例（仅说明，不落代码）

```json
{
  "release_control_wiring_attempted": true,
  "release_control_wiring_scope": "navigation_governance_action_release_control_wiring_v0",
  "release_control_wiring_status": "wired_inactive|wired_action_ready|blocked|not_applicable",
  "reason": "..."
}
```

