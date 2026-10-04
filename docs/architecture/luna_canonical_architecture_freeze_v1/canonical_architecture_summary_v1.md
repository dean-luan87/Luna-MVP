# Canonical Architecture Summary v1

## Freeze disposition

`ARCHITECTURE_FROZEN`. `RUNTIME_READY` is **false** and is not implied by this record. The reviewed architecture is coherent with deferred runtime and implementation gaps; the verified controlled slices and consolidated regression preserve the owner model.

## 03｜Luna Canonical Architecture

### 03.1 System Principles

Authority implies responsibility; one mutation domain has one owner; candidates require governed admission; derived state and reads do not own source state; policy and enforcement are separate; persistence is mechanical; no global version; failures return to their responsible boundary.

### 03.2 Canonical Module Map

Brain governs global purpose and consequence. A governs local reality thinking. Intent, Role, Field, Context, Task, Decision, Action, Capability, Model, Provider, Observation, Evidence/Gateway, Outcome, Diagnostics, Working Envelope and Protocol retain their specialized domains. Semantic Outline, Cognitive Snapshot, Perspective Projection and Current World candidates are derived or candidate products. Memory/Experience remain candidate-only placeholders.

### 03.3 Authority & Responsibility

Brain owns Goal/Concern/Grant/global constraints/final Outcome adjudication. A owns Need/Hypothesis/Relevance/Sufficiency/Reconsideration/Next-step/local consequence. Capability owns logical resolution and Capability↔Model binding lifecycle. Provider owns Model↔Provider binding lifecycle and runtime boundary. Action owns side-effect admission. Loop owns only mechanical persistence.

### 03.4 State Ownership

Authoritative source states have one mutation authority. Current World, Attention, Runtime Admission, Evidence and Outcome are candidates or admission records unless their ledger row explicitly says otherwise. Semantic Outline, Cognitive Snapshot and Perspective Projection are local-derived. Provider/Action results are external results. MemoryCandidate and ExperienceCandidate are deferred candidates.

### 03.5 Canonical Cognitive Flow

`Brain Concern/Grant/Envelope → Semantic Outline + Cognitive Snapshot → A → Need/Requirement → Attention → Capability → Runtime Admission → Observation/Provider → Evidence → Field/Current World candidates → A → Decision → Task → Action → Provider → Result → Task/A/Outcome → Brain adjudication → Loop mechanics.`

### 03.6 Execution / Observation Flow

Observation and Action have separate request/admission/execution boundaries. Decision commits, Task organizes, Action admits side effects, Provider invokes later. Provider Result and Action Result return through Evidence/Task/A/Outcome candidates; they do not declare reality or completion directly.

### 03.7 Constraint Governance

Precedence is hard Safety, hard Permission, Grant validity, protected Resource ceiling/reserve, Resource optimization, then local priority. Brain owns global precedence binding; Safety, Permission and Resource retain policy authority; boundary owners enforce supplied refs.

### 03.8 Version / Invalidation

Each domain versions itself. Source changes propagate by version/invalidation refs to derived products and bindings, then to the owning re-admission/refresh boundary. No direct cross-owner mutation and no global state version exist.

### 03.9 Failure Responsibility

Policy errors return to policy owners; declaration errors to declaration owners; mapping/admission errors to the boundary that owns them; translation errors to adapters; semantic consequences to A; global consequences to Brain; mechanical persistence to Loop. Failure cannot fabricate success.

### 03.10 Role / Perspective

`Shared Information Once, Perspective Augmentation Many.` Shared world/base information remains stable. Role is social identity position plus responsibility/skill/domain relevance. Perspective Projection is role-conditioned derived augmentation only. Emotion is deferred and is not a current conditioner or projection input.

### 03.11 Maintenance Plane

Diagnostics observes and classifies health/drift. Model Governance owns model declarations/lifecycle. Protocol Governance owns representation/version/change lifecycle. Baseline, calibration, registry and filesystem remain distinct source/reference boundaries. None may silently become runtime admission or remediation authority.

### 03.12 Legacy / Deferred

Legacy direct routing, Gateway mutation risks, Loop semantic helpers, duplicate payloads and historical terminology remain compatibility/migration records. Emotion, full Memory/Experience, Retrieval, Learning, semantic compression, Scheduler, Planner, retry/fallback, active probes, remediation, streaming and production runtime consolidation remain deferred.

### 03.13 Change Control

