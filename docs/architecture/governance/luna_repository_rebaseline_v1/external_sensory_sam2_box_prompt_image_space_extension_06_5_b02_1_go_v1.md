# 06.5-B02.1 SAM2 Box Prompt & Image-Space Compatibility Extension — GO / Freeze Receipt Preparation

## Record identity and status

- `PHASE=06.5-B02.1`
- `TITLE=SAM2 Box Prompt & Image-Space Compatibility Extension`
- `SOURCE_BASELINE=5ab066a049e0fc630c1aeae071cbc78ab1f1758f`
- `IMPLEMENTATION_SCOPE=TEST_ONLY_CONTROLLED_REOPEN`
- `INTERFACE_EVOLUTION_CLASS=E1_ADDITIVE_COMPATIBLE`
- `FROZEN_PATH_INTERSECTION=YES`
- `FROZEN_CONTRACT_IMPACT=YES`
- `FUNCTIONAL_GO=YES`
- `ENGINEERING_FROZEN=NO`
- `FREEZE_COMMIT=PENDING`

This phase is a controlled reopen of the frozen SAM2 B02 synthetic provider contract. It adds BOX prompt support and a bounded test-only image-space declaration while preserving the original POINT and video propagation semantics.

## Exact implementation scope

The three implementation/test paths are:

1. `tests/external_sensory_contract_harness/fixtures_sam2_06_5_b02_v1.json`
2. `tests/external_sensory_contract_harness/sam2_assertions_06_5_b02_v1.py`
3. `tests/external_sensory_contract_harness/test_sam2_06_5_b02_v1.py`

No production code, central Harness core, Grounding DINO B01 file, or C01 composite artifact was changed.

## BOX prompt contract

SAM2 remains an independent provider contract. `SAM2_BOX_PROMPT_INDEPENDENT_OF_GROUNDING=YES` and `GROUNDING_DINO_INPUT_REQUIRED=NO`.

The image prompt contract now supports:

- `POINT` — historical B02 semantics;
- `BOX` — additive B02.1 semantics.

The BOX native contract is:

```text
prompt_type=BOX
coordinate_basis=IMAGE_PIXEL
box_encoding=XYXY
coordinate_type=FINITE_FLOAT_PIXEL_COORDINATES
box=[x_min, y_min, x_max, y_max]
```

The native assertion requires finite numeric coordinates and:

```text
0 <= x_min < x_max <= image_width
0 <= y_min < y_max <= image_height
```

## Image-space declaration

The minimum test-only image-space declaration records:

```text
image_ref
image_width
image_height
orientation
resize
crop
letterbox
```

The synthetic positive basis is one source image with explicit `orientation=UPRIGHT`, `resize=NONE`, `crop=NONE`, and `letterbox=NONE`. These fields are declared spatial metadata and transformation basis only. They do not create world truth, canonical spatial state, Current World, currentness, or canonical image identity.

`TRANSFORM_ID=NOT_IMPLEMENTED`, `TRANSFORM_MATRIX=NOT_IMPLEMENTED`, and `COORDINATE_FRAME_ID=NOT_IMPLEMENTED`.

`GROUNDING_NORMALIZED_CXCYWH_TO_SAM2_PIXEL_XYXY=NOT_IMPLEMENTED`; no cross-provider coordinate conversion or same-image proof was added in B02.1.

## Lineage and authority boundaries

The implementation uses the existing A3 relation schema and actual stored direction:

```text
relation kind=CONDITIONED_BY
source_ref=explicit BOX prompt
subject_ref=SAM2 invocation

relation kind=PRODUCED_FROM
source_ref=SAM2 invocation
```

Therefore `CONDITIONED_BY != PRODUCED_FROM`. The relations remain bounded formation/lineage records:

```text
CONDITIONED_BY_CREATES_AUTHORITY=NO
PRODUCED_FROM_CREATES_AUTHORITY=NO
RELATION_CREATES_AUTHORITY=NO
```

`DERIVED_PROMPT_ENDPOINT_BINDING=NOT_IMPLEMENTED` and `GROUNDING_TO_SAM2_HANDOFF=NOT_IMPLEMENTED`. No Grounding DINO reference, score, phrase, or local identity is required by the BOX contract.

