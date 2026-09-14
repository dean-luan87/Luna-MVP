# RULE_GOVERNED_EXECUTION

任何受治理 Phase 必须有 `PhaseGovernanceProfileV1`，并由 `resolve_applicable_governance_set` 根据 domain、owner、profile、contract refs 进行 exact matching。

Phase profile 不声明 applicable rule list。没有匹配规则时返回 `GOVERNANCE_SCOPE_UNRESOLVED`，preflight 返回 `GOVERNANCE_PREFLIGHT_BLOCKED`。本阶段没有实现 governance exemption shortcut。
