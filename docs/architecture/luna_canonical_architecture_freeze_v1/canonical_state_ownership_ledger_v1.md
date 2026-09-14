# Canonical State Ownership Ledger v1

| State | Final authority / source | Class | Candidate producers / consumers | Mutation and lifecycle rule |
|---|---|---|---|---|
| Goal / Concern / Grant | Brain | AUTHORITATIVE | Brain; A, Envelope, Decision consume | Only Brain creates/modifies/supersedes/closes |
| Intent | Intent Governance | AUTHORITATIVE | A/Brain/Task candidates; Envelope refs | Intent owner controls lifecycle |
| Role / Identity / Relationship | Role source governance | EXTERNAL / AUTHORITATIVE at source | Perspective, Permission, A | No derived boundary mutates source |
| Need / Hypothesis / Sufficiency | A | AUTHORITATIVE_LOCAL | Envelope/Evidence/results → A | A-local semantic mutation only |
| Perspective Projection Result | Perspective Projection | LOCAL_DERIVED / CANDIDATE | Role/shared refs → A | Recompute/supersede projection; no source mutation |
| Field state / Field Event | Field | AUTHORITATIVE / CANDIDATE | Gateway/Observation event candidates | Field admission/reducer is sole mutation authority |
| Context | Context | AUTHORITATIVE | Field/World/Task refs → Envelope/A | Context owner controls framing/lifecycle |
| Current World | Current World / State Formation | CANDIDATE | Evidence → A/State Formation | Candidate formation/version only; never World Truth |
| Semantic Working Outline | Semantic Module | LOCAL_DERIVED | Envelope → A | Semantic Module owns local-derived lifecycle |
| Cognitive Snapshot | Cognitive State Formation | LOCAL_DERIVED / CANDIDATE | Envelope/source refs → A | Formation owns alignment/version; A adopts/uses |
| Attention allocation | Attention | CANDIDATE | A/constraints → Observation/Capability | Allocation only; no Need/policy mutation |
| Capability / Slot / Logical Resolution | Capability Governance | AUTHORITATIVE / CANDIDATE | A/Task/Model → Runtime | Capability owner controls identity and logical scope |
| Capability↔Model binding | Capability Governance | AUTHORITATIVE binding / CANDIDATE input | Model declarations → Runtime | Capability Governance owns binding lifecycle |
| Model identity / asset / lifecycle | Model Governance | AUTHORITATIVE declaration | Provisioning/filesystem/Diagnostics → Runtime | Model Governance controls registration/lifecycle |
| Model↔Provider binding | Provider Governance | AUTHORITATIVE binding / CANDIDATE input | Model/Provider declarations → Runtime | Provider Governance owns binding lifecycle |
| Runtime Admission | Runtime Admission | CANDIDATE / ADMISSION RESULT | Capability/Model/Diagnostics/constraints → Observation/Action | No model registry or source mutation |
| Observation Request | Observation | AUTHORITATIVE request | A/Attention/Runtime → Provider/Gateway | Observation owns request lifecycle |
| Provider Result | Provider | EXTERNAL RESULT | Provider → Evidence/Task/A/Outcome | Result is not Evidence or World Truth |
| Evidence | Observation Gateway | CANDIDATE / admitted evidence ref | Provider/Observation → Field/World/A | Gateway owns normalization/admission only |
| Decision | Decision Governance | AUTHORITATIVE | A/Brain/Intent → Task/Action | Decision owns commitment/revocation/supersession |
| Task | Task | AUTHORITATIVE | Decision → Action/Outcome | Task owns readiness/progress/completion |
| Action Contract / Admission | Action Governance | AUTHORITATIVE boundary | Decision/Task → Provider | Action owns side-effect admission; not execution semantics |
| Action Result | Action/Provider boundary | EXTERNAL RESULT | Action/Provider → Task/A/Outcome | Never directly completes Task or Concern |
| Outcome Candidate | Outcome Evaluation | CANDIDATE | Action/Task/A/source refs → Brain | Evaluation does not adjudicate or close Concern |
| Brain Adjudication / Assimilation | Brain | AUTHORITATIVE | Outcome Candidate → Goal/Concern consequence | Brain owns final global consequence |
| Diagnostic fact/finding | System Diagnostics | AUTHORITATIVE within diagnostic scope | Probes/telemetry → governance/admission | Diagnostic truth only; no remediation |
| Safety / Permission / Resource policy | Domain governance / Brain global | AUTHORITATIVE policy | Evidence/diagnostics → enforcement refs | Policy owner distinct from enforcement point |
| Working Envelope | Working Envelope | AUTHORITATIVE binding / CANDIDATE version | Brain/source refs → Semantic/State/A | Envelope owns binding/invalidation/supersession, not source payload |
| Protocol identity/lifecycle | Protocol Governance | AUTHORITATIVE | Source-owner proposals → bindings | Protocol owner does not own source state |
| Loop record | Loop | MECHANICAL | All authorized refs → history | Persistence only; no semantic inference |
| MemoryCandidate | Candidate producer / future Memory Governance | CANDIDATE | Brain/Outcome/A/Loop → future governance | No current admission/storage/retrieval |
| ExperienceCandidate | Candidate producer / future Experience Governance | CANDIDATE | Brain/Outcome/A/Loop → future governance | No current learning/generalization |

No mutable second copy of Field, Context, Intent, Task, Role, Model or other authoritative source state is canonical. A ref, version, summary or derived view is not a second mutation domain.

