# Governance profiles

Canonical type：`PhaseGovernanceProfileV1`。

Profile 只声明 Phase identity、owner、domains、touched owners、maturity/runtime level、authority/responsibility refs、input/output contracts、protocol/constitution refs 和 boundary capabilities。

第一版 common profiles：

- `CANDIDATE_ONLY`
- `READ_ONLY`
- `NO_TRUTH`
- `NO_WORLD_MUTATION`
- `NO_RUNTIME`
- `NO_PROVIDER_INVOCATION`
- `NO_MODEL_INVOCATION`
- `NO_DECISION_ACTION_TASK`

Profile 不可直接选择 applicable rules。
