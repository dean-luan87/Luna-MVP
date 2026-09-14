# Target Loop mechanical surface

The future Loop surface should be close to:

`MATERIALIZE`, `RECORD_STATE_VERSION`, `RECORD_REFS`, `RECORD_NEED_REF`, `RECORD_REQUIREMENT_REF`, `RECORD_B_BRANCH_REF`, `PAUSE`, `WAIT`, `RESUME_RECORDED_STATE`, `SUPERSEDE_RECORDED_REF`, `CLOSE`, `FREEZE_FINAL_STATE`, `RECORD_OUTCOME_REF`, `ARCHIVE_HISTORY_BOUNDARY`, `APPEND_TRACE`.

Existing reusable pieces:

- `LoopIdentityCandidateV1` for identity/reference envelope;
- `LoopLocalStateCandidateV1` for bounded mechanical state storage;
- `LoopMaterializationCandidateV1` for Brain-governed materialization record;
- `LoopClosureRecordCandidateV1`, `FinalStateFreezeCandidateV1`, `HistoryBoundaryCandidateV1`;
- `MechanicalCommandCandidateV1`, `MechanicalCommandValidationCandidateV1`, `LoopMechanicalStateCandidateV1`, and `LoopMechanicalReturnCandidateV1` from the Authority Grant phase.

Semantic helpers that should eventually disappear from Loop integration include `_local_disposition`, local construction of `ReconsiderationCandidateV1`, direct resume decision derivation, and any local choice of Need, Sufficiency, Capability or closure reason.

