# Canonical Version / Invalidation Ledger v1

There is **no global Luna state version**. Each owner versions its own state, contract, candidate or binding. Cross-domain continuity uses refs and invalidation records.

| Domain | Owner / meaning | Stale condition | Invalidation producer | Downstream targets / refresh owner |
|---|---|---|---|---|
| Goal / Concern / Grant | Brain scope and authority version | superseded, revoked, closed, expired | Brain | Envelope, A, Decision, Loop / Brain |
| Working Envelope | binding-set version | source/Grant/constraint ref changed | Envelope/source/Brain | Outline, Snapshot, A / Envelope |
| Role / Identity | source version | source relationship changed | Role source | Perspective, Permission, Envelope / source owner |
| Perspective Projection | derived projection version | Role/Context/shared info changed | Perspective/source owner | Outline/A / Perspective |
| Intent | Intent lifecycle version | superseded/changed | Intent Governance | A, Decision, Task, Envelope / Intent |
| Field | operational state/event version | admitted transition or source event changes | Field | Context, World, Envelope/A / Field |
| Context | framing/validity version | situation/source framing changes | Context | Envelope, A, Task / Context |
| Current World | candidate representation version | Evidence/Field/source refresh or stale | Current World/State Formation | A, Snapshot / State Formation |
| Semantic Outline | derived outline version | Envelope/source version changes | Semantic Module | A / Semantic Module |
| Cognitive Snapshot | aligned structural version | Envelope/source alignment changes | State Formation | A / State Formation |
| A reasoning cycle | local cognition cycle version | Concern/Envelope/source invalidation | A/Envelope/Brain | A / A |
| Requirement / Attention | requirement/focus candidate version | Need, Grant, constraints or context change | A/Attention/Brain | Capability/Observation / owner |
| Capability / Slot | logical capability version | taxonomy/scope/contract change | Capability Governance | Runtime/Binding / Capability |
| Capability↔Model binding | binding lifecycle version | capability/model declaration/version changes | Capability Governance | Runtime / Capability |
| Model / weights / manifest / loader | declaration/version domains | asset/declaration/loader change or retirement | Model Governance | Binding/Runtime / Model |
| Model↔Provider binding | provider compatibility version | Model/Provider/adapter/loader change | Provider Governance | Runtime/Provider Admission / Provider |
| Provider | provider contract/session version | instance/session/adapter change | Provider Governance/Diagnostics | Runtime/Observation/Action / Provider |
| Runtime Admission | assessment version | diagnostics, binding, constraint or TTL change | Runtime Admission/Diagnostics | Observation/Action / Runtime |
| Observation | request/correlation version | request/provider/focus/constraint change | Observation | Provider/Gateway/A / Observation |
| Evidence | evidence/provenance version | stale, duplicate, malformed, source change | Gateway/Diagnostics | Field/World/A/Outcome / Gateway |
| Decision | commitment version | revoked/superseded/constraint change | Decision Governance/Brain | Task/Action/A / Decision |
| Task | readiness/progress version | dependency, Decision, resource or target change | Task | Action/A/Outcome / Task |
| Action / Action Result | admission/execution/result version | target/permission/safety/resource/result stale | Action/Provider | Task/A/Outcome / Action/Provider |
| Outcome | candidate evaluation version | source/result uncertainty or stale | Outcome Evaluation | Brain / Outcome Evaluation |
| Brain adjudication | global consequence version | new Outcome/Concern/Grant consequence | Brain | Loop, Intent candidates, Memory/Experience candidates / Brain |
| Loop | mechanical record version | command/history supersession | Loop | history only / Loop |
| Diagnostics | snapshot/finding version and TTL | expiry, restart, environment/device change | Diagnostics | Runtime/Resource/Safety/Permission/Model/Provider / consumer |
| Protocol | representation/version/fingerprint | supersession/deprecation/drift | Protocol Governance/Diagnostics | Producer/consumer binding / affected owner |
| Memory/Experience candidates | source-bound candidate version | source/Concern/Grant version change | candidate producer | Future governance / deferred |

## Propagation rule

`source change → version/invalidation ref → derived/binding invalidation → re-admission or refresh by the owning boundary → A or Brain semantic consequence.` No direct cross-owner mutation is permitted.

