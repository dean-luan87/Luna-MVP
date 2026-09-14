# Compatibility

## Legacy exact coverage

没有 `alternative_satisfaction_basis_refs` 的既有 rule 不迁移：

```text
condition_ref
  + exact satisfaction_coverage_refs ⊆ current coverage
  → SATISFIED
```

缺少任一 legacy coverage ref 时仍为 `UNSATISFIED`。因此既有 Required
Cognitive Condition fixtures 保持兼容。

## New semantic requirement

有显式 alternatives 的 rule 使用：

```text
requirement_ref
  + (basis A OR basis B OR basis C)
  + current coverage contains basis B
  → requirement SATISFIED
```

`satisfaction_coverage_refs` 只包含实际命中的 basis。Requirement 的 active
required set 不变；既有 Information Need owner 仍负责从 required conditions
和 current coverage 计算 necessary unknown。

Sandbox 的 local adapter projection 把形成结果的
`satisfied_condition_refs` 与原始 coverage 合并为 Need 输入 coverage。这是
下游接口适配，不是对 Information Need subtraction algorithm 的重写。
