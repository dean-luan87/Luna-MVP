# Luna Governance Core Architecture v1

## Purpose

This planning baseline places existing A3 Cognitive Analysis, Translation Layer, and Runtime Boundary governance assets into Luna's L0/L1 architecture. It defines governance responsibilities only; it does not implement a Governance Runtime, modify a Capability, register a Capability, or activate Runtime.

## LUNA_SUPREME_DESIGN_PRINCIPLE

### Goal-Driven Structural Projection

`Goal-Driven Structural Projection` is Luna's supreme design principle. It is higher than Architecture, Functional Boundary, Authority, Canonical Fact, Lifecycle, Contract, Module, Model Integration, Algorithm Integration, Runtime Design, and Code Design. Every lower-level design must be explainable as a consequence of Luna's long-term goal, product form, business model, real user value, and intended future operating form.

Design must not be justified only by current implementability, current test success, or local modification convenience. The required judgment is:

```text
CURRENTLY_WORKS ≠ ARCHITECTURALLY_SUITABLE
TESTS_PASS ≠ LONG_TERM_STRUCTURAL_VALIDITY
LOCAL_CORRECTNESS ≠ SYSTEM_GOAL_ALIGNMENT
```

Before an important architecture, function, data, model, algorithm, authority, contract, module, integration, refactor, or runtime design is selected, Luna must project the structure through capability growth, additional models and algorithms, provider growth, multimodal composition, model replacement, local/cloud switching, capability versioning, continuous operation, persistent state change, learning/evolution, fault isolation, and long-term maintenance.

The design comparison must address, where applicable:

- advantages and disadvantages;
- current and future cost;
- scaling and coupling growth;
- Authority and Canonical Identity stability;
- lifecycle/currentness/invalidation behavior;
- replacement and composition cost;
- failure propagation;
- test/production consistency;
- long-term evolution cost.

### Goal-to-Code Design Order

Luna's design order is:

```text
L0  Luna Goal / Product / Business Model
L1  Future Scenario & Scale Projection
L2  Required Structural Properties
L3  System Question
L4  Functional Boundary
L5  Responsibility
L6  Canonical Fact / Semantic Model
L7  Owner / Authority Graph
L8  Lifecycle / Currentness / Invalidation
L9  Contract / Artifact
L10 Module
L11 Code
L12 Runtime Projection / Execution
L13 Verification
```

Existing Functional Boundary, Authority, Canonical Fact, Lifecycle, and verification rules remain binding. They are not replaced; they are evaluated inside this goal-driven structural order.

### Minimum Sufficient Architecture

Goal-Driven Structural Projection does not authorize implementing every imagined future. It determines the direction in which the structure must grow. Minimum Sufficient Architecture determines how much Luna builds at the current stage.

The target is:

```text
TODAY:  small enough, clear enough, and sufficient for the real need.
FUTURE: able to grow naturally toward Luna's target form.
```

Implementation changes, module splits/merges, performance optimization, and provider replacement remain allowed. Normal capability growth should not repeatedly force Luna to overturn core semantics, canonical responsibility, fundamental lifecycle models, or Authority ownership.

> Today should be small enough to build and clear enough to govern; tomorrow should be able to grow without overturning core semantics, core responsibility, or core Authority.

### Structural Guardrails

Goal-Driven Structural Projection must not be used to predict every possible future, pre-build unnecessary Managers/Registries/Governance Layers/Artifacts, abstract for its own sake, or put future model capabilities into Luna's core prematurely. It must not grant external models new Canonical Truth Authority or use a business goal to violate Semantic Owner and Authority integrity. Safety, factual truth, explicit user constraints, and non-negotiable system boundaries remain higher-order constraints on every candidate structure.

## CANONICAL_ARCHITECTURE_GOVERNANCE

### Canonical Fact Governance Six-Law

The `Canonical Fact Governance Six-Law` is Luna's standing canonical-architecture governance layer beneath `Goal-Driven Structural Projection` and above Functional Boundary, Authority Graph, Lifecycle, Contract, Artifact, Module, Code, and Runtime Projection.

```text
Goal-Driven Structural Projection
        ↓
Canonical Fact Governance Six-Law
        ↓
Functional Boundary / Authority Graph / Lifecycle
        ↓
Contract / Artifact
        ↓
Module / Code / Runtime
```

