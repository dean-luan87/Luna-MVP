# 06.5-A3 External Sensory Harness Relation Semantics Extensibility — GO / Freeze Receipt Preparation

## Record identity and current status

- `PHASE=06.5-A3`
- `SOURCE_BASELINE=cf305524513a28c49be290c0d1d110211dfb7c97`
- `IMPLEMENTATION_SCOPE=TEST_ONLY_CONTROLLED_CORRECTION`
- `06_5_A3_FUNCTIONAL_GO=YES` (user/ChatGPT phase decision after user-terminal verification)
- `06_5_A3_GIT_FREEZE_COMPLETE=NO`
- `06_5_A3_ENGINEERING_FROZEN=NO`
- `FREEZE_COMMIT=PENDING`; this document is not a Git freeze or remote-publication receipt.

This is a controlled correction lineage of the frozen 06.5-A2 Harness. It does not amend, erase, or reinterpret the A2 freeze history.

## Trigger and architecture adjudication

The second 06.5-B01 Grounding DINO execution stopped with `STOP_CONDITION_TRIGGERED=LINEAGE_VOCABULARY_INSUFFICIENT`: the frozen Harness treated the relation vocabulary used by historical fixtures as a Universal fixed allowlist. Grounding DINO had not failed a Native Contract test; both earlier B01 stops occurred at Harness abstraction boundaries.

The 06.5-A3-01 read-only audit found:

- `CURRENT_RELATION_KIND_COUNT=4`: `PRODUCED_FROM`, `GROUNDED_FROM`, `ALIGNED_WITH`, `RELATION_ENDPOINT_FROM`.
- `CURRENT_VOCABULARY_ROLE=MIXED_TEST_ONLY_HISTORICAL_ALLOWLIST`.
- `CONDITIONED_BY_EQUIVALENT_TO_PRODUCED_FROM=NO`; `CONDITIONED_BY_EQUIVALENT_TO_GROUNDED_FROM=NO`.
- `CONDITIONED_BY_HAS_INDEPENDENT_SEMANTIC_MEANING=YES`.
- `RELATION_VOCABULARY_GENERALIZATION_GAP=YES`.
- `SEDIMENTATION_VOCABULARY_RELATIONSHIP=SHARED_PRINCIPLES_BOUNDED_HARNESS_SUBSET`.

The selected architecture is **Option B: Bounded Test-only Relation Declaration + Universal Relation Governance + Provider-specific Relation Assertion**. The Harness does not define Luna's canonical relation ontology, a runtime registry, or a Lineage Manager. A structurally valid declaration does not self-authorize a relation's Provider Native meaning: Universal validity is not Provider-specific semantic proof.

`CONDITIONED_BY` means that an identified inference/work occurrence *declares* formation under an explicit input condition that constrains or shapes its result. At most, a fixture records the occurrence-to-condition association. It does not prove that the provider actually followed the condition, that a prompt caused a real-world object, or that an output is true, current, canonically identified, admitted, or authorized. `CONDITIONED_BY_CREATES_AUTHORITY=NO`; lineage edges record relationships and never create authority outcomes.

## Correction result and historical preservation

- `RELATION_DECLARATION_CONTRACT_ADDED=YES`.
- `BOUNDED_SEMANTIC_CLASS_ADDED=YES`.
- `FIXED_RELATION_NAME_ALLOWLIST_AS_UNIVERSAL_GATE_REMOVED=YES`.
- `CONDITIONED_BY_GENERALIZATION_SUPPORTED=YES`, using an anonymous test-only probe, not a stored model fixture.
- `ARBITRARY_RELATION_STRING_AUTO_ACCEPTED=NO`; bounded declaration shape, class/role compatibility, reference checks, and negative-authority checks remain required.
- `UNKNOWN_RELATION_PROVIDER_SEMANTICS_AUTO_GRANTED=NO`.
- `PROVIDER_SPECIFIC_ASSERTIONS_PRESERVED=YES`; `AUTHORITY_NEGATIVE_GUARDS_PRESERVED=YES`.
- `GROUNDING_DINO_MODEL_ADDED=NO`; `GROUNDING_DINO_FIXTURE_ADDED=NO`.

The historical 06.5-A inventory remains **five models, 20 fixture cases, and ten snapshots**: YOLO26, Qwen3-VL, Qwen3-ASR, ORB-SLAM3, and RelateAnything. Its four recorded relation kinds, `source_ref` values, and `creates_authority=false` semantics were not deleted or overwritten. Additive relation declarations and the in-memory generalization probe do not rewrite those historical fixtures.

The three user-terminal-verified correction files are:

1. `tests/external_sensory_contract_harness/validator_v1.py`
2. `tests/external_sensory_contract_harness/fixtures_v1.json`
3. `tests/external_sensory_contract_harness/test_contract_harness_v1.py`

They must remain unchanged during this receipt-preparation step. A future Git freeze must stage only the separately authorized exact paths and record its actual commit and path-set receipt.

## User-terminal verification evidence

The following evidence was reported from the **user terminal**, not inferred from Agent static inspection:

- `MODEL_COUNT=5`; `FIXTURE_CASE_COUNT=20`; `CONTRACT_SNAPSHOT_COUNT=10`.
- `HISTORICAL_06_5_A_COUNTS=PASS`.
- `HISTORICAL_RELATION_KINDS_CHECK=PASS` for `ALIGNED_WITH`, `GROUNDED_FROM`, `PRODUCED_FROM`, and `RELATION_ENDPOINT_FROM`.
- `PYTHON_AST=PASS`.
- `HARNESS_TESTS=65 passed in 0.10s`.
- `GIT_DIFF_CHECK=PASS`; `STAGED_RESIDUE=NONE`.

The Agent did not run pytest, runner, verifier, or py_compile during this receipt preparation.

## Authority boundary, limitations, and next step

- `PRODUCTION_CODE_CHANGE=NO`; `AUTHORITY_CHANGE=NO`.
- `NEW_CANONICAL_FACT_COUNT=0`; `NEW_OWNER_COUNT=0`; `NEW_MANAGER_COUNT=0`; `NEW_RUNTIME_REGISTRY_COUNT=0`.
- `FROZEN_PATH_INTERSECTION=YES`; `FROZEN_CONTRACT_IMPACT=YES`. These are expected for an authorized controlled correction to frozen test-only Harness paths; they do not imply production authority transfer.
- Universal relation governance validates bounded fixture structure and negative claims. It cannot prove actual provider behavior, world causality, truth, currentness, identity, admission, or authorization. Future provider contracts still require their own Native relation assertions.

`GROUNDING_DINO_NATIVE_CONTRACT_STATUS=UNTESTED`. After A3's separate exact-path Git freeze and final receipt, the proposed next phase is `06.5-B01 Grounding DINO Independent Contract — Execution 03`, using the **actual A3 freeze commit** as its new `SOURCE_BASELINE`. No Grounding DINO implementation is authorized by this receipt.
