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