Owner, authority, mutation, admission, state class, edge, transition class, failure responsibility, precedence, version ownership, World Truth boundary or deferred boundary changes require architecture review. Implementation-only changes are allowed only when the ledger remains true.

### 03.14 Architecture Invariants

I01 authority implies responsibility; I02 one mutation domain/one owner; I03 governed candidates require admission; I04 derived state cannot mutate source; I05 reads do not imply ownership; I06 semantic modules do not invoke Provider; I07 Provider Result ≠ Evidence; I08 Evidence ≠ World Truth; I09 Action Result ≠ Task completion; I10 Task completion ≠ Concern closure; I11 Outcome Candidate ≠ Brain adjudication; I12 Loop is mechanical-only; I13 A owns local consequence; I14 Brain owns global consequence; I15 no global version; I16 invalidation propagates by refs; I17 enforcement cannot weaken policy; I18 failure cannot fabricate success; I19 source mutation occurs only at source owner; I20 Role projection does not duplicate world information; I21 Emotion is deferred; I22 Memory/Experience admission is deferred; I23 historical versions remain traceable; I24 no active legacy bypass.

### 03.15 Brain–Organ Separation Principle

Luna's sensing/model-execution side ("Organ side") and governed cognition/world-processing side ("Brain side") are logically separate. These are descriptive architectural sides, **not new canonical Owners**. Organ-side work includes sensing and external information acquisition through existing owned boundaries, native Provider/Model execution, provider-specific input/output semantics, and provider-specific normalization. Where existing contracts suffice, model-family-specific semantics terminate at the governed Provider Runtime normalization seam, `ProviderRuntimeResultV1`. Organ output is candidate information: it cannot declare admitted Evidence, World Truth, Field truth, Current World truth, a cognition result, or Decision authority.

After that seam, provider families reuse `ProviderRuntimeResultV1 → RuntimeObservationEnvelopeV1 → Observation Gateway → Evidence →` the existing governed Context, Field, Current World, Cognition and Decision paths. No family-specific Observation or Evidence pipeline is authorized without separate canonical adjudication. The governed downstream layers must not depend on a particular model family's internals when these contracts suffice; replacement or addition of Grounding DINO, SAM2, YOLO, VLM, relationship-perception, audio or speech providers remains an Organ/Provider Runtime concern within those boundaries. The [canonical acquisition flow](../luna_canonical_cognitive_flow_freeze_v1/canonical_acquisition_flow_v1.md) and [External Model / Provider Integration SOP](../luna_external_model_provider_integration_sop_v1.md) retain the detailed ingress and execution contracts.

This principle preserves every existing Runtime Admission, Provider Runtime, Observation Gateway, Evidence admission, Field, Current World, Cognition and Decision Owner and authority. In particular, "Brain side" does **not** mean that the Brain module owns Observation Gateway, Evidence, Field or Current World. Provider Result remains distinct from admitted Evidence, and Evidence remains distinct from World Truth.

Logical separation permits later evaluation of same-process, separate-process, local-device, remote-device, edge-device or robot/sensor-hosted Organs; `LOGICAL_SEPARATION != MANDATORY_REMOTE_DEPLOYMENT`. No network transport, RPC, distributed runtime or remote deployment is required now. This principle does not authorize an OrganManager, OrganBus, OrganRegistry, OrganAuthority, distributed scheduler, RPC protocol, new Canonical Fact, or parallel Observation/Evidence pipeline. Such additions require separate architecture/governance adjudication supported by repeated implementation evidence of a real contract gap. The existing 06.1 Model/Version → 06.2 Engineering Integration → 06.4 Interface Evolution → 06.5 Experiment/Failure Evidence → qualified feedback governance chain continues to apply.

#### Brain–Organ Integration Modes

`DIRECT_INTEGRATION` means an Organ operates in a tightly coupled execution environment and connects through a local API, in-process call, or local runtime interface. Low latency, high-frequency interaction, or a persistent local sensory capability (potentially including future voice/hearing use cases) may motivate this form; none is a present model-specific implementation requirement. Closer invocation or transport coupling does not weaken the semantic or authority boundary: direct mode cannot bypass Provider Runtime, Runtime Observation, or Observation Gateway; create admitted Evidence; mutate Field or Current World; or directly invoke cognition authority without separate canonical architecture adjudication.

`COMMUNICATION_INTEGRATION` means an Organ may run in a separate process, device, edge node, robot, or sensor host and exchange governed data with Luna over a communication transport. Bluetooth, Wi-Fi, LAN, and other future transports are examples, **not canonical semantic contracts or mandatory architecture**. This mode does not change Evidence admission, Field or Current World ownership, cognition ownership, or Decision ownership.

