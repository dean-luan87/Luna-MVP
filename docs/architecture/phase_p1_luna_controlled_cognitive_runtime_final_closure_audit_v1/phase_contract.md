# Phase contract

The final audit is a candidate for closure only when all five mandatory
dimensions pass:

```text
operational_result = PASS
cognitive_logic_result = PASS
governance_result = PASS
traceability_result = PASS
contract_integrity_result = PASS
blocker_count = 0
```

The Verifier emits
`LUNA_CONTROLLED_COGNITIVE_RUNTIME_BASELINE_V1_CLOSED` only from those
observed conditions. Real runtime absence is deferred, not a failure.