The Six-Law does not replace the supreme design principle. Goal-Driven Structural Projection asks where Luna's structure should grow in service of its long-term product, business, and user goals. The Six-Law asks whether a proposed Canonical Fact remains valid in ownership, authority origin, identity, lifecycle, projection, and migration.

### Canonical Fact precondition

Before applying the Six-Law, determine whether the object is actually a Canonical Fact:

```text
IS_CANONICAL_FACT=YES/NO
```

Do not infer Canonical Fact status from any single implementation property:

- having a dataclass;
- having a status field;
- being used across modules;
- having a lifecycle-looking field;
- being serialized or stored.

An object is a Canonical Fact only when it answers an independent semantic question, has a Semantic Owner and Final Authority, has an independent lifecycle/currentness or validity question, and has downstream semantic significance. Candidate, DTO, mechanical projection, transport object, evaluation result, and execution record are not promoted by default. This precondition prevents `CANONICAL_ARTIFACT_OVERPROMOTION` and `ARCHITECTURE_ATOMIZATION`.

### CANONICAL_OWNERSHIP_LAW

Every Canonical Fact has exactly one clear Semantic Owner and one Final Authority. The design must answer:

```text
WHO owns this fact?
```

Multiple final authorities, implicit ownership, caller-as-owner, orchestrator authority accumulation, and mechanical-layer semantic ownership are prohibited.

### AUTHORITY_ORIGIN_LAW

Correct ownership alone does not establish correct authority origin. The design must answer:

```text
WHY is this Owner allowed to establish this fact?
```

Every establishment, admission, mutation, and currentness declaration requires an independent, traceable authority basis. Self-authorizing input, caller-positive predicates, authority laundering, mechanical authority upgrades, and Owner trust in caller assertions are prohibited.

### OWNER_REQUERY_CLOSURE_LAW

After issuance, the following must be sufficient to uniquely re-establish authoritative currentness, validity, and admission:

```text
canonical identity + Owner-internal state → authoritative result
```

The Owner may not require a caller-selected profile, namespace, truth selector, or implicit authority context that can change the result. Explicit context may remain only as a consistency assertion or diagnostic constraint; it cannot select the authoritative truth namespace. The design must answer:

```text
Can the Owner uniquely re-establish the authoritative state?
```

### CANONICAL_IDENTITY_ISSUANCE_CLOSURE_LAW

Any Owner-controlled operation that produces a new canonical identity must close both state establishment and Owner resolution before the identity becomes externally projectable:

```text
Canonical Identity Issuance
        ↓
Owner State Establishment + Owner Resolution Establishment
        ↓
Externally Projectable Identity
```

This applies to real transitions such as initial admission, new version formation, refresh, supersession, replacement, renewal, and re-admission. A mutation that keeps the same identity must not create unnecessary resolver state. The design must answer:

```text
Was Owner-requery closure established when this identity was issued?
```

### CROSS_OWNER_PROJECTION_INTEGRITY_LAW

When a Canonical Fact crosses an Owner, Functional Boundary, Module, or Runtime Boundary, every downstream-required canonical identity, version, scope, and lineage element must be preserved exactly. Reconstruction, version loss, scope loss, legacy substitution, string parsing, and implicit fallback are prohibited.

```text
LINEAGE_PRESERVATION ≠ AUTHORITY_OWNERSHIP
```

Preserving lineage does not transfer currentness, mutation, admission, authorization, or truth authority to the downstream object. The design must answer:

```text
Was canonical identity/version/scope preserved without transferring authority?
```

### LEGACY_AUTHORITY_EXTINCTION_LAW

After an architecture migration:

```text
LEGACY_REPRESENTATION_ALLOWED ≠ LEGACY_AUTHORITY_ALLOWED
```

Legacy representation may remain for serialization compatibility, diagnostics, historical records, or controlled compatibility callers. Legacy authority must be absent from both positive and negative paths. Legacy data cannot authorize, deny canonical authorization, establish currentness, admission, or validity, substitute canonical identity, override canonical projection, or change canonical truth.

The design must answer:

```text
Has the legacy representation actually lost authority?
```

### Unified Six-Law gate

For every `IS_CANONICAL_FACT=YES` design or audit, emit this gate:

