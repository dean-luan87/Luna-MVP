# CWR Integration DryRun Runbook v1

## Commands

From the repository root:

```bash
python -m capabilities.cognitive_flow.current_world_representation_integration.runner.run_current_world_representation_integration_dryrun_v1
python -m capabilities.cognitive_flow.current_world_representation_integration.verifier.verify_current_world_representation_integration_dryrun_v1
```

## Output directory

`_eval_out/current_world_representation_integration_dryrun_v1_smoke_v0/`

- `current_world_representation_integration_dryrun_result_v1.json`
- `current_world_representation_integration_dryrun_case_matrix_v1.json`
- `current_world_representation_integration_dryrun_verification_v1.json`

## Component success and failure

The result verifier reports component readiness only. Its `GO` value means all fixture-contract checks passed; it is not Final Phase Verification and does not grant phase GO. `NO_GO` means failed case or negative-guard checks. `BLOCKED` is reserved by the contract for an execution blocker.

## Cleanup

Remove only the named output directory when its artifacts are no longer needed:

```bash
rm -rf _eval_out/current_world_representation_integration_dryrun_v1_smoke_v0
```

The runner changes no business module, state store, database, model, network resource, or external service.
