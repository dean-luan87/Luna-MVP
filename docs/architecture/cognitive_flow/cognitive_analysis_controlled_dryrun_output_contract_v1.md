# Cognitive Analysis Controlled DryRun Output Contract v1

## Planned result models

`DryRunRunResultV1` must include phase, run ID, Contract reference, fixture
baseline reference, frozen runtime/simulation flags, case counts, warning and
blocker counts, case results, negative-guard summary, and final candidate
decision.

`DryRunCaseResultV1` must include case ID/name, fixture reference, expected and
observed status, object/reference/semantic/permission/negative checks,
warnings, failures, blockers, and pass flag.

`DryRunVerificationResultV1` must include verifier ID, source run reference,
expected/observed case counts, passed/failed checks, blocker/warning counts,
boundary result, fixture-only/runtime/simulation flags, and final candidate
decision.

These are planning shapes only; no types are created in this phase.

## Planned deterministic output set

Canonical baseline directory: `_eval_out/a3_cognitive_analysis_controlled_dryrun_v1_smoke_v0_run1/`.
Deterministic comparison directory: `_eval_out/a3_cognitive_analysis_controlled_dryrun_v1_smoke_v0_run2/`.
The unsuffixed legacy reference is deprecated and nonexistent.

1. `cognitive_analysis_dryrun_run_result_v1.json`
2. `cognitive_analysis_dryrun_case_results_v1.json`
3. `cognitive_analysis_dryrun_negative_guard_report_v1.json`
4. `cognitive_analysis_dryrun_reference_closure_v1.json`
5. `cognitive_analysis_dryrun_verification_result_v1.json`
6. `cognitive_analysis_dryrun_summary_v1.md`

Outputs must be deterministic, valid JSON where applicable, free of system
time, absolute user paths, model output, real user data, and real perception
data.

## Fixture baseline

`A3_COGNITIVE_ANALYSIS_FIXTURE_BASELINE_V1` binds the nine object types,
current enum set, current Contract, eight fixture cases and mappings,
Context-only input boundary, zero State writeback, fixture-only scope, and
simulation-only flags. Changes to types, enums, Contract, or fixtures require
a new baseline version; V1 may not be silently overwritten.
