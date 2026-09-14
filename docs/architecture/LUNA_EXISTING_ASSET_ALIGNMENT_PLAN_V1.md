# Luna Existing Asset Alignment Plan v1

## 1. Phase Position

- Phase: `Phase-A1.7-Luna-Existing-Asset-Alignment-Planning-v1-001`
- Execution Mode: Planning Only
- Constitutional references:
  - `docs/architecture/LUNA_ENGINEERING_ARCHITECTURE_CONSTITUTION_V1.md`
  - `docs/architecture/LUNA_CANONICAL_TERMINOLOGY_REGISTRY_V1.md`
- Scope: establish formal positions for existing assets in the future Cognitive Architecture

This plan is an alignment map, not a refactor plan. It creates no code, file rename, registry change, baseline change, lifecycle change, or migration execution.

## 2. Coexistence Model

Luna's historical engineering path and Cognitive Architecture coexist through explicit boundaries:

```text
Historical path
Perception -> Midplatform -> Task -> Execution

Canonical Cognitive Architecture
External organs -> Evidence -> Cognitive Flow -> Field -> Understanding
                  -> Decision Candidate -> Action Governance
```

The historical path supplies governed capabilities and execution boundaries. The Cognitive Architecture supplies the language and ownership of understanding. Neither path silently replaces the other.

## 3. Alignment Matrix

| Current Module | Current Position | Canonical Position | Future Role | Alignment Requirement | Migration Priority | Planning Status |
| --- | --- | --- | --- | --- | --- | --- |
| Field Event Admission | Event Governance; admits/rejects/defer candidates with source, evidence, trace, and temporal checks | L1/L2 boundary: **Cognitive Admission Boundary** | Gate from Candidate Event to Admitted Event for Field Kernel use | Preserve current admission statuses and trace/evidence/source semantics; map input/output terminology to Canonical Observation, Evidence, Candidate, and Admitted Event without changing behavior | P0 — before A2 contract freeze | **Keep / Align** |
| Field State Reducer | State Mutation Authority; consumes admitted events and emits candidate state | L1 Field Kernel: **Field Kernel Mutation Authority** | Sole reducer of Admitted Event into candidate Field State | Preserve singular mutation authority, temporal/provenance behavior, and candidate-only output; A2 must adapt to it rather than create a competing reducer | P0 — mandatory A2 dependency | **Core Asset** |
| Field State Read Model | Read Projection | L1 Field Kernel: **World Representation Query Layer** | Read-only query/projection of current Field representation for analysis and delivery candidates | Preserve read-only semantics; define future Field Snapshot as a compatible read surface, not a database bypass or second state store | P0 — A2 snapshot/query boundary | **Keep** |
| Task Manager | Task Governance; lifecycle, confirmation, safety, owner gates | L2: **Action Execution Governance** | Receives future Decision/Exploration Candidates at explicit authorization boundary | Keep cognitive truth separate from task authority; no direct Cognitive Analysis-to-execution path | P1 — after A2, before action integration | **Keep Boundary** |
| Model Manager | Model Asset Governance | L2/L3: **External Capability Governance** | Governs model/provider capability access as external organs | Rename conceptually, not physically, only after an approved compatibility plan; preserve provider governance and forbid Fact/Decision authority | P1 — before real capability integration | **Keep** |
| Observation Attention | Observation Scheduling; priority and follow-up route candidates | L1/L3 support: **Cognitive Attention Support** | Allocates observation resources and proposes bounded follow-up capability routes | Upgrade contracts from region/model-route emphasis toward Information Gap and Exploration Request support; remain non-factual and non-executing | P2 — after A3 protocol work | **Upgrade Candidate** |
| Human Correction Layer | Human Feedback and correction/review candidates | L1/L2: **Human Review and Learning Signal Source** | Supplies correction evidence, review signals, and later Experience review inputs | Preserve no-overwrite/no-ground-truth boundary; align correction records to Evidence and Outcome/Experience review protocols later | P2 — after A3/A5 protocols | **Keep** |
| Situation Understanding Model | External Understanding Capability; emits uncertainty, missing information, case and capability hints | L3 attachment to L1: **Teacher / Advisor** | Proposes analysis inputs; may support Hypothesis, Difference Point, and Information Gap candidates | Decompose future outputs into canonical protocols; prohibit final understanding, Fact, Decision, or Action claims | P2 — after A3 contracts | **Boundary Defined** |
| Evidence Chain | Source chain, evidence lifecycle, acceptance/non-substitution governance | L1/L2: **Evidence and Provenance Substrate** | Common lineage basis for Observation, Evidence, Admission, State, Outcome, and Experience | Reuse source-chain and non-substitution rules; align terms to Canonical Evidence without treating evidence as truth | P0 — A2 provenance requirement | **Keep / Align** |
| Temporal Validity | Event time assessment, expiry, deferral, duplicate/order checks | L1 Field Kernel temporal boundary | Governs temporal eligibility before state reduction | Reuse as admission-side temporal authority; do not duplicate timestamp semantics inside A2 Field Kernel | P0 — mandatory A2 dependency | **Keep / Align** |
| Case Library | Reviewed situation-case records with provenance and candidate-only handling | L1 Experience System precursor | Future Experience Episode/Kernel substrate | Do not relabel cases as Experience automatically; define episode/outcome/review compatibility in A5 | P3 — Experience System phase | **Upgrade Candidate** |
| OCR / SLAM / Vision / Audio / ASR / TTS | Perception, expression, and model capabilities | L3 **External Capability Layer** | External organs and capability attachments | Route all output through Observation/Evidence/Admission contracts; no direct Field State or decision mutation | P1 — before real capability connection | **Future Adapter Role** |

