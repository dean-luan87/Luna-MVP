# Protocol State Ownership v1

| State | Classification | Owner |
|---|---|---|
| Protocol identity/canonical contract | AUTHORITATIVE | Protocol Governance |
| Canonical/schema/contract version | AUTHORITATIVE | Protocol Governance / contract owner |
| Compatibility declaration | AUTHORITATIVE | Protocol Governance |
| Lifecycle/deprecation/supersession | AUTHORITATIVE | Protocol Governance |
| Change proposal/approval | CANDIDATE / AUTHORITATIVE after approval | Protocol Governance |
| Producer/consumer binding | REFERENCE_ONLY / owner-declared | Producer/consumer |
| Adapter mapping | AUTHORITATIVE for adapter boundary | Adapter owner under protocol declaration |
| Migration requirement | AUTHORITATIVE declaration | Protocol Governance |
| Migration implementation | EXTERNAL | Affected source/consumer owner |
| Observed drift/diagnostic snapshot | REFERENCE_ONLY / LOCAL_DERIVED | System Diagnostics |
| Source payload/source-state version | EXTERNAL | Source owner |
| Historical protocol ref | REFERENCE_ONLY | Registry/history |
