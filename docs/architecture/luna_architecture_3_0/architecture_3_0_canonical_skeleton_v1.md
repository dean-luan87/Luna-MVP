# Luna Architecture 3.0 — Canonical Skeleton v1

ARCHITECTURE_ID=LUNA_ARCHITECTURE_3_0_CANONICAL_SKELETON  
STATUS=FROZEN  
FREEZE_DATE=2026-09-30  
FREEZE_BASIS=EXPLICIT_HUMAN_CONSTITUENT_FREEZE_DECISION  
CONSTITUTION=LUNA_ENGINEERING_CONSTITUTION_3_0  
CONSTITUTION_STATUS=FROZEN

This document is the repository-side canonical representation of the frozen Architecture 3.0 Skeleton. It records semantic classification and boundary doctrine; it does not freeze implementation classes, APIs, schemas, runtime behavior, or subordinate connection-family counts.

## 1. General model

The Constitution is the supreme normative boundary and is not an architecture axis.

```text
Constitution
    bounds
Semantic / System Axis × Governance Axis
    connected by
Contracts / Mappings / Protocols / Relations
    realized by
Implementation and observed through Runtime / Evidence
```

- Semantic / System Axis: `WHERE DOES IT BELONG?`
- Governance Axis: `WHAT GOVERNS IT?`
- Connection mechanisms: `HOW IS IT CONNECTED?`
- Authority model: `WHO MAY DECIDE / MUTATE / AUTHORIZE IT?`

Connection mechanisms are not a third axis.

## 2. Canonical Domains

DOMAIN_COUNT=14

| ID | Domain |
|---|---|
| CD-C01 | Governed Identity & Semantic Role |
| CD-C02 | Capability & Organ Declaration |
| CD-C03 | Observation Need & Cognitive Requirement |
| CD-C04 | Execution Request Formation |
| CD-C05 | Permission & Effect Authorization |
| CD-C06 | Resource & Execution Readiness |
| CD-C07 | Organ Runtime & Native Capability Execution |
| CD-C08 | Observation Admission & Evidence |
| CD-C09 | Field & World Information Assimilation |
| CD-C10 | Cognitive State & Local Reality Reasoning |
| CD-C11 | Task Organization |
| CD-C12 | Decision & Action Intent |
| CD-C13 | Global Policy, Safety & Action Admission |
| CD-C14 | Memory & Experience |

## 3. Non-Domain surfaces

- `AS-CW`: Current World, a governed Projection / Read Model. It is not a Canonical Domain and does not own external world truth.
- `AS-CONN`: Contracts, Mappings, Protocols, Relations, Resolution, Routing and Binding. These are connection mechanisms, not a Domain.

Lifecycle, Currentness, Confidence and Protocol are not Canonical Domains. Routing and Binding are not Canonical Domains and do not authorize execution.

## 4. Governance Dimensions

GOVERNANCE_DIMENSION_COUNT=16

| ID | Dimension |
|---|---|
| GD-01 | Temporal |
| GD-02 | Validity |
| GD-03 | Currentness |
| GD-04 | Lifecycle |
| GD-05 | State Transition |
| GD-06 | Coordinate |
| GD-07 | Spatial Frame |
| GD-08 | Identity |
| GD-09 | Reference |
| GD-10 | Provenance / Lineage |
| GD-11 | Confidence |
| GD-12 | Uncertainty |
| GD-13 | Truth / Admission |
| GD-14 | Version |
| GD-15 | Compatibility |
| GD-16 | Failure / Degradation / Unknown |

Governance Dimension != Domain != Manager != global mutable state.

Required distinctions include:

- Temporal != Validity != Currentness
- Coordinate != Spatial Frame
- native confidence != Evidence confidence != cognitive confidence
- same timestamp != same temporal meaning
- latest != current; valid != current; unexpired != current
- version match != compatibility
- UNKNOWN != FALSE; INSUFFICIENT != INVALID; CONFLICT != ERROR
- PREPARED != ALLOCATED != AVAILABLE != AUTHORIZED
- EMPTY_SUCCESS != FAILURE; NOT_CURRENT != INVALID; DEGRADED != FAILED

## 5. Connection doctrine

The four semantic connection classes are frozen:

`CONTRACT`, `MAPPING`, `PROTOCOL`, `RELATION`

They are not Domains and not a third axis.

```text
SEMANTIC_FLOW != AUTHORITY_FLOW != CHANNEL_PROTOCOL_FLOW
```

Default connection behavior is `AUTHORITY_TRANSFER=NO`. Mapping and Relation do not inherently carry authority. Binding is a semantic execution-selection basis, not an authorization basis. Transport does not create semantic or runtime authority.

The semantic classes are frozen, but subordinate family counts are not:

