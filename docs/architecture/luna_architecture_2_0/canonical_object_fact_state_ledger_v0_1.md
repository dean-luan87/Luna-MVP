# Architecture 2.0 — Canonical Object / Fact / State Ledger v0.1

OBJECT_CLASS_COUNT=12  
BATCH=ACM-02 03  
STATUS=DESIGN_IN_PROGRESS; CANONICAL_ARCHITECTURE_FROZEN=NO

Repository-side transcription of [Notion 03.7 Architecture 2.0](https://app.notion.com/p/3c3113b33a6d81dfa4efeac030352d96), A2.0-87–96, read 2026-09-30. This ledger records candidate Canonical Architecture semantics, not Python DTOs, production conformance, runtime authorization or gap closure. Frozen Constitution v1 remains in [its separate file](architecture_2_0_constitution_v1.md).

### A2.0-87｜ACM-02 Batch 03 — Canonical Object / Fact / State Ledger
**STATUS:** SEMANTIC_OBJECT_LEDGER_CANDIDATE
**INPUT:** Reconciled D01–D16 / P-A / P-D
**CONSTITUTION_BASE:** C01–C48 FROZEN
**IMPLEMENTATION_CLASS_MAPPING:** NOT_STARTED
**CODE_CHANGE_AUTHORIZED:** NO
Purpose: define what kinds of canonical semantic objects exist before mapping current Python classes to them.

### A2.0-88｜Canonical Semantic Object Classes
**OC-01 DECLARATION** — versioned statement of identity/capability/contract/configured semantic meaning. A declaration is not proof of currentness, admission, availability or effect authority.
**OC-02 REQUEST / NEED CANDIDATE** — proposed need/request/intent awaiting required formation/admission/authorization semantics.
**OC-03 FORMATION CANDIDATE** — newly formed domain object that has not crossed the governed admission/decision boundary required by its target semantics.
**OC-04 ADMITTED FACT** — information accepted by the canonical Owner/Admission boundary as a governed fact within a defined semantic scope. Admission scope must be explicit; admitted fact is not universal/world truth.
**OC-05 DECISION** — authoritative judgment for a defined question/effect/scope, with basis and currentness requirements. A decision does not prove that the authorized effect occurred.
**OC-06 CURRENT STATE** — Owner-governed answer to a current-state question for a defined scope, including invalidation/currentness semantics. Latest record is not automatically current state.
**OC-07 PROJECTION / READ MODEL** — bounded derived view of canonical facts/state for a consumer. It does not become a second authoritative source.
**OC-08 EFFECT RESULT** — record/result of an effect that actually occurred or was attempted under its execution contract. Effect result is not automatically Evidence or epistemic/world fact.
**OC-09 HISTORICAL RECORD** — durable history/audit/revision/supersession record. Historical existence does not imply currentness.
**OC-10 DERIVED COGNITIVE STATE** — governed local reasoning product such as hypothesis/gap/sufficiency; revisable and distinct from source world information.
**OC-11 POLICY / CONSTRAINT FACT** — governed global policy/safety/operational constraint applicable to a defined scope. It does not rewrite local world facts.
**OC-12 EVALUATION / ASSURANCE EVIDENCE** — evidence about contract/process/conformance behavior. It cannot self-promote runtime lifecycle, authority or Architecture Truth.
Object-class invariants:
DECLARATION != CURRENT_STATE.
CANDIDATE != ADMITTED_FACT.
ADMITTED_FACT(scope A) != universal truth.
DECISION != EFFECT_RESULT.
EFFECT_RESULT != EVIDENCE unless a governed mapping/admission establishes Evidence.
PROJECTION != SOURCE_FACT.
HISTORICAL_RECORD != CURRENT_STATE.
DERIVED_COGNITIVE_STATE != WORLD_SOURCE_FACT.
POLICY_CONSTRAINT != LOCAL_WORLD_FACT.
EVALUATION_EVIDENCE != PRODUCTION_AUTHORITY.

### A2.0-89｜D01–D03 Foundation Ledger
**D01 Identity & Semantic Role**
Canonical objects:
- Governed Identity Declaration — OC-01.
- Semantic Role Assignment / Relation Role — OC-04 when established by the owning relation/contract; may begin as OC-03.
- Identity Link / Alias Relation — OC-04 within identity-link scope.
- Identity/Role Current Resolution — OC-06 or OC-07 depending whether Owner judgment or consumer projection.
- Identity/Role History — OC-09.
Negative facts: request_id, trace_ref, provenance_ref, object possession and field-name compatibility are not Identity Declaration or Role Assignment.
**D02 Capability & Organ Declaration**
Canonical objects:
- Capability Declaration — OC-01.
- Organ Declaration — OC-01.
- Model Declaration / Provider Declaration — OC-01 specializations where applicable.
- Capability-to-Organ Semantic Compatibility Declaration — OC-01 when statically declared; dynamic compatibility judgment belongs D06.
- Native Semantic Contract Declaration — OC-01.
- Declaration Version/History — OC-09.
Negative facts: declaration does not establish ACTIVE, available, routable, authorized or successfully executable.
**D03 Lifecycle & Availability State**
Canonical objects:
- Lifecycle Transition Candidate — OC-03.
- Lifecycle Admission/Transition Decision — OC-05.
- Lifecycle Current State — OC-06.
- Asset Availability Current State — OC-06.
- Lifecycle/Availability Projection — OC-07.
- Lifecycle Transition History — OC-09.
Negative facts: declaration version, registry presence, last-updated timestamp, test pass or successful historical execution do not prove current lifecycle/availability.

### A2.0-90｜D04–D09 Execution Formation Ledger
**D04 Observation Need**
- Observation Need Candidate — OC-02.
- Observation Gap Candidate — OC-02 / OC-10 depending source.
- Governed Observation Need Formation — OC-04 within cognition/task formation scope; it is not execution admission.
- Observation Need Projection — OC-07.
- Need/Gap History — OC-09.
Negative: Observation Need cannot itself name an authorized provider effect.
**D05 Execution Request Formation**
- Execution Demand Candidate — OC-02.
- Execution Request Candidate — OC-02.
- Governed Execution Request — OC-04 after legitimate source/role/formation basis is established.
- Request Purpose / Policy Class — part of governed request semantics, not authority.
- Request Source/Requester Relation — D01-governed relation carried by D05.
- Request History — OC-09.
Negative: controlled-evaluation fixture/case/runner invocation alone is not a Governed Execution Request.
**D06 Resolution, Routing & Binding**
- Capability Resolution Candidate — OC-03.
- Routing Candidate / Target Candidate — OC-03.
- Compatibility Judgment — OC-05 for the bounded compatibility question; not effect authorization.
- Binding Candidate — OC-03.
- Governed Binding / Routing Resolution — OC-04 or OC-05 according to whether the contract establishes a fact association or judgment.
- Routing/Binding Current Projection — OC-07.
- Resolution/Binding History — OC-09.
Negative: compatible/resolved/bound target is not permission to execute.
**D07 Permission & Effect Authorization**
Two distinct authority decision families under one domain:
A. Entry Admission:
- Entry Admission Request/Basis — OC-03 derived from governed D05 request + required dependencies.
- Entry Admission Decision — OC-05.
- Entry Admission Current State/Query Result — OC-06/OC-07.
B. Runtime Effect Authorization:
- Runtime Authorization Input/Basis — OC-03.
- Runtime Effect Authorization Decision / Grant — OC-05.
- Runtime Authorization Current State — OC-06.
- Authorization Projection/Query Result — OC-07.
- Authorization/Invalidation History — OC-09.
Negative: Entry Admission Decision != Runtime Effect Authorization Decision; neither requester nor runner may mint either.
**D08 Resource & Execution Readiness**
- Resource Requirement / Preparation Candidate — OC-03.
- Resource Allocation Decision — OC-05 for allocation question.
- Resource Availability Current State — OC-06.
- Execution Readiness Decision — OC-05 if architecture requires a distinct readiness judgment.
- Allocation/Availability Projection — OC-07.
- Resource/Allocation History — OC-09.
Negative: preparation reference or allocation record does not automatically prove current physical availability.
**D09 Organ Runtime & Native Capability Execution**
- Organ Invocation Candidate — OC-03.
- Authorized Invocation Basis Projection — OC-07; authority remains D07.
- Native Execution Attempt / Effect — effect occurrence governed by execution contract.
- Native Result — OC-08.
- Normalized Organ Runtime Result — OC-08.
- Execution Failure / Empty Result — OC-08 with explicit semantic state.
- Execution History — OC-09.
Negative: Native/normalized Organ result and model confidence are not Evidence, world truth or cognitive confidence.

### A2.0-91｜D10–D12 World Information Ledger
**D10 Observation Admission & Evidence**
- Observation Mapping Candidate — OC-03 from D09 result.
- Observation Candidate/Envelope — OC-03.
- Evidence Admission Decision — OC-05.
- Admitted Evidence — OC-04 within Evidence scope.
- Evidence Projection/Query — OC-07.
- Evidence/Admission History — OC-09.
- Absence/Empty Observation Semantics — explicit Evidence-scope semantics; zero output does not become negative world fact automatically.
Negative: Organ result != Evidence; Evidence != Context/Field/Current World.
**Context & Situational Framing — canonical formation layer**
- Context Formation Candidate — OC-03.
- Governed Context Projection/Formation — OC-07 or OC-04 only within explicitly defined context scope.
- Context source relation — explicit D10/D11/D12 mapping basis.
Context has no independent universal truth/currentness authority in v0.2.
Negative: Context cannot rewrite Evidence or manufacture Field/world fact.
**D11 Field & World Information Assimilation**
- Field Event Candidate — OC-03.
- Field Event Admission Decision — OC-05.
- Admitted Field Event — OC-04.
- Field State Formation Candidate — OC-03.
- Field Current State — OC-06.
- Field State Projection / Read Model — OC-07.
- Supersession/Invalidation Relation — OC-04/OC-09 according to contract.
- Field/Event History — OC-09.
Temporal role/validity/currentness is contract-governed.
Negative: reducer output/read model is not second source truth; arrival time does not establish world-effective time.
**D12 Current World Projection**
- Current World Formation Candidate — OC-03.
- Current World Projection — OC-07.
- Current World Currentness Judgment — OC-05/OC-06 when explicitly owned.
- Current World Source Basis — explicit D10/D11/context provenance relation.
- Current World Revision/Supersession History — OC-09.
Negative: Current World is a governed cognition-facing projection, not immutable external truth, not direct Organ output and not a competing Field source.

### A2.0-92｜D13–D16 Cognition / Action / Memory Ledger
**D13 Cognitive State & Local Reality Reasoning**
- Attention Candidate/State — OC-10.
- Hypothesis Candidate/State — OC-10.
- Observation Gap / Contradiction Judgment — OC-10.
- Sufficiency Judgment — OC-10; where it gates a local cognitive transition it may carry OC-05 decision semantics for that bounded question.
- Stop/Continue Judgment — OC-10/OC-05 within local cognition scope.
- Cognitive State Projection — OC-07.
- Cognitive Revision History — OC-09.
Negative: hypothesis/sufficiency/stop does not grant runtime Organ or action authority.
**D14 Task, Decision & Action Intent**
- Task Candidate / Governed Task State — OC-02/OC-06 according to lifecycle.
- Decision Candidate — OC-03.
- Action Intent Candidate — OC-03.
- Reconsideration/Feedback Candidate — OC-03.
- Task/Decision Projection — OC-07.
- Task/Decision History — OC-09.
Negative: Decision Candidate/Action Intent is not action-effect authorization.
**D15 Global Policy, Safety & Action Admission**
- Global Policy/Constraint Fact — OC-11.
- Safety Current State — OC-06/OC-11.
- Action Admission Input/Basis — OC-03.
- Action Admission Decision — OC-05.
- Working/Execution Envelope — OC-04/OC-05 according to whether it states admitted scope or decision.
- Degraded/Survival Constraint — OC-11.
- Policy/Safety/Admission History — OC-09.
Negative: global policy/safety does not rewrite D11/D12 world information; Action Admission does not by itself prove action effect occurred.
**D16 Memory & Experience**
- Memory Object / Stable Ontology Record — OC-04/OC-09 depending live canonical fact vs historical record.
- Relationship Record/Graph Edge — OC-04/OC-09 with role/perspective semantics explicit.
- Experience Record — OC-09.
- Memory Retrieval Projection — OC-07.
- Memory Update/Assimilation Candidate — OC-03.
- Memory Revision/Supersession Relation — OC-09.
- Learning Candidate — OC-03 future-facing only; no model-write authority.
Negative: retrieval projection is not current world; experience does not automatically become current fact; semantic compression is not assumed.

### A2.0-93｜Cross-Cutting Plane Object Semantics
**P-A Assurance & Evaluation Plane**
- Evaluation Plan/Case Declaration — OC-01/OC-02.
- Evaluation Run Record — OC-09.
- Verification Result / Conformance Evidence — OC-12.
- Architecture Audit Evidence — OC-12.
- Effectiveness Status — OC-12.
Negative: PASS does not freeze architecture, activate lifecycle, grant execution authority or prove production deployment.
**P-D Deployment, Composition & Operational Continuity Plane**
This plane does not own duplicate domain truth objects.
It defines cross-domain requirements/relations for:
- Deployment/Topology Declaration — OC-01.
- Transport/Integration Declaration — OC-01.
- Local Autonomy Policy/Constraint — OC-11.
- Restart/Recovery Record — OC-09.
- Reconciliation Candidate/Decision — OC-03/OC-05 only for reconciliation scope; it may not overwrite domain Owner facts without their governed contract.
- Degraded Operation Constraint — OC-11.
- Remote Execution/Composition Relation — governed relation, not authority transfer.
Negative: process/node/transport/topology does not become semantic identity/Owner/Authority by itself.

### A2.0-94｜Fact-Level Promotion Rules
Canonical promotion is question/scope specific, not a universal pipeline.
Allowed general pattern:
DECLARATION → governed current-state/compatibility judgment only through relevant Owner.
CANDIDATE → ADMITTED FACT only through target admission contract.
REQUEST → AUTHORIZATION only through explicit Authority decision; request itself never promotes.
DECISION → CURRENT STATE only if the owning contract defines current-state registration/query/invalidation.
EFFECT RESULT → EVIDENCE only through Observation Mapping + Evidence Admission.
EVIDENCE → FIELD EVENT only through explicit Context/World mapping + Field Event Admission.
FIELD STATE → CURRENT WORLD only through governed projection/formation.
CURRENT WORLD → COGNITIVE STATE through local reasoning/derivation, not truth transfer.
COGNITIVE STATE → ACTION INTENT through governed decision formation, not execution authority.
ACTION INTENT → ACTION EFFECT only through required global/action admission and effect authorization contracts.
HISTORY → CURRENT STATE never by recency alone.
EVALUATION EVIDENCE → ARCHITECTURE CHANGE only through architecture governance; never automatic.

### A2.0-95｜Batch 03 Gap Impact
CA-GAP-01 now resolves around missing/underdefined D05 Governed Execution Request + D07 Entry Admission Decision/currentness contract.
CA-GAP-02 resolves around D07 Runtime Authorization Basis dependency declaration and D03/D06 current Owner queries.
CA-GAP-03 resolves around D08 distinction among Preparation Candidate, Allocation Decision, Availability Current State and optional Readiness Decision.
CA-GAP-04 becomes a cross-object temporal contract concern: D07 authorization expiry/currentness, D11 world-effective validity, D12 projection currentness, P-D restart/reconciliation.
CA-GAP-05 resolves around D10 Admitted Evidence → Context Formation → D11 Field Event Admission/State → D12 Current World Projection.
CA-GAP-06 remains deployment/canonical path reconciliation; object classes prevent legacy runtime result/candidate from becoming canonical by survival.
CA-GAP-07 resolves around OC-06 Current State + invalidation/requery/persistence semantics under P-D.
IMPL-NC-01 remains a violation of D01/D05/D06 semantic provenance and cannot be fixed until D05/D07 contracts are adjudicated.

### A2.0-96｜Batch 03 Adjudication
- CANONICAL_OBJECT_CLASSES=12
- CORE_DOMAINS_COVERED=16/16
- CROSS_CUTTING_PLANES_COVERED=2/2
- DECLARATION_CURRENT_STATE_SEPARATED=YES
- CANDIDATE_ADMITTED_FACT_SEPARATED=YES
- DECISION_EFFECT_RESULT_SEPARATED=YES
- EFFECT_RESULT_EVIDENCE_SEPARATED=YES
- PROJECTION_SOURCE_FACT_SEPARATED=YES
- HISTORY_CURRENT_STATE_SEPARATED=YES
- COGNITIVE_STATE_WORLD_FACT_SEPARATED=YES
- POLICY_WORLD_FACT_SEPARATED=YES
- EVALUATION_PRODUCTION_AUTHORITY_SEPARATED=YES
- IMPLEMENTATION_CLASS_MAPPING_STARTED=NO
- CANONICAL_OBJECT_LEDGER_STATUS=CANDIDATE
- CODE_CHANGE_AUTHORIZED=NO
- PR_ADMISSION_02_RESUME=NO
- GROUNDING_DINO_RESUME=NO
Next: ACM-02 Batch 04 — Canonical Owner / Authority / Writer / Reader Matrix. Assign each authoritative question/object family to exactly one canonical ownership semantics; distinguish Owner, Authority, Writer, Executor, Custodian, Projector and Reader. This is the prerequisite for later Contract and Mapping ledgers.

## Source and status guard

Source: [Notion 03.7 Architecture 2.0](https://app.notion.com/p/3c3113b33a6d81dfa4efeac030352d96), A2.0-87–96. Historical Batch status is preserved above. For current gap status see [Batch 07 temporal/currentness ledger](temporal_currentness_validity_ledger_v0_1.md): CA-GAP-04 and CA-GAP-07 are RESOLVED_AT_CANONICAL_LEVEL only; five Canonical gaps and IMPL-NC-01 remain OPEN; both implementation audits are NOT_STARTED. No code remediation, PR-ADMISSION-02 resumption or Grounding DINO implementation is authorized.
