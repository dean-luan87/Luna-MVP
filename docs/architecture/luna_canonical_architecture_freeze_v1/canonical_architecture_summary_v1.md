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

## Conflict audit

- **Canonical owner conflicts:** none found in the reviewed evidence.
- **Terminology conflicts:** earlier `AUTHORITY_VACUUM` descriptions for Current World adoption, Cognitive Snapshot adoption, Semantic Outline lifecycle, shared bindings, precedence and Envelope refresh are superseded by the targeted vacuum-closure records. They were terminology/lifecycle gaps, not remaining owners.
- **Shared-contract conflicts:** Capability↔Model and Model↔Provider retain separate source declarations and one binding lifecycle owner each; this is a valid split, not dual mutation authority.
- **Legacy conflicts:** direct routing, Gateway mutation risks, Loop semantic helpers and historical FPO/Attention ownership remain compatibility or migration records. They are not current-flow authorities; no active bypass is recorded in the verified consolidated regression.
- **Deferred conflicts:** Emotion, full Memory/Experience, Learning, compression, Scheduler, Planner, retry/fallback, active probes, remediation and production runtime remain intentionally deferred.
- **Freeze blockers:** none. Runtime incompleteness is not an architecture-freeze blocker.

## Status

Architecture freeze complete: 30 canonical module/boundary rows, 31 canonical edges and 24 high-value invariants. Runtime remains incomplete/deferred. No production GO is declared.
