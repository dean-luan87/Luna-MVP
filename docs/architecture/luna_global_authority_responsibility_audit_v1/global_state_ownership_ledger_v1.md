# Global State Ownership Ledger v1

`AUTHORITATIVE` means one boundary may make the final state transition. `CANDIDATE` means a proposal requiring the named admission owner. `REFERENCE_ONLY` means read/binding material. `EXTERNAL` means supplied by an external/source owner. `LOCAL_DERIVED` means a derived view that cannot mutate its source.

| State | Final authority | Producer / consumers | Mutation and lifecycle authority | Class |
|---|---|---|---|---|
| Goal / Concern / Grant | Brain | Brain, A, Envelope, Decision | Brain | AUTHORITATIVE |
| Role / Identity / Relationship | source-governed identity boundary | source, Perspective, Permission | source owner | EXTERNAL / AUTHORITATIVE at source |
| Perspective Projection | Perspective Projection | Role/Context/Envelope, A | Projection boundary | LOCAL_DERIVED |
| Field State / Field Event | Field boundary / Field Reducer | Observation, Gateway, Context, A | Field admission/reducer | AUTHORITATIVE / CANDIDATE |
| Context | Context Foundation | Field/World/Task/Envelope/A | Context owner | AUTHORITATIVE |
| Current World | current-world representation boundary; final adoption contract remains open | Observation/Gateway/State Formation/A | candidate formation; admission gap | CANDIDATE |
| Intent | Intent Governance | Brain/A/Task/Envelope | Intent Governance | AUTHORITATIVE |
| Attention allocation | Attention | A/Role/Task/Brain, Observation | Attention | CANDIDATE / LOCAL_DERIVED |
| Capability / Slot | Capability Governance | A/Task/Attention/Model | Capability Governance | AUTHORITATIVE |
| Executable Capability Candidate | Runtime Admission | Capability/Model/Diagnostics/constraints | Runtime Admission | CANDIDATE |
| Decision | Decision Governance | A/Brain/Intent/Task | Decision Governance; Brain override | AUTHORITATIVE |
| Task | Task | Decision/Action/A | Task | AUTHORITATIVE |
| Action Contract / Action Result | Action Governance / execution boundary | Task/Capability/Provider | Action admission/result; provider executes | AUTHORITATIVE / EXTERNAL result |
| Outcome Candidate / final outcome | Outcome Evaluation / Brain | Action/Task/A/World/Decision | candidate evaluation / Brain assimilation | CANDIDATE / AUTHORITATIVE global consequence |
| Observation Request | Observation | A/Attention/Capability | Observation lifecycle | AUTHORITATIVE request |
| Provider identity/admission/invocation/result | Provider Governance | Runtime/Model/Action/Observation | Provider Governance/runtime | AUTHORITATIVE / EXTERNAL result |
| Evidence Candidate / Evidence Admission | Observation Gateway | Provider/Observation | Gateway admission | CANDIDATE / AUTHORITATIVE admission record |
| Safety Policy | Brain/Safety sub-boundary | Brain, diagnostics, risk sources | policy/override under Brain | AUTHORITATIVE |
| Permission Policy/Grant | Brain/Permission sub-boundary | Identity/Role/Context | Permission Governance; Brain grant separate | AUTHORITATIVE |
| Resource Policy/Budget/Reservation | Brain/Resource sub-boundary | Diagnostics, Attention, Task | Resource Governance | AUTHORITATIVE / CANDIDATE reservation |
| Diagnostic Evidence/Finding | System Diagnostics | probes, OS, runtime, devices | Diagnostics | AUTHORITATIVE diagnostic classification |
| Model identity/asset/lifecycle | Model Governance | provisioning/filesystem/diagnostics | Model Governance | AUTHORITATIVE declaration |
| Protocol identity/lifecycle | Protocol Governance | source owners/registry/diagnostics | Protocol Governance | AUTHORITATIVE |
| Working Envelope | Envelope binding boundary | Brain/source refs | envelope admission/invalidation; refresh gap | AUTHORITATIVE binding |
| Semantic Working Outline | Semantic Module | Envelope/Context/World | Semantic Module derived lifecycle; gap | LOCAL_DERIVED |
| Cognitive Snapshot | Cognitive State Formation | Envelope/World/Evidence | formation; adoption gap | LOCAL_DERIVED / CANDIDATE |
| Loop record/package | Loop | all canonical owners | Loop mechanics only | AUTHORITATIVE mechanical record |
| MemoryCandidate / ExperienceCandidate | candidate producer; future governance | Brain Assimilation/Outcome/A/source refs | future Memory/Experience Governance | CANDIDATE |

## Finding

The main duplication risk is copied mutable payload in derived boundaries. Refs, versions, applicability and provenance are valid shared information; a second writable copy is not.