```text
IS_CANONICAL_FACT=

WHO=
OWNER=
FINAL_AUTHORITY=

WHY=
AUTHORITY_ORIGIN=

REQUERY=
CAN_OWNER_REQUERY_FROM_CANONICAL_IDENTITY=
CALLER_TRUTH_CONTEXT_REQUIRED=

ISSUANCE=
IDENTITY_PRODUCING_TRANSITIONS=
ISSUANCE_REQUERY_CLOSURE=

PROJECTION=
CROSS_OWNER_PROJECTIONS=
IDENTITY_VERSION_SCOPE_PRESERVED=
AUTHORITY_TRANSFERRED=

LEGACY=
LEGACY_REPRESENTATION_EXISTS=
LEGACY_CAN_AUTHORIZE=
LEGACY_CAN_DENY=
LEGACY_CAN_CHANGE_CURRENTNESS=

SIX_LAW_RESULT=PASS/FAIL/NOT_APPLICABLE
```

`IS_CANONICAL_FACT=NO` objects must explain why the Six-Law is `NOT_APPLICABLE`; they must not be promoted merely to satisfy the gate.

### Relationship to existing principles

These principles are complementary:

| Principle | Question answered |
| --- | --- |
| Goal-Driven Structural Projection | Does this structure serve Luna's long-term goal, and how should it grow? |
| Canonical Fact Governance Six-Law | Does this Canonical Fact remain valid in authority, identity, lifecycle, projection, and migration? |
| Functional Boundary | Which independent responsibility boundary should answer the system question? |
| Minimum Sufficient Architecture | How much structure is actually required at the current stage? |

None substitutes for another. Goal projection must not justify speculative architecture, and the Six-Law must not turn every DTO, candidate, or runtime record into a Canonical Fact.

### Future architecture design rules

The accepted contract is `BOUNDED_VERSIONED_BRANCHING_INFORMATION_RELATIONS_WITH_SELECTIVE_CANONICAL_COMMITMENTS`. The following eight core rules and four derived guards refine design-time review beneath Goal-Driven Structural Projection and alongside the existing Six-Law. They change no Owner or runtime authority and do not claim that a Workspace, Sedimentation Graph, or Lineage Spine exists in production.

#### Eight core design rules

1. **Goal-driven structure.** Derive lasting boundaries from Luna's system/product question and projected scale, not current files, DTOs, modules, models, providers, or implementation convenience. Every new structure needs a system-level reason.
2. **Semantic stage is not Canonical Fact.** A processing or semantic stage does not itself establish an independently governed fact. A type, ref, ID, module, serialization, persistence, or candidate object cannot establish canonicality.
3. **Selective canonical commitment.** First prove an independent System Question and distinct commitment/lifecycle/currentness need. If upstream identity + version + information relation + formation/execution occurrence preserves the requirement without semantic loss, default to `DO_NOT_PROMOTE_TO_CANONICAL_FACT`. Determine an Owner only after proving the fact; never invent an Owner to justify promotion.
4. **Relationships before duplicated state.** Information may be transformed, combined, selected, interpreted, revised, superseded, abandoned, or committed in bounded, versioned, branching relations; this is neither a linear pipeline nor a truth ladder. Preserve upstream identity/version and relation/occurrence rather than parallel state. Not every relation endpoint needs a DTO, persistent node, canonical identity, or Owner-issued object.
5. **Every cognitive work occurrence is bounded.** Specify applicable Concern, read-basis, Role/Perspective, resource constraints, and stop/cancellation conditions. This does not require a `WorkScopeV1` artifact: first check Concern, Cognitive Grant, Working Envelope, CState/read-basis, and Task/runtime context. A Work Scope organizes work but owns no truth, admission, currentness, mutation, or execution; a new Workspace authority requires separate adjudication.
6. **Shared relation semantics, distributed recording, non-authoritative reconstruction.** Where semantically valid, forward formation, reverse provenance, and forward impact read the same logical information relationships recorded by bounded producers/Owners. A transformation feeding a canonical commitment preserves sufficient source, upstream artifact/version, occurrence, producer/model/config where relevant, temporal role, Role/Perspective/Concern where relevant, and authority refs for reconstruction. A relation query answers what was recorded, not what is authoritative now. `LINEAGE != AUTHORITY`; no central Graph or Lineage Truth Store follows from this rule.
7. **System semantics are not Domain Truth.** Temporal, Spatial, Identity, Reference, Version, and similar primitives/governance define shared representation and comparison semantics, not Domain state, currentness, or admission. `FIRST_CONSUMER != SYSTEM_OWNER`; `FIRST_IMPLEMENTER != DEFINITION_AUTHORITY`; `SYSTEM_SEMANTICS != DOMAIN_TRUTH`.
8. **Snapshot currentness is not effect currentness.** Distinguish latest input, current Field interpretation, cognitive read-basis version, active semantic product/hypothesis, current admitted Action, current effect eligibility, and continued execution eligibility. `READ_BASIS_VERSION != GLOBAL_WORLD_SNAPSHOT`: multiple Concerns reading one CState version do not establish a globally consistent instant across Owners. Cognition may use a permitted historical read-basis; execution must pass its effect-time Owner contract. Temporal coordinates never perform Owner requery.

