# Current Regression Inventory

This inventory covers the current canonical paths selected for the full
regression. It distinguishes transient output replacement from durable
archive writing and stable case identity from per-execution identity.

## Stage 1–4 runner safety matrix

| Priority | Component / runner | Verifier | `_eval_out` | Archive write | Fixed identity present | Per-execution identity | Historically present | Classification |
|---|---|---|---:|---:|---:|---:|---:|---|
| P1 | `level1_cognitive_evaluation_run.runner_v1` | `level1_cognitive_evaluation_run.verifier_v1` | yes | yes | historical v1 record only | yes | yes | `RERUN_SAFE` |
| P1 | `observation_gateway.run_observation_gateway_controlled_integration_v1` | embedded checks | yes | no | no | n/a | yes | `RERUN_SAFE` |
| P1 | `cognitive_state_formation.run_cognitive_state_formation_controlled_implementation_v1` | embedded checks | yes | no | no | n/a | yes | `RERUN_SAFE` |
| P1 | `a_route_cognitive_whitebox_foundation.runner_v1` | `a_route_cognitive_whitebox_foundation.verifier_v1` | yes | no | no | n/a | yes | `RERUN_SAFE` |
| P0 | `a_route_orchestration.run_a_route_controlled_replay_runtime_enablement_v1` | `a_route_orchestration.verify_a_route_controlled_replay_runtime_enablement_v1` | yes | no | no | n/a | yes | `RERUN_SAFE` |
| P0 | `level1_cognitive_evaluation_run.run_controlled_replay_integration_v1` | `level1_cognitive_evaluation_run.verify_controlled_replay_integration_v1` | yes | yes | historical fixed record only | yes | yes | `RERUN_SAFE` after per-execution remediation |
| P0 | `level1_cognitive_evaluation_run.run_minimum_sufficient_cognition_loop_controlled_replay_v1` | `level1_cognitive_evaluation_run.verify_minimum_sufficient_cognition_loop_controlled_replay_v1` | yes | yes | no current fixed identity | yes | yes | `RERUN_SAFE` |

The three archive-writing runners are `runner_v1`,
`run_controlled_replay_integration_v1`, and
`run_minimum_sufficient_cognition_loop_controlled_replay_v1`. Each current
execution must derive a new Evaluation Run identity. The old synthetic and
replay fixed-identity archive files are historical evidence; they are not
targets for overwrite or rerun.

## Current output paths and arguments

| Runner | Required arguments | Expected output |
|---|---|---|
| `capabilities.evaluation.level1_cognitive_evaluation_run.runner_v1` | none | `_eval_out/level1_cognitive_evaluation_run_boundary_v1/runner_summary_v1.json` |
| `capabilities.midplatform.core.observation_gateway.run_observation_gateway_controlled_integration_v1` | none | `_eval_out/a_route_perception_observation_gateway_controlled_integration_v1/observation_gateway_result_v1.json` |
| `capabilities.midplatform.core.cognitive_state_formation.run_cognitive_state_formation_controlled_implementation_v1` | none | `_eval_out/cognitive_state_formation_controlled_implementation_v1/cognitive_state_formation_result_v1.json` |
| `capabilities.evaluation.a_route_cognitive_whitebox_foundation.runner_v1` | none | `_eval_out/a_route_cognitive_whitebox_trace_and_execution_profile_foundation_v1/synthetic_cognitive_whitebox_runner_v1.json` |
| `capabilities.midplatform.core.a_route_orchestration.run_a_route_controlled_replay_runtime_enablement_v1` | none | `_eval_out/a_route_controlled_replay_runtime_enablement_v1/runner_summary_v1.json` |
| `capabilities.evaluation.level1_cognitive_evaluation_run.run_controlled_replay_integration_v1` | none | `_eval_out/level1_replay_evaluation_whitebox_archive_governance_integration_v1/runner_summary_v1.json`; one new archive record |
| `capabilities.evaluation.level1_cognitive_evaluation_run.run_minimum_sufficient_cognition_loop_controlled_replay_v1` | none | `_eval_out/level1_minimum_sufficient_cognition_loop_controlled_replay_v1/runner_summary_v1.json`; per-case archive records |

All listed current runners are retained in the plan. The synthetic boundary
runner is P1 because it is compatibility coverage, not a prerequisite for
controlled replay cognition. Contract-only Dataset Registry and Level-1
Field Cognition Suite assets are audited through dependent runners and their
validators; they are not blindly invoked as historical CLIs.

## Historical and deferred assets

`run_a_route_orchestration_controlled_integration_v1` is historical/supporting
coverage and is not a P0 current-system command. Existing archive records,
including partial Case A history from an earlier failed two-case run, remain
read-only historical records. The audit classifies them without deletion,
repair, or overwrite.
