# Luna — Navigation Governance Action Approval Boundary Minimal Implementation v0（已批准治理动作边界层：最小非动作实现）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-38：将批准边界层从冻结文档推进为**统一对象的最小非动作实现**

关联：
- 批准边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_APPROVAL_BOUNDARY_V0.md`
- 治理动作边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_V0.md`
- 治理动作边界最小非动作实现：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_BOUNDARY_IMPLEMENTATION_V0.md`
- 治理动作执行器本体定义：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 治理动作执行器模块骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`
- 治理动作状态对象冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_STATUS_OBJECT_V0.md`

---

## A. 文档定位（写死）

- 这是已批准治理动作边界层的**正式实现版**文档。
- 当前目标：最小非动作实现，产出统一 `navigation_governance_action_approval_boundary_v0`。
- 当前不做真实回退/中断/释权；不接地图；不驱动语音/记忆；不改变现有主线行为。

---

## B. 为什么现在要先实现批准边界层

- governance action boundary 已有 implemented object。
- approval 结果集合与映射规则已冻结。
- 若无最小实现，执行器仍可能直接面对普通 `request_*`。
- 因此必须先把 approved boundary 对象实现出来。
- 当前仍不能触发任何真实治理动作。

---

## C. implemented approval boundary 的最小定义（写死）

- 不是真实批准执行链。
- 不是治理动作执行器。
- 是「普通动作边界 → 已批准动作边界」的正式实现版对象。
- 作用：收束为治理动作执行器未来可消费的 approved boundary 对象（当前仍非执行）。

---

## D. 当前最小输入依据（写死）

主输入：implemented `navigation_governance_action_boundary_v0`。

可选只读一致性校验：`navigation_rollback_and_interruption_governance_decision_v0`、`navigation_rollback_and_interruption_governance_entry_v0`、`navigation_real_executor_status_v0`、`navigation_execution_monitoring_status_v0`。

无合法 action boundary 对象则 relevant-only 不写。

---

## E. 输出位（写死）

- `result.metadata["navigation_governance_action_approval_boundary_v0"]`

最小结构：

```json
{
  "governance_action_approval_attempted": true,
  "governance_action_approval_scope": "navigation_governance_action_approval_boundary_v0",
  "governance_action_approval_status": "approved_hold_executor_state|approved_interrupt|approved_release_control|approved_rollback|approval_blocked",
  "reason": "..."
}
```

---

## F. 最小判断规则（实现口径）

见 `capabilities/mid_platform/runtime/navigation_governance_action_approval_boundary_v0.py`：已知 boundary 状态映射到五态之一；未知 boundary 状态保守为 `approval_blocked`。

---

## G. 实现落点

- Builder：`capabilities/mid_platform/runtime/navigation_governance_action_approval_boundary_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`（在 `navigation_governance_action_boundary_v0` 之后）