#### Four derived implementation guards

- **Guard A — Traceability is not truth adjudication.** `FIRST_TRANSFORMATION_DIVERGENCE != FIRST_SEMANTIC_ERROR`. The earliest observable divergence may be a set of branches or indeterminate when records are missing; semantic-error attribution requires independent evidence, feedback, contract violation, observation, available ground truth, or explicit adjudication.
- **Guard B — Edges record, never create, authority outcomes.** `EDGE_RECORDS_AUTHORITY_OUTCOME; EDGE_NEVER_CREATES_AUTHORITY_OUTCOME`. Candidate relation vocabulary includes `PRODUCED_FROM`, `SELECTED_FROM`, `REVISED_FROM`, `ALTERNATIVE_TO`, and `BOUND_TO`; this is not a universal ontology or authorization API. `SUPERSEDES`, `ADMITTED_FROM`, and `EXECUTED_AS` only mirror facts already established by the relevant Owner. Avoid a generic `AUTHORIZED_FROM` that launders lineage into authorization. `DERIVED_FROM != CAUSED_BY` and `TRACE_PARENT != CAUSAL_PARENT`.
- **Guard C — Memory is selective sedimentation.** Keep ephemeral semantic product, retained diagnostic trace, durable operational state, and admitted long-term Memory separate. A recorded relation grants neither Memory admission nor truth status and does not require permanent payload retention.
- **Guard D — Minimum Sufficient Architecture.** Do not pre-build a Global Manager, Central Truth Store, global Ref Resolver, global Currentness Manager, globally writable Blackboard, Global Invalidation Bus, full-repository Event Sourcing, generic distributed coordination framework, or central Sedimentation/Lineage Graph authority. Escalate only for a concrete requirement not closable within bounded responsibility and lifecycle contracts.

Current World remains a derived view; Attention a working/selection facet; Hypothesis and Decision Candidate semantic products. Their types/refs do not require independent canonical stores. CState version remains a separately governed read-basis version, not a global world snapshot. None of this collapses Concern, Cognitive Grant, Working Envelope, Action, Safety, or Runtime Authorization authority. Preserve `LINEAGE_PRESERVATION != AUTHORITY_OWNERSHIP`, `LEGACY_REPRESENTATION_ALLOWED != LEGACY_AUTHORITY_ALLOWED`, and `CONTROLLED_WORLD != CONTROLLED_TRUTH`.

### CANONICAL_FACT_UPGRADE_GATE_V1

Apply this precondition before the existing Six-Law, in decision order:

1. **Prove the fact.** Name its independent System Question and downstream commitment/state. Ask: "If its independent identity is removed, can upstream refs + version + relation + occurrence represent the requirement without semantic loss?" If yes, return `DO_NOT_PROMOTE_TO_CANONICAL_FACT` unless another independently documented lifecycle/commitment need exists.
2. **Prove independent governance.** Identify the required identity, lifecycle/currentness (or terminal issuance), downstream use, and why a view, projection, handoff, serialization form, or existing canonical state cannot suffice.
3. **Then identify Semantic Owner and authority origin.** Show why that Owner may establish the fact and re-establish authoritative state from its canonical identity. Never invent an Owner first and use it to justify the fact.
4. **Apply existing governance.** Run WHO / WHY / REQUERY / ISSUANCE / PROJECTION / LEGACY and the applicable TEMPORAL authority check. Examine any new authority path; preserve Owner-requery, identity-issuance, projection-integrity, and legacy positive/negative-authority closure. This gate adds no new authority law and does not replace the Six-Law.

