# 06.5-B02 SAM2 Independent Synthetic Provider Contract — GO / Freeze Receipt Preparation

## Record identity and current status

- `PHASE=06.5-B02`
- `SOURCE_BASELINE=b61e1995547cce2f77393cfcd71dd8e5dac3849a`
- `IMPLEMENTATION_SCOPE=TEST_ONLY_INDEPENDENT_SYNTHETIC_PROVIDER_CONTRACT`
- `06_5_B02_FUNCTIONAL_GO=YES` (reported phase decision following user-terminal verification)
- `06_5_B02_GIT_FREEZE_COMPLETE=NO`
- `06_5_B02_ENGINEERING_FROZEN=NO`
- `FREEZE_COMMIT=PENDING`; this preparation record is not a Git freeze or remote-publication receipt.

## Independent contract and fixture result

SAM2 is represented only as a **prompt-conditioned segmentation / mask propagation provider**. The synthetic contract covers `IMAGE_SEGMENTATION_AND_VIDEO_MASK_PROPAGATION` within one independent model contract. A prompt or prior-mask seed is a provider inference condition, not Luna Object Truth, Canonical Object Identity, Evidence Admission, or a Current World fact. A mask candidate is not any of those facts either.

`GROUNDING_DINO_USED_AS_INPUT=NO` and `CROSS_MODEL_RELATION_ADDED=NO`. This phase did not establish a Grounding DINO → SAM2 handoff or Grounded SAM2 pipeline. The SAM2 contract stands independently of Grounding DINO.

- `SAM2_MODEL_NUMBER=7`; `NEW_FIXTURE_CASE_COUNT=5`.
- Cases: `NORMAL_POSITIVE`, `EMPTY_OR_NO_RESULT`, `AUTHORITY_NEGATIVE`, `VERSION_VARIANT`, and `TEMPORAL_OR_ORDER_EDGE` (stored with stable `_001` case identities).
- `SAM2_BASELINE_SNAPSHOT_COUNT=1`; `SAM2_SIMULATED_VARIANT_COUNT=1`.
- `source_kind=SYNTHETIC`; `simulation=True`; `REAL_GOLDEN_CASE_COUNT=0`.
- The variant is synthetic contract evolution, not an official SAM2/SAM2.1 release, checkpoint, or provider revision.

The test-only native fixture retains a bounded mask descriptor and explicit `IMAGE_PIXEL` prompt/mask spatial basis rather than reducing segmentation to a bounding box. `MASK_REPRESENTATION_PRESERVED=YES`; `MASK_SPATIAL_BASIS_EXPLICIT=YES`. Its bounded lineage assertions distinguish:

- SAM2 Invocation `CONDITIONED_BY` Prompt or prior-mask seed.
- Mask Candidate `PRODUCED_FROM` SAM2 Invocation.

These relations record declared synthetic formation context; they do not establish truth, identity, admission, authorization, or currentness. A valid `masks=[]` result means only that this provider invocation produced no mask candidates—not that the world lacks an object, Evidence was rejected, or the provider necessarily failed.

## Propagation, score, and identity boundaries

`PROPAGATION_INCLUDED=YES`. The fifth fixture, `TEMPORAL_OR_ORDER_EDGE`, records a sequence/frame reference, frame index, propagation order, prior-mask seed, sequence-local object index, and propagated mask candidate. It tests the explicit negative boundary `PROVIDER_PROPAGATION_TREATED_AS_CURRENTNESS=NO`: **provider propagation is not Luna currentness**. Frame, object, mask, and propagation identifiers remain provider-, invocation-, media-, or sequence-local; `LOCAL_IDENTITY_ESCALATION=NO`.

Mask quality is a `PROVIDER_LOCAL_SCORE`. `PROVIDER_LOCAL_SCORE_ONLY=YES`; `CROSS_PROVIDER_SCORE_COMPARISON_ALLOWED=NO`. A provider quality signal is not Luna epistemic confidence, and it is not directly comparable to Grounding DINO's score. The authority-negative case confirms that a high score or native mask cannot directly establish world truth, admission, currentness, canonical identity, or authorization; lineage has `creates_authority=false`.

## Extensibility proof and exact engineering scope

The seventh model was added through three additive test-only paths:

1. `tests/external_sensory_contract_harness/fixtures_sam2_06_5_b02_v1.json`
2. `tests/external_sensory_contract_harness/sam2_assertions_06_5_b02_v1.py`
3. `tests/external_sensory_contract_harness/test_sam2_06_5_b02_v1.py`

These user-terminal-verified files must remain unchanged during receipt preparation. The cumulative set is `BASE_MODEL_COUNT=5`, `GROUNDING_DINO_MODEL_COUNT=1`, `SAM2_MODEL_COUNT=1`, `TOTAL_MODEL_COUNT=7`, `TOTAL_FIXTURE_CASE_COUNT=29`, and `TOTAL_CONTRACT_SNAPSHOT_COUNT=14`. `CENTRAL_VALIDATOR_CHANGED=NO`, `FROZEN_HARNESS_CORE_CHANGED=NO`, and `GROUNDING_DINO_B01_CHANGED=NO`; thus `HARNESS_GENERALIZATION_MODEL_7=PASS` for the synthetic contract extension. Provider-specific native assertions remain distinct from Universal envelope validity.

## User-terminal verification evidence

The following results were **reported from the user terminal**, not produced by Agent execution during this receipt step:

- `B02_CUMULATIVE_COUNTS=PASS`; `SAM2_AST=PASS`.
- Frozen base Harness regression: `65 passed in 0.10s`.
- Frozen Grounding DINO regression: `23 passed in 0.06s`.
- SAM2 B02: `30 passed in 0.06s`.
- Complete cumulative suite: `118 passed in 0.17s`.
- `GIT_DIFF_CHECK=PASS`; `FROZEN_HARNESS_CORE_DIFF=EMPTY`; `FROZEN_GROUNDING_DINO_B01_DIFF=EMPTY`; `STAGED_RESIDUE=NONE`.

The Agent did not run pytest, runner, verifier, or py_compile during this receipt preparation.

## Governance boundary, limitations, and next step

- `PRODUCTION_CODE_CHANGE=NO`; `AUTHORITY_CHANGE=NO`.
- `NEW_CANONICAL_FACT_COUNT=0`; `NEW_OWNER_COUNT=0`; `NEW_MANAGER_COUNT=0`; `NEW_RUNTIME_REGISTRY_COUNT=0`.
- `FROZEN_PATH_INTERSECTION=NO`; `FROZEN_CONTRACT_IMPACT=NO`; `REAL_MODEL_USED=NO`.

`06_5_B02_FUNCTIONAL_GO=YES` covers only the independent synthetic SAM2 provider contract. It does **not** establish real SAM2 checkpoint validation, `REAL_GOLDEN` validation, production integration, Observation Gateway or Evidence Admission, Luna currentness, or canonical object identity.

Exact-path Git staging/commit, actual freeze-commit receipt, and final freeze adjudication remain pending. Only after B02 is frozen may a **separate** Grounding DINO → SAM2 Composite Contract phase be considered to validate bounded cross-model handoff and lineage between two independently frozen provider contracts. No composite fixture or pipeline is established by this record.
