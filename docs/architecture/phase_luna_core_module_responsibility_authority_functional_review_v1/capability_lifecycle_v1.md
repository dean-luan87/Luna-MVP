# Capability Lifecycle v1

The lifecycle is split across domains rather than one Capability state machine:

```text
Registry definition
→ logical availability
→ requirement received
→ scope assessed
→ logical resolution candidate
→ Runtime Admission ready/blocked/degraded/stale
→ Executable Capability Candidate
→ Provider Admission
→ execution/result/evidence
```

Ownership:

- registry definition, slot and logical lifecycle: Capability Governance;
- model asset/provisioning: Model Manager;
- health/integrity evidence: Diagnostics/Model Manager sources;
- admission assessment: Capability Admission Governance;
- executable candidate: Runtime Admission boundary;
- Provider admission/execution: Provider Governance;
- evidence mapping: Observation/Gateway;
- cognitive consequence: A; global consequence: Brain.

Do not collapse logical availability, runtime availability and execution result
into one state.
