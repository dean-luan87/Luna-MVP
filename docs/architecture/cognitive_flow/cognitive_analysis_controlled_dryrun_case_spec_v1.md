# Cognitive Analysis Controlled DryRun Case Specification v1

## Common case rules

Each future case uses its mapped existing fixed fixture, preserves its local
IDs, and must report `local_reference_closure=true`,
`cross_case_reference_count=0`, and `dangling_reference_count=0`. A planned
Case ID is report metadata; it does not rename the skeleton fixture ID.

| Planned case | Actual fixture | Expected object/status | Expected warnings/reasons | Negative guard and stop condition |
| --- | --- | --- | --- | --- |
| `A3_DR_CASE_001_SUPPORTED_SINGLE_HYPOTHESIS` | `case_01_supported` | admitted Admission; one supported Hypothesis; `supports` Assessment; sufficient Sufficiency; complete Result. | None required. | No Fact/Decision/Event Candidate/State writeback. Any enabled prohibited flag is blocker. |
| `A3_DR_CASE_002_UNRESOLVED_COMPETING_HYPOTHESES` | `case_02_competing` | at least two Hypotheses; Set `unresolved`; empty dominant ref; provisional Result. | `competing_hypotheses_unresolved`. | Do not select/remove a hypothesis; State writeback is blocker. |
| `A3_DR_CASE_003_CONTRADICTED_HYPOTHESIS` | `case_03_contradicted` | `contradicts` Assessment with contradiction reason; contradicted Hypothesis; provisional Result. | `evidence_conflict`. | Preserve contradictory Evidence; no unconditional complete Result. |
| `A3_DR_CASE_004_CONTEXT_INSUFFICIENT_BLOCKED` | `case_04_insufficient` | blocked Admission/Sufficiency/Result; fixture Hypothesis is structural only, not a valid conclusion. | `context_insufficient`, `gap:critical`. | No admission upgrade, model completion, effective interpretation, or Decision boundary. |
| `A3_DR_CASE_005_REVOKED_EVIDENCE_STALE` | `case_05_revoked` | revoked Assessment; underdetermined Hypothesis; stale Result. | `evidence_revoked`, `context_refresh_required`. | Revoked Evidence cannot support; preserve history; no substitute Evidence. |
| `A3_DR_CASE_006_TEMPORAL_UNKNOWN_CONDITIONAL` | `case_06_temporal_unknown` | conditionally admitted; conditionally sufficient; provisional Result. | `temporal_validity_unknown`. | Unknown is neither valid nor false; no unconditional complete Result. |
| `A3_DR_CASE_007_GAP_REFINEMENT_OBSERVATION_REQUEST` | `case_07_gap_request` | Gap Refinement with source gap/question/criteria; Request references Refinement; incomplete Result references both. | `critical_information_gap` is actual fixture reason. | `execution_admitted=false`; any observation call/callback is blocker. |
| `A3_DR_CASE_008_STATE_WRITEBACK_DENIED` | `case_08_writeback_denied` | blocked Admission/Sufficiency/Result; all Result boundary flags remain false/true as frozen. | `analysis_blocked`. | No mutation command, Context/Snapshot/State change, Reducer runtime, or bypass path. |

## Actual-field compatibility notes

The current blocked fixture contains an explicit candidate-only
`provisional_interpretation` field. Future validation must interpret
`result_status=blocked` as non-effective: the text may be present for
structural serialization but cannot be treated as an analysis conclusion.

The current Gap fixture exposes the request through
`observation_request_candidate_refs` and `execution_admitted=false`; a future
runner may report candidate creation as a check, but must not invent an
unrecorded fixture warning or execute observation.
