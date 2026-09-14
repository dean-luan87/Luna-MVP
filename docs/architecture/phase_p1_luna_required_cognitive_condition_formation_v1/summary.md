# Summary

本 Phase 为 A-Route 增加一个最小、candidate-only 的 Required Cognitive
Condition formation boundary。它用显式 governed objective condition rules
与当前最小认知情况的集合关系，形成当前 active required set，并保留
satisfied/dormant/recoverable 状态。

关键区别：

```text
Required Cognitive Condition = 为推进 objective 当前必须成立/获知的条件
Current Cognitive Coverage    = 当前已经拥有的相关认知信息
Information Need              = Required Conditions - Current Coverage
```

因此本实现不是把 `GoalContextV1.success_condition_refs` 改名，而是在
objective applicability、state activation/suppression、coverage satisfaction
和 minimum-set selection 后形成 candidate。Requirement applicability 与
satisfaction 是正交维度：已满足的 required condition 仍保留在
`active_required_condition_refs`，只通过 `satisfied_condition_refs` 表达其
当前 coverage。既有 Information Need 算法继续负责缺口计算，未被修改。

本阶段的兼容扩展允许一个语义 Requirement 声明多个显式 governed
`alternative_satisfaction_basis_refs`。任一当前 coverage basis 即可使该
Requirement `SATISFIED`；candidate 只记录实际命中的 coverage ref。没有
alternative basis 的旧规则继续使用 exact `satisfaction_coverage_refs`。
Requirement 不再因为满足而从 required set 消失，且该扩展不把 acquisition
path 变成 Required Condition。

Self information、External information、Role、Field 和 governed Context
signals 通过同一个 exact-reference selection mechanism 参与；opaque refs
只保留为 context/provenance。

阶段状态仍为：`WAITING_FOR_USER_TERMINAL_VERIFICATION`。
