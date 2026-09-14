# Canonical Flow Edge Ledger v1

`runtime` and `mutation` describe permission of the canonical edge, not whether current controlled implementations execute it.

| Edge | Producer → consumer | Class / contracts | Authority / admission | Failure return | Version / invalidation | Runtime / mutation / status |
|---|---|---|---|---|---|---|
| E01 | Brain → Working Envelope | BINDING / VALIDATION / ADMISSION; Concern/Grant→Envelope | Envelope; Brain owns Concern/Grant | Envelope / Brain | Grant/source versions invalidate | No runtime; Envelope binding only; CONTRACT |
| E02 | Envelope → Semantic Outline | FORMATION; Envelope refs→Outline | Semantic Module | Semantic Module / A | Envelope change supersedes outline | No; no source mutation; CONTRACT |
| E03 | Envelope → Cognitive Snapshot | FORMATION; Envelope refs→Snapshot | Cognitive State Formation | State Formation / A | Source alignment invalidates | No; no source mutation; CONTRACT |
| E04 | A → Attention | FORMATION / ADOPTION; Requirement→Attention candidate | Attention allocation | A / Attention | Requirement/Grant/constraint stale | No; no Need mutation; VERIFIED_CONTROLLED |
| E05 | A → Capability Requirement | FORMATION; Need→Requirement | A owns requirement | A | Need/Concern invalidation | No; no Capability mutation; CONTRACT |
| E06 | Capability → Capability↔Model | BINDING / VALIDATION; Capability/Model declaration | Capability Governance | Capability Governance | Model/capability version invalidates | No; no runtime; VERIFIED_CONTROLLED |
| E07 | Capability/Model → Runtime Admission | ADMISSION; binding/declarations→assessment | Runtime Admission | Runtime Admission | binding/diagnostic/constraint stale | No model registry mutation; CONTRACT |
| E08 | Runtime Admission → Observation | ADMISSION / BINDING; Executable Capability→Observation Request | Observation owns request; Runtime supplies readiness | Runtime Admission / Observation | executable/constraint stale | No invocation; VERIFIED_CONTROLLED |
| E09 | Runtime Admission → Action | ADMISSION / BINDING; executable refs→Action input | Action Governance | Runtime / Action | executable/target/constraint stale | No action execution; CONTRACT |
| E10 | Observation → Provider | ADMISSION / EXECUTION boundary; Request→Provider | Provider Admission | Observation / Provider | request/provider binding stale | Invocation allowed only later; CONTRACT |
| E11 | Provider → Provider Result | EXECUTION; Provider runtime→external result | Provider Governance | Provider | invocation/session version | Runtime only in future; no source mutation; CONTRACT |
| E12 | Provider Result → Evidence | FORMATION / MAPPING / VALIDATION | Gateway Evidence admission | Provider/Gateway | result/provenance/freshness stale | No runtime/source mutation; VERIFIED_CONTROLLED |
| E13 | Evidence → Current World Candidate | FORMATION / MAPPING | Current World/State Formation | Gateway / Current World | evidence/source version invalidates | Candidate only; no Truth; VERIFIED_CONTROLLED |
| E14 | Evidence → Field Event Candidate | FORMATION / MAPPING | Field later admits/reduces | Gateway / Field | evidence/effective-time/version invalidates | Candidate only; no reducer; VERIFIED_CONTROLLED |
| E15 | Current World/Field candidate → A | ADOPTION / CONSUMPTION | A semantic use authority | A | candidate stale/partial returns A | No source mutation; CONTRACT |
| E16 | A → B-CR | FORMATION / ADOPTION | A owns local reasoning | A / B-CR | Need/Concern/Grant stale | No global consequence; CONTRACT |
| E17 | B-CR → A | FORMATION / EVALUATION | A interprets contingency | B-CR / A | B-CR source invalidation | No A mutation by B-CR; CONTRACT |
| E18 | A → Decision | FORMATION / ADMISSION candidate | Decision Governance | A / Decision | Intent/constraint/Need stale | No commitment by A; CONTRACT |
| E19 | Decision → Task | ADMISSION / BINDING | Task readiness/lifecycle | Decision / Task | Decision/task version invalidates | No Action execution; CONTRACT |
| E20 | Decision → Action | ADMISSION input; bounded direct path | Action Governance | Decision / Action | Decision/target/constraint stale | No direct execution; VERIFIED_CONTROLLED |
| E21 | Task → Action | ADMISSION input; organized path | Action Governance | Task / Action | Task/dependency/target stale | No Action execution; VERIFIED_CONTROLLED |
| E22 | Action → Provider | ADMISSION / EXECUTION boundary | Provider after Action admission | Action / Provider | permission/safety/resource/provider stale | Invocation later only; CONTRACT |
| E23 | Action Result → Task | FORMATION / EVALUATION | Task interprets progress/completion | Action Governance / Task | result/version stale | Candidate only; no direct completion; VERIFIED_CONTROLLED |
| E24 | Action Result → A | FORMATION / EVALUATION | A semantic reassessment | Action Governance / A | result/version stale | Candidate only; no Sufficiency; VERIFIED_CONTROLLED |
| E25 | Action/Task/A/source refs → Outcome | EVALUATION / FORMATION | Outcome Evaluation | Outcome Evaluation / A | source/result stale or contested | No Brain adjudication; CONTRACT |
| E26 | Outcome Evaluation → Brain | FORMATION / ADOPTION input | Brain adjudication | Outcome Evaluation / Brain | outcome/source versions invalidate | Candidate input only; VERIFIED_CONTROLLED |
| E27 | Brain → Loop | MECHANICAL_PERSISTENCE | Loop mechanics after authorized command | Brain/Loop | command/version history | Mechanical only; no semantic mutation; CONTRACT |
| E28 | Brain Assimilation → MemoryCandidate | FORMATION / HANDOFF | Future Memory Governance | Brain/candidate producer | source/Concern versions | Candidate only; no persistence; DEFERRED |
| E29 | Brain Assimilation → ExperienceCandidate | FORMATION / HANDOFF | Future Experience Governance | Brain/candidate producer | source/Concern versions | Candidate only; no learning; DEFERRED |
| E30 | Constraint policy → Envelope/Decision/Task/Runtime | BINDING / VALIDATION | Policy owners publish; boundaries enforce | Policy owner / enforcing boundary | policy/version/revocation invalidates | No policy weakening; CONTRACT |
| E31 | Diagnostics → governance/admission consumers | OBSERVATION / CLASSIFICATION | Diagnostics classification | Diagnostics / consumer boundary | TTL/runtime/device changes stale | No remediation or admission decision; VERIFIED evidence |

## Edge invariant

No edge creates authority. Every edge carries source refs, versions, provenance and invalidation behavior. Every failed edge returns to the boundary responsible for the failed transition.