## Backward compatibility and counts

The original B02 cases and snapshot meanings remain intact:

```text
POINT_PROMPT_SEMANTICS_CHANGED=NO
VIDEO_PROPAGATION_SEMANTICS_CHANGED=NO
HISTORICAL_B02_SAM2_CASE_COUNT=5
B02_1_ADDITIVE_CASE_COUNT=1
CURRENT_SAM2_CASE_COUNT=6
BASE_HARNESS_CASE_COUNT=20
GROUNDING_DINO_B01_CASE_COUNT=4
FROZEN_B02_CUMULATIVE_CASE_COUNT=29
CURRENT_CUMULATIVE_CASE_COUNT=30
HISTORICAL_SNAPSHOT_COUNT=2
THIRD_SNAPSHOT_ADDED=NO
```

The additive case is `BOX_PROMPT_POSITIVE_001`. The original `v1` and `variant` snapshots were retained; no third snapshot was introduced.

## Negative boundaries and non-goals

```text
PROVIDER_LOCAL_SCORE_ONLY=YES
CROSS_PROVIDER_SCORE_COMPARISON_ALLOWED=NO
PROVIDER_LOCAL_ID_TO_CANONICAL_ID=NO
BOX_PROMPT_CREATES_TRUTH=NO
IMAGE_SPACE_DECLARATION_CREATES_TRUTH=NO
IMAGE_SPACE_DECLARATION_CREATES_CURRENTNESS=NO
CONDITIONED_BY_CREATES_AUTHORITY=NO
PRODUCED_FROM_CREATES_AUTHORITY=NO
OBSERVATION_ADMISSION_CREATED=NO
EVIDENCE_ADMISSION_CREATED=NO
RUNTIME_AUTHORIZATION_CREATED=NO
```

The following remain explicitly unimplemented:

- `TRANSFORM_ID`, `TRANSFORM_MATRIX`, and `COORDINATE_FRAME_ID`;
- Grounding normalized `CXCYWH` to SAM2 pixel `XYXY` conversion;
- cross-provider image-space proof;
- derived BOX prompt endpoint binding;
- Composite Handoff;
- real SAM2 model or checkpoint integration;
- `REAL_GOLDEN` payload.

`PRODUCTION_READY=NO`.

## Architecture and authority impact

```text
PRODUCTION_CODE_CHANGE=NO
AUTHORITY_CHANGE=NO
NEW_CANONICAL_FACT_COUNT=0
NEW_OWNER_COUNT=0
NEW_MANAGER_COUNT=0
NEW_RUNTIME_REGISTRY_COUNT=0
CENTRAL_VALIDATOR_CHANGED=NO
GROUNDING_DINO_B01_CHANGED=NO
NEW_RELATION_KIND_ADDED=NO
COMPOSITE_HANDOFF_ADDED=NO
```

## User-terminal verification evidence

The following evidence was supplied by the user terminal; it was not executed by the Agent during receipt preparation:

- `SAM2 B02/B02.1: 38 passed in 0.07s`;
- `Complete cumulative suite: 126 passed in 0.18s`;
- Base Harness: 65 tests;
- Grounding DINO B01: 23 tests;
- SAM2 B02/B02.1: 38 tests;
- `CENTRAL_HARNESS_CORE_DIFF=EMPTY`;
- `GROUNDING_DINO_B01_DIFF=EMPTY`;
- `GIT_DIFF_CHECK=PASS`;
- `STAGED_RESIDUE=NONE`.

## GO adjudication and freeze state

`FUNCTIONAL_GO=YES` records successful user-terminal functional verification only. `ENGINEERING_FROZEN=NO` remains required until exact-path staging, commit, freeze receipt completion, and subsequent adjudication are complete. No future commit hash is recorded here.

This receipt does not authorize or establish 06.5-C01. Grounding DINO → SAM2 coordinate conversion, cross-provider image-space proof, derived prompt endpoint binding, and Composite Handoff remain separate future work.