## 4. Boundary Judgments

### 4.1 Field Event Admission

Field Event Admission is jointly located at the L1/L2 boundary. Its meaning is cognitive because it gates Candidate Event into Admitted Event, the only event form that may reach Field State mutation. Its operating controls are Midplatform-governed because admission requires protocol, temporal, trace, and diagnostic discipline.

It must not be absorbed wholly into either a generic Midplatform service or a Field Kernel reducer. Its boundary role is the gate itself.

### 4.2 Field State Reducer

Field State Reducer is the core asset for A2. Its unique authority must remain intact:

```text
Admitted Event -> Field State Reducer -> Field State candidate
```

Cognitive Analysis, external models, Observation Attention, and any future Field Kernel orchestration must not bypass this path or write state directly.

### 4.3 Read Model

The Read Model is formally positioned as the World Representation Query Layer. It is not a generic database query utility. Future cognitive modules should read a governed current-world projection through this layer rather than reach into a storage or reducer-internal representation.

### 4.4 Model Manager and External Models

Model Manager's future architectural name is External Capability Governance. This is a conceptual alignment only; existing names and files remain unchanged in this phase. OCR, SLAM, LLM, VLM, audio, map, and expression capabilities are organs. Their outputs are Evidence/Observation Candidates, never self-authorized facts, understanding, decisions, or action commands.

### 4.5 Observation Attention

Observation Attention is a high-value future bridge to Cognitive Attention Support. Its current priority and follow-up route candidates should later become inputs to Information Gap and Exploration Request protocols. It must not itself infer facts, select a final cognitive explanation, execute a model route, or update Field State.

## 5. A2 Field Kernel Reuse Decision

The A2 Field Kernel must reuse existing core assets by contract, not recreate their authority:

| A2 concern | Existing asset to reuse | A2 rule |
| --- | --- | --- |
| Candidate-event eligibility | Field Event Admission + Temporal Validity | accept only Admitted Event candidates; do not duplicate admission logic |
| Field State mutation | Field State Reducer | use adapter/composition; do not create another state mutation owner |
| Current-world query | Field State Read Model | expose compatible Field Snapshot/read contracts; do not query storage directly |
| Provenance and source lineage | Evidence Chain | preserve source/evidence/trace semantics across Field Identity, Unit, Relation, State, and Snapshot |
| Action boundary | Task Manager | A2 emits no Decision or Action; Task Manager remains downstream and out of scope |

Therefore A2 can define Field Identity, Field Unit, Field Relation, and Field Snapshot as a composition/snapshot surface around the existing Field State authority. It must not replace the Reducer or add a parallel world-state store.

## 6. Alignment Work Packages (Planning Only)

| Priority | Work package | Required result | Explicitly excluded |
| --- | --- | --- | --- |
| P0 | Admission-to-Field contract alignment | canonical mapping of Observation/Evidence/Candidate/Admitted Event and temporal provenance | code or protocol mutation |
| P0 | Reducer/Read Model A2 compatibility note | Field Kernel adapter and snapshot ownership boundaries | new reducer or storage layer |
| P0 | Evidence/temporal preservation note | required provenance, source chain, trace and time fields across A2 | fact admission expansion |
| P1 | External capability governance alignment | Model Manager/organ vocabulary mapping and output-candidate boundary | model integration |
| P1 | Task/action governance alignment | Decision Candidate to Task Manager handoff preconditions | action execution |
| P2 | Attention and Situation Understanding alignment | Information Gap / Exploration / Teacher-Advisor compatibility plan | analysis implementation |
| P2 | Human Correction alignment | correction evidence to review/learning signal mapping | automatic learning or truth promotion |
| P3 | Case Library to Experience System plan | Episode/Kernel compatibility and review criteria | experience implementation |

## 7. Permanent Non-Actions for This Plan

- Do not modify code or refactor modules.
- Do not rename files, modules, capability IDs, registries, manifests, baselines, or lifecycles.
- Do not execute migration.
- Do not change the existing Reducer, Read Model, Task Manager, or model/provider behavior.
- Do not infer that alignment status grants runtime authority, production status, Fact authority, or decision authority.

## 8. Current Phase Stop Point

This document completes A1.7 planning and awaits human review. A2 Field Kernel implementation may start only after the alignment decisions, particularly the A2 reuse decision, are reviewed and explicitly authorized. This plan makes no final declaration.

