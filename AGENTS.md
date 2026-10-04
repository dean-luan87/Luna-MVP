# Luna Repository Agent Instructions

These instructions are the persistent repository-level guidance for Codex and other engineering agents working in Luna-Core.

## Mandatory governance pre-read

Before any Luna phase, read the applicable phase instruction and these repository governance assets:

- `docs/architecture/governance/luna_engineering_execution_and_verification_governance_v1/luna_engineering_phase_execution_role_standard_v1.md`
- `docs/architecture/governance/luna_engineering_execution_and_verification_governance_v1/luna_phase_verification_execution_authority_standard_v1.md`
- `docs/architecture/governance/luna_engineering_execution_and_verification_governance_v1/luna_execution_mode_verification_authority_matrix_v1.json`
- `docs/architecture/governance/luna_engineering_execution_and_verification_governance_v1/luna_phase_instruction_required_fields_standard_v1.json`
- `docs/architecture/governance/luna_engineering_execution_and_verification_governance_v1/luna_phase_instruction_template_v1.md`
- `docs/architecture/governance/luna_engineering_execution_and_verification_governance_v1/luna_runner_and_verifier_naming_standard_v1.md`
- `docs/architecture/governance/luna_engineering_execution_and_verification_governance_v1/luna_verification_status_registry_v1.json`
- `docs/architecture/governance/luna_engineering_execution_and_verification_governance_v1/luna_verification_failure_classification_and_remediation_standard_v1.json`
- `docs/architecture/governance/luna_engineering_execution_and_verification_governance_v1/luna_agent_product_development_compliance_contract_v1.json`

Do not rely on chat history or editor memory as the sole source. Identify the Execution Mode before editing, respect V0/V1/V2/V3 authority, never run the Final Phase Verifier unless governance explicitly changes that rule, never declare GO, and stop at `WAITING_FOR_USER_TERMINAL_VERIFICATION` or the applicable blocked status.

## Supreme design priority

```text
SUPREME_DESIGN_PRIORITY=GOAL_DRIVEN_STRUCTURAL_PROJECTION
```

The formal name is `Goal-Driven Structural Projection`. It is Luna's highest design criterion above local implementation convenience, the smallest current diff, single-module elegance, fast test success, and historical implementation inertia. It does not override Safety, factual truth, explicit user constraints, or non-negotiable system boundaries.

The canonical architecture definition is in:

`docs/architecture/governance/luna_governance_core_architecture_v1.md`

## Required observation before important design

Before making an important architecture, new module, Canonical Artifact, Authority change, model integration, algorithm integration, provider integration, cross-owner dependency, or major refactor decision, perform:

```text
GOAL_DRIVEN_STRUCTURAL_PROJECTION_OBSERVATION
```

The observation must answer:

- `GOAL_ALIGNMENT`: which Luna long-term goal, product capability, business model, or real user value this serves;
- `CURRENT_STAGE_REQUIREMENT`: the real requirement and scale now;
- `FUTURE_SCENARIOS_PROJECTED`: next-stage and target-scale growth in models, algorithms, providers, capabilities, multimodal input, continuous state, replacement, concurrency, and operation;
- `CANDIDATE_STRUCTURES`: materially different candidate structures considered;
- `STRUCTURAL_ADVANTAGES` and `STRUCTURAL_DISADVANTAGES`: including current and future cost;
- `SCALING_BEHAVIOR`: coupling and failure propagation as scale grows;
- `CORE_SEMANTIC_STABILITY`: whether Brain, core semantic contracts, Canonical Owners, and lifecycle models remain stable;
- `AUTHORITY_STABILITY`: whether Authority remains correctly owned and re-queryable;
- `MODEL_ALGORITHM_EXTENSION_IMPACT`: whether new models and algorithms extend edge capability rather than rewrite core semantics;
- `FAILURE_MODES`: structural failure and migration risks;
- `OVERDESIGN_RISK` and `UNDERDESIGN_RISK`;
- `MINIMUM_SUSTAINABLE_STRUCTURE`;
- `GOAL_DRIVEN_STRUCTURAL_PROJECTION_RESULT`.