If the first two steps fail, classify the object as source/observation, transformation, view/projection, semantic product, execution record, or lineage/diagnostic record. Do not demote an already independent Owner fact merely because a relation graph can refer to it.

### NEW_AUTHORITY_STRUCTURE_GUARD_V1

Before adding an Owner, Manager, Registry, Store, or Resolver, identify its independent system responsibility and lifecycle; show why existing Owner boundaries cannot legally own it; prove it does not duplicate query/requery authority or centralize unrelated Domain Truth; and state its explicit negative authority boundary. If this cannot be shown, return `DO_NOT_CREATE_NEW_AUTHORITY_STRUCTURE`. A system-level definition contract alone does not imply system-level domain-state management.

### Stable development, frozen contract, and integration governance

This protocol governs development after the architecture rules above; it neither changes their eight core rules/four derived guards nor creates runtime authority. `LUNA_STABLE_BASELINE_V1` is a target, not an existing baseline.

| State | Meaning |
| --- | --- |
| `DEVELOPMENT` | Code may change within authorized scope; no stability promise. |
| `VERIFIED` | Required functional/contract verification has passed, but freeze/archive is incomplete. |
| `FROZEN` | GO, required source closure, local documentation, Notion where applicable, exact-path Git freeze, and receipt are complete for a module/phase/contract. |
| `STABLE_BASELINE` | A compatible set of frozen modules/contracts has passed required integration regression and has explicit integration approval as the source for future development. |

`GO != ENGINEERING_FROZEN`; `ENGINEERING_FROZEN != INTEGRATION_APPROVED`; `INTEGRATION_APPROVED != STABLE_BASELINE`. A phase freeze proves its bounded receipt, not integration of the full system. Integration requires compatible contract review and applicable verification before approval. Agent V0/V1 checks cannot grant GO or integration approval; preserve the existing V2 User Terminal and V3 ChatGPT decision boundary.

#### Frozen module and contract protection

Frozen does not mean unchangeable. It requires `CONTROLLED_REOPEN_PROTOCOL`:

`FROZEN → REOPEN REQUEST → ISOLATED BRANCH → IMPLEMENTATION → FOCUSED VERIFICATION → SENSITIVE REGRESSION → SOURCE CLOSURE → ARCHITECTURE / CONTRACT REVIEW` where applicable `→ FREEZE CANDIDATE → INTEGRATION APPROVAL → NEW FROZEN VERSION → NEW STABLE BASELINE` where applicable.

An isolated `feature/<scope>`, `fix/<scope>`, or `hotfix/<scope>` branch (or an approved equivalent naming policy) is required for future production-behavior work; a stable-baseline branch is not the ordinary development branch. Hotfix does not bypass verification. Before editing frozen code, record `SOURCE_BASELINE`, `CHANGE_BRANCH`, `CHANGE_REASON`, `AFFECTED_FROZEN_MODULES`, and `AFFECTED_FROZEN_CONTRACTS`. Classify `CONTRACT_CHANGE`, `AUTHORITY_CHANGE`, `CANONICAL_FACT_CHANGE`, `PUBLIC_INTERFACE_CHANGE`, and `MIGRATION_REQUIRED`. A reopened item cannot inherit the old GO as verification for changed behavior.

Freeze impact is two-dimensional: `FROZEN_PATH_INTERSECTION` and `FROZEN_CONTRACT_IMPACT`. The latter may be material without a frozen-file edit: changes to callers/consumers, canonical identity interpretation, authority origin, Owner requery, version, currentness, scope, lifecycle, effect-time, or legacy compatibility can change a frozen contract. Either material impact requires controlled reopen or explicit compatibility review before integration. `FROZEN_FILE_UNCHANGED != FROZEN_CONTRACT_UNCHANGED`.

Retain original freeze commits and receipts as historical evidence; never overwrite them. A new freeze/archive receipt records, where applicable: module/phase and version; source and parent baselines; freeze commit; exact path set and deterministic path-set hash; Canonical Facts, Owners, public contracts, and negative boundaries; dependencies and downstream consumers; verification evidence; known limitations; reopen conditions and migration notes; Notion receipt; and remote publication state. For a DOC_ONLY freeze, mark non-applicable fields explicitly rather than fabricate production facts.

#### LUNA_PRE_EXPANSION_STABILIZATION_MASTER_WORKLIST_V1

