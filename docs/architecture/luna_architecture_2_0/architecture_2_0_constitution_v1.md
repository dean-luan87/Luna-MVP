# Architecture 2.0 Constitution v1

CONSTITUTION_STATUS=FROZEN  
FREEZE_EFFECTIVE_DATE=2026-09-30  
CONSTITUTION_RULE_COUNT=48  
SOURCE_LINEAGE_COVERAGE=162/162

This is the repository-side exact-wording transcription of the frozen C01–C48 rule set from [Notion 03.7, A2.0-58 and freeze record A2.0-71](https://app.notion.com/p/3c3113b33a6d81dfa4efeac030352d96). The A2.0-58 source heading says “Freeze Candidate” because it is the preserved historical wording source; A2.0-71 records the subsequent user-authorized freeze. The rule statements below are unchanged. Any amendment or supersession requires explicit versioned architecture governance and preserved lineage.

Constitution frozen != current code conforms. Constitution frozen != Canonical Architecture frozen. No implementation remediation is authorized here.

## Frozen C01–C48 wording

#### C01–C05｜Architecture Truth & Normative Boundary
**C01 Architecture Precedence** — Architecture Truth governs canonical semantic/contract intent; Code Truth and Runtime Truth must conform and cannot silently redefine it.
**C02 Explicit Responsibility Boundary** — Architecture-significant domains/modules must have explicit responsibility and negative boundaries; possession, call position, implementation convenience or historical behavior do not create responsibility.
**C03 Single Canonical Meaning** — Within a defined version/scope, a canonical concept must not have conflicting canonical meanings; alternate representations require explicit relation to that meaning.
**C04 No Accidental Architecture** — Repeated use, code existence, runtime success, test success or historical survival does not by itself establish canonical architecture.
**C05 Normative Level Must Be Explicit** — Constitution, Canonical Architecture, Domain Rules, Engineering Rules and Evidence must not silently substitute for one another.
#### C06–C10｜Semantic Integrity & Identity
**C06 Semantic Equivalence Requires Proof** — Same name, compatible structure, field copying or serialization compatibility does not prove semantic equivalence.
**C07 Role Before Interpretation** — Identity and semantic role must be established before Owner, Authority, Currentness or effect interpretation.
**C08 Roles Do Not Collapse by Implementation** — Requester, Owner, Writer, Executor, Provider, Custodian, Projector and analogous roles do not become equivalent merely because one implementation/entity currently performs several roles.
**C09 Source Meaning Cannot Be Silently Rewritten** — Context, projection, perspective or downstream need may derive/reinterpret meaning only through explicit governed semantics; source facts/ontology/history remain distinguishable.
**C10 Trace and Provenance Are Not Identity or Authority** — Traceability/provenance can support evidence and audit but cannot substitute for governed identity or confer authority.
#### C11–C16｜Mapping & Derivation
**C11 Cross-Domain Semantic Transfer Requires Explicit Mapping Basis** — No cross-domain semantic transfer is canonical without an explicit mapping basis.
**C12 Mapping Must Declare Semantic Behavior** — Architecture-significant mappings must make information/identity/authority/provenance behavior explicit enough to determine what is preserved, reduced, derived, reinterpreted, linked or newly decided.
**C13 Authority Does Not Follow Data** — Data, references, mappings, projections, resolution or binding do not transfer Admission/Authorization/Authority unless an explicit authority contract establishes a new valid decision.
**C14 No Fabrication of Missing Semantics** — A downstream layer may not manufacture missing upstream intent, identity, requester/source basis, lineage, authority, world fact or history merely to satisfy its contract.
**C15 Derivation Must Remain Explicit** — Derived facts/meaning must preserve an auditable derivation relation to legitimate source basis.
**C16 Mapping Accountability** — Architecture-significant mapping ownership/accountability must be explicit and mapping chains must remain auditable.
#### C17–C22｜Ownership & Authority
**C17 One Canonical Owner per Authoritative Question** — For a defined authoritative question/scope there must be one canonical ownership semantics; replicas, writers, executors, custodians and projections do not create competing ownership.
**C18 Canonical Mutation Requires Legitimate Authority** — Mutation of canonical governed state requires explicit legitimate mutation authority; implicit multi-writer ownership is prohibited.
**C19 Authority Is Effect-Specific and Basis-Dependent** — Authority exists only for a defined effect/scope and requires canonical decision basis; possession of data, lifecycle state, purpose or execution position is insufficient.
**C20 No Self-Authorization** — A component requesting, forming, routing or executing an effect cannot manufacture the authority required for that effect.
**C21 Admission Is Not Effect Authorization** — Permission to enter governed formation/admission does not by itself authorize the final runtime/world/action effect.
**C22 Authority Scope Cannot Silently Expand** — Local authority does not become global authority, and Owner/Authority transfer or expansion is an architecture-significant change requiring explicit review.
#### C23–C28｜Facts, State & Currentness
**C23 Candidate Is Not Admitted Fact** — Candidate/proposed/derived input cannot be consumed as admitted canonical fact without the governed boundary required by its contract.
**C24 Projection Is Not Source Fact** — Read models, projections and derived views do not become second sources of canonical truth.
**C25 Native Result Is Not Epistemic Fact** — Model/provider/native output, including native confidence, remains execution/organ information until governed semantic admission; it cannot declare higher-level epistemic/world truth.
**C26 Absence Requires Explicit Semantic Basis** — Missing output, zero detection or absence of evidence does not automatically establish a negative world fact.
**C27 Currentness Must Be Governed, Not Inferred from Recency** — Record existence, version recency, cache freshness, timestamp or historical status does not prove semantic currentness; currentness belongs to the relevant governed semantic scope.
**C28 Required Unknown Authority/Currentness Blocks Only the Dependent Effect** — When an effect contract requires authority/currentness and that requirement is unknown or unverifiable, that effect is not authorized. This does not convert general cognitive uncertainty into system failure.
#### C29–C33｜State Change, Process Correctness & Failure Honesty
**C29 Canonical State Transition Requires Legitimate Transition Authority** — Observers, routers, caches and projections cannot mutate canonical state merely by seeing or carrying it; governed current state must also have explicit invalidation semantics.
**C30 Outcome Correctness and Process Correctness Are Independent Axes** — A correct result does not legitimize an invalid process; an incorrect/revisable result does not by itself prove the process illegal.
**C31 Governed Process Requires Legitimate Inputs and Traceability** — Architecture-significant formation, decision and effect must use contract-legitimate inputs and remain auditable/explainable at contract level.
**C32 Revision Must Preserve Historical Integrity** — Revisable cognitive/derived/current projections may change, but revision/supersession must not silently rewrite source facts or erase material history.
**C33 Failure, Unknown and Degradation Must Remain Semantically Honest** — Failure/unknown/degraded states must not masquerade as success, completeness, normal availability or admitted truth.
#### C34–C37｜Cognition Boundary
**C34 Global Governance and Local Reality Reasoning Are Distinct** — Global policy/constraints and local reality reasoning are distinct authority scopes; neither silently absorbs the other.
**C35 Cognition Consumes Governed Information** — Cognitive reasoning must not treat provider-native or unadmitted candidate information as canonical world truth; concrete governed information types are defined by Canonical Architecture.
**C36 Cognitive Need Does Not Confer Execution Authority** — Need, attention, hypothesis or observation desire may justify formation of an execution request but cannot directly authorize provider/model/runtime effects.
**C37 Perspective-Dependent Meaning Does Not Rewrite Source Ontology** — Role/perspective may change relevance and derived meaning while preserving the distinguishability of source ontology/facts.
#### C38–C41｜Brain–Organ & Execution Boundary
**C38 Organ Is Bounded Capability, Not Cognitive Authority** — Organ/provider/model components own bounded sensing/native capability execution as defined by contract and cannot assume cognitive/world authority.
**C39 Provider-Specific Semantics Must Terminate at a Governed Integration Boundary** — Provider-native semantics must be normalized/mapped before crossing into canonical downstream semantics; exact implementation seam is Canonical Architecture.
**C40 Organ Replaceability Must Preserve Canonical Semantics** — Replacing model/provider/transport/deployment must not silently change canonical capability meaning, fact level, mapping, Owner or Authority.
**C41 Intent, Request, Authorization and Effect Must Not Collapse** — Formation/resolution/binding/purpose do not themselves confer execution authority; each effect uses its contract-required current dependencies and legitimate authority basis.
#### C42–C44｜Temporal Integrity
**C42 Temporal Meaning Requires Governed Contract Semantics** — Timestamp/expiry/reference/arrival order alone does not establish observed/effective/valid/current/expired semantics; relevant temporal role and validity interpretation must be governed.
**C43 Observation Time and Effective Time Are Distinct Unless Explicitly Bound** — Time of observation/receipt and time at which a represented world fact is effective must remain distinguishable unless contract semantics explicitly equate them.
**C44 Temporal Uncertainty and Required Temporal Scope Must Survive Mapping** — Mapping must not fabricate temporal certainty or silently drop temporal scope required for valid target interpretation.
#### C45–C48｜Evolution, Scale & Constitution Governance
**C45 Architecture-Significant Change Is Governed by Semantic Blast Radius** — Discovery/evidence is not decision, decision is not implementation authorization, and impact is determined by semantic/Owner/Authority/Mapping/State propagation rather than LOC or file count.
**C46 Frozen Architecture Evolves by Explicit Versioned Change** — Frozen contracts/constitutional rules are not silently rewritten; amendment/supersession/deprecation/retirement preserves historical meaning, and compatibility is semantic rather than merely structural.
**C47 Deployment Scale Does Not Redefine Luna Semantics** — Hive is scaled/composed Luna rather than a separate constitutional architecture; deployment topology, copies and transport do not create new canonical meaning/Owner/Authority, and capability meaning remains stable across deployment.
**C48 Constitution Change/Exception/Freeze Requires Explicit Architecture Governance** — Constitution cannot create conflicting authority, silently accept exceptions, over-govern replaceable implementation detail, or be frozen/changed by implementation agents, tests or runtime success alone; constitutional change requires explicit architecture-level decision and versioned lineage.

## Source lineage

The 162 historical source rules have exactly one primary final destination each. SOURCE_LINEAGE_COVERAGE=162/162. The source lineage remains in [Notion 03.7, A2.0-63–65](https://app.notion.com/p/3c3113b33a6d81dfa4efeac030352d96); it is not reconstructed or renumbered here.
