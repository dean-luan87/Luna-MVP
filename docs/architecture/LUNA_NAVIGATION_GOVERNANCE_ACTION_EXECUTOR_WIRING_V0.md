# Luna — Navigation Governance Action Executor Wiring v0（治理动作执行器接线边界：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_V0.md`  
**性质**：Phase-Next-47：冻结 readiness gate 之后到 executor skeleton 之前的**接线边界**（不落代码）

**核心一句（写死）**：governance action executor wiring 只负责把合格前提接到 executor skeleton 的**安全接线态**，不直接执行任何治理动作。

**最小合法接线前提（缺一不可）**：

1. implemented `navigation_governance_action_executor_input_v0`
2. implemented `navigation_governance_action_status_v0`
3. implemented `navigation_governance_action_approval_status_v0`
4. `navigation_governance_action_executor_readiness_gate_v0.governance_action_executor_readiness_status == "ready_candidate"`
5. governance action executor skeleton identity / capability 正常
6. 可选：implemented `navigation_governance_action_approval_boundary_v0`（仅一致性校验）

**最小接线结果集合**：`wired_inactive` | `wired_action_ready` | `blocked` | `not_applicable`

**下一步**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_IMPLEMENTATION_V0.md`（最小非动作实现）。
