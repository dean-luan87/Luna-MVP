# Temporal Coordinate System V1 — Conditional Duration Policy Additive Extension

## Record identity

- Phase: `Temporal Coordinate System V1 — Conditional Duration Policy Additive Extension`
- Change type: `FOUNDATION_ADDITIVE_EXTENSION`
- Source baseline / parent: `3d99e523db760fa3fca7b6e9e0b39c46a939ec72`
- Technical decision: `GO=YES`
- Engineering freeze state at record creation: `PENDING_EXACT_PATH_GIT_FREEZE`
- Remote publication: `NO`

This record closes the conditional-duration foundation gap only. It is not the P1-01A Field Event migration, a Temporal V2, or a new authority subsystem.

## Purpose and semantic boundary

The frozen V1 foundation previously allowed numeric duration arithmetic for `SAFE` ClockDomains and failed closed for `CONDITIONAL` domains. This additive extension introduces a typed, immutable declaration that permits one explicitly bounded local-policy delta when the applicable Domain Contract declares that operation.

`ConditionalDurationPolicyV1` is a `DOMAIN_CONTRACT_DECLARATION`. Its `policy_id` and `policy_version` identify a stable declaration; they are not an Authorization Token, Authority Proof, Runtime Grant, Admission Record, capability, or currentness proof.

Temporal Coordinate System owns temporal coordinate semantics and operation-legality mechanics. The Domain Contract Owner owns the domain-specific reason for declaring conditional duration applicability. `LINEAGE != AUTHORITY`.

The extension preserves:

- `TEMPORAL_DOMAIN_TRUTH_AUTHORITY=NONE`
- `TEMPORAL_CURRENTNESS_AUTHORITY=NONE`
- `TEMPORAL_EFFECT_ELIGIBILITY_AUTHORITY=NONE`
- `TEMPORAL_ADMISSION_AUTHORITY=NONE`
- `TEMPORAL_DOMAIN_MUTATION_AUTHORITY=NONE`

No Temporal Manager, Temporal Registry, Policy Registry, Policy Store, Owner Resolver, global mutable state, or second duration arithmetic path is created.

## Duration contract

`duration_between()` remains the single canonical public duration operation and accepts only a keyword-only typed `ConditionalDurationPolicyV1` when needed.

| ClockDomain suitability | Policy behavior |
| --- | --- |
| `SAFE` | Existing behavior is unchanged; a conditional policy cannot alter or elevate it. |
| `CONDITIONAL` | A matching typed policy is mandatory. Domain identity, canonical ClockDomain semantics, comparability, exactness, operation, and basis must all pass. |
| `UNSAFE` | Always fail closed; a policy cannot bypass the block. |
| `UNKNOWN` | Always fail closed; a policy cannot infer or establish semantics. |

Different domains, same-identity semantic conflicts, uncertainty/non-exact points, missing or mismatched policy, and invalid suitability do not produce numeric duration. No boolean escape hatch, `force` flag, caller trust flag, or silent coercion exists.

The resulting conditional delta means only a domain-declared bounded local-policy delta. It is not physical elapsed-time truth, world-duration truth, synchronization proof, domain truth, currentness, effect eligibility, or admission authority.

## Verification evidence

User-terminal authoritative evidence bound to this source state:

- `PY_COMPILE=PASS`
- `CONTRACT_JSON_PARSE=PASS`
- `FOCUSED_AND_FOUNDATION_REGRESSION=34/34 PASS`
- `GIT_DIFF_CHECK=PASS`
- `AUTHORIZED_TRACKED_CHANGED_PATHS=4`
- `UNAUTHORIZED_TRACKED_CHANGED_PATHS=0`
- `POLICY_CONSTRUCTION_FAIL_CLOSED=PASS`
- `POLICY_AUTHORITY_INFLATION_COUNT=0`
- `CONDITIONAL_POLICY_BYPASS_PATH_COUNT=0`
- `DOMAIN_SEMANTIC_CONFLICT_BYPASS=NO`
- `UNCERTAINTY_BYPASS=NO`
- `SAFE_PATH_SEMANTIC_DRIFT=NO`
- `PUBLIC_DURATION_OPERATION_COUNT=1`
- `SECOND_DURATION_ARITHMETIC_PATH=NO`
- `CONTRACT_IMPLEMENTATION_DRIFT_COUNT=0`
- `UNINTENDED_PUBLIC_EXPORT_COUNT=0`
- `NEW_AUTHORITY_SURFACE_COUNT=0`
- `LINEAGE_FUTURE_COMPATIBILITY=PASS`
- `FOUNDATION_EXTENSION_ISOLATION=PASS`
- `MISSING_CRITICAL_TEST_PARTITIONS=NONE`

No tests, runner, or verifier were executed during the documentation/freeze stage.

## Exact engineering-owned paths

The implementation/test path set is exactly:

1. `capabilities/midplatform/core/temporal_coordinate/temporal_coordinate_v1.py`
2. `capabilities/midplatform/core/temporal_coordinate/__init__.py`
3. `capabilities/midplatform/core/temporal_coordinate/temporal_coordinate_contract_v1.json`
4. `tests/temporal_coordinate/test_temporal_coordinate_v1.py`

This closure document is the only additional path authorized for this freeze. Historical unrelated tracked/untracked workspace artifacts remain outside the freeze set.

## Scope isolation and follow-up

Field Event, Observation Gateway, Evidence Adapter, Runtime, Provider, Field Temporal Evolution, Memory, Brain, and Phase E source/tests are unchanged. P1-01A remains blocked pending this foundation extension while this Git/Notion freeze is incomplete; after the actual freeze commit it becomes `UNBLOCKED_BY_FOUNDATION_EXTENSION`, but `P1_01A_IMPLEMENTATION_STARTED=NO`.

The System Information Lineage Spine is future system-layer work and is not implemented here. `policy_id` and `policy_version` remain sufficient future derivation-reference hooks without creating a central lineage store or provenance manager.

## Freeze boundary

Until exact-path staging, commit, post-commit receipt verification, and Notion 03/03.7/03.8/03.9 synchronization are complete:

`ENGINEERING_FROZEN=NO`

The final freeze receipt is bound to the actual commit and exact sorted path-set hash recorded in Notion 03.9 after commit. This document does not claim `RELEASED`, `PRODUCTION_READY`, or remote publication.
