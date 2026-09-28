# 06.5-C01 Grounding DINO → SAM2 Composite Synthetic Contract — GO / Freeze Receipt Preparation

## Record identity and status

- `PHASE=06.5-C01`
- `TITLE=Grounding DINO → SAM2 Composite Synthetic Contract`
- `SOURCE_BASELINE=f547eced8f369e0f444f1c5cb17d3bf8480d2fff`
- `COMPOSITE_KEY=GROUNDING_DINO_TO_SAM2`
- `COMPOSITE_TYPE=SYNTHETIC_CROSS_PROVIDER_HANDOFF`
- `UPSTREAM_PROVIDER=GROUNDING_DINO`
- `DOWNSTREAM_PROVIDER=SAM2`
- `FUNCTIONAL_GO=YES`
- `ENGINEERING_FROZEN=NO`
- `FREEZE_COMMIT=PENDING`

C01 is a bounded cross-provider synthetic contract, not Model #8, a production pipeline, a runtime handoff service, a Canonical Fact, or a new Authority.

## Provider and fixture counts

```text
CURRENT_PROVIDER_MODEL_COUNT=7
PROVIDER_FIXTURE_CASE_COUNT=30
C01_COMPOSITE_FIXTURE_CASE_COUNT=9
PROVIDER_CONTRACT_SNAPSHOT_COUNT=14
C01_MODEL_COUNT_INCREMENT=0
C01_PROVIDER_CONTRACT_SNAPSHOT_INCREMENT=0
```

The nine composite cases are:

```text
NORMAL_HANDOFF
EMPTY_UPSTREAM
INVALID_COORDINATE_HANDOFF
IMAGE_SPACE_MISMATCH
LINEAGE_BREAK
AUTHORITY_NEGATIVE
SCORE_BOUNDARY
IDENTITY_ESCALATION_NEGATIVE
TEMPORAL_ORDER_EDGE
```

Composite cases are stored in a dedicated composite collection and are not added to provider `models[]`.

## Complete synthetic handoff chain

```text
Original Text Prompt
→ Grounding DINO Invocation
→ Grounding Detection Candidate
→ C01-local Mechanical Handoff Mapping
→ Derived SAM2 BOX Prompt
→ SAM2 Invocation
→ SAM2 Mask Candidate
```

`FULL_SYNTHETIC_PROMPT_PROVENANCE=PASS`. Original prompt, Grounding phrase/query references, detection reference, derived BOX prompt reference, SAM2 invocation, and mask reference remain traceable. `GROUNDING_PHRASE_OR_QUERY_IS_WORLD_TRUTH=NO`; `TRACEABILITY_EQUALS_AUTHORITY=NO`.

## Mechanical transform

Grounding DINO provides `IMAGE_NORMALIZED` / `CXCYWH`. The C01-local derived SAM2 prompt uses `IMAGE_PIXEL` / `XYXY` / `FINITE_FLOAT_PIXEL_COORDINATES`.

```text
x_min=(cx-w/2)*W
y_min=(cy-h/2)*H
x_max=(cx+w/2)*W
y_max=(cy+h/2)*H
```

The transform requires:

- same `image_ref`;
- same width and height;
- same orientation;
- same resize basis;
- same crop basis;
- same letterbox basis;
- valid normalized coordinates;
- no implicit clipping;
- no implicit rounding.

`MECHANICAL_TRANSFORM_CREATES_AUTHORITY=NO`. Invalid source or target coordinates fail closed.

## Synthetic image-space boundary

C01 records a test-only image-space declaration containing:

```text
image_ref
image_width
image_height
orientation
resize
crop
letterbox
```

`SYNTHETIC_IMAGE_SPACE_PROOF=YES`; `REAL_PROVIDER_IMAGE_SPACE_PROOF=NO`. The declaration is not Canonical Spatial State and does not establish world truth, Current World, identity, or currentness.

## C01-local handoff mapping

The handoff mapping is test-only, composite-local, mechanical, and non-authoritative:

```text
HANDOFF_MAPPING_AUTHORITY=NONE
DERIVED_PROMPT_ENDPOINT_BINDING=COMPOSITE_LOCAL_MECHANICAL_MAPPING
```

It records the source detection reference, derived prompt reference, source/target coordinate contracts, image-space basis, transform, and occurrence order. It is not a Luna Relationship Graph, Canonical Relation, Evidence, Observation Admission, Current World, Identity Resolution, or Runtime Grant.

```text
NEW_RELATION_KIND_ADDED=NO
A3_RELATION_VOCABULARY_CHANGED=NO
```

Frozen provider-internal lineage remains:

```text
Grounding Invocation CONDITIONED_BY Original Text Prompt
Grounding Detection Candidate PRODUCED_FROM Grounding Invocation
SAM2 Invocation CONDITIONED_BY Derived BOX Prompt
SAM2 Mask Candidate PRODUCED_FROM SAM2 Invocation
```