These are integration/transport forms, **not two Luna cognition architectures**. Both preserve the same expectations: Organ-specific execution → governed runtime/result boundary → canonical Runtime Observation, Observation Gateway, Evidence, and downstream processing. Brain/world-processing layers must not depend on whether an Organ arrived by Bluetooth, Wi-Fi, local API, same-process invocation, or another transport. Transport is not semantic authority.

No `BrainOrganProtocolV1`, Organ wire or RPC contract, serialization standard, device discovery, heartbeat, reconnect or remote authentication protocol, distributed scheduler, OrganManager, OrganBus, or OrganRegistry is defined or authorized here. A first real remote-Organ use case must establish an engineering need before any communication protocol proposal enters separate architecture/governance adjudication; neither mode implements a remote runtime now.

Grounding DINO is the **planned, not yet proven**, first engineering proof vehicle for `native Organ execution → ProviderRuntimeResultV1 → RuntimeObservationEnvelopeV1 → Observation Gateway → Evidence`. It is an example, not part of this model-family-independent principle's definition; this statement makes no real-runtime completion claim.

### 03.16 Luna Model / Organ Integration Protocol

This is the **target canonical architecture** accompanying Brain–Organ Separation, not a new runtime protocol object. Brain–Organ Separation answers how Organ execution and governed world/cognition processing retain distinct semantic and authority boundaries. Model / Organ Integration answers how an external model becomes a usable Organ, runs within those boundaries, and is upgraded, replaced, or retired. The governing approach is `CONCEPTUALLY_UNIFIED; RESPONSIBILITY_SEPARATED; IMPLEMENTATION_REUSED`.

The protocol has four layers:

1. **Identity & Capability.** Existing Model, Provider, Capability, version, asset and binding declarations answer who the Organ is, what it can do, and on which assets it depends. Registration or binding alone grants no runtime authority. The existing 06.1 Model/Version → 06.2 Engineering Integration → 06.4 Interface Evolution → 06.5 Experiment/Failure Evidence → qualified feedback chain governs additions, upgrades and changes.
2. **Admission & Lifecycle.** `candidate → evaluating → admitted → active` remains governed by the existing lifecycle owners. A candidate/evaluating Provider may undergo `CONTROLLED_REAL_EVALUATION` only through an Owner-approved controlled evaluation profile, an active and matching `RuntimeExecutionGrantDecisionV1`, and a bounded scope. That execution is not production routing eligibility, does not mutate lifecycle, cannot auto-admit or auto-activate, and must fail closed with auditable execution/evaluation evidence. `PRE_ADMIT_THEN_PROVE=INVALID_BOOTSTRAP`. Production routing uses its own eligibility/authorization entry after activation; it is not a fallback for candidate evaluation, and evaluation is not an `allow_candidate` switch on the production selector.
3. **Runtime Semantic Contract.** Controlled real evaluation and production runtime have **different authorization entries but the same runtime semantic contract**: provider-specific native execution → provider-specific normalization → `ProviderRuntimeResultV1` → `RuntimeObservationEnvelopeV1` → Observation Gateway → admitted `PerceptionEvidenceV1` → existing governed downstream paths. Provider output remains candidate information; neither entry may bypass Gateway or declare world truth. Evaluation status does not create parallel `EvaluationEvidenceV1`, `EvaluationObservationV1`, or `CandidateRuntimeResultV1` types. Successful real execution yields execution evidence, Provider Runtime result, runner/verifier artifacts and existing evaluation/governance records for a **separate** admission decision; `REAL_EXECUTION_SUCCESS != ADMITTED`, and `ADMITTED != ACTIVE`.
4. **Transport / Integration.** The existing `DIRECT_INTEGRATION` and `COMMUNICATION_INTEGRATION` forms may vary physical placement and transport. Bluetooth, Wi-Fi and LAN are transport examples, not canonical semantic contracts. Transport changes neither identity, admission, runtime-result semantics nor Evidence authority, and does not authorize a network or device protocol here.

```text
Model / Organ → Identity & Capability → Candidate
                                   ├─ Controlled Real Evaluation
                                   │    Owner-approved profile + bounded, current evaluation grant
                                   │    candidate/evaluating; no production routing eligibility
                                   └─ Production Runtime
                                        active + production routing eligibility/authorization
                                   ↓ distinct authorization entries, shared semantic contract
Provider-specific execution/normalization → ProviderRuntimeResultV1
  → RuntimeObservationEnvelopeV1 → Observation Gateway → PerceptionEvidenceV1
```