```text
FREEZE_CONNECTION_FAMILY_SEMANTIC_CLASSES=YES
FREEZE_CONNECTION_FAMILY_EXACT_COUNTS=NO
CONNECTION_MECHANISM_CLASS_COUNT=4
AUDIT_CANDIDATE_COUNTS=CONTRACT:13,MAPPING:15,PROTOCOL:4,RELATION:8
```

Mappings and Relations do not use a generic authority-input category.

## 6. Authority and execution boundaries

- Identity != Permission.
- Need != Request != Admission.
- Declared != Compatible != Routable != Available != Authorized.
- Request Formation != Entry Admission != Runtime Effect Authorization.
- Prepared != Allocated != Available != Authorized.
- Decision != Authorization; Intent != Permission.
- Authority to authorize != authorization to execute.

For `CD-C05 → CD-C07`:

```text
AUTHORITY_FLOW=AUTHORIZATION_BASIS
AUTHORITY_TRANSFER=NO
EXECUTION_PERMISSION_CLASS=BOUNDED_AUTHORIZATION_BASIS_NOT_DELEGATION
BINDING_AS_AUTHORIZATION_BASIS=NO
```

The canonical execution-side concept is `BOUNDED_EFFECT_EXECUTION_CONTRACT`. CD-C07 may exercise one exact, current and already-authorized effect. It does not issue, expand or redelegate authorization.

## 7. Admission and truth boundaries

```text
Native Result != Evidence
Evidence != Field Fact
Field != Current World
Current World != Cognitive Truth
Cognitive Decision != Action Admission
Action Admission != Runtime Effect Authorization
Runtime Effect Authorization != Execution
Execution Success != World Truth
```

Organ output remains a native/candidate result until governed downstream admission. Brain–Organ semantic and authority boundaries remain transport-independent.

## 8. Current World and Memory

```text
CURRENT_WORLD_CLASS=GOVERNED_PROJECTION_READ_MODEL
SOURCE_STATE_OWNER=CD-C09
PROJECTION_CONSUMER=CD-C10
CURRENT_WORLD_RUNTIME_AUTHORITY_REQUIRED=NO
CURRENT_WORLD_SOURCE_TRUTH_OWNER=NO
```

Projection governance requires source identity/reference, source currentness, projection rule and version, projection validity, provenance and failure/unknown semantics. No `CurrentWorldAuthority`, `CurrentWorldManager`, `WorldTruthAuthority` or second world-truth store is part of this skeleton.

CD-C14 remains Memory & Experience. Memory retrieval is not truth authority and must be revalidated for current cognitive use. Semantic compression is deferred and is not part of this skeleton.

## 9. Controlled execution and integration

Controlled evaluation and production runtime may use different governed entry layers, but must preserve the same downstream semantic and authority contracts. Controlled evaluation may not fabricate requester/source, binding lineage, authority, readiness, compatibility or provenance.

Future integration modes are `DIRECT_INTEGRATION` and `COMMUNICATION_INTEGRATION`. Transport changes do not change semantic authority. `OrganBus`, `UniversalRPC`, `GlobalProtocolManager` and `TransportAuthority` are not introduced.

## 10. Frozen challenge evidence

P3-03E adversarial challenge:

```text
CHALLENGE_COUNT=184
PASS_COUNT=79
PASS_WITH_GAP_COUNT=105
FAIL_COUNT=0
BLOCKER_COUNT=0
AF_CRITICAL_COUNT=0
AF_MAJOR_COUNT=0
AF_MINOR_COUNT=6
CONSTITUTION_VIOLATION_COUNT=0
NEW_DOMAIN_REQUIRED_COUNT=0
NEW_GOVERNANCE_DIMENSION_REQUIRED_COUNT=0
AUTHORITY_MODEL_CHANGE_REQUIRED_COUNT=0
CONNECTION_MODEL_CHANGE_REQUIRED_COUNT=0
```

P3-03F readiness:

```text
AFRG_PASS_COUNT=12
AFRG_FAIL_COUNT=0
AFRG_UNRESOLVED_COUNT=0
FREEZE_BLOCKER_COUNT=0
ARCHITECTURE_3_0_SKELETON_FREEZE_READY=YES
```

## 11. Freeze negative boundary

Skeleton Freeze does not establish implementation conformance, implementation completion, production readiness, API/schema/class-name/runtime freezes, exact connection-family count freeze, gap closure, PR-ADMISSION-02 authorization, Grounding DINO authorization, repository cleanup authorization, Git commit authorization or upload authorization.

```text
CURRENT_CODE_CONFORMS=NOT_ESTABLISHED
CODE_CHANGE_AUTHORIZED=NO
WORKTREE_CLEANUP_AUTHORIZED=NO
PR_ADMISSION_02_RESUME=NO
GROUNDING_DINO_RESUME=NO
```

Future changes to Domain classification, Governance Dimensions, Current World classification, authority ownership, admission boundaries, authority transfer rules, Brain–Organ boundaries or the two-axis model require the Constitution-governed Architecture Mutation process. Conformant subordinate materialization may evolve without Skeleton amendment.
