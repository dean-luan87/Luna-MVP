# 06.5-A2 External Sensory Simulation Harness Extensibility Correction — GO / Freeze Receipt Preparation

## Record identity and status

- `PHASE=06.5-A2`
- `TITLE=Harness Extensibility Correction 01`
- `SOURCE_BASELINE=cbb937c688c2b7092652497773432460212ccaeb`
- `IMPLEMENTATION_SCOPE=TEST_ONLY`
- `FUNCTIONAL_GO=YES` (user/ChatGPT phase decision following user-terminal verification)
- `ENGINEERING_FROZEN=NO` until the separate exact-path Git freeze and final receipt are complete.
- `FREEZE_COMMIT=PENDING`; no commit or remote-publication claim is made by this document.

This is a controlled correction lineage of the frozen 06.5-A Harness. It neither amends nor replaces the historical 06.5-A freeze commit `cbb937c688c2b7092652497773432460212ccaeb` or its receipt.

## Correction reason and architecture decision

The initial 06.5-B01 Grounding DINO Generalization Gate exposed an exact five-model closed-set assumption, `model_not_in_v1_set`, and a model-name-driven coordinate requirement. Grounding DINO itself had not failed a Native Contract test; the failure occurred at the Harness extensibility boundary before that model could be admitted to contract validation.

The selected correction is **Declared-requirement Universal Validation + Bounded Provider-specific Native Assertions + Historical Baseline Regression**. Collection validity no longer means that every future collection contains exactly the original five models. A bounded test-only contract requirement declaration determines applicable coordinate, temporal, identity, score, and lineage metadata checks; existing provider-native assertions remain separate. Passing the universal envelope contract for an unknown provider does **not** establish that its native contract has been validated.

This correction does not grow the central model-name switch for each future model, and introduces no runtime plugin system, Provider Registry, or ExternalModelManager.

## Historical preservation and exact correction scope

The original 06.5-A historical baseline remains five models, 20 fixture cases, and ten contract snapshots:

1. YOLO26
2. Qwen3-VL
3. Qwen3-ASR
4. ORB-SLAM3
5. RelateAnything

The prior fixture/snapshot semantics were neither deleted nor overwritten. Historical regression checks retain the five-model/20-case/10-snapshot proof independently of open collection validity. The sixth-model generalization probe exists only in test memory; it is not a stored model fixture, an official model version, or Grounding DINO.

The three correction paths, already user-terminal verified and not modified during this receipt preparation, are:

1. `tests/external_sensory_contract_harness/validator_v1.py`
2. `tests/external_sensory_contract_harness/fixtures_v1.json`
3. `tests/external_sensory_contract_harness/test_contract_harness_v1.py`

- `FIXED_MODEL_COUNT_ASSUMPTION_REMOVED=YES`
- `MODEL_NAME_COORDINATE_REQUIREMENT_REMOVED=YES`
- `DECLARED_REQUIREMENT_CONTRACT_ADDED=YES`
- `PROVIDER_SPECIFIC_ASSERTIONS_PRESERVED=YES`
- `UNKNOWN_PROVIDER_UNIVERSAL_VALIDATION_SUPPORTED=YES`
- `UNKNOWN_PROVIDER_NATIVE_VALIDATION_AUTO_GRANTED=NO`
- `GENERALIZATION_PROBE_ADDED=YES`
- `GROUNDING_DINO_MODEL_ADDED=NO`

## User-terminal verification evidence

The following are reported user-terminal results, not Agent static-inspection proof:

- `MODEL_COUNT=5`; `FIXTURE_CASE_COUNT=20`; `CONTRACT_SNAPSHOT_COUNT=10`; `HISTORICAL_06_5_A_COUNTS=PASS`.
- `JSON_PARSE=PASS`; `PYTHON_AST=PASS`.
- `HARNESS_TESTS=55 passed in 0.09s`.
- `GIT_DIFF_CHECK=PASS`; `STAGED_RESIDUE=NONE`.

The Agent did not run pytest, runner, verifier, or py_compile during this receipt-preparation step.

## Authority, freeze impact, and limitations

- `PRODUCTION_CODE_CHANGE=NO`; `AUTHORITY_CHANGE=NO`.
- `NEW_CANONICAL_FACT_COUNT=0`; `NEW_OWNER_COUNT=0`; `NEW_MANAGER_COUNT=0`; `NEW_RUNTIME_REGISTRY_COUNT=0`.
- `FROZEN_PATH_INTERSECTION=YES`; `FROZEN_CONTRACT_IMPACT=YES`. These are expected consequences of a controlled correction to frozen test-only Harness paths and semantics, not a claim that production authority changed.
- The Harness remains test-only. Universal validation and expected projection are not Provider Native Contract proof, Gateway admission, Evidence/Field truth, or runtime authority.

`KNOWN_LIMITATION=YES`: requirement declarations currently live at the model-record level. Evolution of requirements between two contract snapshots of the same model is not resolved here. `CURRENT_A2_BLOCKER=NO`; revisit this boundary when a real model-version evolution requires it.

After a separate A2 Git freeze and verified final receipt, the next proposed phase is a renewed `06.5-B01 Grounding DINO Independent Provider Contract`. Grounding DINO will be the first new model to test the correction's extensibility in practice. No Grounding DINO fixture or integration is part of this receipt.
