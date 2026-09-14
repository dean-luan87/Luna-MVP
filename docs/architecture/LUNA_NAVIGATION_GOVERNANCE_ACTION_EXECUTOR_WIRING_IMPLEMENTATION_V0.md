# Luna — Navigation Governance Action Executor Wiring Minimal Implementation v0（治理动作执行器接线：最小非动作实现）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-48：把 wiring 从设计冻结推进为统一结果对象的最小非动作实现（只读、可观察、可回归）

关联：

- 接线边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_V0.md`
- 就绪门控冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_V0.md`
- 就绪门控最小实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_IMPLEMENTATION_V0.md`
- 执行器本体最小定义：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 执行器模块骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`

---

## A. 文档定位（写死）

- 这是治理动作执行器接线边界的**正式实现版文档**（最小非动作实现）。
- 当前目标：把 wiring 从冻结文档推进到最小非动作实现，产出统一接线结果对象。
- 当前不做真实批准链执行。
- 当前不做真实治理动作实现。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在要先实现 wiring

- governance action executor readiness gate 已有 implemented object。
- executor input / action status / approval status 都已有 implemented object。
- wiring 的最小前提与结果集合已冻结（`wired_inactive` / `wired_action_ready` / `blocked` / `not_applicable`）。
- 若无最小实现，后续仍会各自判断「是否接到 skeleton」，边界漂移风险高。
- 因此必须先把 wiring 对象实现出来。
- 但当前仍**不能触发任何真实治理动作**。

---

## C. implemented wiring 的最小定义（写死）

- 它不是真实治理动作执行器。
- 不是真实批准链。
- 它是「从 readiness 到 executor skeleton 的最小统一接线对象」的正式实现版。
- 作用：把 input object、approval status、action status、readiness、executor identity 收束为 **四态之一**。

---

## D. 当前最小输入依据（写死：只消费标准化对象）

1. implemented `navigation_governance_action_executor_input_v0`
2. implemented `navigation_governance_action_status_v0`
3. implemented `navigation_governance_action_approval_status_v0`
4. implemented `navigation_governance_action_executor_readiness_gate_v0`（`ready_candidate` 才可能进入安全接线正路径）
5. governance action executor skeleton 的 identity / capability
6. 可选只读：`navigation_governance_action_approval_boundary_v0`（仅一致性校验，不得扩权）

写死禁止：

- 没有合法 executor input object 时，不得声称已完成「合法接线」的正路径（实现上可落到 `not_applicable`）。
- 禁止直接读取 `request_* / approved_* / raw metadata` 作为接线主输入。

---

## E. 当前最小输出位（写死）

- `result.metadata["navigation_governance_action_executor_wiring_v0"]`

最小结构：

```json
{
  "governance_action_executor_wiring_attempted": true,
  "governance_action_executor_wiring_scope": "navigation_governance_action_executor_wiring_v0",
  "governance_action_executor_wiring_status": "wired_inactive|wired_action_ready|blocked|not_applicable",
  "reason": "..."
}
```

---

## F. 当前最小判断规则（与实现对齐）

- 规则 1：核心对象缺失 → `not_applicable`
- 规则 2：readiness gate 不是 `ready_candidate` → `not_applicable`
- 规则 3：executor skeleton identity / capability 不合法 → `blocked`
- 规则 4：批准状态 / 输入对象 / 状态对象明显不一致 → `blocked`
- 规则 5：前提齐备但仍保持最保守接线态 → `wired_inactive`；仅当可选批准边界一致性审计通过时，**极窄**升级为 `wired_action_ready`

默认偏保守；不做复杂评分模型。

---

## G. 当前最小语义（写死）

产出 wiring 对象只表示：系统已能统一判断是否把治理动作执行器**合法接到** skeleton 的安全接线态；不表示任何真实治理动作已执行或已开始。

---

## H. 当前不允许做什么（写死）

- 不允许真实回退/中断/释放控制权动作
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 `wired_action_ready` 当治理动作已开始

---

## I. 实现落点

- Builder：`capabilities/mid_platform/runtime/navigation_governance_action_executor_wiring_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`（readiness gate 之后）
- Skeleton 识别-only：`capabilities/governance/runtime/navigation_governance_action_executor_v0.py`（`wire_governance_action_executor`）
