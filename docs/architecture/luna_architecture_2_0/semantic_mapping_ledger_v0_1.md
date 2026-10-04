# Architecture 2.0 — Semantic Mapping Ledger v0.1

SEMANTIC_MAPPING_COUNT=25  
BATCH=ACM-02 06  
STATUS=DESIGN_IN_PROGRESS; CANONICAL_ARCHITECTURE_FROZEN=NO

Repository-side transcription of [Notion 03.7 Architecture 2.0](https://app.notion.com/p/3c3113b33a6d81dfa4efeac030352d96), A2.0-117–126, read 2026-09-30. This ledger records candidate Canonical Architecture semantics, not Python DTOs, production conformance, runtime authorization or gap closure. Frozen Constitution v1 remains in [its separate file](architecture_2_0_constitution_v1.md).

### A2.0-117｜ACM-02 Batch 06 — Semantic Mapping Ledger + Protocol Governance Reconciliation
**STATUS:** SEMANTIC_MAPPING_LEDGER_CANDIDATE
**INPUT:** D01–D16; CC-01–CC-26; relation taxonomy; prior Census X01–X18; existing 06.2/06.4 protocol/interface governance
**CONSTITUTION_BASE:** C01–C48 FROZEN
**CODE_CHANGE_AUTHORIZED:** NO

### A2.0-118｜Architecture vs Protocol Governance — Non-Duplication Adjudication
Architecture 2.0 MUST NOT create a second protocol-management system.
Three levels are distinguished:
**L2/L3 Canonical Architecture (03.7)**
Answers:
- What semantic domains/objects exist?
- What authoritative question does each Owner answer?
- What cross-domain semantic relation exists?
- What identity/information/authority/provenance/temporal/currentness behavior is allowed?
- Which semantic boundary must exist regardless of implementation?
Artifacts: Domain Ledger, Object Ledger, Owner/Authority Matrix, Canonical Contract Ledger, Semantic Mapping Ledger.
These are architecture truth/specification, not protocol-version operations.
**Engineering Integration Rules (06.2)**
Answers:
- How must an implementation realize a canonical boundary?
- What implementation-level contract shape/adapter/provider/harness rules apply?
- What bounded technical behavior is required for integration/conformance?
**Interface Evolution Governance (06.4)**
Answers:
- How are interface/protocol changes proposed, classified, reviewed, versioned, frozen, migrated and verified?
- What compatibility/freeze/impact rules govern evolution?
Existing ES-03..ES-08 and EA principles remain governance mechanisms; Architecture 2.0 does not replace them.
**Experiment / Failure Evidence (06.5)**
Answers:
- What happened in an experiment/runtime/audit?
- What failed, under what baseline, and what evidence supports a proposed architecture/engineering change?
Canonical flow:
03.7 ARCHITECTURE MEANING
→ 06.2 IMPLEMENTATION REALIZATION RULES
→ 06.4 CHANGE / VERSION / FREEZE GOVERNANCE
→ implementation
→ 06.5 EVIDENCE
→ governed feedback to 03.7 / 06.2 / 06.4.
Non-duplication rule:
03.7 does NOT manage protocol versions, provider adapters, freeze mechanics or test commands.
06.2/06.4 do NOT redefine canonical semantic meaning, Owner/Authority or cross-domain mapping behavior.
A protocol may implement one or more Canonical Contracts/Mappings; a Canonical Contract is not automatically a wire/API protocol.

### A2.0-119｜Semantic Mapping Record Schema
Every architecture-significant cross-domain mapping must declare:
MAP_ID
SOURCE_DOMAIN
SOURCE_OBJECT_CLASS/ROLE
TARGET_DOMAIN
TARGET_OBJECT_CLASS/ROLE
RELATION_TYPE
MAPPING_OWNER/ACCOUNTABILITY
IDENTITY_BEHAVIOR = PRESERVE \| LINK \| NEW \| REDUCE \| NOT_APPLICABLE
INFORMATION_BEHAVIOR = PRESERVE \| REDUCE \| DERIVE \| REINTERPRET_WITH_BASIS
AUTHORITY_BEHAVIOR = NOT_TRANSFERRED \| NEW_DECISION_REQUIRED \| PRESERVED_ONLY_BY_EXPLICIT_CONTRACT
PROVENANCE_BEHAVIOR = PRESERVE \| EXTEND \| DERIVE_WITH_SOURCE_LINK
TEMPORAL_BEHAVIOR = PRESERVE \| REBIND_WITH_BASIS \| DERIVE \| NOT_APPLICABLE
CURRENTNESS_BEHAVIOR = SOURCE_CURRENTNESS_REQUIRED \| TARGET_OWNER_DECIDES \| NOT_TRANSFERRED \| NOT_APPLICABLE
UNKNOWN_FAILURE_BEHAVIOR
NEGATIVE_GUARANTEES
IMPLEMENTING_CANONICAL_CONTRACTS.
Default rules:
AUTHORITY_BEHAVIOR defaults to NOT_TRANSFERRED.
CURRENTNESS defaults to NOT_TRANSFERRED.
IDENTITY is never PRESERVE merely because IDs/fields are copied.
REINTERPRET requires explicit semantic basis.
No mapping may silently upgrade OC class.

### A2.0-120｜Execution-Side Semantic Mappings
**MAP-01 D04 Observation Need → D05 Execution Request**
Contracts: CC-02.
Relation: REFINEMENT + MATERIALIZATION.
Identity: NEW target request identity linked to source need identity.
Information: REDUCE/REFINE to executable scope.
Authority: NOT_TRANSFERRED.
Provenance: EXTEND with source need/requester relation.
Temporal: preserve need timing where relevant; request validity separately governed.
Currentness: source need validity may be required; target request legitimacy owned by D05.
Unknown: missing source role/basis blocks materialization.
Negative: request is not the need; requester is not request_id.
**MAP-02 Governed Non-Cognitive Source → D05 Execution Request**
Contracts: CC-03/CC-23.
Relation: MATERIALIZATION.
Identity: NEW request identity linked to governed source identity.
Information: DERIVE bounded execution semantics from allowed source/purpose.
Authority: NOT_TRANSFERRED.
Provenance: PRESERVE+EXTEND.
Temporal/currentness: source qualification/currentness per source policy; D05 owns request semantics.
Unknown: unqualified source blocks request.
Negative: no fabricated D04 Cognitive Need; controlled fixture/runner is not automatically source authority.
**MAP-03 D05 Request → D07 Entry Admission Decision**
Contract: CC-04.
Relation: ADMISSION.
Identity: request identity LINKED, decision identity NEW.
Information: decision DERIVED from request + policy basis.
Authority: NEW_DECISION_REQUIRED by D07.
Provenance: EXTEND with decision basis.
Temporal/currentness: decision validity/invalidation owned D07.
Unknown: fail closed for entry-dependent formation.
Negative: request does not carry admission authority.
**MAP-04 D05/D02/D03 → D06 Resolution**
Contract: CC-05.
Relation: RESOLUTION.
Identity: request and declared asset identities LINKED; resolution identity NEW where materialized.
Information: DERIVE compatibility/selection.
Authority: no runtime authority transfer; D06 may issue only bounded compatibility/resolution judgment.
Provenance: EXTEND all source refs.
Currentness: D03 source currentness REQUIRED where contract says.
Unknown: unresolved, never fabricate candidate.
Negative: declared compatibility != dynamic resolution; resolution != authorization.
**MAP-05 D06 Resolution → D06 Binding**
Contract: CC-06.
Relation: BINDING.
Identity: source identities LINKED; binding identity NEW.
Information: DERIVE association.
Authority: NOT_TRANSFERRED.
Provenance: PRESERVE+EXTEND authentic routing/compatibility lineage.
Currentness: binding validity owned D06.
Unknown: missing lineage blocks binding.
Negative: request/trace refs cannot impersonate routing/compatibility refs.
**MAP-06 D05/D06 → D08 Resource Preparation**
Contract: CC-07.
Relation: MATERIALIZATION.
Identity: execution/request/binding identities LINKED; resource preparation/allocation identity NEW.
Information: DERIVE resource requirements.
Authority: NOT_TRANSFERRED; D08 resource decision separate.
Provenance: EXTEND.
Currentness: D08 owns resource availability.
Unknown: explicit unavailable/unknown.
Negative: prepared != allocated != currently available.
**MAP-07 D03/D05/D06/D08/(D15) → D07 Runtime Effect Authorization**
Contracts: CC-08/CC-24.
Relation: AUTHORIZATION.
Identity: dependency identities LINKED; authorization decision identity NEW.
Information: DERIVE effect-specific decision.
Authority: NEW_DECISION_REQUIRED by D07.
Provenance: EXTEND complete required basis.
Temporal: expiry/validity interpreted under D07 contract.
Currentness: required dependency Owner queries; not copied.
Unknown: required unknown blocks only dependent effect.
Negative: no generic authorized flag may substitute for dependency-specific decision.
**MAP-08 D07/D06/D08 → D09 Organ Invocation**
Contract: CC-09.
Relation: AUTHORIZED EFFECT MATERIALIZATION.
Identity: execution/invocation identity NEW, linked to authorization/binding/resource basis.
Information: REDUCE authorization scope to exact executable effect.
Authority: authorization PRESERVED ONLY as explicit effect basis; executor receives no authority to expand/reissue.
Provenance: EXTEND.
Temporal/currentness: effect-time checks as contract requires.
Unknown: no effect when required basis unknown/not-current.
Negative: executor/provider cannot self-authorize.

### A2.0-121｜Observation / World Semantic Mappings
**MAP-09 D09 Organ Result → D10 Observation Candidate**
Contract: CC-10.
Relation: OBSERVATION_MAPPING.
Identity: observation identity NEW; execution/model/provider identities LINKED.
Information: REINTERPRET_WITH_BASIS from provider/native semantics into canonical observation semantics.
Authority: NOT_TRANSFERRED.
Provenance: PRESERVE+EXTEND.
Temporal: observation/source timestamps preserved by role, not collapsed.
Currentness: NOT_TRANSFERRED.
Unknown/failure: native failure/empty preserved honestly.
Negative: native confidence != epistemic confidence; effect success != Evidence admission.
**MAP-10 D10 Observation Candidate → D10 Admitted Evidence**
Contract: CC-11.
Relation: ADMISSION.
Identity: candidate/evidence relation explicit; admitted Evidence identity per contract.
Information: admitted semantic scope explicitly declared.
Authority: NEW_DECISION_REQUIRED by Evidence Admission Authority.
Provenance: PRESERVE+EXTEND.
Temporal: source observation temporal roles preserved.
Currentness: Evidence validity governed in Evidence scope, not world currentness.
Unknown: invalid basis rejects admission.
Negative: Evidence != Field fact/Current World.
**MAP-11 D10 Evidence → Context Formation**
Contract: CC-12.
Relation: PROJECTION + DERIVATION.
Identity: source Evidence identity LINKED; Context formation identity NEW if materialized.
Information: REINTERPRET_WITH_BASIS using role/task/situation; source Evidence remains unchanged.
Authority: NOT_TRANSFERRED.
Provenance: PRESERVE+EXTEND.
Temporal: preserve source temporal semantics; context may add bounded scope.
Currentness: target consumer contract decides required context validity.
Unknown: missing context remains unknown.
Negative: no Context truth authority.
**MAP-12 D10/Context → D11 Field Event Candidate**
Contract: CC-13.
Relation: ASSIMILATION + MATERIALIZATION.
Identity: Field Event identity NEW; Evidence/Context identities LINKED.
Information: DERIVE event semantics from admitted source + field/time basis.
Authority: NOT_TRANSFERRED.
Provenance: PRESERVE+EXTEND.
Temporal: explicit observed/occurred/effective/received role mapping.
Currentness: not inherited; Field admission/state Owner decides.
Unknown: temporal/source ambiguity survives or blocks per contract.
Negative: timestamp/ref presence does not prove temporal role or field membership.
**MAP-13 D11 Field Event Candidate → Admitted Field Event**
Contract: CC-14.
Relation: ADMISSION.
Identity: candidate/admitted event relation explicit.
Information: admitted within Field scope.
Authority: NEW_DECISION_REQUIRED by Field Event Admission Authority.
Provenance: PRESERVE+EXTEND.
Temporal: candidate temporal semantics validated/preserved.
Currentness: admission != current Field state.
Unknown: reject/no mutation.
Negative: admission != immutable universal truth.
**MAP-14 Admitted Field Events + Prior Field State → D11 Field Current State**
Contract: CC-15.
Relation: ASSIMILATION + DERIVATION + INVALIDATION/SUPERSESSION.
Identity: event identities LINKED; state identity/version NEW or revised per contract.
Information: DERIVE current Field state.
Authority: no cross-domain authority transfer; D11 Owner owns state transition/currentness semantics.
Provenance: EXTEND full contributing event/state lineage.
Temporal: effective/validity/supersession rules applied.
Currentness: TARGET_OWNER_DECIDES.
Unknown/conflict: represented, not discarded.
Negative: latest event != current state by recency alone.
**MAP-15 D11/D10/Context → D12 Current World**
Contract: CC-16.
Relation: PROJECTION + DERIVATION.
Identity: Current World projection identity NEW; sources LINKED.
Information: REDUCE/DERIVE for role/perspective/task/current scope.
Authority: NOT_TRANSFERRED.
Provenance: PRESERVE+EXTEND.
Temporal: source validity preserved; projection currentness separately judged.
Currentness: TARGET_OWNER_DECIDES.
Unknown: gaps/conflicts survive.
Negative: Current World != Field source truth; projection cannot mutate Field.

### A2.0-122｜Cognition / Action / Memory Semantic Mappings
**MAP-16 D12 → D13 Cognitive State**
Contract: CC-17.
Relation: DERIVATION.
Identity: cognitive state identity NEW; Current World/source refs LINKED.
Information: DERIVE hypothesis/attention/gap/sufficiency.
Authority: world-source authority NOT_TRANSFERRED; bounded cognitive decision semantics arise only in D13.
Provenance: EXTEND.
Temporal: cognition may reason over temporal scope but cannot rewrite source time.
Currentness: D13 state currentness separate.
Unknown: uncertainty remains reasoning input/state.
Negative: hypothesis != world fact.
**MAP-17 D13 Gap/Insufficiency → D04 Observation Need**
Contract: CC-18.
Relation: DERIVATION.
Identity: new/revised need identity linked to cognitive gap.
Information: DERIVE requested observation purpose.
Authority: NOT_TRANSFERRED.
Provenance: EXTEND causal link.
Temporal: need timing/scope explicit.
Currentness: D04 owns need validity.
Negative: gap does not directly invoke Organ.
**MAP-18 D13/D14/(D15 constraints) → D14 Action Intent**
Contract: CC-19.
Relation: DERIVATION.
Identity: decision/action-intent identity NEW.
Information: DERIVE.
Authority: D15 action authority NOT_TRANSFERRED; D14 task authority only within its own scope.
Provenance: EXTEND.
Temporal/currentness: required source states explicitly read.
Unknown: unresolved inputs may yield no intent/hold/reconsider according to task contract.
Negative: intent != admission/effect authorization.
**MAP-19 D14 + D15 Policy/Safety → D15 Action Admission**
Contract: CC-20.
Relation: ADMISSION/AUTHORIZATION for action-control scope.
Identity: admission decision identity NEW; action intent linked.
Information: DERIVE policy/safety decision.
Authority: NEW_DECISION_REQUIRED by D15.
Provenance: EXTEND.
Currentness: policy/safety dependencies Owner-governed.
Unknown: required unknown blocks dependent action.
Negative: admission does not prove action effect or rewrite cognition.
**MAP-20 D10–D15 Eligible Information → D16 Memory Assimilation**
Contract: CC-21.
Relation: ASSIMILATION.
Identity: memory/history identity NEW or linked under memory contract.
Information: REDUCE/PRESERVE/DERIVE only as explicitly declared.
Authority: source authority NOT_TRANSFERRED; D16 assimilation/revision authority separate.
Provenance: PRESERVE+EXTEND.
Temporal: historical/source time preserved; memory time separately recorded.
Currentness: source currentness not automatically retained as memory currentness.
Unknown: unsupported source rejected/preserved as uncertain.
Negative: memory write cannot mutate source.
**MAP-21 D16 Memory → D10–D14 Retrieval Projection**
Contract: CC-22.
Relation: PROJECTION.
Identity: source memory identity LINKED; retrieval projection identity NEW if materialized.
Information: REDUCE according to query/context.
Authority: NOT_TRANSFERRED.
Provenance: PRESERVE.
Temporal: historical temporal scope preserved.
Currentness: NOT_TRANSFERRED; consumer decides applicability.
Negative: retrieved memory != Current World.

### A2.0-123｜Deployment / Assurance Mapping Rules
**MAP-22 P-A Controlled Evaluation Source → D05**
Contracts: CC-03/CC-23.
Relation: MATERIALIZATION.
Identity: governed evaluation source linked; D05 request identity new.
Authority: NOT_TRANSFERRED.
Provenance: evaluation purpose preserved.
Negative: evaluation status/PASS cannot become runtime authority or lifecycle state.
**MAP-23 Owner OC-06 Current State → Dependent Domain Query**
Contract: CC-24.
Relation: PROJECTION.
Identity: subject/Owner identity preserved/linked.
Information: REDUCE to required currentness answer.
Authority: NOT_TRANSFERRED.
Provenance: Owner/state version basis preserved.
Temporal/currentness: source Owner decides; caller does not infer.
Negative: cache/latest record cannot replace Owner query semantics.
**MAP-24 Historical/Recovered State → Owner Reconciliation**
Contract: CC-25.
Relation: RECONCILIATION = DERIVATION + domain-specific ADMISSION/DECISION.
Identity: preserve/link canonical subject identities.
Information: derive candidate restored state; never silent overwrite.
Authority: NEW_DECISION_REQUIRED where domain Owner requires.
Provenance: preserve recovery/restart lineage.
Currentness: TARGET_OWNER_DECIDES.
Unknown/conflict: unresolved remains not-current/unknown.
Negative: P-D is not global currentness Owner.
**MAP-25 Local ↔ Remote/Composed Execution Representation**
Contract: CC-26.
Relation: REPRESENTATION/TRANSPORT projection; no new semantic authority relation.
Identity: canonical semantic identities preserved or explicitly linked across representation.
Information: preserve canonical semantics; encoding may change.
Authority: NOT_TRANSFERRED/NOT_EXPANDED.
Provenance: preserve/extend transport trace without substituting semantic lineage.
Temporal: transport delay does not silently redefine observation/effect time.
Currentness: governed by original domain contracts.
Negative: topology/transport cannot create a new Owner/Authority.

### A2.0-124｜Census X01–X18 Reconciliation Rule
The historical Census X01–X18 remain implementation-discovered mapping evidence, not target architecture truth.
Reconciliation method for each X mapping in the next implementation-reconciliation pass:
1. Identify target MAP-01–MAP-25 or mark NO_CANONICAL_TARGET.
2. Verify source/target domain and object class.
3. Verify identity behavior.
4. Verify information behavior.
5. Verify authority behavior.
6. Verify provenance behavior.
7. Verify temporal/currentness behavior.
8. Classify:
	CONFORMS
	PARTIAL
	SEMANTIC_DRIFT
	IMPLICIT_MAPPING
	RESPONSIBILITY_LEAK
	LEGACY_NO_TARGET
	TARGET_NOT_IMPLEMENTED.
9. Any implementation fix remains unauthorized until the relevant target mapping/contract is adjudicated stable enough.
Known prior issue IMPL-NC-01 is provisionally:
TARGET=MAP-05 / CC-06
EXPECTED_CLASS=SEMANTIC_DRIFT + FABRICATED_LINEAGE
because FPO request_id/control trace were used where routing/compatibility lineage semantics were required.
No code remediation is authorized by this classification.

### A2.0-125｜Mapping vs Protocol Governance Decision
A **Semantic Mapping** is canonical architecture when changing it changes meaning across domains.
A **Protocol/Interface** is an implementation realization when it transports/serializes/invokes that meaning.
A **Protocol Evolution Rule** governs how the realization changes over time.
Therefore:
- MAP-xx and CC-xx live in 03.7 Architecture 2.0.
- Concrete DTO/API/provider/adapter/harness realization rules live in 06.2.
- Version/freeze/compatibility/change-impact rules live in 06.4.
- Failures/experiments/audit evidence live in 06.5.
- 06.1 continues factual model/version records.
No new Protocol Manager, Mapping Manager, Architecture Registry or second freeze system is authorized.
When a concrete interface change touches a MAP/CC semantic boundary, governance flow is:
03.7 semantic impact check
→ 06.2 implementation-rule impact
→ 06.4 interface-evolution classification/freeze process
→ implementation/verification
→ 06.5 evidence
→ feedback.

### A2.0-126｜Batch 06 Adjudication
- TARGET_SEMANTIC_MAPPINGS=25
- EXECUTION_SIDE_MAPPINGS=8
- OBSERVATION_WORLD_MAPPINGS=7
- COGNITION_ACTION_MEMORY_MAPPINGS=6
- ASSURANCE_DEPLOYMENT_MAPPINGS=4
- AUTHORITY_DEFAULT_TRANSFER=NO
- CURRENTNESS_DEFAULT_TRANSFER=NO
- IMPLICIT_FIELD_COPY_ACCEPTED=NO
- PROTOCOL_GOVERNANCE_DUPLICATION_CREATED=NO
- 03_7_CANONICAL_MEANING_OWNER=YES
- 06_2_IMPLEMENTATION_REALIZATION_RULES_RETAINED=YES
- 06_4_EVOLUTION_GOVERNANCE_RETAINED=YES
- 06_5_EVIDENCE_ROLE_RETAINED=YES
- CENSUS_X01_X18_REPLACED=NO
- CENSUS_X01_X18_RECONCILIATION_DEFERRED_TO_IMPLEMENTATION_PASS=YES
- IMPL_NC_01_TARGET_LOCATED=MAP_05_CC_06
- CODE_CHANGE_AUTHORIZED=NO
- PR_ADMISSION_02_RESUME=NO
- GROUNDING_DINO_RESUME=NO
- CANONICAL_MAPPING_LEDGER_STATUS=CANDIDATE
Next: ACM-02 Batch 07 — Temporal / Currentness / Validity Canonical Ledger. Resolve the cross-cutting meanings of observed_time, occurred/effective_time, received_time, validity, expiry, invalidation, staleness and Owner currentness across D03/D07/D10–D12/D16/P-D. This is required before CA-GAP-04 and CA-GAP-07 can be adjudicated.

## Source and status guard

Source: [Notion 03.7 Architecture 2.0](https://app.notion.com/p/3c3113b33a6d81dfa4efeac030352d96), A2.0-117–126. Historical Batch status is preserved above. For current gap status see [Batch 07 temporal/currentness ledger](temporal_currentness_validity_ledger_v0_1.md): CA-GAP-04 and CA-GAP-07 are RESOLVED_AT_CANONICAL_LEVEL only; five Canonical gaps and IMPL-NC-01 remain OPEN; both implementation audits are NOT_STARTED. For MAP-05 / CC-06, [Batch 08 identity/reference/provenance adjudication](identity_reference_provenance_ledger_v0_1.md) classifies IMPL-NC-01 as INVALID_SEMANTIC_LINEAGE + REFERENCE_ROLE_SUBSTITUTION; the source section above retains its historical shorthand. No code remediation, PR-ADMISSION-02 resumption or Grounding DINO implementation is authorized.