If an item is not applicable, state why. Do not mechanically fill the fields.

## Canonical Fact Governance Six-Law

`Goal-Driven Structural Projection` remains the supreme design priority. Directly beneath it, Luna applies the `Canonical Fact Governance Six-Law` to every object that may be a Canonical Fact.

The Six-Law is mandatory at design time, review time, and change time:

```text
DESIGN_TIME_SIX_LAW_CHECK=MANDATORY
REVIEW_TIME_SIX_LAW_CHECK=MANDATORY
CHANGE_TIME_SIX_LAW_RECHECK=MANDATORY
```

First determine:

```text
IS_CANONICAL_FACT=YES/NO
```

Do not promote an object merely because it has a dataclass, status, lifecycle field, cross-module use, or persistence. Candidate, DTO, mechanical projection, transport object, evaluation result, and execution record remain non-canonical unless they answer an independent semantic question, have a Semantic Owner and Final Authority, have an independent lifecycle/currentness, and matter semantically to downstream consumers.

For `IS_CANONICAL_FACT=YES`, apply all six laws:

1. `CANONICAL_OWNERSHIP_LAW` — one Semantic Owner and one Final Authority; no caller, orchestrator, or mechanical layer may become an implicit owner.
2. `AUTHORITY_ORIGIN_LAW` — the Owner must have an independent, traceable basis for establishing, admitting, mutating, or declaring currentness; caller-positive predicates cannot be laundered into truth.
3. `OWNER_REQUERY_CLOSURE_LAW` — canonical identity plus Owner-internal state must uniquely re-establish currentness, validity, and admission without caller-selected profile, namespace, truth selector, or implicit authority context. Explicit context may only be a consistency assertion or diagnostic constraint.
4. `CANONICAL_IDENTITY_ISSUANCE_CLOSURE_LAW` — every Owner transition that creates a new canonical identity must establish Owner state and Owner resolution before the identity is externally projectable. Existing transitions include admission, version formation, refresh, supersession, replacement, renewal, and re-admission when present.
5. `CROSS_OWNER_PROJECTION_INTEGRITY_LAW` — identity, version, scope, and required lineage must survive cross-owner projection without reconstruction, parsing, fallback, or authority transfer. `LINEAGE_PRESERVATION != AUTHORITY_OWNERSHIP`.
6. `LEGACY_AUTHORITY_EXTINCTION_LAW` — legacy representation may remain for compatibility, diagnostics, or history, but legacy authority must be absent in both positive and denial paths. Legacy data cannot authorize, deny, establish currentness/admission/validity, substitute canonical identity, or override canonical truth.

The mandatory gate for an important Canonical Fact design or audit is:

```text
IS_CANONICAL_FACT=
WHO: OWNER= / FINAL_AUTHORITY=
WHY: AUTHORITY_ORIGIN=
REQUERY: CAN_OWNER_REQUERY_FROM_CANONICAL_IDENTITY= / CALLER_TRUTH_CONTEXT_REQUIRED=
ISSUANCE: IDENTITY_PRODUCING_TRANSITIONS= / ISSUANCE_REQUERY_CLOSURE=
PROJECTION: CROSS_OWNER_PROJECTIONS= / IDENTITY_VERSION_SCOPE_PRESERVED= / AUTHORITY_TRANSFERRED=
LEGACY: LEGACY_REPRESENTATION_EXISTS= / LEGACY_CAN_AUTHORIZE= / LEGACY_CAN_DENY= / LEGACY_CAN_CHANGE_CURRENTNESS=
SIX_LAW_RESULT=PASS/FAIL/NOT_APPLICABLE
```

