# Architecture 2.0 — Identity / Reference / Provenance Canonical Ledger v0.1

BATCH=ACM-02 08  
STATUS=IDENTITY_REFERENCE_PROVENANCE_LEDGER_CANDIDATE  
CANONICAL_ARCHITECTURE_FROZEN=NO  
CANONICAL_IDENTITY_CONCEPTS=12  
CANONICAL_REFERENCE_CLASSES=12  
REFERENCE_NON_EQUIVALENCE_INVARIANTS=20  
PROVENANCE_CLASSES=8  
LINEAGE_STATUSES=5  
NO_CHAIN_SUBSTITUTION=YES  
STRUCTURAL_REFERENCE_VALIDITY_SUFFICIENT=NO  
SEMANTIC_REFERENCE_VALIDITY_REQUIRED=YES

Repository-side transcription of [Notion 03.7 Architecture 2.0, A2.0-138–149](https://app.notion.com/p/3c3113b33a6d81dfa4efeac030352d96), read 2026-09-30. This ledger defines semantic requirements, not a Python DTO, new Manager/Registry, runtime validator, implementation conformance or code-change authorization. The [frozen Constitution v1](architecture_2_0_constitution_v1.md) and Batch 01–07 ledgers remain unchanged in their source meaning.

### A2.0-138｜ACM-02 Batch 08 — Identity / Reference / Provenance Canonical Ledger
**STATUS:** IDENTITY_REFERENCE_PROVENANCE_LEDGER_CANDIDATE
**INPUT:** C06/C07/C08/C09/C10/C11/C12/C13/C14/C15/C16/C17/C18/C19/C20; D01/D05/D06/D07/D09/D10/D11/D16; CC-02/03/05/06/08/09/10/11/13/21/22/24; MAP-01–25
**CONSTITUTION_BASE:** C01–C48 FROZEN
**CODE_CHANGE_AUTHORIZED:** NO
A reference establishes addressability/association only to the extent declared by its contract. A reference-shaped value is not proof of identity equivalence, semantic role, lineage, provenance, authority, compatibility, binding, admission, currentness or truth.

### A2.0-139｜Canonical Identity Concepts
**I-01 CANONICAL_IDENTITY**
The governed identity of a semantic subject/object within a declared identity namespace/domain.
Identity answers “which governed thing is this?”, not “what is currently true about it?”
**I-02 IDENTITY_NAMESPACE**
The governed scope in which an identifier has meaning and uniqueness expectations.
Equal raw strings across namespaces do not establish same identity.
**I-03 SEMANTIC_ROLE**
The role an identity/object occupies in a specific governed relation or contract.
Role is relational/contextual and cannot be inferred merely from object type or identifier shape.
**I-04 IDENTITY_LINK**
An explicit governed relation between distinct identities.
Linking does not merge identities.
**I-05 IDENTITY_PRESERVATION**
A mapping behavior where source and target intentionally refer to the same canonical subject under proven semantic equivalence.
Must be declared; field-copy does not establish it.
**I-06 NEW_DERIVED_IDENTITY**
A new canonical identity formed for a target semantic object while retaining explicit source links/provenance.
**I-07 REPRESENTATION_IDENTITY**
Identity of a serialized/transport/cache/DTO representation.
Representation identity does not replace semantic object identity unless contract explicitly binds them.
**I-08 EXECUTION_IDENTITY**
Identity of an invocation/effect attempt/execution instance.
Provider/model/request identities may be linked but are not execution identity.
**I-09 DECISION_IDENTITY**
Identity of an Authority decision.
A decision identity is not the identity of its subject/request/effect.
**I-10 STATE_IDENTITY**
Identity/version identity of a governed state representation.
State identity does not redefine subject identity.
**I-11 HISTORICAL_RECORD_IDENTITY**
Identity of a retained record/history entry.
Record identity is custody/history identity, not automatically canonical subject identity.
**I-12 SOURCE_IDENTITY**
Identity of the semantic source from which a mapping/derivation/admission obtains its basis.
Source identity alone does not establish source legitimacy/currentness.

### A2.0-140｜Canonical Reference Classes
**REF-01 IDENTITY_REFERENCE**
Points to a governed identity in a declared namespace.
Proves only the referenced identity relation defined by the contract.
**REF-02 SEMANTIC_OBJECT_REFERENCE**
Points to a specific semantic object/version.
Does not prove the object is current/admitted/valid unless separately stated.
**REF-03 PROVENANCE_REFERENCE**
Points to a source/basis contributing to formation, derivation, admission or decision.
Must declare provenance role.
**REF-04 TRACE_REFERENCE**
Operational observability/correlation reference.
Useful for debugging/audit.
Does not establish semantic lineage by itself.
**REF-05 DECISION_REFERENCE**
Points to an Authority decision.
Does not mean the decision is valid/current/applicable to the current effect.
**REF-06 STATE_REFERENCE**
Points to a state/version.
Does not establish currentness without Owner-governed query/validity semantics.
**REF-07 BINDING_REFERENCE**
Points to a governed D06 binding object/relation.
Only valid as binding evidence if formed under CC-06.
**REF-08 ADMISSION_REFERENCE**
Points to an admission decision/admitted-object relation.
Does not broaden admission scope.
**REF-09 EXECUTION_REFERENCE**
Points to an invocation/effect result/execution instance.
Does not establish Evidence admission or world truth.
**REF-10 EXTERNAL_SOURCE_REFERENCE**
Points to external/provider/native source material.
Its trust/meaning is bounded by the integration/admission contract.
**REF-11 HISTORICAL_REFERENCE**
Points to historical/memory/audit record.
Does not establish present currentness.
**REF-12 REPRESENTATION_REFERENCE**
Points to file/DTO/cache/transport representation.
Cannot substitute for semantic identity/lineage unless explicitly mapped.

### A2.0-141｜Reference Non-Equivalence Invariants
RI-01 SAME_STRING != SAME_IDENTITY unless namespace/identity contract proves it.
RI-02 REFERENCE_EXISTS != REFERENCED_OBJECT_VALID.
RI-03 TRACE_REF != PROVENANCE_REF by default.
RI-04 PROVENANCE_REF != IDENTITY_EQUIVALENCE.
RI-05 REQUEST_REF != REQUESTER_IDENTITY.
RI-06 REQUEST_REF != ROUTING_LINEAGE.
RI-07 CONTROL_TRACE_REF != COMPATIBILITY_BASIS.
RI-08 PROVIDER_REF != EXECUTION_IDENTITY.
RI-09 MODEL_REF != CAPABILITY_BINDING.
RI-10 DECISION_REF != CURRENT_AUTHORIZATION.
RI-11 STATE_REF != CURRENT_STATE.
RI-12 EVIDENCE_REF != FIELD_MEMBERSHIP.
RI-13 FIELD_EVENT_REF != CURRENT_FIELD_STATE.
RI-14 MEMORY_REF != CURRENT_WORLD.
RI-15 FILE/DTO_REF != CANONICAL_SEMANTIC_OBJECT.
RI-16 REFERENCE_SHAPE_COMPATIBILITY != SEMANTIC_ROLE_COMPATIBILITY.
RI-17 MULTIPLE_REFS_TO_SAME_OBJECT != SAME_RELATION_ROLE.
RI-18 PROVENANCE_CHAIN != AUTHORITY_CHAIN.
RI-19 AUTHORITY_CHAIN != DATA_FLOW_CHAIN.
RI-20 DATA_FLOW_CHAIN != IDENTITY_LINEAGE.

### A2.0-142｜Canonical Provenance Model
Provenance answers:
“What governed sources/bases contributed to this semantic object/decision/result, through what declared relation?”
Minimum architecture-significant provenance entry:
SOURCE_REFERENCE
SOURCE_SEMANTIC_ROLE
RELATION_TYPE
MAPPING_OR_CONTRACT_BASIS
TARGET_REFERENCE
FORMATION_OR_DECISION_ACTOR_ROLE
TEMPORAL_BASIS_IF_RELEVANT
TRANSFORMATION_SUMMARY
UNCERTAINTY_OR_LOSS_IF_RELEVANT.
Provenance classes:
**PV-01 SOURCE_PROVENANCE**
Origin/source basis.
**PV-02 TRANSFORMATION_PROVENANCE**
What mapping/refinement/derivation changed semantic information.
**PV-03 DECISION_PROVENANCE**
Inputs/basis used by an Authority decision.
**PV-04 ADMISSION_PROVENANCE**
Candidate/source and admission basis producing admitted fact.
**PV-05 EXECUTION_PROVENANCE**
Authorization/binding/resource/executor/result relation for an effect.
**PV-06 STATE_PROVENANCE**
Events/prior state/rules contributing to a current-state formation.
**PV-07 PROJECTION_PROVENANCE**
Source facts/state plus role/perspective/task basis used for projection.
**PV-08 HISTORICAL_PROVENANCE**
Revision/supersession/assimilation chain preserving historical integrity.
Trace may support provenance evidence, but trace is not provenance semantics by itself.

### A2.0-143｜Lineage Model
Lineage is a specific governed provenance relation showing semantic ancestry/formation across objects.
Canonical lineage requires:
1. identifiable source semantic object/identity;
2. declared source semantic role;
3. declared target semantic object/identity;
4. declared relation type;
5. mapping/formation/admission/decision basis;
6. preservation of relevant provenance;
7. no prohibited semantic upgrade.
Lineage statuses at architecture level:
PROVEN
PARTIAL
UNKNOWN
INVALID
NOT_APPLICABLE.
A lineage reference is valid only for the semantic relation it proves.
A valid request lineage does not automatically prove routing lineage.
A valid routing lineage does not automatically prove compatibility.
A valid compatibility basis does not automatically prove binding.
A valid binding does not automatically prove authorization.
A valid authorization does not automatically prove effect occurrence.
A valid execution does not automatically prove Evidence admission.

### A2.0-144｜Identity / Provenance Behavior Across Main Spine
**D04 → D05**
New request identity; source need linked.
Requester role must be explicit.
No requester identity reconstruction from request_id.
**Non-Cognitive Source → D05**
New request identity; governed source identity linked.
Evaluation runner/test case may be orchestrator/representation, not automatically requester/source authority.
**D05 → D06**
Request identity linked, not transformed into routing/binding identity.
D06 forms new resolution/binding semantic objects with authentic compatibility/routing basis.
**D06 → D07**
Binding/resolution references are decision inputs.
They do not transfer D06 Authority into D07.
D07 creates new decision identity and decision provenance.
**D07 → D09**
Authorization decision reference is effect basis only if current/applicable under CC-08/09.
D09 execution identity is new.
Authorization identity != execution identity.
**D09 → D10**
Execution/provider/model refs become source provenance links.
Observation/Evidence semantic identity is new/explicitly mapped.
Provider result identity cannot become Evidence identity by field reuse.
**D10 → D11**
Evidence identity remains source identity.
Field Event identity is new.
Evidence refs establish provenance only; Field membership requires CC-13/14.
**D11 → D12**
Field state identity remains source.
Current World projection identity is new.
Projection provenance links Field/Evidence/Context; no source identity collapse.
**D12 → D13**
Current World identity linked as reasoning source.
Cognitive State identity is new.
**D10–D15 → D16**
Memory/experience record identity is new or explicitly linked under D16 assimilation rules.
Historical provenance preserved.
Memory identity does not replace source domain identity.

### A2.0-145｜Authority and Provenance Separation
Authority is not provenance.
A decision may cite provenance, but provenance does not issue the decision.
An Authority chain records legitimate decision/effect authority relations.
A provenance chain records semantic/source formation relations.
A data-flow chain records where representations moved.
A trace chain records operational correlation.
These chains may intersect but MUST NOT be collapsed.
Canonical rule:
NO_CHAIN_SUBSTITUTION.
Specifically prohibited:
TRACE_AS_PROVENANCE without declared mapping;
PROVENANCE_AS_AUTHORITY;
DATA_FLOW_AS_LINEAGE;
IDENTIFIER_REUSE_AS_IDENTITY_EQUIVALENCE;
REQUEST_LINEAGE_AS_ROUTING_LINEAGE;
ROUTING_LINEAGE_AS_AUTHORIZATION.

### A2.0-146｜IMPL-NC-01 Canonical Adjudication
Observed historical implementation issue:
controlled real FPO path used request/control-trace-shaped references where D06 routing/compatibility lineage was required.
Canonical target:
CC-06 Runtime Binding Formation
MAP-05 D06 Resolution → Binding
RI-06 REQUEST_REF != ROUTING_LINEAGE
RI-07 CONTROL_TRACE_REF != COMPATIBILITY_BASIS
RI-16 REFERENCE_SHAPE_COMPATIBILITY != SEMANTIC_ROLE_COMPATIBILITY
NO_CHAIN_SUBSTITUTION.
Therefore:
IMPL-NC-01_CANONICAL_CLASSIFICATION=
INVALID_SEMANTIC_LINEAGE + REFERENCE_ROLE_SUBSTITUTION.
Previous shorthand SEMANTIC_DRIFT + FABRICATED_LINEAGE remains historically valid, but the canonical classification is now more precise.
Runtime remediation remains unauthorized.
Implementation reconciliation later must identify the legitimate D06 source object/decision or prove it does not exist.

### A2.0-147｜CA-GAP-01 Impact
CA-GAP-01 Controlled Execution Entry / Governed Request Source remains OPEN.
Batch 08 narrows the missing architecture information:
- governed source identity namespace/semantic role;
- legitimate requester/source relation;
- source→D05 lineage basis;
- whether source is persistent declaration, admitted evaluation request, or another canonical object class;
- who owns/admit/currentness of that source relation.
The gap cannot be solved by:
- assigning request_id as requester identity;
- assigning runner/test-case identity as source authority by convention;
- reusing trace/provenance refs;
- creating a generic “controlled” string flag;
- letting D05 or D07 fabricate the missing upstream source.
Required next adjudication for CA-GAP-01 is an explicit Controlled Evaluation Request Source semantic object/role fit decision, not an implementation DTO decision.

### A2.0-148｜Reference Validation Rule
At every architecture-significant boundary, a required reference is validated on two axes:
**STRUCTURAL_REFERENCE_VALIDITY**
- reference exists;
- namespace/type/format resolvable;
- referenced object can be located when required.
**SEMANTIC_REFERENCE_VALIDITY**
- referenced object has the required semantic role;
- relation type is legitimate;
- source Owner/Authority/currentness requirements are satisfied;
- reference proves the exact basis required by the target contract.
Structural validity without semantic validity is insufficient.
This generalizes the earlier open-world/provider contract lessons without creating a second protocol-validation system. Concrete validation realization remains 06.2; evolution/freeze remains 06.4.

### A2.0-149｜Batch 08 Adjudication
- CANONICAL_IDENTITY_CONCEPTS=12
- CANONICAL_REFERENCE_CLASSES=12
- REFERENCE_NON_EQUIVALENCE_INVARIANTS=20
- PROVENANCE_CLASSES=8
- LINEAGE_STATUSES=5
- NO_CHAIN_SUBSTITUTION=YES
- STRUCTURAL_REFERENCE_VALIDITY_SUFFICIENT=NO
- SEMANTIC_REFERENCE_VALIDITY_REQUIRED=YES
- IMPL_NC_01_CANONICAL_CLASSIFICATION=INVALID_SEMANTIC_LINEAGE+REFERENCE_ROLE_SUBSTITUTION
- CA_GAP_01_ARCHITECTURE_STATUS=OPEN_NARROWED
- REMAINING_OPEN_CANONICAL_GAPS=5
- RUNTIME_CONFORMANCE_ESTABLISHED=NO
- CANONICAL_ARCHITECTURE_FROZEN=NO
- CODE_CHANGE_AUTHORIZED=NO
- PR_ADMISSION_02_RESUME=NO
- GROUNDING_DINO_RESUME=NO
- IDENTITY_REFERENCE_PROVENANCE_LEDGER_STATUS=CANDIDATE
Next: ACM-02 Batch 09 — Controlled Evaluation Request Source / Entry Admission Canonical Adjudication. Resolve CA-GAP-01 at the semantic-object/Owner/Authority level without designing Python DTOs or resuming PR02.

## Local status and non-implementation boundary

CA-GAP-01 remains OPEN_NARROWED, not resolved. IMPL-NC-01 remains OPEN; its canonical classification is INVALID_SEMANTIC_LINEAGE + REFERENCE_ROLE_SUBSTITUTION, with SEMANTIC_DRIFT + FABRICATED_LINEAGE retained as historical shorthand. Five Canonical gaps remain open. Reference validity is both structural and semantic; implementation realization belongs to 06.2 and version/freeze/evolution to 06.4. This documentation does not authorize PR-ADMISSION-02, Grounding DINO, or runtime remediation.
