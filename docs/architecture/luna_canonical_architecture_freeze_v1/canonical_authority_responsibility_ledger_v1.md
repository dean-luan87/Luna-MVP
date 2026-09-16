# Canonical Authority / Responsibility Ledger v1

| Authority domain | Canonical owner | Responsibility | Allowed mutation / admission | Candidate producers | Failure owner | Semantic / global consequence |
|---|---|---|---|---|---|---|
| Goal / Concern / Grant | Brain | Correct global work scope and grant | Create, modify, supersede, close | A, Decision, Outcome candidates | Brain | Brain / A as applicable |
| A local cognition | A | Correct Need, Hypothesis, relevance, Sufficiency and Next-step | A-local semantic state | Envelope, Evidence, B-CR, results | A | A local; Brain if global |
| Intent | Intent Governance | Intent identity/lifecycle correctness | Intent admission/update/supersession | A/Brain/Outcome candidates | Intent Governance | A/Brain |
| Role / Identity / Relationship | Role source governance | Identity and relationship truth | Source lifecycle | External source systems | Source owner | Permission/Perspective consumers |
| Perspective Projection | Perspective boundary | Correct role-conditioned derived projection | Projection result only | Role + shared information | Projection boundary | A-local use |
| Field | Field | Correct admitted operational transition/state | Field admission/reducer mutation | Gateway/Observation event candidates | Field | A/Brain |
| Context | Context | Correct situation framing/validity | Context lifecycle | Field/World/Task/source refs | Context | A/Brain |
| Current World candidate | Current World / State Formation | Correct candidate formation, version, stale/supersession | Candidate formation/version, no Truth | Evidence/Gateway/State Formation | Current World boundary | A |
| Attention | Attention | Correct allocation/competition | Focus allocation candidate | A, Role, Task, constraints | Attention | A |
| Capability / Slot | Capability Governance | Correct taxonomy, scope, logical resolution and binding lifecycle | Capability and Capability↔Model binding lifecycle | A/Task/Model declarations | Capability Governance | Runtime Admission |
| Runtime Admission | Runtime Admission | Correct executable eligibility assessment | Runtime admission candidate | Capability/Model/Diagnostics/constraints | Runtime Admission | Task/A/Brain |
| Model declaration | Model Governance | Correct model identity, asset, version, loader, dependency and lifecycle metadata | Registration/provisioning/retirement | Provisioning/evaluation candidates | Model Governance | Runtime Admission |
| Model↔Provider binding | Provider Governance | Correct provider-facing compatibility binding | Binding lifecycle | Model/Provider declarations | Provider Governance | Provider Admission |
| Provider runtime | Provider Governance | Correct runtime invocation/result boundary | Provider admission/invocation | Runtime/Action/Observation inputs | Provider Governance | Task/A/Outcome |
| Observation request | Observation | Correct acquisition request identity/lifecycle/correlation | Observation request lifecycle | A/Attention/Runtime Admission | Observation | A/Gateway |
| Evidence admission | Observation Gateway | Correct normalization, provenance, freshness and correlation | Evidence admission record | Provider/Observation results | Gateway | A/Field/Current World |
| Decision commitment | Decision Governance | Correct commitment, revocation and supersession | Decision lifecycle/commitment | A/Brain/Intent | Decision Governance | Task/Action/A |
| Task organization | Task | Correct dependencies, readiness, progress and completion | Task lifecycle/readiness | Decision/Action results | Task | A/Outcome |
| Action admission | Action Governance | Correct side-effect target/precondition/constraint enforcement | Action candidate/admission | Decision/Task | Action Governance | Task/A/Outcome |
| Outcome candidate | Outcome Evaluation | Correct multi-source evaluation and uncertainty | Outcome candidate formation/evaluation | Action/Task/A/source refs | Outcome Evaluation | Brain |
| Brain adjudication | Brain | Correct final global consequence and Assimilation | Final Outcome/Concern/Goal consequence | Outcome Candidate | Brain | Loop command / future candidates |
| Safety policy | Brain/Safety | Correct protected-state and non-harm policy | Policy/ref publication and override | Risk evidence/diagnostics | Safety/Brain for policy; enforcing boundary for enforcement | A/Brain |
| Permission policy | Permission Governance | Correct scoped allow/deny/grant/revocation | Permission admission/revocation | Identity/Role/Context evidence | Permission Governance | A/Brain |
| Resource policy | Resource Governance | Correct ceilings, reserves, budgets and reservations | Budget/reservation admission | Diagnostics/priority | Resource Governance | A/Brain |
| Diagnostic classification | System Diagnostics | Correct observed fact, health/drift/freshness classification | Diagnostic evidence/finding/snapshot | Probes/telemetry | Diagnostics | Governance/admission consumers |
| Working Envelope binding | Working Envelope | Correct Concern/Grant/source binding, version/invalidation and supersession | Envelope admission/refresh/supersession | Brain/source refs | Working Envelope | A/Brain |
| Protocol lifecycle | Protocol Governance | Correct protocol identity/version/compatibility/change control | Registration/change/deprecation/supersession | Source-owner proposals | Protocol Governance | Affected owner adaptation |
| Contract integrity / input shape | Canonical owner boundary for each contract; shared protocol is governance text | Correct structural validation and local contract rejection | Validate raw/external/reconstructed structure before semantic processing; no semantic admission or authority mutation | Producers, adapters, replay and tests | Boundary that owns the declared contract | Typed contract may proceed to its existing semantic/admission owner |
| Loop mechanics | Cognitive Loop | Correct mechanical persistence of authorized refs | OPEN/CONTINUE/FREEZE/CLOSE/ARCHIVE mechanics | All owner commands | Loop implementation | None; semantic owner remains source |
| Memory candidate | Candidate producer now; future Memory Governance | Candidate source binding/provenance correctness | Candidate handoff only | Brain/Outcome/A/Loop | Candidate producer | Deferred Memory governance |
| Experience candidate | Candidate producer now; future Experience Governance | Candidate bounded relation/provenance correctness | Candidate handoff only | Brain/Outcome/A/Loop | Candidate producer | Deferred Experience governance |

## Enforcement split

Safety, Permission, Resource, Grant and Protocol policies retain their policy/version authority. Decision, Task, Runtime Admission, Provider, Observation and Action enforce supplied refs at their own boundaries. Enforcement failure belongs to the enforcing boundary; policy-definition failure belongs to the policy owner. No enforcement point may weaken or replace policy.