This is the single sequential STAB-00–STAB-07 worklist. Recording a future item is not authorization to execute it. At each item, stop, return evidence, and await ChatGPT adjudication and required User Terminal verification; no Agent may mark later items complete.

| Item | Bounded objective | Completion gate |
| --- | --- | --- |
| `STAB-00` | Finalize the eight core rules/four guards and stable-development, frozen-path/contract, branch, integration, and controlled-reopen governance; no production change. | Architecture rules final; stable-development and reopen protocols plus both freeze-impact guards defined. |
| `STAB-01` | Reconstruct auditable frozen module/contract inventory: responsibility, Owner/Final Authority, facts, contracts, negative boundaries, paths/receipt, dependencies/consumers, evidence, limitations, reopen triggers. Do not redesign merely because a module is old. | Frozen module and contract inventories complete; unknown critical freeze boundaries = 0. |
| `STAB-02` | Enumerate actual product/runtime/provider/effect entries; distinguish real product, controlled, synthetic, legacy, and non-effect paths. Stop on confirmed bypass before broad remediation. | Real and governed/legacy effect-entry counts known; authority bypass entry count = 0. |
| `STAB-03` | Audit actual Observation→Evidence→Field→CState/read-basis→reasoning→Envelope→Action→Safety→Authorization→effect projections without promoting every stage to fact. | Canonical identity/version/scope breaks, caller authority substitution, and legacy authority fallback counts = 0. |
| `STAB-04` | Classify critical reachable behavior as `PRODUCTION`, `CONTROLLED_RUNTIME`, `SYNTHETIC`, `CONTRACT_ONLY`, `LEGACY`, or `DEPRECATED`, especially Decision, Memory/Experience/Learning, Provider sessions/invocations, and controlled loops. | No unknown critical maturity; no synthetic/controlled path misrepresented as production; legacy authority ambiguity = 0. |
| `STAB-05` | Audit owner-local query/mutation/invalidation/requery namespaces, prioritizing Action mutation; fix only confirmed defects under separate authorization. | Confirmed namespace conflicts, query–mutation identity mismatches, and Owner-requery–mutation mismatches = 0. |
| `STAB-06` | Select applicable py_compile, focused/sensitive regression, controlled checks, source closure, governance pre/postflight, and `git diff --check`; Agent prepares commands but does not execute authoritative terminal verification. Preserve the known `tests/freeze` external `luna_badge_v1_2` NOT_EXECUTED exception unless environment changes. | Applicable failures = 0; source closure and applicable governance pre/postflight PASS; unexplained critical NOT_EXECUTED = 0. |
| `STAB-07` | Integrate compatible frozen scope and create `LUNA_STABLE_BASELINE_V1` with local/Notion governance, exact-path Git freeze, archive receipt, baselines, path set/hash, evidence, limitations, and publication state; no push without separate authorization. | STAB-00–06 adjudicated complete; stable baseline created and engineering freeze/integration approval recorded. |

Temporal P1-01A implementation must not start before `LUNA_STABLE_BASELINE_V1` is established; afterward it is the next engineering-development candidate, not an automatic transition. For the current governance-edit item, only STAB-00 is authorized; STAB-01 remains pending and unauthorized.

### Finding taxonomy mapping

The Six-Law maps evidence-backed findings as follows. The existence of a taxonomy entry does not create a finding; each finding requires source evidence.

| Six-Law question | Finding classes |
| --- | --- |
| WHO | `SEMANTIC_OWNER_DRIFT`, `MULTIPLE_FINAL_AUTHORITY` |
| WHY | `AUTHORITY_ORIGIN_GAP`, `AUTHORITY_LAUNDERING` |
| REQUERY | `OWNER_REQUERY_CLOSURE_GAP`, `OWNER_NAMESPACE_LEAK`, `CALLER_SELECTED_TRUTH_CONTEXT` |
| ISSUANCE | `CANONICAL_IDENTITY_ISSUANCE_CLOSURE_GAP` |
| PROJECTION | `CROSS_OWNER_PROJECTION_IDENTITY_LOSS`, `SKIPPED_AUTHORITY_PROJECTION`, `CROSS_OWNER_PROJECTION_VERSION_DRIFT` |
| LEGACY | `COMPATIBILITY_AUTHORITY_LEAK`, `LEGACY_CANONICAL_AUTHORITY`, `LEGACY_DENIAL_AUTHORITY` |

