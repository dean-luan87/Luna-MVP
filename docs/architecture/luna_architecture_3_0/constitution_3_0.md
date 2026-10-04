# Luna Engineering Constitution 3.0

DOCUMENT_ID=LUNA_ENGINEERING_CONSTITUTION_3_0  
NORMATIVE_CLASSIFICATION=CONSTITUTIONAL_NORMATIVE  
VERSION=3.0  
RULE_SET=E01–E58  
RULE_COUNT=58  
ADOPTED=YES  
EFFECTIVE=YES  
FROZEN=YES  
FREEZE_DATE=2026-09-30  
FREEZE_GATE=PASS  
EFFECTIVE_DATE=2026-09-30  
CONSTITUENT_ROLE=LUNA_PROJECT_CONSTITUENT_STEWARD  
CONSTITUENT_HOLDER=LUNA_PROJECT_OWNER

This is the single repository-side canonical representation of the frozen Luna Engineering Constitution 3.0. Supporting records are not additional Constitution bodies. Exact wording is transcribed from Notion 03.7, L3.0-073–106, read 2026-09-30. Freeze does not establish current code conformance or authorize implementation.

## Part I — Constitutional Supremacy & Rule Legality

### E01 — Constitutional Supremacy
Every engineering-significant architecture, rule, protocol, implementation, state mutation, decision, effect, verification claim and governance action SHALL conform to all applicable effective Constitution rules.
A subordinate rule or implementation cannot override Constitution through convention, historical use, technical necessity, runtime success or test result.

### E02 — Constituent Authority
The authority to adopt, amend, supersede or constitutionally except the Luna Engineering Constitution originates in legitimate Constituent Authority external to the Constitution's delegated internal authority.
Constituent Authority is not created by the Constitution it adopts.
Constituent Authority does not automatically confer universal runtime, domain, state-mutation, effect or implementation authority.

### E03 — Legitimate Rule-Making Source
Every binding or governance-relevant rule/artifact SHALL declare its normative classification/level and legitimate rule-making source where applicable.
Every binding subordinate governance rule SHALL trace to a legitimate rule-making authority derived from the effective Constitution.
Minimum constitutional classification model:
- CONSTITUTIONAL_NORMATIVE
- CANONICAL_ARCHITECTURE_NORMATIVE
- SUBORDINATE_GOVERNANCE_NORMATIVE
- ENGINEERING_REALIZATION
- VERIFICATION_EVIDENCE
- HISTORICAL_NONCURRENT
Subordinate governance may refine this taxonomy but SHALL NOT collapse normative truth with implementation/evidence/history.
A descriptive artifact with no legitimate normative classification/source cannot silently become binding.
No document, architecture artifact, implementation, codebase, protocol, test, tool, AI/Agent output, convention or historical practice may self-create binding rule-making authority.

### E04 — Rule-Making Authority Ceiling
A subordinate governance authority may regulate only within its constitutionally delegated scope.
Subordinate rule-making authority SHALL NOT expand its own scope, redefine Constitution meaning, create Constitution exceptions, silently re-delegate rule-making power, or regulate another governance scope without legitimate basis.

### E05 — Canonical Normative Meaning
For the same normative question, scope and effective version, Luna SHALL have one canonical governing meaning.
Parallel representations may exist, but independently editable competing normative meanings are prohibited.

### E06 — Normative Lifecycle & Effectiveness
Binding rules SHALL have governed lifecycle/effectiveness semantics.
Documented, proposed, reviewed, implemented, tested, newest or used does not by itself mean EFFECTIVE.
An effective rule requires legitimate adoption/effectiveness basis.
Historical/superseded rules remain traceable but do not become current by recency or storage presence.

## Part II — Semantic Integrity & Truth Boundaries

### E07 — Explicit Responsibility & Negative Boundary
Every architecture-significant domain, module, governance scope, canonical role, decision boundary and effect boundary SHALL explicitly define:
1. its positive responsibility scope; and
2. its prohibited responsibility / negative boundary.
The negative boundary requirement is unconditional for architecture-significant boundaries.
Subordinate Architecture Governance may define representation format and granularity, but may not omit the negative boundary.
Responsibility does not itself create Authority.

### E08 — Semantic Equivalence Requires Governed Basis
Name, shape, identifier, reference, implementation reuse, transport compatibility or field similarity does not prove semantic equivalence.
Semantic equivalence or transfer across a boundary requires an explicit legitimate basis appropriate to that boundary.

