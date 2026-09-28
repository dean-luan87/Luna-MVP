# 06.5-A External Sensory Simulation Contract Harness — GO / Freeze Record

## Record identity and status

- `PHASE=06.5-A`
- `TITLE=External Sensory Simulation Contract Harness Minimum Skeleton`
- `SOURCE_BASELINE=7419042b0f3dde07dc7f02f7ead46b6824bf901e`
- `IMPLEMENTATION_SCOPE=TEST_ONLY`
- `FUNCTIONAL_GO=YES` (user/ChatGPT phase decision, supported by the user-terminal evidence below)
- `ENGINEERING_FROZEN=NO` until the required documentation, Notion, exact-path Git commit, and final freeze receipt are complete.
- `FREEZE_COMMIT=PENDING`; `REMOTE_PUBLISHED=NO`.

This record prepares the 06.5-A freeze. The source baseline names the pre-freeze HEAD, not a commit containing the currently untracked Harness files. It does not establish `PRODUCTION_READY=YES` or `REAL_PROVIDER_INTEGRATION_READY=YES`.

## Exact engineering scope and fixture counts

The three GO Harness files, whose verified contents must not change during freeze preparation, are:

1. `tests/external_sensory_contract_harness/fixtures_v1.json`
2. `tests/external_sensory_contract_harness/validator_v1.py`
3. `tests/external_sensory_contract_harness/test_contract_harness_v1.py`

The planned freeze path set consists of these three files plus this record. It is a plan, not a staged-path or committed-path receipt; the exact set and source binding must be checked before and after a future commit.

- `MODEL_COUNT=5`: YOLO26, Qwen3-VL, Qwen3-ASR, ORB-SLAM3, RelateAnything.
- `FIXTURE_CASE_COUNT=20`: four synthetic cases per model.
- `CONTRACT_SNAPSHOT_COUNT=10`.
- `SYNTHETIC_BASELINE_COUNT=5`.
- `SIMULATED_CONTRACT_VARIANT_COUNT=5`.

The ten snapshots are **not** ten official Provider Model Revisions. `SIMULATED_CONTRACT_VARIANT` verifies interface evolution and historical coexistence only; it does not claim an official model release, a real checkpoint revision, or a real SDK/API revision. Provider model revision and synthetic contract snapshot are separate version dimensions. No `PROVIDER_MODEL_REVISION_COUNT=10` freeze statistic is asserted.

## Semantic and authority boundary

The Harness is a `TEST_ONLY CONTRACT HARNESS`, not a production runtime schema, runtime provider registry, canonical Observation or Evidence schema, world-truth source, identity authority, temporal authority, or score authority.

Native synthetic payload remains provider-like test input. The expected projection records a declared native-to-candidate transformation; it is **not** Observation Gateway/Evidence/Field Admission. Synthetic fixtures cannot establish production truth. Lineage records transformation/provenance; a relation edge cannot create an authority outcome. Provider-local identifiers and scores do not become Luna canonical identities or epistemic confidence merely by appearing in a fixture. Raw provider time does not establish temporal currentness or authority.

- `NEW_CANONICAL_FACT_COUNT=0`; `NEW_OWNER_COUNT=0`; `NEW_MANAGER_COUNT=0`; `NEW_RUNTIME_REGISTRY_COUNT=0`.
- `PRODUCTION_CODE_CHANGE=NO`; `AUTHORITY_CHANGE=NO`.
- `EXISTING_GATEWAY_AUTHORITY_CHANGED=NO`; `TEMPORAL_AUTHORITY_CHANGED=NO`.
- `EP01_TOUCHED=NO`; `EP02_TOUCHED=NO`; `EP03_PRODUCTION_PATH_TOUCHED=NO`.
- `FROZEN_PATH_INTERSECTION=NO`; `FROZEN_CONTRACT_IMPACT=NO` for this test-only Harness scope.

## User-terminal verification evidence

User-terminal evidence for the GO Harness contents:

- `HARNESS_TEST=40 passed in 0.06s`.
- `JSON_PARSE=PASS`.
- `VALIDATOR_AST=PASS`.
- `TEST_AST=PASS`.
- `UNTRACKED_CONTENT_CHECK=PASS`.
- `AUTHORIZED_FILE_SET=3 implementation/test files`.
- `CORRECTION_01=PASS`.

Correction 01 makes missing `coordinate_metadata` on a coordinate-requiring model produce the stable generic `coordinate_basis_invalid`; a model-specific error may coexist. It also proves deterministic enumeration of 20 unique synthetic executable cases and distinguishes simulated contract variants from official model revisions. The Agent did not run tests, runner, or verifier during this freeze-preparation step.

## Known limitations and next boundary

1. Only five representative models are covered; the remaining eight are not adapted.
2. All stored cases are synthetic; there is no `REAL_GOLDEN` payload.
3. No real model call or real Adapter/Gateway runtime execution occurred.
4. EP-01 and EP-02 remain unfixed; the EP-03 production path remains unfixed.
5. The Harness does not prove production integration readiness or real-provider compatibility.

ChatGPT review, applicable Notion synchronization, exact-path staging/commit, verified source/path-set receipt, and final adjudication remain outside this preparation step. `GO != ENGINEERING_FROZEN`; this document must not be read as the final freeze receipt.
