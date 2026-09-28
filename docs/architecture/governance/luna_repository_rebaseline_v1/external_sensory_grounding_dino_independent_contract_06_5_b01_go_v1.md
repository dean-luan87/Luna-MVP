# 06.5-B01 Grounding DINO Independent Synthetic Provider Contract — GO / Freeze Receipt Preparation

## Record identity and current status

- `PHASE=06.5-B01`
- `SOURCE_BASELINE=aa5b9460fa0022845eaad068ec5f147efe0e41ce`
- `IMPLEMENTATION_SCOPE=TEST_ONLY_INDEPENDENT_SYNTHETIC_PROVIDER_CONTRACT`
- `06_5_B01_FUNCTIONAL_GO=YES` (reported user-terminal verification and phase decision)
- `06_5_B01_GIT_FREEZE_COMPLETE=NO`
- `06_5_B01_ENGINEERING_FROZEN=NO`
- `FREEZE_COMMIT=PENDING`; this preparation record is not a Git freeze or remote-publication receipt.

## Historical lineage

Grounding DINO B01 had three executions. Execution 01 stopped at `HARNESS_ABSTRACTION_INSUFFICIENT`: the frozen Harness coupled collection validity to exactly five models and model-name-driven requirements. That led to the 06.5-A2 extensibility correction. Execution 02 stopped at `LINEAGE_VOCABULARY_INSUFFICIENT`: the frozen historical relation allowlist could not precisely express prompt conditioning. That led to the 06.5-A3 relation-semantics correction. Neither stop was a Grounding DINO Native Contract failure. Execution 03 established the independent synthetic contract and received the user-terminal verification recorded below.

## Independent contract and fixture result

Grounding DINO is represented here only as a `TEXT-CONDITIONED OPEN-SET DETECTION PROVIDER`. Its synthetic input is an image plus a prompt/caption; its synthetic native output is a set of provider-native detection candidates. Neither the output nor the expected projection establishes Luna Object Truth, Ontology Identity, Field Object, Memory Object, Observation or Evidence Admission, Current World, Canonical Object Identity, or Runtime Authorization.

- `GROUNDING_DINO_MODEL_NUMBER=6`; `NEW_FIXTURE_CASE_COUNT=4`.
- Cases: `NORMAL_POSITIVE`, `EMPTY_OR_NO_RESULT`, `AUTHORITY_NEGATIVE`, and `VERSION_VARIANT` (stored with stable `_001` case identities).
- `GROUNDING_DINO_BASELINE_SNAPSHOT_COUNT=1`; `GROUNDING_DINO_SIMULATED_VARIANT_COUNT=1`.
- `source_kind=SYNTHETIC`; `simulation=True`; `REAL_GOLDEN_CASE_COUNT=0`.
- The variant is a simulated contract-evolution snapshot, not an official release, checkpoint, or provider revision.

The test-only declared requirements are `coordinate=REQUIRED`, `score=REQUIRED`, and `lineage=REQUIRED`. The native box basis and encoding are explicitly normalized image coordinates and `CXCYWH`; this is not a world-coordinate claim. The prompt/caption remains a first-class inference condition. The bounded lineage assertions distinguish:

- Grounding Invocation `CONDITIONED_BY` Prompt.
- Detection Candidate `PRODUCED_FROM` Grounding Invocation.

`CONDITIONED_BY != PRODUCED_FROM`. These relations record declared test lineage; they do not establish world causality, truth, currentness, identity, admission, or authorization. The score remains `PROVIDER_LOCAL_SCORE`: `LUNA_EPISTEMIC_CONFIDENCE=NO` and `CROSS_PROVIDER_SCORE_COMPARISON_ALLOWED=NO`. Detection/query/phrase indexes remain provider- or invocation-local: `LOCAL_IDENTITY_ESCALATION=NO`. An empty detection list is a valid no-result output, not a world-truth claim. In its empty case, score metadata describes the configured threshold, not an invented detection score.

## Extensibility proof and exact engineering scope

The sixth model was added through three additive test-only paths:

1. `tests/external_sensory_contract_harness/fixtures_grounding_dino_06_5_b01_v1.json`
2. `tests/external_sensory_contract_harness/grounding_dino_assertions_06_5_b01_v1.py`
3. `tests/external_sensory_contract_harness/test_grounding_dino_06_5_b01_v1.py`

These user-terminal-verified files must not be modified during receipt preparation. `CENTRAL_VALIDATOR_CHANGED=NO` and `FROZEN_A3_HARNESS_CORE_CHANGED=NO`. Model #6 is the first actual new-model contract to exercise the 06.5-A2 and 06.5-A3 extensibility corrections without reopening their frozen central Harness. Provider-specific native assertions remain separate from Universal contract validation; Universal validity alone is not Provider Native semantic proof.

## User-terminal verification evidence

The following results were reported from the **user terminal**, not produced by Agent execution during this receipt step:

- `BASE_MODEL_COUNT=5`; `GROUNDING_DINO_MODEL_COUNT=1`.
- `TOTAL_MODEL_COUNT=6`; `TOTAL_FIXTURE_CASE_COUNT=24`; `TOTAL_CONTRACT_SNAPSHOT_COUNT=12`.
- `B01_COMBINED_COUNTS=PASS`; `AST=PASS`.
- Frozen Harness regression: `65 passed in 0.11s`.
- Grounding DINO B01: `23 passed in 0.06s`.
- Combined Harness suite: `88 passed in 0.13s`.
- `GIT_DIFF_CHECK=PASS`; `FROZEN_CORE_DIFF=EMPTY`; `STAGED_RESIDUE=NONE`.

The Agent did not run pytest, runner, verifier, or py_compile during this receipt preparation.

## Governance boundary, limitations, and next step

- `PRODUCTION_CODE_CHANGE=NO`; `AUTHORITY_CHANGE=NO`.
- `NEW_CANONICAL_FACT_COUNT=0`; `NEW_OWNER_COUNT=0`; `NEW_MANAGER_COUNT=0`; `NEW_RUNTIME_REGISTRY_COUNT=0`.
- `FROZEN_PATH_INTERSECTION=NO`; `FROZEN_CONTRACT_IMPACT=NO`; `CROSS_MODEL_RELATION_ADDED=NO`; `REAL_MODEL_USED=NO`.

`06_5_B01_FUNCTIONAL_GO=YES` covers only the independent synthetic Grounding DINO provider contract. It does **not** establish real Grounding DINO integration, real checkpoint or `REAL_GOLDEN` validation, Observation Gateway integration, Evidence Admission, or production readiness.

Exact-path Git staging/commit, actual freeze-commit receipt, and final freeze adjudication remain pending. Only after B01 is frozen may `06.5-B02 SAM2 Independent Provider Contract` be considered. Grounding DINO → SAM2 composition has not started; any composite relation requires both independent contracts to be frozen and a separately authorized phase.