Standard onboarding is `REGISTER IDENTITY → CANDIDATE → CONTROLLED REAL EVALUATION → EVALUATION EVIDENCE → separate ADMISSION DECISION → ADMITTED → separate ACTIVATION → ACTIVE → PRODUCTION ROUTING`. Upgrade, replacement and retirement retain the same separated identity, lifecycle, authorization and version/invalidation ownership; this section does not specify new transition APIs. Grounding DINO, SAM2 and future visual, audio or relationship-perception Organs should follow these semantics rather than acquire a model-specific bootstrap architecture. Their native invocation, normalization, asset/configuration and capability-specific payloads remain provider-specific.

Existing Owners remain distinct: Model Governance and the existing identity/registry surfaces own model/version/asset declarations and model lifecycle; Capability Governance owns capability identity and Capability↔Model binding lifecycle; Provider Governance owns Provider identity and Model↔Provider binding lifecycle; Permission / Admission Manager owns bounded runtime execution authorization; Provider Runtime owns governed execution/result; provider-specific adapters own native invocation/normalization; Observation Gateway owns Observation-to-Evidence admission/classification. Downstream Context, Field, Current World, Cognition and Decision retain their own Owners. No Model Manager super-authority, new Canonical Fact, Manager, Registry, Authority or `ModelOrganProtocolV1` is established.

**Target is not current implementation conformance.** The 06.5 evidence item `PR-ADMISSION-01` remains `CONTROLLED_EVALUATION_ENTRY_GAP`: a provider-independent bounded **real** evaluation entry is not yet implemented. Grounding DINO remains `BLOCKED_PENDING_CONTROLLED_EVALUATION_ENTRY`; neither this documentation nor existing synthetic evaluation profiles closes that blocker. A separate *Model / Organ Integration Protocol Architecture Conformance Audit* must inspect Model Manager/Registry, capability binding, lifecycle state machine, Permission / Admission Manager, `RuntimeExecutionGrantDecisionV1`, controlled evaluation profiles, production selector, Provider Runtime, provider-specific adapters, Runtime Observation, Observation Gateway, YOLO, OCR and the planned Grounding DINO path. This document does not perform that audit.

**Deployment-scale clarification (target).** Hive is a scaled Luna deployment, not an external capability-supply system or a fork of Model / Organ governance. Model / Organ, Version and Protocol repositories, Integration Packages, and compatibility governance remain Luna architectural capabilities; their capacity and placement may scale up, scale down or compose by deployment profile without changing canonical authority semantics. Interpret any earlier “Hive-migratable authority” planning language as **authority placement by deployment profile**, not migration out of Luna. A local/personal Luna may retain bounded local repository and version/protocol information, resident packages, a Minimum Survival Capability Set, and local admission/runtime/safety authority; a Hive-scale Luna may support larger histories, model pools, shared packages and multi-node supply. Capability coverage may shrink with scale, but local autonomy must remain: a survival-minimum profile must still be a valid Luna deployment, not require the full Hive capability set or an online Hive authorization for each execution. This clarification does not implement Hive, distributed runtime, or a network protocol.

## Conflict audit

- **Canonical owner conflicts:** none found in the reviewed evidence.
- **Terminology conflicts:** earlier `AUTHORITY_VACUUM` descriptions for Current World adoption, Cognitive Snapshot adoption, Semantic Outline lifecycle, shared bindings, precedence and Envelope refresh are superseded by the targeted vacuum-closure records. They were terminology/lifecycle gaps, not remaining owners.
- **Shared-contract conflicts:** Capability↔Model and Model↔Provider retain separate source declarations and one binding lifecycle owner each; this is a valid split, not dual mutation authority.
- **Legacy conflicts:** direct routing, Gateway mutation risks, Loop semantic helpers and historical FPO/Attention ownership remain compatibility or migration records. They are not current-flow authorities; no active bypass is recorded in the verified consolidated regression.
- **Deferred conflicts:** Emotion, full Memory/Experience, Learning, compression, Scheduler, Planner, retry/fallback, active probes, remediation and production runtime remain intentionally deferred.
- **Freeze blockers:** none. Runtime incompleteness is not an architecture-freeze blocker.

## Status

Architecture freeze complete: 30 canonical module/boundary rows, 31 canonical edges and 24 high-value invariants. Runtime remains incomplete/deferred. No production GO is declared.
