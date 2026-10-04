# Architecture 2.0 — Canonical Contract Ledger v0.1

CANONICAL_CONTRACT_COUNT=26  
BATCH=ACM-02 05  
STATUS=DESIGN_IN_PROGRESS; CANONICAL_ARCHITECTURE_FROZEN=NO

Repository-side transcription of [Notion 03.7 Architecture 2.0](https://app.notion.com/p/3c3113b33a6d81dfa4efeac030352d96), A2.0-108–116, read 2026-09-30. This ledger records candidate Canonical Architecture semantics, not Python DTOs, production conformance, runtime authorization or gap closure. Frozen Constitution v1 remains in [its separate file](architecture_2_0_constitution_v1.md).

### A2.0-108｜ACM-02 Batch 05 — Canonical Contract Ledger
**STATUS:** CANONICAL_CONTRACT_LEDGER_CANDIDATE
**INPUT:** D01–D16; OC-01–OC-12; R-OWNER/R-AUTHORITY/R-WRITER/R-EXECUTOR/R-CUSTODIAN/R-PROJECTOR/R-MAPPER/R-READER/R-AUDITOR
**CONSTITUTION_BASE:** C01–C48 FROZEN
**DTO_SCHEMA_DESIGN:** NOT_STARTED
**IMPLEMENTATION_MAPPING:** NOT_STARTED
**CODE_CHANGE_AUTHORIZED:** NO
A Canonical Contract is architecture-significant when changing or bypassing it can change semantic meaning, identity/role legitimacy, Owner/Authority, admitted fact/state, currentness/temporal interpretation, or effect legitimacy. Function calls, serializers, caches and transports are not Canonical Contracts merely because code depends on them.
Each contract must define:
SOURCE_DOMAIN_AND_ROLE; TARGET_DOMAIN_AND_ROLE; PURPOSE; REQUIRED_INPUT_SEMANTICS; OUTPUT_OBJECT_CLASS; OWNER_OR_AUTHORITY; RELATION_TYPE; IDENTITY_BEHAVIOR; AUTHORITY_BEHAVIOR; PROVENANCE_BEHAVIOR; TEMPORAL_CURRENTNESS_REQUIREMENTS; FAILURE_UNKNOWN_BEHAVIOR; NEGATIVE_GUARANTEES.

### A2.0-109｜Formation & Execution Contracts
**CC-01 Observation Need Formation**
Source: D12/D13/D14 governed world/cognitive/task information.
Target: D04 Observation Need Owner.
Purpose: form an explicit observation need/gap without execution semantics.
Output: OC-02/OC-04 Observation Need according to formation lifecycle.
Relation: DERIVATION.
Authority: none for Organ execution.
Failure/unknown: inability to establish source basis leaves need unformed/unknown; no provider request may be inferred.
Negative: no provider/model/binding/authorization is created.
**CC-02 Cognitive Need → Execution Request Materialization**
Source: D04 legitimate Observation Need.
Target: D05 Execution Request Formation Owner.
Purpose: materialize a bounded executable request from cognitive need.
Required: source need identity, requester/source role, requested capability/observation semantics, purpose/scope, required provenance.
Output: governed D05 request candidate/fact.
Relation: REFINEMENT + MATERIALIZATION.
Authority: no D07 authority transfer.
Failure: missing source/role/provenance fails formation.
Negative: D05 may narrow execution semantics but may not rewrite/reconstruct D04 intent.
**CC-03 Legal Non-Cognitive Source → Execution Request Materialization**
Source: governed non-D04 source allowed by canonical policy, including controlled evaluation only when explicitly qualified.
Target: D05.
Purpose: legal execution request without fabricating Cognitive Need.
Required: governed source identity, requester/source relation, allowed request purpose/policy class, capability need/scope, provenance.
Output: governed D05 request.
Relation: MATERIALIZATION.
Authority: source does not self-authorize.
Failure: unknown/unqualified source fails request formation.
Negative: no fake D04 Observation Need; evaluation case/runner existence alone is insufficient.
This contract is the canonical home of the controlled-entry source problem.
**CC-04 Execution Entry Admission**
Source: governed D05 request + contract-required identity/purpose/policy dependencies.
Target: D07 Entry Admission Authority.
Purpose: decide whether the request may enter governed execution formation.
Output: OC-05 Entry Admission Decision plus current-state registration/query semantics where required.
Relation: ADMISSION.
Authority: D07 Entry Admission Authority.
Currentness: decision validity/invalidation must be explicit.
Failure/unknown: fail closed for entry-dependent formation/effects only.
Negative: Entry Admission is not Runtime Effect Authorization and cannot invoke Organ.
This contract closes the semantic target of CA-GAP-01 once its concrete basis is adjudicated.
**CC-05 Capability Resolution & Routing**
Source: admitted/legitimate D05 request + D02 declarations + D03 current lifecycle/availability.
Target: D06 Resolution/Binding Owner.
Purpose: resolve compatible capability/organ/model/provider/runtime target candidates.
Output: OC-03 candidates and/or bounded OC-05 compatibility/resolution judgments.
Relation: RESOLUTION.
Currentness: required D03 reads must be Owner-governed/current for the routing contract.
Failure: no compatible/current candidate → unresolved; no fallback fabrication.
Negative: resolution/routability is not D07 authorization.
**CC-06 Runtime Binding Formation**
Source: D06 resolution/routing result + authentic source lineage + target/runtime requirements.
Target: D06 Binding Owner.
Purpose: form governed association between request and execution target.
Output: OC-03/OC-04 binding object according to binding contract.
Relation: BINDING.
Failure: missing/incompatible lineage fails binding.
Negative: trace/request-shaped refs cannot substitute for routing/compatibility source semantics; binding is not authorization.
IMPL-NC-01 is evaluated against this contract.
**CC-07 Resource Preparation / Allocation**
Source: D05/D06 request-target scope plus allowed D07 entry state where required.
Target: D08 Resource Owner.
Purpose: prepare/allocate resources needed for a prospective effect.
Output: OC-03 preparation, OC-05 allocation decision, OC-06 availability state as distinct semantics.
Relation: MATERIALIZATION + domain decision.
Failure: preparation/allocation failure is explicit.
Negative: preparation/allocation does not prove effect-time availability or Organ authorization.
**CC-08 Runtime Effect Authorization**
Source: D05 governed request + D06 governed binding + contract-required current dependencies from D03/D08/D15/etc. + valid D07 entry basis where contract requires.
Target: D07 Runtime Effect Authorization Authority.
Purpose: decide whether a specific runtime effect may occur now.
Output: OC-05 Runtime Effect Authorization Decision/Grant + OC-06 current authorization semantics.
Relation: AUTHORIZATION.
Currentness: effect-time revalidation requirements are contract-specific; expiry/invalidations must be interpretable, not ref-only.
Failure/unknown: if a required dependency is unknown/not current, only the dependent effect is unauthorized.
Negative: no universal dependency list is assumed; no requester/router/provider self-authorization.
This contract is the canonical home of CA-GAP-02 and CA-GAP-04.
**CC-09 Authorized Organ Invocation**
Source: D07 current effect authorization + D06 binding + D08 required readiness + D02/D03 runtime identity/currentness required by the effect contract.
Target: D09 Organ Executor.
Purpose: perform exactly the authorized Organ/native effect.
Output: OC-08 Native/Normalized Organ Runtime Result.
Relation: authorized EFFECT.
Failure: no current required authorization/readiness → no invocation; invocation failure/empty result remains explicit OC-08 state.
Negative: executor cannot expand effect scope, mint authority, or declare Evidence/world truth.
CA-GAP-03 is resolved through CC-07/08/09 boundaries.

### A2.0-110｜Observation & World Information Contracts
**CC-10 Organ Result → Observation Candidate Mapping**
Source: D09 OC-08 result.
Target: D10 Observation/Evidence formation boundary.
Purpose: normalize bounded Organ semantics into canonical observation candidate semantics.
Output: OC-03 Observation Candidate/Envelope.
Relation: OBSERVATION_MAPPING.
Identity: execution/model/provider refs linked, not reinterpreted as Evidence authority.
Provenance: preserved/extended.
Failure/empty: provider-specific failure/empty semantics terminate at governed integration boundary and map honestly.
Negative: native confidence does not become epistemic confidence; zero result does not automatically become negative world fact.
**CC-11 Evidence Admission**
Source: D10 observation candidate + required provenance/schema/semantic basis.
Target: D10 Evidence Admission Authority.
Purpose: decide what is admitted as governed Evidence.
Output: OC-05 admission decision + OC-04 Admitted Evidence.
Relation: ADMISSION.
Failure: invalid/unknown admission basis rejects/fails closed for Evidence admission.
Negative: admitted Evidence is scoped Evidence, not Field/Current World/world truth.
**CC-12 Evidence → Context Formation**
Source: D10 admitted Evidence plus explicit role/task/situational source where required.
Target: Context formation layer under target World Information contract.
Purpose: form bounded situational framing without rewriting source Evidence.
Output: OC-03/OC-07 Context formation/projection.
Relation: PROJECTION / DERIVATION.
Authority: no independent Context truth authority.
Failure: missing required frame remains absent/unknown; cannot invent.
Negative: Context does not mutate Evidence or itself admit Field fact.
**CC-13 Context/Evidence → Field Event Materialization**
Source: D10 admitted Evidence + legitimate Context/source/field/time basis.
Target: D11 Field Event formation.
Purpose: materialize a Field Event candidate with explicit semantic and temporal basis.
Output: OC-03 Field Event Candidate.
Relation: ASSIMILATION + MATERIALIZATION.
Temporal: observed/occurred/effective/received roles must be explicitly bound where used.
Failure: missing authoritative field/time/source basis blocks candidate formation or preserves unknown per contract.
Negative: field_ref/context_ref/timestamp string presence is not semantic proof.
This is the first half of CA-GAP-05.
**CC-14 Field Event Admission**
Source: D11 Field Event Candidate.
Target: D11 Field Event Admission Authority.
Purpose: admit candidate into Field event history/state semantics.
Output: OC-05 admission decision + OC-04 Admitted Field Event.
Relation: ADMISSION.
Failure: invalid candidate does not mutate Field.
Negative: admission does not make event immutable universal truth.
**CC-15 Field State Reduction / Currentness**
Source: D11 admitted events + prior legitimate Field state/history.
Target: D11 Field Information Owner.
Purpose: derive/register current Field state under explicit reduction, supersession, invalidation and temporal rules.
Output: OC-03 state candidate → OC-06 Field Current State; OC-09 history.
Relation: ASSIMILATION + DERIVATION + INVALIDATION/SUPERSESSION.
Currentness: Owner-governed; recency alone insufficient.
Failure/unknown: unresolved conflict/temporal uncertainty must remain represented, not silently discarded.
Negative: reducer implementation is not Owner merely by computing state.
**CC-16 Field/World Information → Current World Projection**
Source: D11 current Field state + relevant D10 Evidence/Context/provenance + role/perspective/task scope.
Target: D12 Current World Formation Owner.
Purpose: form cognition-facing current-world projection.
Output: OC-07 Current World Projection plus OC-05/06 currentness judgment where contract requires.
Relation: PROJECTION + DERIVATION.
Failure/unknown: uncertainty/source gaps survive projection.
Negative: D12 does not rewrite D11; Current World is not external absolute truth.
CC-12–16 together are the canonical target of CA-GAP-05.

### A2.0-111｜Cognition, Action & Memory Contracts
**CC-17 Current World → Cognitive State Formation**
Source: D12 governed Current World + permitted D10/D11 supporting projections + D16 memory/experience projections where explicitly requested.
Target: D13 Local Cognitive Reasoning Owner.
Purpose: form attention/hypothesis/gap/contradiction/sufficiency/stop state.
Output: OC-10 Derived Cognitive State.
Relation: DERIVATION.
Failure/unknown: insufficient/contradictory information remains cognitive state and may cause D04 re-observation need.
Negative: source world facts are not rewritten by hypothesis; cognitive confidence is not provider confidence.
**CC-18 Cognitive Re-observation Loop**
Source: D13 gap/insufficiency judgment.
Target: D04 Observation Need.
Purpose: form new/revised observation need with explicit causal link to the cognitive gap.
Output: OC-02/04 Observation Need.
Relation: DERIVATION.
Negative: loop does not bypass D05/D07 for actual Organ execution.
**CC-19 Cognitive State → Task/Decision/Action Intent Formation**
Source: D13 cognitive state + D14 task state + applicable D15 global constraints as input facts.
Target: D14 Task/Decision Owner.
Purpose: form task transition/decision/action-intent candidate.
Output: OC-03/OC-06 according to object lifecycle.
Relation: DERIVATION.
Negative: action intent is not action admission/effect authority.
**CC-20 Action Admission**
Source: D14 action intent + D15 current global policy/safety + other contract-required facts.
Target: D15 Action Admission Authority.
Purpose: decide whether proposed action may proceed within policy/safety scope.
Output: OC-05 Action Admission Decision / admitted working envelope where applicable.
Relation: ADMISSION/AUTHORIZATION for action-control scope.
Failure/unknown: required unknown safety/policy blocks only dependent action effect.
Negative: action admission does not rewrite D13/D12 facts and does not prove action occurred.
**CC-21 Memory Assimilation / Revision**
Source: governed D10–D15 facts/projections/results explicitly eligible for memory + prior D16 history.
Target: D16 Memory/Experience Owner.
Purpose: preserve/revise memory/experience with provenance and supersession semantics.
Output: OC-03 assimilation candidate → OC-04/09 memory/history record after admission.
Relation: ASSIMILATION + INVALIDATION/SUPERSESSION.
Failure: unsupported source cannot become canonical memory fact.
Negative: memory assimilation does not mutate source domain facts.
**CC-22 Memory Retrieval Projection**
Source: D16 canonical memory/experience history.
Target: D10–D14 consumer under explicit query/context.
Purpose: provide bounded historical projection.
Output: OC-07 retrieval projection.
Relation: PROJECTION.
Negative: retrieved history is not D12 current world or D11 current Field state.

### A2.0-112｜Cross-Cutting Contracts
**CC-23 Controlled Evaluation Execution Contract**
Plane: P-A interacting with D05/D07 and ordinary runtime domains.
Purpose: permit controlled evaluation to use legal execution semantics without creating parallel authority/runtime truth.
Required: governed evaluation source identity/purpose, CC-03 request materialization, ordinary D07 admission/authorization, ordinary D06/D08/D09 execution contracts.
Output: runtime objects remain ordinary domain objects; evaluation artifacts are OC-12.
Negative: evaluation PASS cannot promote D03 lifecycle, mint D07 authority, bypass D10 admission, or redefine Architecture Truth.
**CC-24 Owner Currentness Query Contract**
Cross-domain pattern.
Purpose: let dependent domains consume authoritative current-state answers without copying ownership.
Required: owner identity/scope, subject identity, state version/basis, invalidation semantics, temporal interpretation where relevant.
Output: OC-07 projection/query result backed by OC-06 Owner state.
Failure: unknown/not-current remains explicit.
Negative: caller cache/last record/timestamp cannot substitute for Owner currentness.
This supports CA-GAP-02/04/07.
**CC-25 Restart / Reconciliation Contract**
Plane: P-D applied to every stateful Owner.
Purpose: re-establish valid current-state semantics after restart/process loss/disconnection/reconnection.
Required: authoritative history/current-state basis, invalidation/version semantics, conflict policy, domain Owner participation.
Output: domain-specific reconciliation candidate/decision/state, never a global replacement truth.
Failure: unresolved state remains unknown/not-current for dependent effects.
Negative: P-D cannot become global currentness Owner.
This is the canonical target of CA-GAP-07.
**CC-26 Remote / Composed Organ Execution Contract**
Plane: P-D across D05–D10.
Purpose: preserve request, identity, authorization, execution-result, provenance and Evidence semantics when transport/topology changes.
Required: same canonical semantic identities/roles/contracts as local path; transport declaration is implementation/deployment detail.
Output: no new semantic class merely because execution is remote/Hive/composed.
Failure: transport failure remains execution/communication failure and cannot fabricate semantic success.
Negative: Bluetooth/Wi-Fi/LAN/RPC/process boundary does not transfer Owner/Authority or change capability meaning.

### A2.0-113｜Contract Dependency Spine
Primary observation/cognition spine:
D12/D13/D14 → CC-01 → D04 → CC-02 → D05
or governed non-cognitive source → CC-03 → D05
D05 → CC-04 → D07 Entry Admission
D05 + D02/D03 → CC-05 → D06 → CC-06 → Binding
D05/D06 → CC-07 → D08
D05/D06/D03/D08/(D15 as required) → CC-08 → D07 Runtime Authorization
D07 + D06 + D08 → CC-09 → D09
D09 → CC-10 → D10 Candidate → CC-11 → Evidence
Evidence → CC-12 → Context → CC-13 → D11 Event Candidate → CC-14 → Admitted Event
D11 → CC-15 → Field Current State → CC-16 → D12 Current World
D12 → CC-17 → D13
D13 gap → CC-18 → D04
D13 → CC-19 → D14 → CC-20 → D15 action admission
governed eligible information → CC-21 → D16; D16 → CC-22 → consumers.
This is a semantic dependency spine, not a mandatory synchronous pipeline. Contracts may be invoked asynchronously, locally/remotely, or skipped when the target semantic object is not required, but no skipped contract may have its semantic effect silently assumed.

### A2.0-114｜Gap Closure Readiness after Contract Ledger
**CA-GAP-01:** canonical location identified: CC-03 + CC-04. Still OPEN because concrete governed controlled source identity/object and Entry Admission basis/currentness schema are not yet adjudicated.
**CA-GAP-02:** canonical location identified: CC-08 + CC-24. Still OPEN because effect-specific dependency sets are not yet enumerated.
**CA-GAP-03:** canonical location identified: CC-07/08/09. Still OPEN because resource availability/readiness semantics are not yet fully specified.
**CA-GAP-04:** canonical location identified: CC-08/13/15/16/24/25. Still OPEN because temporal role/expiry semantics require dedicated ledger.
**CA-GAP-05:** canonical location identified: CC-10–16. Still OPEN because exact semantic mappings and admission bases require Mapping Ledger.
**CA-GAP-06:** canonical location: P-D + CC-26 and implementation reconciliation. OPEN.
**CA-GAP-07:** canonical location: CC-24/25. OPEN.
**IMPL-NC-01:** contract violation target identified as CC-06 plus D01 role/provenance requirements. No remediation authorized.
No gap is marked CLOSED merely because its target contract now exists conceptually.

### A2.0-115｜Contract Negative Guarantees
NG-01 No contract output inherits source Authority unless the target contract explicitly issues a new Authority decision.
NG-02 No currentness is inferred from recency, presence, cache, version string or successful prior use.
NG-03 No candidate becomes admitted fact through serialization/storage/routing alone.
NG-04 No effect result becomes Evidence through adapter naming alone.
NG-05 No Evidence becomes Field/Current World through field-copy alone.
NG-06 No projection mutates its source domain.
NG-07 No evaluation/deployment plane creates a shadow runtime Owner.
NG-08 No controlled path fabricates Cognitive Need or production routing provenance.
NG-09 No remote/composed path weakens local semantic/authority contracts.
NG-10 No unknown required dependency is silently converted to affirmative state.
NG-11 No failure/empty/absence semantics are promoted beyond their admitted semantic scope.
NG-12 No contract is considered satisfied merely because a current Python object has matching fields.

### A2.0-116｜Batch 05 Adjudication
- CANONICAL_CONTRACT_CANDIDATES=26
- CORE_FORMATION_EXECUTION_CONTRACTS=9
- OBSERVATION_WORLD_CONTRACTS=7
- COGNITION_ACTION_MEMORY_CONTRACTS=6
- CROSS_CUTTING_CONTRACTS=4
- PRIMARY_SEMANTIC_SPINE_DEFINED=YES
- MANDATORY_SYNCHRONOUS_PIPELINE_DEFINED=NO
- CONTRACT_NEGATIVE_GUARANTEES=12
- CA_GAPS_CLOSED=0
- CA_GAPS_LOCATED=7/7
- IMPLEMENTATION_NONCONFORMANCE_LOCATED=YES
- DTO_SCHEMAS_AUTHORIZED=NO
- IMPLEMENTATION_MAPPING_STARTED=NO
- CANONICAL_CONTRACT_LEDGER_STATUS=CANDIDATE
- CODE_CHANGE_AUTHORIZED=NO
- PR_ADMISSION_02_RESUME=NO
- GROUNDING_DINO_RESUME=NO
Next: ACM-02 Batch 06 — Semantic Mapping Ledger. Apply the relation taxonomy to every architecture-significant cross-domain edge, explicitly declaring identity/information/authority/provenance/temporal/currentness behavior. Reconcile Census X01–X18 against the target mapping ledger, but do not change implementation yet.

## Source and status guard

Source: [Notion 03.7 Architecture 2.0](https://app.notion.com/p/3c3113b33a6d81dfa4efeac030352d96), A2.0-108–116. Historical Batch status is preserved above. For current gap status see [Batch 07 temporal/currentness ledger](temporal_currentness_validity_ledger_v0_1.md): CA-GAP-04 and CA-GAP-07 are RESOLVED_AT_CANONICAL_LEVEL only; five Canonical gaps and IMPL-NC-01 remain OPEN; both implementation audits are NOT_STARTED. For CC-06 / MAP-05, [Batch 08 identity/reference/provenance adjudication](identity_reference_provenance_ledger_v0_1.md) supplies the current IMPL-NC-01 semantic-lineage classification; the source sections above remain historical Batch 05 wording. No code remediation, PR-ADMISSION-02 resumption or Grounding DINO implementation is authorized.