### E09 — Role Before Interpretation
Semantic interpretation SHALL respect declared semantic role/context.
Distinct roles SHALL NOT collapse merely because one implementation object or field can represent them.
Perspective-dependent meaning may derive contextual interpretation but SHALL NOT silently rewrite source ontology.

### E10 — Source Meaning & Derivation Integrity
Source meaning SHALL NOT be silently rewritten.
Derived/projection/refined/materialized meaning SHALL preserve the required derivation basis and SHALL NOT masquerade as source fact.

### E11 — No Fabrication of Missing Semantics
Missing identity, role, authority, provenance, currentness, validity, compatibility, truth, intent, lineage or other required semantics SHALL NOT be fabricated from convenient references, traces, fields, paths, defaults or successful execution.

### E12 — Semantic State-Class Separation
Candidate, declaration, admitted fact, current state, projection/read model, native/effect result, historical record, cognitive derivation and evaluation evidence SHALL remain distinct unless a legitimate governed transition/mapping establishes the target semantic class.
Storage/routing alone does not promote semantic class.

## Part III — Ownership, Authority & Effect

### E13 — Canonical Ownership of Authoritative Questions
Every authoritative question/state/effect class requiring canonical judgment SHALL have a legitimate Owner/Authority scope.
Owner, Authority, Writer, Executor, Custodian, Projector, Mapper, Reader and Auditor roles SHALL NOT be treated as equivalent solely because one actor performs multiple roles.

### E14 — Legitimate Internal Authority Source
Every exercise of Luna internal constitutional/subordinate rule-making authority, canonical decision authority, state-transition authority, admission authority, or effect authority SHALL trace to:
1. legitimate original authority established by the effective Constitution/canonical governance within its delegated scope; or
2. explicit legitimate delegation from an authority that possesses and may delegate that scope.
Constituent Authority is governed separately by E02/E53–E58 and is not derived from E14.
No third internal authority source is valid.

### E15 — Authority Conservation
For delegation: DelegatedAuthority ⊆ DelegableAuthority(Source) ⊆ Authority(Source).
For re-delegation: RedelegatedAuthority ⊆ ExplicitRedelegableAuthority(Delegate) ⊆ DelegatedAuthority(Delegate).
No lower actor/layer may create, enlarge or launder authority.

### E16 — Effect-Specific Scoped Authority
Authority SHALL be interpreted by exact authoritative question/effect, subject, scope, constraints, validity/currentness and applicable conditions.
Authority in one question/effect/scope SHALL NOT imply authority in another.

### E17 — Responsibility, Authority & Execution Separation
RESPONSIBILITY_ASSIGNMENT != AUTHORITY_DELEGATION != EXECUTION_ASSIGNMENT.
Work responsibility or execution assignment SHALL NOT manufacture decision/effect/rule-making authority.
Execution success SHALL NOT retroactively prove authorization.

### E18 — No Self-Authorization
Requester, Owner label, Writer, Executor, Provider, Mapper, Projector, Custodian, Auditor, test, Agent, implementation component or data holder SHALL NOT authorize itself solely by occupying or performing that role.

### E19 — Reserved Authority & Delegability
Constitution/canonical governance may designate Authority as reserved/non-delegable, bounded-delegable, or explicitly re-delegable.
Delegation/re-delegation is prohibited unless legitimate delegability exists.
Assignment of preparation/execution work does not transfer reserved authority.

### E20 — Delegation Lifecycle & Currentness
Delegated authority SHALL explicitly identify source, holder/delegate, scope, conditions, validity/currentness basis, revocation authority and re-delegation semantics where applicable.
A historical grant does not prove current usability.
When required delegation/source/currentness evidence cannot be established for a dependent effect, the required authority condition SHALL remain UNKNOWN_CURRENTNESS or otherwise non-affirmative according to the applicable contract rather than presumed continuation.
Absence or unavailability of a required currentness source SHALL NOT be interpreted as continuing authorization.
When affirmative current authority is required, the dependent effect SHALL NOT proceed while that authority condition remains non-affirmative.
Where those semantics are required, the applicable subordinate authority/effect contract MUST declare CURRENTNESS_EVIDENCE_BASIS, RECHECK_REQUIREMENT and UNAVAILABLE_SOURCE_BEHAVIOR.
Constitution does not prescribe polling, cache or network algorithms.

