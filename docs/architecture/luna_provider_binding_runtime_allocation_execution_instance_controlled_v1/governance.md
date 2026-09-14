# Governance Backbone integration

Evaluation 直接复用 `PhaseGovernanceProfileV1`、
`CORE_GOVERNANCE_RULE_REGISTRY_V1`、applicable-rule resolver、preflight、postflight
和 `compute_unified_final_decision`。本 phase 使用通用的 mechanical-authority
profile 维度：允许形成 authoritative binding/allocation/identity records，但仍
禁止 runtime invocation、truth/world mutation、session、Gateway 和 Provider/Model
调用。责权记录分别覆盖 Provider Binding、Runtime Allocation 和 Execution Identity。

`RULE_GOVERNED_EXECUTION`、authority/responsibility symmetry、failure ownership、
requester/executor complexity、candidate/adapter/no-truth/no-runtime guards 均由
Backbone 与 phase verifier 联合验证；没有手写 applicable rule list。
