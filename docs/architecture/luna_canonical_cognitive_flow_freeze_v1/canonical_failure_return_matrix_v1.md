# Canonical Failure Return Matrix v1

| Condition | Detecting/responsible boundary | Immediate return | Semantic evaluator | Global escalation / continuation |
|---|---|---|---|---|
| Envelope invalid/stale | Working Envelope | A/Brain | A | refresh or global grant review; Concern continues unless Brain closes |
| Evidence insufficient | A | A acquisition loop | A | Brain only if global constraint/Concern issue |
| Evidence stale/duplicate | Gateway/Diagnostics | A/refresh | A | usually continues |
| Capability unavailable | Runtime Admission/Capability | A/Task | A | alternative cognition only through governed path |
| Runtime blocked | Runtime Admission | Task/A | A | Brain for protected resource/policy |
| Provider unavailable | Provider Governance | Observation/Action/Task | A/Outcome | Brain for global degradation |
| Provider invocation failed | Provider | Task/A/Outcome | A/Outcome | Concern may continue |
| Decision rejected | Decision Governance | A | A/Decision | Brain for veto/Goal conflict |
| Task blocked | Task | A/Decision | A | Brain for global resource/safety |
| Action blocked | Action Governance | Task/A | A/Outcome | Brain for policy/revocation |
| Action failed/partial | Action/Provider | Task/A/Outcome | A/Outcome | Concern continues unless Brain consequence |
| Action result uncertain | Action/Outcome | A/Outcome | A/Outcome | no fabricated success |
| Safety blocked | Safety/enforcing boundary | mechanical block | A for local meaning | Brain override/escalation |
| Permission revoked | Permission/enforcing boundary | invalidate/cancel | A/Brain | global authorization consequence |
| Resource degraded | Resource/Runtime/Provider | degraded candidate/block | A/Decision | Brain protected reserve |
| Protocol mismatch | Diagnostics/validator/Protocol | reject binding | affected owner | Protocol change/adaptation |
| Model retired | Model/Runtime | invalidate candidate | A/Decision/Task | governed alternate or continue |
| Outcome mismatch/uncertain | Outcome Evaluation | Outcome Candidate | Brain final; A local | Concern continues or closes only by Brain |