### E21 — Revocation, Suspension & Supersession
Only legitimate authority may suspend, revoke or supersede delegated authority.
Revocation/suspension failure, unavailable revocation evidence, or unavailable revocation/currentness authority SHALL NOT make a stale grant permanent and SHALL NOT be interpreted as continuing authorization.
When required revocation/currentness evidence cannot be established, the dependent authority condition SHALL remain UNKNOWN_CURRENTNESS or otherwise non-affirmative according to the applicable contract.
When affirmative current authority is required, the dependent effect SHALL NOT proceed while that condition remains non-affirmative.
Revocation changes current usability; it SHALL NOT erase historical authority provenance or historically legitimate decisions/effects.
Where required, the applicable subordinate authority/effect contract MUST declare the revocation/currentness evidence basis, recheck requirement and unavailable-source behavior.

### E22 — Authority Does Not Follow Data, Communication or Execution
Authority SHALL NOT transfer merely through data flow, references, trace/provenance, routing/binding, message transport, receipt/acknowledgement, execution, successful result, storage, naming or physical possession.

### E23 — Scoped Authority Graph
Luna Authority is a typed, scoped relation graph, not a universal administrative tree.
Delegation establishes constrained authority relations.
Authority superiority is question/scope-specific except for Constitution's normative supremacy over internal engineering governance.

### E24 — Joint Authority
A governed decision/effect MAY require multiple independent authorities/conditions only through an explicit applicable composition rule.
Permitted constitutional composition classes are:
- SINGLE
- CONJUNCTIVE
- SEQUENTIAL
- THRESHOLD
For any non-single composition, the governing contract SHALL define REQUIRED_AUTHORITY_IDENTITIES/ROLES, REQUIRED_SCOPES, COMPOSITION_CLASS, ORDER where sequential, THRESHOLD/ELIGIBLE_SET where threshold, CURRENTNESS_REQUIREMENT, and UNKNOWN/REJECTED/NOT_CURRENT behavior.
No declared composition rule = no authority composition.
Joint requirements SHALL preserve each participant's independent authority source, decision identity, scope, validity/currentness and provenance.
Multiple grants held by the same actor SHALL NOT be unioned into a broader authority identity/scope unless the exact effect contract independently accepts those authorities for that effect.
Joint authority combines conditions for an effect; it does not merge authority identities.
A joint requirement SHALL NOT create an implicit super-authority or permit one participant/executor to synthesize another participant's missing authority.

### E25 — Authority Escalation
An actor outside proven authority scope SHALL NOT self-expand or fabricate basis.
When required delegation/source/revocation/currentness evidence cannot be established, unresolved authority SHALL remain UNKNOWN_CURRENTNESS or otherwise non-affirmative according to the applicable contract.
The dependent effect SHALL NOT proceed when affirmative current authority is required.
Escalation SHALL target the legitimate authority/governance source declared for the exact authority question.
If no legitimate escalation terminal can be established, UNKNOWN remains unresolved; no fallback authority is created.
Where required, the applicable subordinate authority/effect contract MUST declare ESCALATION_TERMINAL together with the applicable currentness/recheck/unavailable-source semantics.
Escalation SHALL NOT itself transfer authority.

## Part IV — State, Time & Historical Integrity

### E26 — Governed Currentness
Currentness SHALL be established by legitimate Owner/Authority semantics and required reconciliation, not solely by recency, presence, cached state or prior successful use.

### E27 — Legitimate State Transition
Canonical state mutation/transition SHALL require legitimate transition authority and applicable current/valid dependencies.
State custody or storage access does not confer transition authority.

### E28 — Temporal Semantic Integrity
Observed time, occurred time, effective time, received/recorded time, decision time, effect time, validity, expiry, invalidation, supersession, staleness and currentness SHALL remain semantically distinct unless explicitly governed as equivalent/bound.
Unknown temporal meaning SHALL NOT silently become “now”.

### E29 — Historical Integrity
Revision, correction, revocation, supersession, migration and reconciliation SHALL preserve required historical truth/provenance.
Historical existence SHALL NOT imply current state.
A later rule, grant, approval, amendment, exception or authority decision SHALL NOT retroactively convert an action that lacked required authority at its effect time into a historically authorized action.
A legitimate later authority may acknowledge, compensate, remediate, ratify a present/future state where its current scope permits, or define future treatment of historical consequences, but SHALL NOT rewrite the historical authorization status of the original effect.
If Constitution/Constituent Authority explicitly creates retroactive normative applicability, it MUST preserve the historical fact that the original action occurred under the then-effective authority state.
Retroactive applicability is not retroactive historical authorization.
RETROACTIVE_AUTHORITY_LAUNDERING=PROHIBITED.

