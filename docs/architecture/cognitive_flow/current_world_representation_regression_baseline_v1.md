# Current World Representation Regression Baseline v1

## 1. Baseline identity

- Baseline: `cwr_integration_dryrun_v1`
- Source output directory: `_eval_out/current_world_representation_integration_dryrun_v1_smoke_v0/`
- Scope: A2.8 fixed-fixture integration only
- Baseline does not represent a runtime baseline, production baseline, State baseline, or semantic-correctness baseline.

## 2. Frozen expectations

| Metric | Expected value |
| --- | --- |
| `expected_case_count` | `6` |
| `expected_passed_checks` | `18` |
| `expected_failed_checks` | `0` |
| `expected_blocker_count` | `0` |
| `runtime_executed` | `false` |
| `simulation_only` | `true` |
| reference-chain results | `6/6 true` |
| version-chain results | `6/6 true` |
| Cognitive Analysis writeback | absent in all six results |
| static negative guards | empty result |

## 3. Expected case set

1. `case_01_complete`
2. `case_02_unknown_time`
3. `case_03_snapshot_refresh`
4. `case_04_multi_context`
5. `case_05_context_insufficient`
6. `case_06_evidence_revoked`

## 4. Governed warnings

The baseline expects, rather than eliminates:

- `unknown_time_preserved`
- `context_v1_refresh_required`
- `refresh_required`

These values indicate preserved uncertainty, immutable Context refresh, and Evidence revocation response. Treating their presence as a failure would weaken the CWR boundary.

## 5. Output-file baseline

- `current_world_representation_integration_dryrun_result_v1.json`
- `current_world_representation_integration_dryrun_case_matrix_v1.json`
- `current_world_representation_integration_dryrun_verification_v1.json`

## 6. Regression failure conditions

A later controlled run regresses this baseline if it changes the expected case set/count; reduces passed checks below 18; reports failed checks or blockers; sets runtime execution true; sets simulation-only false; loses any reference/version-chain result; removes preserved warnings by automatic completion; permits Analysis writeback; adds non-Reducer State mutation; or reports a forbidden static guard.