This gate is required before and during any new Canonical Artifact, Owner, Authority, lifecycle state, version model, admission model, cross-owner projection, authority migration, compatibility migration, or major runtime architecture change. It must be re-run whenever an existing Canonical Fact's identity, owner, authority, lifecycle, projection, or legacy compatibility changes. Small local edits that do not affect these dimensions need not emit the full gate; the agent must state why it is not applicable when ambiguity exists.

Required important-design output fields are:

```text
CANONICAL_FACT_PRECONDITION=
WHO=
WHY=
REQUERY=
ISSUANCE=
PROJECTION=
LEGACY=
SIX_LAW_RESULT=
```

The architecture definitions and finding taxonomy are maintained in `docs/architecture/governance/luna_governance_core_architecture_v1.md`. This persistent instruction does not grant GO, override Safety or factual truth, or authorize speculative Managers, Registries, Governance Layers, Artifacts, or core model-specific coupling.

## Design hierarchy and minimum sufficient architecture

Use this order for significant design:

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

Goal-Driven Structural Projection determines where the structure should grow. Minimum Sufficient Architecture determines how much to build now. Do not use future projection to justify speculative Managers, Registries, Governance Layers, Artifacts, or model-specific core coupling.

## Future architecture design rules

The eight core design rules and four derived implementation guards in `docs/architecture/governance/luna_governance_core_architecture_v1.md` are mandatory beneath the Supreme Design Principle and alongside the Six-Law. They govern future proposals; they do not assert a Workspace, Sedimentation Graph, or Lineage Spine is implemented.

Core rules for design and review:

1. Derive structure from Luna's product/system question and projected scale, not current files, DTOs, models, providers, or convenience.
2. A semantic stage, type, ref, ID, module, persistence, or candidate does not itself establish a Canonical Fact.
3. Prove an independent commitment/lifecycle first. If upstream refs + version + relation + occurrence suffice, `DO_NOT_PROMOTE_TO_CANONICAL_FACT`; determine an Owner only after proving the fact.
4. Prefer bounded, versioned, branching information relationships over parallel copied state. Not every endpoint needs a DTO, persisted node, canonical identity, or Owner.
5. Bound each cognitive work occurrence as applicable, but do not infer a `WorkScopeV1` artifact or Workspace authority. Check Concern, Cognitive Grant, Working Envelope, CState/read-basis, and Task/runtime context first.
6. Share logical formation/provenance/impact relation semantics through distributed recording, never a central Truth Store. Relation queries do not establish current authority; `LINEAGE != AUTHORITY`.
7. System primitives define shared semantics, not Domain Truth: `FIRST_CONSUMER != SYSTEM_OWNER`; `FIRST_IMPLEMENTER != DEFINITION_AUTHORITY`; `SYSTEM_SEMANTICS != DOMAIN_TRUTH`.
8. Keep read-basis, Field, semantic product, Action, effect-time, and continued-execution currentness distinct. `READ_BASIS_VERSION != GLOBAL_WORLD_SNAPSHOT`; shared CState version does not establish a global instant.

Derived guards: (A) first observable transformation divergence is not first semantic error; independent evidence/adjudication is required. (B) `EDGE_RECORDS_AUTHORITY_OUTCOME; EDGE_NEVER_CREATES_AUTHORITY_OUTCOME`; lineage cannot authorize, admit, establish currentness, or execute. (C) Ephemeral product, retained trace, durable operational state, and admitted long-term Memory stay separate. (D) Default to Minimum Sufficient Architecture, not global Managers, Registries, Resolvers, Blackboards, event sourcing, or central graph authority.

Classify each proposed artifact as `SOURCE / OBSERVATION`, `TRANSFORMATION`, `VIEW / PROJECTION`, `SEMANTIC PRODUCT`, `CANONICAL COMMITMENT / STATE`, `EXECUTION RECORD`, or `LINEAGE / DIAGNOSTIC RECORD`. Current World is a derived view, Attention a selection facet, Hypothesis and Decision Candidate semantic products; their existing types/candidates require no independent canonical stores. CState version remains an independently governed read-basis, not a global world snapshot. Do not collapse Concern, Grant, Envelope, Action, Safety, or Runtime Authorization authority.