## Part V — Process, Decision & Effect Legality

### E30 — Process Correctness Is Independent
Outcome correctness and process correctness are independent.
A correct result reached through an illegitimate process does not establish conformance.

### E31 — Legitimate Basis & Traceability
Governed decisions/effects SHALL consume legitimate required inputs/bases and preserve traceability/provenance appropriate to their semantic and authority scope.
Traceability itself does not create authority, identity or truth.

### E32 — Intent, Request, Admission, Authorization & Effect Separation
Need/intent, request, admission, authorization, execution/effect and evidence SHALL NOT silently collapse.
A prior stage may form a legitimate basis for a later stage but does not automatically become the later stage.

### E33 — Honest Unknown, Failure, Absence & Degradation
Unknown, failure, empty/absence, contradiction, degradation and unavailable states SHALL retain their governed semantics.
They SHALL NOT be silently promoted to affirmative success, truth, authority, currentness or admission.
Required unknown blocks only the dependent effect according to governing contract; it does not automatically invalidate unrelated truth.

## Part VI — Luna System Boundaries

### E34 — Global Governance and Local Reality Reasoning Are Distinct
Global policy/safety/governance authority and local cognition/world reasoning SHALL remain distinct.
Neither may silently appropriate the other's canonical question.

### E35 — Cognition Consumes Governed Information
Cognition may derive attention, hypotheses, gaps, contradiction, sufficiency, stop and intent from governed information.
Cognitive derivation SHALL NOT retroactively rewrite source truth/authority.
Cognitive need/intent SHALL NOT itself confer Organ/runtime execution authority.

### E36 — Organ Is Bounded Capability
An Organ/provider/model performs bounded sensing/native capability execution/provider-specific normalization as governed.
It SHALL NOT acquire cognitive authority, world-truth authority, Evidence/Field admission authority, policy authority or decision authority merely through sensing/execution.

### E37 — Provider-Specific Semantics Terminate at Governed Integration Boundary
Provider/model-specific semantics SHALL terminate or be explicitly normalized/mapped at the governed integration boundary before canonical downstream semantics.
Provider replacement SHALL NOT silently alter downstream canonical meaning.

### E38 — Replaceability & Composition Preserve Canonical Semantics
Provider/model/transport/process/deployment/composition replacement SHALL preserve applicable canonical semantics, authority and truth boundaries.
Deployment scale does not redefine Luna.

## Part VII — Protocol, Channel & Communication

### E39 — Channel Does Not Create Authority
Communication, connectivity, transport, routing, receipt, acknowledgement, protocol conformance or endpoint possession SHALL NOT create Authority.

### E40 — Authority-Sensitive Channel Integrity
A channel carrying authority-sensitive request/decision/grant/revocation/currentness information SHALL preserve required identity/role, scope, validity/currentness, provenance and decision semantics.
Ordinary information transport does not thereby become Authority delegation.

### E41 — Judgment Requires Legitimate Question & Judge
Every governed judgment SHALL identify the authoritative question and legitimate Decision Authority.
No generic judge, protocol handler or receiver may decide arbitrary scopes.

### E42 — Communication Stage Non-Collapse
Where semantically applicable, sent, received, acknowledged, admitted, authorized, executed and evidenced stages SHALL remain distinct unless an explicit canonical contract binds them.
This rule does not require every channel to instantiate every stage.

### E43 — Transport Independence
Transport technology may alter mechanics but SHALL NOT silently alter canonical semantic/authority meaning.
Local call, Bluetooth, WiFi, RPC, queue, file or future transport receives no special semantic privilege.

### E44 — Protocol Governance Boundary
Protocol/interface governance may define realization, compatibility, versioning, migration and freeze within delegated scope.
It SHALL NOT redefine Constitution or canonical Architecture meaning outside that scope.

## Part VIII — Engineering, Code, Naming & Structural Legality

### E45 — No Accidental Normative, Architecture or Authority Creation
Documentation convention, implementation/code, runtime behavior, naming, historical survival, generated artifact, AI/Agent output, test expectation, tool behavior or technical convenience SHALL NOT by itself create binding governance, Architecture Truth or Authority.
All implementation sources are equal under governance; no human/AI/generated-code exemption exists.

