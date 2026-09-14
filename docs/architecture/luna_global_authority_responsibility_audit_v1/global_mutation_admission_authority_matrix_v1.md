# Global Mutation and Admission Authority Matrix v1

## Mutation authority

| State / transition | Create | Modify | Supersede / close / retire | Candidate submitters | Dual mutation result |
|---|---|---|---|---|---|
| Goal, Concern, Grant | Brain | Brain | Brain | A, Decision, Outcome | NO_CONFLICT |
| Intent | Intent Governance | Intent Governance | Intent Governance | A/Brain/Outcome candidates | NO_CONFLICT |
| Field | Field boundary/reducer | Field boundary/reducer | Field lifecycle | Gateway/Observation events | NO_CONFLICT by contract; runtime skeleton |
| Context | Context Foundation | Context owner | Context owner | source bindings | NO_CONFLICT |
| Decision | Decision Governance | Decision Governance | Decision Governance; Brain supersession | A/Brain/Intent | SPLIT_VALID |
| Task | Task | Task | Task | Decision | NO_CONFLICT |
| Action | Action Governance | Action boundary | Action boundary | Task/Decision | NO_CONFLICT |
| Outcome global consequence | Brain | Brain | Brain | Outcome Evaluation | SPLIT_VALID |
| Model registry/lifecycle | Model Governance | Model Governance | Model Governance | provisioning/evaluation | NO_CONFLICT |
| Protocol registry/lifecycle | Protocol Governance | Protocol Governance | Protocol Governance | source owners/change proposals | NO_CONFLICT |
| Loop record | Loop | Loop | Loop mechanics | all owners’ refs | NO_CONFLICT; semantic bypass forbidden |

## Admission authority

| Admission | Authority | Evidence / policy suppliers | Consumer / consequence | Responsibility for wrong admission |
|---|---|---|---|---|
| Concern / Grant | Brain | Goal, policy, priority, source refs | Envelope/A | Brain |
| Working Envelope | narrow Envelope binding under Brain admission | Brain Grant, source versions, constraints | Semantic/State/A | contract owner gap; future existing-boundary consolidation |
| Intent | Intent Governance | purpose/source refs | A/Decision/Task | Intent Governance |
| Capability logical resolution | Capability Governance | requirement, taxonomy, mappings | Runtime Admission | Capability Governance |
| Runtime Admission | Runtime Admission | Diagnostics, Model, Provider compatibility, constraints | Executable candidate | Runtime Admission |
| Provider Admission | Provider Governance | executable candidate, health, policy refs | invocation | Provider Governance |
| Observation Request | Observation | A requirement, Attention, capability, constraints | Provider/Gateway | Observation |
| Evidence | Observation Gateway | Provider Result, request/invocation refs, freshness | Current World/Field/A | Gateway |
| Decision commitment | Decision Governance | A candidate, Brain constraints, Intent | Task/Action | Decision Governance |
| Task readiness | Task | Decision, dependencies, constraints, resources | Action | Task |
| Action | Action Governance | Decision/Task, Permission/Safety/Resource, target | Provider/runtime | Action Governance |
| Permission | Permission Governance | identity/role/context evidence, policy | consumers | Permission Governance |
| Safety enforcement | boundary-local enforcement of Brain/Safety policy | risk evidence, policy refs | Decision/Task/Runtime/Action | enforcing boundary for enforcement; Safety/Brain for policy |
| Resource budget/reservation | Resource Governance | Diagnostics facts, priority and ceilings | Attention/Task/Runtime | Resource Governance |
| Model registration | Model Governance | provisioning/manifest/integrity declaration | Capability/Runtime | Model Governance |
| Protocol change | Protocol Governance | source owner impact review | producer/consumer bindings | Protocol Governance |

## Mutation rule

No candidate producer may bypass the named admission authority. Brain may globally veto or supersede governed commitments, but that does not make Brain the local owner of every downstream state.

