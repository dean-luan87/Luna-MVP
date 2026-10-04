# Architecture 2.0 — Canonical Architecture v0.2

CANONICAL_ARCHITECTURE_STATUS=DESIGN_IN_PROGRESS  
CANONICAL_ARCHITECTURE_FROZEN=NO  
CONSTITUTION_BASE=Architecture 2.0 Constitution v1 (C01–C48, FROZEN)  
ACM_02_BATCHES=01–08 DOCUMENTED  
CORE_DOMAIN_COUNT=16  
CROSS_CUTTING_PLANE_COUNT=2  
AUTHORITATIVE_QUESTION_COUNT=24

This is current candidate Canonical Architecture, not current-code conformance or production authorization. [Notion 03.7 A2.0-74–86](https://app.notion.com/p/3c3113b33a6d81dfa4efeac030352d96) is the design source; the [historical Freeze v1](../luna_canonical_architecture_freeze_v1/README.md) is preserved, not retroactively revised.

## Batch 01 → Batch 02 version lineage

Batch 01 (A2.0-74–79) established a skeleton of 18 candidate domains, cross-domain relation classes and Owner/Authority boundaries. Batch 02 reviewed those candidates, separated Observation Need from Execution Request Formation, and reclassified Evaluation and Deployment as cross-cutting planes, Context as a formation layer, and Learning as a future candidate. The reconciled current candidate set is D01–D16 below. Batch 01 numbering/semantics remain historical lineage, not parallel current domain truth.

## Batch 02 — reconciled domains and boundaries

### A2.0-81｜Domain-by-Domain Reconciliation
**D01 Identity & Semantic Role — KEEP.**
Independent question: what entity/reference is this and what role does it play in this relation? Identity/role interpretation is prerequisite to, but not equivalent to, authority/currentness/mapping. Stable across implementations.
**D02 Capability & Model/Provider Semantics — KEEP, RENAME to Capability & Organ Declaration.**
Reason: Model/Provider are important current Organ identities but Canonical Architecture should not imply all future capabilities must be model/provider-shaped. Domain owns declared capability/organ identity/version/semantic meaning. Concrete Model/Provider subtypes remain canonical specializations.
**D03 Lifecycle & Eligibility — KEEP, NARROW to Lifecycle & Availability State.**
Eligibility is overloaded: lifecycle currentness and routing/effect eligibility are different questions. D03 owns lifecycle/admission/activation/current availability state of capability/organ assets. Routing compatibility remains D06 below; effect authorization remains Permission domain.
**D04 Observation Need & Execution Demand — SPLIT.**
These answer different questions and source layers:
- D04 Observation Need: what information does cognition/task require and why?
- D05 Execution Request Formation: what bounded executable request/demand has been legitimately materialized from an allowed source layer?
Reason: preserving this separation is necessary for EA-01/EA-02/EA-03 and prevents non-cognitive controlled entry from fabricating Cognitive intent.
**Old D05 Resolution, Routing & Binding — KEEP as new D06.**
Resolution/routing/binding can share one domain because they answer one bounded target-selection/association question and none grants effect authority. Internal stages may remain separate contracts.
**Old D06 Permission, Admission & Effect Authorization — KEEP as one Domain, but explicitly two authority questions inside one canonical Authority Domain.**
New D07 Permission & Effect Authorization.
Entry Admission and Runtime Effect Authorization remain distinct decisions/effect boundaries of the same Permission/Admission authority family. Splitting them into separate Domains would risk creating a second authority system; merging their decisions would violate C21. Therefore: one Domain, two explicit authority contracts.
**Old D07 Resource & Execution Readiness — KEEP as new D08.**
Independent authoritative question: resource preparation/allocation/availability. Must not be absorbed by routing or execution authorization.
**Old D08 Organ Runtime & Native Capability Execution — KEEP as new D09.**
Independent effect domain. Provider/model implementation is replaceable; bounded Organ execution semantics are durable.
**Old D09 Observation Admission & Evidence — KEEP as new D10.**
Evidence admission is an epistemic boundary distinct from Organ execution and world-state formation.
**Old D10 Context & Situational Framing — DO NOT KEEP AS STANDALONE OWNER DOMAIN; RECLASSIFY as Canonical World-Information Formation Layer under new D11.**
Reason: current evidence does not establish an independent authoritative current-state question that requires a separate Context Owner. Context is a governed semantic formation/projection between Evidence and Field/World, and must remain explicit, but Domain status would overstate ownership and risk a Context truth authority. Concrete Context candidate/admission contracts remain canonical.
**Old D11 Field & Temporal World State + old D12 Current World Formation — KEEP SEPARATE, grouped under World Information Architecture.**
New D11 Field & World Information Assimilation: owns admitted event/Field state assimilation and temporal validity/current Field state.
New D12 Current World Projection: owns governed cognition-facing current-world projection.
Reason: Field state and Current World answer different authoritative questions; Current World is role/perspective/task-bounded projection and must not become Field truth.
**Old D13 Cognitive State & Local Reality Reasoning — KEEP as D13.**
Independent local reasoning authority; Hypothesis/Sufficiency/Stop remain canonical semantics here.
**Old D14 Task, Decision & Action Intent — KEEP as D14.**
Task/decision/action candidate formation is semantically distinct from local reality reasoning and from action admission/effect.
**Old D15 Global Policy, Safety & Action Admission — KEEP as D15, but separate Global Policy facts from Action Admission decision contracts internally.**
One governance/action-control domain is acceptable because both answer whether candidate action may proceed under global constraints, while local cognition remains D13. Internal Owner questions must remain explicit.
**Old D16 Memory, Experience & Learning Candidates — SPLIT conceptually but NOT into two Domains yet. KEEP as D16 Memory & Experience; move Learning Candidate formation to a canonical subdomain/view pending future Learning architecture.**
Reason: durable Memory/Experience is current architecture; Learning is intentionally future-facing and must not create premature model-write authority. Semantic compression remains deferred. A later Learning Domain requires independent authoritative question and lifecycle.
**Old D17 Evaluation, Verification & Architecture Evidence — RECLASSIFY from business/semantic Domain to Cross-Cutting Assurance Plane.**
Reason: evaluation/verification observes and proves properties of other domains; it should not become a parallel runtime semantic truth domain. Controlled Evaluation may legally create requests/evidence through ordinary canonical domains, but its evaluation artifacts and conformance evidence belong to Assurance. It has no authority to promote lifecycle, authorize runtime effect, or redefine architecture.
**Old D18 Deployment, Composition & Operational Continuity — RECLASSIFY to Cross-Cutting Deployment & Continuity Plane.**
Reason: topology/restart/disconnection/remote transport cut across all stateful/authority domains. Treating deployment as a peer semantic Domain could create duplicate ownership of currentness/authority. The plane defines preservation/reconciliation requirements; each canonical Owner retains its authoritative question.

### A2.0-82｜Reconciled Canonical Domain Set v0.2
Final candidate set after Batch 02:
**Core semantic domains — 16**
D01 Identity & Semantic Role
D02 Capability & Organ Declaration
D03 Lifecycle & Availability State
D04 Observation Need
D05 Execution Request Formation
D06 Resolution, Routing & Binding
D07 Permission & Effect Authorization
D08 Resource & Execution Readiness
D09 Organ Runtime & Native Capability Execution
D10 Observation Admission & Evidence
D11 Field & World Information Assimilation
D12 Current World Projection
D13 Cognitive State & Local Reality Reasoning
D14 Task, Decision & Action Intent
D15 Global Policy, Safety & Action Admission
D16 Memory & Experience
**Cross-cutting planes — 2**
P-A Assurance & Evaluation Plane
P-D Deployment, Composition & Operational Continuity Plane
**Canonical formation layer, not standalone Domain**
Context & Situational Framing — explicit governed formation/projection within World Information Architecture, primarily between D10 and D11/D12.
**Future candidate, not admitted Domain**
Learning — remains future canonical candidate. No current model-write/training authority is created.

### A2.0-83｜Authoritative Question Reconciliation
D01: What identity/reference and semantic role is this?
D02: What bounded capability/organ declaration and semantic meaning exists?
D03: What lifecycle/current availability state does that declared asset have?
D04: What information is needed for cognition/task reasoning?
D05: What executable request has legitimately been formed from an allowed source layer?
D06: What compatible target/resolution/routing/binding has been formed for the request?
D07: May the request enter governed execution formation, and may the final specified effect occur under required current dependencies?
D08: Are required resources prepared/allocated/available for that effect?
D09: What bounded Organ/native execution occurred and what normalized result was produced?
D10: What observed information is admitted as governed Evidence?
D11: What admitted information/events are assimilated into Field/world-information state with temporal/currentness semantics?
D12: What governed current-world projection is available to cognition for this role/perspective/task?
D13: What local cognitive state/hypothesis/gap/sufficiency/stop judgment is formed?
D14: What task/decision/action intent candidate is formed?
D15: Under global policy/safety constraints, may the proposed action proceed?
D16: What historical Memory/Experience is preserved/retrieved/revised with provenance?
No two questions are judged semantically identical. D07 intentionally contains two distinct authority decisions under one Authority Domain; they must not be collapsed into one decision.

### A2.0-84｜Boundary Challenge Results
**D03 vs D06:** lifecycle availability is not routing compatibility. KEEP SEPARATE.
**D04 vs D05:** observation need is not execution request. SPLIT REQUIRED and accepted.
**D05 vs D06:** request formation is not target resolution/binding. KEEP SEPARATE.
**D06 vs D07:** routing/binding is not permission. KEEP SEPARATE.
**D07 vs D08:** authorization is not resource availability. KEEP SEPARATE.
**D08 vs D09:** resource readiness is not execution effect. KEEP SEPARATE.
**D09 vs D10:** Organ output is not Evidence. KEEP SEPARATE.
**Context vs D10/D11:** Context remains explicit mapping/formation semantics but no independent truth/currentness Owner proven. DOWNCLASSIFY from Domain.
**D11 vs D12:** Field/world state is not Current World projection. KEEP SEPARATE.
**D12 vs D13:** Current World projection is governed information, not hypothesis/reasoning. KEEP SEPARATE.
**D13 vs D14:** local reality judgment is not task/decision intent. KEEP SEPARATE.
**D14 vs D15:** decision/action intent is not global action admission. KEEP SEPARATE.
**D16 Learning:** no premature Learning authority. Learning remains future candidate.
**Assurance:** cross-cutting evidence plane, not runtime semantic Owner.
**Deployment/Continuity:** cross-cutting preservation plane, not competing Owner.

### A2.0-85｜Gap Placement after Domain Reconciliation
CA-GAP-01 Controlled Execution Entry → D01 + D05 + D07. P0.
CA-GAP-02 Effect Contract Dependency Scope → D03 + D06 + D07. P0.
CA-GAP-03 Resource Preparation/Availability → D08 + D07 + D09. P1.
CA-GAP-04 Expiry/Temporal Validity → D07 plus temporal semantics of D11/D12 and P-D. P0.
CA-GAP-05 Live World Information Mapping → D10 → Context formation → D11 → D12. P0.
CA-GAP-06 Badge/MVP vs Midplatform → P-D plus D09–D15 reconciliation. P1.
CA-GAP-07 Restart/Process Currentness → P-D requirements applied to D03/D07/D11/D12/D15/D16 and other stateful Owners. P1.
IMPL-NC-01 remains blocked by CA-GAP-01/02.
ENG-GAP-01/02 remain Development Manual / Assurance concerns.

### A2.0-86｜Batch 02 Adjudication
- INPUT_DOMAIN_CANDIDATES=18
- RECONCILED_CORE_DOMAINS=16
- CROSS_CUTTING_PLANES=2
- STANDALONE_CONTEXT_DOMAIN=NO
- CONTEXT_SEMANTICS_PRESERVED=YES
- OBSERVATION_NEED_EXECUTION_REQUEST_SPLIT=YES
- ENTRY_ADMISSION_EFFECT_AUTHORIZATION_SAME_DOMAIN_DISTINCT_DECISIONS=YES
- LEARNING_DOMAIN_ADMITTED=NO
- ASSURANCE_RUNTIME_TRUTH_OWNER=NO
- DEPLOYMENT_RUNTIME_TRUTH_OWNER=NO
- OWNER_AUTHORITY_DUPLICATION_FOUND=NO
- ACCIDENTAL_IMPLEMENTATION_DOMAIN_FOUND_AND_REMOVED=YES
- MISSING_CORE_DOMAIN_CONFIRMED=NO
- CANONICAL_DOMAIN_SET_STATUS=CANDIDATE_RECONCILED
- CANONICAL_ARCHITECTURE_FROZEN=NO
- CODE_CHANGE_AUTHORIZED=NO
- PR_ADMISSION_02_RESUME=NO
- GROUNDING_DINO_RESUME=NO
Next: ACM-02 Batch 03 — Canonical Object / Fact / State Ledger. For D01–D16, identify canonical semantic objects and classify each as declaration, candidate, admitted fact, decision, current-state projection, historical record or effect result. Do not map to Python classes yet; implementation reconciliation follows semantic ledger stabilization.

## Batch 03–08 document locations

- [Object / Fact / State Ledger](canonical_object_fact_state_ledger_v0_1.md) — OC-01–OC-12, candidate/admission/state distinctions.
- [Owner / Authority Matrix](canonical_owner_authority_matrix_v0_1.md) — R-OWNER through R-AUDITOR; Q01–Q24.
- [Canonical Contract Ledger](canonical_contract_ledger_v0_1.md) — CC-01–CC-26.
- [Semantic Mapping Ledger](semantic_mapping_ledger_v0_1.md) — MAP-01–MAP-25 and 03.7 / 06.2 / 06.4 / 06.5 governance layering.
- [Temporal / Currentness Ledger](temporal_currentness_validity_ledger_v0_1.md) — T-01–T-14, TV-01–TV-16 and TM-01–TM-10.
- [Identity / Reference / Provenance Ledger](identity_reference_provenance_ledger_v0_1.md) — I-01–I-12, REF-01–REF-12, RI-01–RI-20, PV-01–PV-08 and lineage validity.

## Current architecture and implementation backlog

CA-GAP-01 Controlled Execution Entry / Governed Request Source — OPEN_NARROWED.  
CA-GAP-02 Effect Contract Dependency Scope — OPEN.  
CA-GAP-03 Resource Preparation / Allocation / Availability — OPEN.  
CA-GAP-04 Expiry / Temporal Validity Interpretation — RESOLVED_AT_CANONICAL_LEVEL; implementation audit NOT_STARTED.  
CA-GAP-05 Live World Information Semantic Mapping — OPEN.  
CA-GAP-06 Badge/MVP vs Midplatform Canonical Reconciliation — OPEN.  
CA-GAP-07 Restart / Process-Boundary Currentness — RESOLVED_AT_CANONICAL_LEVEL; implementation audit NOT_STARTED.  
IMPL-NC-01 Fabricated Routing/Compatibility Lineage in Controlled Runner — OPEN; target CC-06 / MAP-05; canonical class INVALID_SEMANTIC_LINEAGE + REFERENCE_ROLE_SUBSTITUTION (historical shorthand: SEMANTIC_DRIFT + FABRICATED_LINEAGE). No code remediation authorized.

The A2.0-85 section above preserves Batch 02 historical gap placement; it is not the latest status. [Batch 07 temporal/currentness adjudication](temporal_currentness_validity_ledger_v0_1.md) resolves CA-GAP-04 and CA-GAP-07 at the canonical level only. [Batch 08 identity/reference/provenance adjudication](identity_reference_provenance_ledger_v0_1.md) narrows CA-GAP-01 and refines IMPL-NC-01's classification without closing either. Five Canonical gaps remain open; IMPL-AUDIT-TEMPORAL-01 and IMPL-AUDIT-RESTART-01 are NOT_STARTED. A documented target does not prove runtime conformance. Current status follows [Notion A2.0-135–149](https://app.notion.com/p/3c3113b33a6d81dfa4efeac030352d96).
