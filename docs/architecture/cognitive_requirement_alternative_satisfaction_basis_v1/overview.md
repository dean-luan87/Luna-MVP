# Cognitive Requirement Alternative Satisfaction Basis v1

状态：`IMPLEMENTATION_READY_FOR_USER_EXECUTION`

本阶段实现最小的语义边界：

```text
Semantic Cognitive Requirement
  → explicit governed alternative satisfaction basis refs
  → satisfaction evaluation
  → Information Need subtraction
```

例如 `exit_direction_known` 是一个 Cognitive Requirement；signage、
spatial/map 或 human-flow/environment 只能作为显式 governed Satisfaction
Bases。任意一个当前有效的 basis 覆盖即可满足该 requirement。它们不是
Required Conditions 的并列 AND 条件，也不是 Acquisition Paths。

本阶段复用 `GovernedObjectiveConditionRuleV1`，只增加一个可选字段
`alternative_satisfaction_basis_refs`。有该字段时执行 ANY basis coverage；
没有该字段时继续 exact legacy coverage。Requiredness 与 satisfaction 保持
正交：已满足的 requirement 仍保留在 `active_required_condition_refs`，
`satisfied_condition_refs` 与 candidate 的 `satisfaction_coverage_refs` 单独
表达 satisfaction。

Information Need 的核心 `required - coverage` subtraction 未改变。Sandbox
adapter 仅将已验证的 satisfied requirement refs 纳入 Need 的 coverage
projection，使现有下游能自然消除已满足 gap。

本阶段不实现 Multiple Sufficient Condition Sets、Boolean sufficiency、
evidence fusion、confidence algebra、Strategy Coordination、Observation
Demand、真实 acquisition 或任何 execution/runtime 能力。
