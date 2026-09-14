# Contract

## Canonical change

`GovernedObjectiveConditionRuleV1` 增加：

```text
alternative_satisfaction_basis_refs: Tuple[str, ...]
```

它是一个 semantic requirement 对显式 governed satisfaction alternatives 的
引用集合。它不是 Acquisition Strategy、Capability Requirement、Observation
Demand、Provider、Model 或 evidence-fusion result。

## Evaluation semantics

```text
if alternative_satisfaction_basis_refs is non-empty:
    matched = alternatives ∩ current cognitive coverage
    SATISFIED iff matched is non-empty
    satisfaction_coverage_refs = actual matched ref(s)
else:
    preserve exact legacy coverage semantics
```

当前实现保留确定性的实际匹配 coverage 引用；声明但未命中的候选 basis 不
会被伪装成 satisfaction evidence。

`active_required_condition_refs` 继续表达当前 required semantics，不因
satisfaction 而删除 requirement。`satisfied_condition_refs` 表达已经满足的
required subset。未选 minimum-set alternative 仍可为 `DORMANT`；这属于
requirement selection，不是 coverage satisfaction suppression。

## Boundary

```text
Cognitive Requirement
  ≠ Satisfaction Basis
  ≠ Information Need
  ≠ Information Gap
  ≠ Acquisition Path
```

本阶段只处理一对多 alternative basis 的 ANY satisfaction。没有通用 basis
到多个 requirements 的 many-to-many engine、嵌套 AND/OR、权重、阈值、排序、
fallback hierarchy 或 evidence fusion。
