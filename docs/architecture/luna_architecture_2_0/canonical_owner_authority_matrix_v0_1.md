# Architecture 2.0 — Canonical Owner / Authority / Writer / Reader Matrix v0.1

RESPONSIBILITY_ROLE_COUNT=9  
AUTHORITATIVE_QUESTION_COUNT=24  
BATCH=ACM-02 04  
STATUS=DESIGN_IN_PROGRESS; CANONICAL_ARCHITECTURE_FROZEN=NO

Repository-side transcription of [Notion 03.7 Architecture 2.0](https://app.notion.com/p/3c3113b33a6d81dfa4efeac030352d96), A2.0-97–107, read 2026-09-30. This ledger records candidate Canonical Architecture semantics, not Python DTOs, production conformance, runtime authorization or gap closure. Frozen Constitution v1 remains in [its separate file](architecture_2_0_constitution_v1.md).

### A2.0-97｜ACM-02 Batch 04 — Canonical Owner / Authority / Writer / Reader Matrix
**STATUS:** OWNERSHIP_AUTHORITY_MATRIX_CANDIDATE
**INPUT:** D01–D16 + OC-01–OC-12
**CONSTITUTION_BASE:** C01–C48 FROZEN
**IMPLEMENTATION_OWNER_MAPPING:** NOT_STARTED
**CODE_CHANGE_AUTHORIZED:** NO
Purpose: assign exactly one canonical ownership semantics to each authoritative question without equating Owner with current Manager/class/module names.

### A2.0-98｜Canonical Responsibility Roles
**R-OWNER — Canonical Owner**
Owns the authoritative meaning/question for a defined scope. Determines what constitutes the canonical answer/fact/state contract. Owner is semantic responsibility, not necessarily storage or execution.
**R-AUTHORITY — Decision Authority**
May issue an OC-05 Decision for a specifically defined admission/authorization/transition question. Authority is effect/question-specific and requires legitimate basis.
**R-WRITER — Authorized Writer**
May persist/register/mutate canonical state only under the Owner/Authority contract. Writer does not become Owner by writing.
**R-EXECUTOR — Effect Executor**
Performs an authorized effect. Executor does not become Authority/Owner and cannot infer permission from receiving work.
**R-CUSTODIAN — State Custodian**
Stores/serves canonical records/state on behalf of Owner. Custody does not create truth/currentness semantics.
**R-PROJECTOR — Projection Former**
Forms OC-07 bounded views/read models from legitimate source facts/state. Projection does not become source ownership.
**R-MAPPER — Semantic Mapper**
Performs an explicit governed cross-domain mapping under declared behavior. Mapping does not transfer authority unless an explicit Authority decision is part of the target contract.
**R-READER — Consumer**
Reads canonical facts/state/projections. Reader has no mutation/authority merely by consumption.
**R-AUDITOR — Assurance Observer**
Produces OC-12 evaluation/conformance evidence. Auditor cannot mutate runtime truth, lifecycle, authority or Architecture Truth.
Role invariants:
OWNER != WRITER.
OWNER != CUSTODIAN.
AUTHORITY != EXECUTOR.
EXECUTOR != PROVIDER IDENTITY.
PROJECTOR != SOURCE OWNER.
MAPPER != AUTHORITY by default.
READER != OWNER.
AUDITOR != RUNTIME AUTHORITY.
One implementation may implement multiple roles only when each role contract remains explicit and no semantic authority is silently inherited.

### A2.0-99｜D01–D03 Ownership Matrix
**D01 Identity & Semantic Role**
Authoritative questions:
Q01 identity declaration/identity-link legitimacy.
Q02 semantic role of an identity within a specific governed relation.
Canonical ownership semantics: Identity/Role Owner for the relevant identity namespace/relation contract.
Authority: only where identity/role admission requires explicit decision.
Writer: identity/role state writer under Owner contract.
Projector: identity/role resolution/read view.
Readers: all domains may consume resolved identity/role.
Negative: downstream consumer, request creator, trace producer or field holder cannot self-assign a governed upstream role.
**D02 Capability & Organ Declaration**
Q03 what capability/organ/model/provider declaration and versioned semantic meaning exists?
Owner: Capability/Organ Declaration Owner(s), scoped by declaration namespace.
Authority: declaration admission/version change where required.
Writer/Custodian: declaration repository under Owner contract.
Readers: D03/D06/D09/P-A.
Negative: repository/registry custody does not establish lifecycle currentness or runtime authority.
**D03 Lifecycle & Availability State**
Q04 what is current lifecycle state?
Q05 what is current asset availability state?
Owner: Lifecycle/Availability Owner for each governed asset identity/scope.
Authority: lifecycle transition/admission Authority.
Writer: transition/current-state writer after valid decision.
Projector: current lifecycle/availability read surface.
Readers: D06/D07/D09/P-A/P-D.
Negative: D06 router, D09 executor or evaluator cannot promote/activate lifecycle.

### A2.0-100｜D04–D09 Ownership Matrix
**D04 Observation Need**
Q06 what information does cognition/task require?
Owner: Observation Need Formation Owner at the legitimate cognition/task source layer.
Writer: need formation/state writer if persisted.
Projector: need read surface.
Readers: D05 and D13/D14 as applicable.
Negative: D05 controlled/non-cognitive requester may form a legal execution request without pretending to own or reconstruct D04 need.
**D05 Execution Request Formation**
Q07 what governed executable request exists and from what legitimate source/requester relation?
Owner: Execution Request Formation Owner.
Authority: formation/admission decision only if the D05 contract requires one; this is not D07 execution authority.
Writer: governed request writer.
Mapper: D04→D05 refinement/materialization or legal non-cognitive source→D05 materialization.
Readers: D06/D07/P-A.
Negative: runner/case/fixture is not Owner merely because it constructs a DTO.
**D06 Resolution, Routing & Binding**
Q08 what capability/target is compatible/resolved?
Q09 what routing/binding association is valid for the request?
Owner: Resolution/Binding Owner for these bounded questions.
Authority: compatibility/resolution/binding decisions only within D06; never runtime effect authority.
Writer: resolution/binding state writer where canonical state exists.
Projector: routing/binding read surface.
Readers: D07/D08/D09.
Negative: D06 cannot issue D07 permission.
**D07 Permission & Effect Authorization**
Q10 may a governed request enter execution formation?
Q11 may the specified runtime effect occur now under required current dependencies?
Canonical ownership semantics: one Permission/Admission Authority Domain; Q10 and Q11 are separate decision contracts.
Authority: Entry Admission Authority for Q10; Runtime Effect Authorization Authority for Q11. They may be implemented by the same Permission/Admission Owner but decisions cannot collapse.
Writer: decision/current-authorization state writer only after Authority decision.
Custodian: authorization state store.
Projector: current authorization query.
Readers: D05/D06/D08/D09/P-A.
Negative: requester, router, binder, resource allocator, executor/provider and state store cannot self-authorize. Entry Admission != Runtime Effect Authorization.
**D08 Resource & Execution Readiness**
Q12 what resources are required/prepared/allocated?
Q13 are required resources actually available/current for the effect?
Owner: Resource/Readiness Owner.
Authority: allocation/readiness decision for resource question only.
Writer: resource allocation/availability state writer.
Executor: resource allocator may perform allocation effect after relevant authorization.
Projector: resource readiness/availability view.
Readers: D07/D09/P-D.
Negative: allocation authority is not Organ execution authority; D07 may depend on D08 current facts without owning them.
**D09 Organ Runtime & Native Capability Execution**
Q14 what authorized Organ/native effect was attempted/performed and what result occurred?
Owner: Organ Execution Contract Owner for effect/result semantics.
Executor: selected Organ/provider runtime executor.
Writer: execution/result record writer.
Custodian: execution history/result store if persisted.
Mapper: D09→D10 Observation Mapping actor under D10 mapping/admission contract.
Readers: D10/P-A/P-D.
Negative: executor/provider cannot issue D07 authorization, D10 Evidence admission, or D13 cognitive judgment.

### A2.0-101｜D10–D12 Ownership Matrix
**D10 Observation Admission & Evidence**
Q15 what Organ/observation information is admissible as governed Evidence and with what Evidence semantics?
Owner: Observation/Evidence Owner.
Authority: Evidence Admission Authority for Evidence scope.
Mapper: D09 result→Observation/Evidence candidate mapping.
Writer: admitted Evidence writer.
Custodian: Evidence store where persisted.
Projector: Evidence query/read model.
Readers: Context formation, D11, D12, D13 where contractually allowed.
Negative: D09 result writer/provider cannot self-admit Evidence; Evidence admission does not declare Field/Current World truth.
**Context & Situational Framing**
No independent global Owner in v0.2.
Formation ownership belongs to the target world-information/cognition contract that requests the Context projection. Mapper/Projector must preserve D10 source meaning and explicit role/task basis.
Negative: no Context super-owner, no Context truth authority.
**D11 Field & World Information Assimilation**
Q16 may a candidate event enter the Field?
Q17 what is the canonical current Field state for the defined Field scope?
Owner: Field Information Owner.
Authority: Field Event Admission Authority for Q16; Field State transition/currentness semantics remain under the same Field ownership family but are not identical decisions.
Writer: admitted event/state writer/reducer only under Field contracts.
Custodian: Field event/state history store.
Projector: Field read model.
Readers: D12/D13/D16/P-A.
Negative: reducer is not automatically Owner; read model is not source; D12 cannot mutate D11 by projection.
**D12 Current World Projection**
Q18 what governed current-world projection is available for the defined role/perspective/task/currentness scope?
Owner: Current World Formation Owner for projection semantics/currentness judgment.
Projector: Current World projector/former.
Writer: only if Current World current projection/state is registered under its Owner contract.
Readers: D13/D14/D16.
Negative: D12 does not own D11 source Field facts; projection currentness does not rewrite Field currentness.

### A2.0-102｜D13–D16 Ownership Matrix
**D13 Cognitive State & Local Reality Reasoning**
Q19 what local attention/hypothesis/gap/contradiction/sufficiency/stop judgment is formed from governed information?
Owner: Local Cognitive Reasoning Owner.
Authority: bounded local cognitive decisions such as sufficiency/stop only for cognitive-flow effects.
Writer: cognitive-state writer if persisted.
Projector: cognitive-state read model.
Readers: D04/D14/D16.
Negative: D13 cannot issue D07 runtime Organ authorization or D15 action admission; global policy cannot rewrite D13 world reasoning.
**D14 Task, Decision & Action Intent**
Q20 what task state/decision/action-intent candidate is formed?
Owner: Task/Decision Formation Owner.
Authority: task/decision transition authority only within D14 lifecycle where required.
Writer: task/decision state writer.
Projector: task/decision read model.
Readers: D04/D15/D16.
Negative: action intent is not action admission or action effect authority.
**D15 Global Policy, Safety & Action Admission**
Q21 what global policy/safety constraints currently apply?
Q22 may the proposed action proceed within those constraints?
Owner: Global Policy/Safety Owner(s) for Q21; Action Admission Owner/Authority for Q22.
Authority: Action Admission Authority for Q22.
Writer: policy/safety current-state writer and action-admission decision writer under their respective Owner contracts.
Projector: policy/safety/action-admission views.
Readers: D14, action executors, D07 where an effect contract depends on them.
Negative: D15 does not own D11/D12 world facts or D13 hypothesis; D13 local sufficiency cannot override D15 safety, and D15 safety cannot fabricate local world observations.
**D16 Memory & Experience**
Q23 what historical memory/experience/relationship record is canonical for its scope?
Q24 what revision/supersession/assimilation is legitimate?
Owner: Memory/Experience Owner.
Authority: memory assimilation/revision admission where required.
Writer: memory/history writer after legitimate assimilation/revision.
Custodian: durable memory/experience store.
Projector: retrieval projection.
Readers: D10–D14 as explicitly governed.
Negative: memory retrieval does not become D12 Current World; Memory Owner cannot silently rewrite D11 Field history or D13 current hypothesis. Learning/model-write authority is absent.

### A2.0-103｜Cross-Cutting Plane Responsibilities
**P-A Assurance & Evaluation**
Role: R-AUDITOR plus controlled-request source roles only when explicitly admitted through ordinary D05/D07 contracts.
Owns evaluation artifacts/conformance evidence, not runtime domain truth.
May read all required domain projections under evaluation contracts.
Cannot mutate D03 lifecycle, issue D07 authorization, admit D10 Evidence merely because a test passed, or freeze architecture.
**P-D Deployment, Composition & Operational Continuity**
Role: cross-domain constraint/mapping/custody coordination, not replacement Owner.
Defines topology/transport/restart/reconciliation/degraded-operation requirements.
Each D01–D16 Owner retains its authoritative question across local/remote/Hive/restart contexts.
P-D may coordinate reconciliation but cannot directly overwrite another domain's canonical current state without that Owner's reconciliation contract.

### A2.0-104｜Owner / Authority Collision Review
**Collision test 01 — D03 vs D06:** no collision. D03 owns lifecycle/availability; D06 owns compatibility/resolution/binding.
**02 — D06 vs D07:** no collision. Binding decision cannot authorize effect.
**03 — D07 vs D08:** no collision. Permission may depend on resource state; it does not own resource availability.
**04 — D07 vs D09:** no collision. Authority vs executor/effect result.
**05 — D09 vs D10:** no collision. execution result vs Evidence admission.
**06 — D10 vs D11:** no collision. Evidence scope vs Field admission/state.
**07 — D11 vs D12:** no collision. Field source state vs Current World projection.
**08 — D12 vs D13:** no collision. world projection vs local reasoning.
**09 — D13 vs D15:** no collision. local reality judgment vs global policy/safety/action admission.
**10 — D14 vs D15:** no collision. intent/decision candidate vs action admission.
**11 — D16 vs D11/D12:** no collision if retrieval remains projection/history and assimilation uses explicit mapping/admission.
**12 — P-A/P-D vs domains:** no collision only if planes remain observer/constraint/reconciliation views and do not become shadow Owners.
Important adjudication:
D07 is allowed one canonical ownership family with two distinct Authority decisions because both answer permission/admission questions for execution effects. This does NOT permit one generic 'authorized=true' state to replace Entry Admission and Runtime Effect Authorization.
D15 contains Q21 policy/safety facts and Q22 action admission, but these must remain separate object/decision contracts; domain grouping does not imply one mutable state blob.

### A2.0-105｜Writer / Custodian / Projection Discipline
For every OC-04/OC-05/OC-06 object family later mapped to implementation, the Canonical Contract Ledger must state:
OWNER
AUTHORITY_IF_ANY
AUTHORIZED_WRITER
CUSTODIAN
CURRENTNESS_QUERY_OWNER
INVALIDATION_OWNER
PROJECTOR
PERMITTED_READERS
WRITE_BASIS
PROVENANCE_REQUIREMENTS
TEMPORAL_REQUIREMENTS
FAILURE_UNKNOWN_BEHAVIOR.
No implementation may be declared conformant merely because it stores the right fields. Conformance requires role legitimacy.
A cache/read model may be physically writable but remains R-PROJECTOR/R-CUSTODIAN, not R-OWNER.
A reducer may compute state but is R-WRITER/formation mechanism unless the architecture explicitly assigns Owner semantics.
A runner/orchestrator may call multiple Owners but remains coordinator/reader unless explicitly assigned another role.
A provider adapter may normalize/execute but cannot inherit Evidence Admission or cognitive authority.
A registry may custody declarations but cannot infer current lifecycle state from presence.

### A2.0-106｜Batch 04 Gap Impact
CA-GAP-01: D05 Execution Request Formation Owner and D07 Entry Admission Authority are now distinct required roles. Missing governed controlled source cannot be solved by runner self-ownership.
CA-GAP-02: D07 effect authorization must read contract-required D03/D06 and other Owner projections; D07 does not absorb those Owners.
CA-GAP-03: D08 owns resource readiness; D07/D09 consume it as required dependency.
CA-GAP-04: expiry/currentness requires each relevant Owner to define temporal/currentness semantics; D07 cannot infer expiry from a ref alone.
CA-GAP-05: D10 Evidence Owner → target Context formation → D11 Field Owner → D12 Current World Owner/projection; no direct provider-to-world ownership transfer.
CA-GAP-06: P-D reconciliation cannot choose canonical architecture based on legacy code survival; D01–D16 ownership remains invariant across deployment families.
CA-GAP-07: P-D restart/reconciliation must re-establish or query each domain Owner's current state; it cannot become a global currentness Owner.
IMPL-NC-01: current controlled runner is coordinator/executor-side code and has no canonical role permitting it to fabricate D01/D06 lineage or D07 authority.

### A2.0-107｜Batch 04 Adjudication
- CORE_DOMAINS_REVIEWED=16/16
- AUTHORITATIVE_QUESTIONS=24
- RESPONSIBILITY_ROLES=9
- OWNER_AUTHORITY_COLLISIONS_CONFIRMED=0
- SHADOW_OWNER_ALLOWED=NO
- SUPER_MANAGER_REQUIRED=NO
- GLOBAL_CURRENTNESS_OWNER_REQUIRED=NO
- D07_ONE_DOMAIN_TWO_DECISIONS=CONFIRMED
- D11_D12_SOURCE_PROJECTION_SEPARATION=CONFIRMED
- D13_D15_LOCAL_GLOBAL_AUTHORITY_SEPARATION=CONFIRMED
- P_A_RUNTIME_TRUTH_OWNER=NO
- P_D_RUNTIME_TRUTH_OWNER=NO
- IMPLEMENTATION_OWNER_MAPPING_STARTED=NO
- OWNERSHIP_AUTHORITY_MATRIX_STATUS=CANDIDATE
- CODE_CHANGE_AUTHORIZED=NO
- PR_ADMISSION_02_RESUME=NO
- GROUNDING_DINO_RESUME=NO
Next: ACM-02 Batch 05 — Canonical Contract Ledger. Define the minimum architecture-significant contracts between D01–D16: source/target roles, required inputs, output semantic class, Owner/Authority, currentness, temporal semantics, failure/unknown behavior, and explicit negative guarantees. Do not define Python DTO schemas yet.

## Source and status guard

Source: [Notion 03.7 Architecture 2.0](https://app.notion.com/p/3c3113b33a6d81dfa4efeac030352d96), A2.0-97–107. Historical Batch status is preserved above. For current gap status see [Batch 07 temporal/currentness ledger](temporal_currentness_validity_ledger_v0_1.md): CA-GAP-04 and CA-GAP-07 are RESOLVED_AT_CANONICAL_LEVEL only; five Canonical gaps and IMPL-NC-01 remain OPEN; both implementation audits are NOT_STARTED. No code remediation, PR-ADMISSION-02 resumption or Grounding DINO implementation is authorized.