### E46 — Implementation Preserves Governed Boundaries
Implementation SHALL preserve applicable canonical semantic, authority, state and process boundaries.
Implementation convenience SHALL NOT collapse boundaries or manufacture missing semantics.

### E47 — Naming & Structural Integrity
Names, aliases, namespaces and structural placement SHALL NOT materially misrepresent canonical role, ownership, identity, equivalence, lifecycle status or Authority.
The prohibition does not depend on proving intent.
When a materially misleading name/structure is discovered, historical identity/lineage must be preserved, correction follows governed change, and the misleading representation does not acquire canonical meaning merely through historical use.
Renaming/restructuring that changes or implies semantic/authority meaning is a governed change.
Concrete naming syntax remains subordinate Engineering/Naming Governance.

### E48 — Governed Change by Semantic/Authority Impact
Architecture/engineering creation, extension, modification, split, merge, recomposition, rename, move, deprecation, supersession, removal, freeze or unfreeze SHALL follow legitimate change governance appropriate to semantic/authority blast radius.
Textual size, LOC or apparent technical simplicity does not determine governance significance.

### E49 — Frozen Meaning Requires Governed Evolution
Frozen Constitution/canonical/interface/protocol meaning SHALL NOT be silently mutated.
Applicable versioning, migration, exception and adoption/effectiveness governance SHALL be followed.

## Part IX — Verification, Deployment & Governed Feedback

### E50 — Verification Does Not Create Normative or Architecture Truth
Tests, runners, verifiers, evaluations, audits and runtime observations may provide evidence of conformance/nonconformance.
PASS/FAIL SHALL NOT create or mutate Constitution, Architecture Truth, Authority or lifecycle state unless a legitimate governing decision explicitly uses that evidence.

### E51 — Evidence Feedback Requires Legitimate Adjudication
Evidence may trigger review and inform decisions.
Rule/architecture/lifecycle/authority mutation requires the legitimate owning authority and SHALL NOT occur automatically from evidence.

### E52 — Deployment & Operational Topology Do Not Redefine Semantics
Single-process, multi-process, remote Organ, Hive, scale-up/down, composition, disconnection or recovery SHALL NOT silently redefine canonical meaning or Authority.
Operational autonomy/degradation during partition/disconnection requires explicit governed contract; topology alone confers no new authority.

## Part X — Amendment, Exception & Governance Delegation

### E53 — Constitutional Adoption, Amendment & Supersession
Constitution adoption/amendment/supersession SHALL require a legitimate Constituent Authority decision, explicit affected/effective version, review basis, effectiveness basis and lineage preservation.
The Constitution cannot self-prove its constituent legitimacy.

### E54 — Constitutional Exception
No subordinate governance may create an exception to Constitution.
Any constitutional exception SHALL require legitimate Constituent Authority under the effective constituent/amendment model, explicit scope, basis, validity/effectiveness and historical record.
Silence creates no emergency or exception power.

### E55 — Constitutional Reserved Powers
Constitutional reserved powers are non-delegable to subordinate internal governance unless a legitimate constituent amendment changes that rule.
Reserved constitutional power does not make the Constitution immune from legitimate Constituent Authority adopting a successor Constitution.

### E56 — Governance Delegation & Orphan Rules
Constitution may establish/delegate bounded rule-making authority to subordinate governance families/specifications.
A subordinate rule with no legitimate rule-making source is ORPHAN_GOVERNANCE and non-binding regardless of documentation, implementation, history or enforcement.

### E57 — Governance Conflict & Escalation
Subordinate governance conflict SHALL be resolved according to legitimate scope/authority.
A governance body SHALL NOT invent precedence outside its authority.
Unresolved conflict escalates to the legitimate common governance source and, for constitutional legitimacy, ultimately to Constituent Authority.

### E58 — Constitution Bootstrap & Normative Source of Truth
The first effective Constitution 3.0 SHALL be adopted through Constituent Authority bootstrap.
Thereafter its effective amendment/lifecycle rules govern future constitutional changes.
The governed normative identity + adoption record + effectiveness record define current normative authority; Git, Notion, code, chat and other representations do not independently confer effectiveness.

Supporting records (not Constitution body): adoption/effectiveness, C01–C48 lineage, Architecture 3.0 general model, and freeze readiness.