### Current R02 reference examples

The following are current R02 architecture references, not an ENGINEERING_FROZEN declaration:

- Action Admission: positive Owner-Requery Closure reference.
- Concern supersede: Canonical Identity Issuance Closure defect/remediation reference.
- Runtime Scope v2: Cross-Owner Projection Integrity reference.
- Legacy `parent_cognitive_problem_ref` and `source_state_ref`: Legacy Authority Extinction reference.
- `MODEL_X2`: Lineage Preservation versus Authority Ownership reference.

These examples remain subject to the current R02 source-closure and terminal-verification process.

## R02 final technical evidence reference

The bounded GPT6-R02 source closure is recorded in:

`docs/architecture/governance/luna_repository_rebaseline_v1/gpt6_global_audit_r02_final_closure_go_v1.md`

The record is evidence consolidation, not a Git freeze declaration. Its final
terminal evidence is:

```text
R02_TECHNICAL_GO=YES
R02_SOURCE_CHANGE_STOP=LOCKED
R02_ENGINEERING_FROZEN=NO
R02_FOCUSED_REGRESSION=108/108 PASS
R02_SENSITIVE_REGRESSION=146/146 PASS
R02_TOTAL_EXECUTED=254/254 PASS
PY_COMPILE=PASS
GIT_DIFF_CHECK=PASS
NEW_P0_FINDINGS=NONE
NEW_P1_FINDINGS=NONE
BLOCKING_FINDINGS=NONE
tests/freeze=NOT_EXECUTED (external luna_badge_v1_2 dependency)
```

The R02 record preserves the multi-owner authority graph, Canonical Fact
Governance Six-Law evidence, MODEL_X2 runtime structure, Runtime Scope v2
legacy extinction rules, known P2 deferred hardening, and the exact Notion
03/03.7/03.8 synchronization plan. It does not claim that all repository
tests, provider effects, production execution, or engineering freeze are
complete.

## Governance Layers

```text
L0 Constitution Layer
  immutable cognitive and authority principles
        ↓
L1 Protocol Governance Layer
  contract identity, input/output compatibility, traceability, boundary rules
        ↓
L1 Permission / Admission Layer
  request eligibility, permission reference, output admission eligibility
        ↓
L1 Capability Registry Layer
  capability identity, owner, lifecycle, declared dependencies
        ↓
L1 Diagnostics Layer
  contract drift, validation status, boundary violations, lifecycle signals
        ↓
Governed Capability Execution
```

## L0 Constitution Layer

L0 freezes principles that no Capability may override:

- Observation/Evidence/Model output is not Fact by default.
- Candidate is not Fact, Decision, Action, State, Memory, or Value judgment.
- Reducer remains the only Field State mutation authority.
- External provider/model identity is provenance, never a Cognitive Entity by itself.
- Hive, Experience, Cognitive Analysis, and external models cannot bypass governed admission or write State directly.

## L1 Protocol Governance Layer

L1 owns Contract references and compatibility rules. For A3, this includes candidate-only input/output symmetry, allowed primitive types, required evidence/context/provenance/trace references, stable Negative Guard inventory, and serializer-compatible output evidence. Protocol Governance does not execute a Capability or create a new A3-specific protocol authority.

## L1 Permission / Admission Layer

L1 owns whether a future request may proceed and whether a future output may enter a separately governed next layer. It references the existing Permission & Admission route; no Capability may invent a runtime-specific permission model. A candidate validation result is not an admission grant.

## L1 Capability Registry Layer

L1 owns Capability identity, owner, lifecycle, dependencies, and manifest/record governance. A3 Translation and Runtime mappings remain candidate/reference-only until a separately authorized L1 registration phase writes the existing Registry.

## L1 Diagnostics Layer

L1 owns reporting of contract drift, validation outcomes, permission/admission status, boundary violations, and lifecycle status through the existing Protocol Manager and Permission/Admission diagnostics route. It does not perform a health Runtime in this phase.

## Current A3 Placement

Negative Guards and forbidden operations are L0-derived L1 boundary rules. Runtime flags are serialized diagnostic evidence. Candidate/Fact separation is a constitutional principle enforced through L1 Contract and Admission checks. Provenance and trace are L1 Protocol Traceability requirements. No A3 asset becomes an independent Registry, Permission Manager, Admission system, or Diagnostics system.