`CONDITIONED_BY != PRODUCED_FROM`; neither relation creates Authority.

## Identity, score, and temporal boundaries

```text
GROUNDING_LOCAL_ID_REUSED_AS_SAM2_LOCAL_ID=NO
DERIVED_BOX_PROMPT_HAS_NEW_LOCAL_ID=YES
LUNA_CANONICAL_ID_CREATED=NO

GROUNDING_SCORE_TRANSFERRED_TO_SAM2_SCORE=NO
SAM2_SCORE_TRANSFERRED_TO_GROUNDING_SCORE=NO
CROSS_PROVIDER_SCORE_COMPARISON_ALLOWED=NO
COMPOSITE_CONFIDENCE_CREATED=NO
LUNA_EPISTEMIC_CONFIDENCE_CREATED=NO
```

The SAM2 image-mode native contract requires explicit `temporal_metadata=[]`. C01 processing order is recorded separately as synthetic occurrence order:

```text
PROCESSING_ORDER_EQUALS_CURRENTNESS=NO
COMPOSITE_CREATES_CURRENTNESS=NO
```

## Correction 01 history

The initial user-terminal verification reported:

```text
C01=3 failed / 3 passed
Complete=3 failed / 129 passed
```

Failure A was caused by the C01-constructed SAM2 image envelope omitting the frozen SAM2 requirement `temporal_metadata=[]`. Correction 01 added the explicit empty temporal metadata while retaining processing order as composite-local data and creating no currentness claim.

Failure B was caused by an identity-negative mutation changing only the derived prompt reference. That unintentionally invalidated the SAM2 handoff target and derived-prompt provenance. Correction 01 kept the intentionally escalated local reference structurally consistent across the handoff target, SAM2 prompt reference, and SAM2 `CONDITIONED_BY` source. The resulting negative case isolates `identity_namespace_escalation`.

The engineering observation is retained as a retrospective input only:

```text
ONE_INTENDED_BOUNDARY_MUTATION
+ EXPLAINABLE_FAIL_CLOSED_CASCADE
```

This receipt does not promote that observation to a global engineering rule.

## Final user-terminal evidence

The following was supplied by the user terminal and was not executed by the Agent during receipt preparation:

- `C01 Composite: 6 passed in 0.04s`;
- `Complete External Sensory Suite: 132 passed in 0.20s`;
- Base Harness: `65 passed`;
- Grounding DINO B01: `23 passed`;
- SAM2 B02/B02.1: `38 passed`;
- `CENTRAL_HARNESS_DIFF=EMPTY`;
- `GROUNDING_DINO_B01_DIFF=EMPTY`;
- `SAM2_B02_B02_1_DIFF=EMPTY`;
- `GIT_DIFF_CHECK=PASS`;
- `STAGED_RESIDUE=NONE`.

## Authority-negative boundary

```text
COMPOSITE_CREATES_TRUTH=NO
COMPOSITE_CREATES_ADMISSION=NO
COMPOSITE_CREATES_CURRENTNESS=NO
COMPOSITE_CREATES_CANONICAL_IDENTITY=NO
COMPOSITE_CREATES_RUNTIME_AUTHORITY=NO
COMPOSITE_CREATES_MUTATION_AUTHORITY=NO
HANDOFF_MAPPING_AUTHORITY=NONE
TRANSFORM_CREATES_AUTHORITY=NO

PRODUCTION_CODE_CHANGE=NO
AUTHORITY_CHANGE=NO
NEW_CANONICAL_FACT_COUNT=0
NEW_OWNER_COUNT=0
NEW_MANAGER_COUNT=0
NEW_RUNTIME_REGISTRY_COUNT=0
```

## Protected frozen surfaces

```text
CENTRAL_VALIDATOR_CHANGED=NO
GROUNDING_DINO_B01_CHANGED=NO
SAM2_B02_B02_1_CHANGED=NO
A3_RELATION_CONTRACT_CHANGED=NO
FROZEN_PATH_INTERSECTION=NO
FROZEN_CONTRACT_IMPACT=NO
```

## Known limitations and non-goals

```text
REAL_GROUNDING_DINO_INTEGRATION=NO
REAL_SAM2_INTEGRATION=NO
REAL_PROVIDER_IMAGE_SPACE_PROOF=NO
REAL_PREPROCESSING_EQUIVALENCE_PROVEN=NO
PRODUCTION_HANDOFF=NO
RUNTIME_PIPELINE=NO
OBSERVATION_GATEWAY_ADMISSION=NO
EVIDENCE_ADMISSION=NO
PRODUCTION_READY=NO
```

C01 does not authorize new model onboarding, PaddleOCR work, or Engineering Retrospective implementation.

## GO adjudication and freeze state

`FUNCTIONAL_GO=YES` records the successful user-terminal verification. `ENGINEERING_FROZEN=NO` remains in force until exact-path staging, commit, freeze receipt completion, and subsequent adjudication. No future freeze commit hash is recorded in this preparation receipt.