Before promotion, apply `CANONICAL_FACT_UPGRADE_GATE_V1` in fact → independent identity/lifecycle → Owner/authority → Six-Law/TEMPORAL order. Before any new Owner/Manager/Registry/Store/Resolver, apply `NEW_AUTHORITY_STRUCTURE_GUARD_V1`. Check information, identity, Owner, authority, and lifecycle duplication; lineage loss; and legacy **positive and negative** authority residue. Changed transformations feeding canonical commitments must preserve reconstructable upstream artifact/version, occurrence, producer/model/config, temporal role, Role/Perspective/Concern, and authority refs where relevant. Prefer the smallest structure preserving semantic responsibility, lifecycle, identity, authority, lineage, and future extensibility. These rules grant no runtime or verification authority.

## Stable development and freeze discipline

The canonical `LUNA_PRE_EXPANSION_STABILIZATION_MASTER_WORKLIST_V1` and stable-development protocol are in `docs/architecture/governance/luna_governance_core_architecture_v1.md`. Execute STAB-00 through STAB-07 sequentially, only when the current item is explicitly authorized. Stop after each item for ChatGPT adjudication and required User Terminal verification; do not self-complete or start a later item. The planned `LUNA_STABLE_BASELINE_V1` is not established by documenting this protocol.

Keep `DEVELOPMENT`, `VERIFIED`, `FROZEN`, and `STABLE_BASELINE` distinct: `GO != ENGINEERING_FROZEN`, `ENGINEERING_FROZEN != INTEGRATION_APPROVED`, and `INTEGRATION_APPROVED != STABLE_BASELINE`. A frozen module or contract may change only through controlled reopen. An original freeze commit and receipt remain immutable historical evidence; hotfixes do not bypass verification.

Future production-behavior feature, fix, and hotfix work requires an isolated branch, not ordinary development on a stable-baseline branch. Before modifying frozen code, record `SOURCE_BASELINE`, `CHANGE_BRANCH`, `CHANGE_REASON`, `AFFECTED_FROZEN_MODULES`, and `AFFECTED_FROZEN_CONTRACTS`; assess contract, authority, Canonical Fact, public-interface, and migration impact. Check both `FROZEN_PATH_INTERSECTION` and `FROZEN_CONTRACT_IMPACT`. An untouched frozen file does not prove its contract is unchanged: caller/consumer assumptions, identity, authority origin, Owner requery, version, currentness, scope, lifecycle, effect-time, and legacy semantics may change elsewhere. Material impact requires controlled reopen or compatibility review before integration.

The controlled path is reopen request → isolated branch → implementation → focused verification → sensitive regression → source closure → architecture/contract review where applicable → freeze candidate → integration approval → new frozen version → new stable baseline where applicable. Verification and integration approval are separate. Preserve exact-path freeze/archive receipts, evidence, limitations, and remote-publication state; never overwrite prior receipts.

## Scope and verification boundaries

- Preserve existing dirty work unless the active phase explicitly authorizes a change.
- Do not modify unrelated modules or cross a phase boundary.
- Keep external models, providers, and algorithms at the edge unless a separately governed semantic contract gives them authority.
- Candidate, projection, provenance, and transport objects must not be promoted into Canonical Truth without an independent semantic question, owner, lifecycle, and authority contract.
- The `Canonical Fact Governance Six-Law` is a standing design and review gate. Current R02 examples remain architecture references pending final closure; do not describe dirty source as frozen or silently convert audit evidence into a final GO decision.
- Notion changes require explicit authorization separate from local repository edits.

The Agent may perform only checks authorized by the active Execution Mode. V0/V1 results never grant final GO. V2 is User Terminal authority and V3 is ChatGPT authority.
