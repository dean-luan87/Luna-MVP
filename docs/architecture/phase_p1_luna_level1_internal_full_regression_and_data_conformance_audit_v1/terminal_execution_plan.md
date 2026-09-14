# Terminal Execution Plan

All commands below are prepared for the user terminal. The Agent does not
execute them. The plan is safe with pre-existing `_eval_out` and durable
archive history: no command deletes or overwrites archive records, and all
archive-writing current runners use a distinct execution-instance identity.

## Stage 0 — compilation, import smoke, and session baseline

```bash
cd /Users/luanlei/Desktop/Luna-Core && python -m compileall -q capabilities/evaluation/level1_cognitive_evaluation_run capabilities/evaluation/a_route_cognitive_whitebox_foundation capabilities/midplatform/core/observation_gateway capabilities/midplatform/core/a_route_orchestration capabilities/midplatform/core/cognitive_state_formation
```

Writes `_eval_out`: no. Writes durable archive: no. Rerun-safe: yes (the
interpreter may refresh bytecode caches only). Purpose: compile/static check.
Stop on failure: yes. A PASS here is not an importability PASS.

```bash
cd /Users/luanlei/Desktop/Luna-Core && python -m capabilities.evaluation.level1_cognitive_evaluation_run.preflight_full_regression_v1 --session-manifest _eval_out/level1_internal_full_regression_and_data_conformance_audit_v1/session_manifest_v1.json
```

Writes `_eval_out`: yes, only the session baseline manifest. Writes durable
archive: no. Rerun-safe: yes before any regression Runner; rerunning it starts
a new baseline and therefore must be treated as a new regression session.
Purpose: import the canonical regression modules without executing cognition,
then record observable hashes/sizes/`mtime_ns` for existing outputs and archive
records. Stop on failure: yes. This is the evidence boundary that prevents an
old PASS artifact from being counted as current-session execution.

The import smoke explicitly covers execution mode, Observation Gateway,
A-Route, Cognitive State Formation, White-box foundation, Evaluation Run,
archive, governance, and this audit module. It is independent of compileall.

## Stage 1 — foundational existing regressions

| Command | `_eval_out` | Durable archive | Rerun safety | Stop rule |
|---|---:|---:|---|---|
| `python -m capabilities.evaluation.level1_cognitive_evaluation_run.runner_v1` | yes | yes | `RERUN_SAFE`; per-execution identity | stop on failure |
| `python -m capabilities.evaluation.level1_cognitive_evaluation_run.verifier_v1 <runner_summary>` | no | no | `READ_ONLY` | stop on failure |
| `python -m capabilities.midplatform.core.observation_gateway.run_observation_gateway_controlled_integration_v1` | yes | no | `RERUN_SAFE` transient replacement | stop on failure |
| `python -m capabilities.midplatform.core.cognitive_state_formation.run_cognitive_state_formation_controlled_implementation_v1` | yes | no | `RERUN_SAFE` transient replacement | stop on failure |
| `python -m capabilities.evaluation.a_route_cognitive_whitebox_foundation.runner_v1` | yes | no | `RERUN_SAFE` transient replacement | stop on failure |
| `python -m capabilities.evaluation.a_route_cognitive_whitebox_foundation.verifier_v1` | no | no | `READ_ONLY` | stop on failure |

The exact commands and output paths are listed in `regression_inventory.md`.

```bash
cd /Users/luanlei/Desktop/Luna-Core && python -m capabilities.evaluation.level1_cognitive_evaluation_run.runner_v1
cd /Users/luanlei/Desktop/Luna-Core && python -m capabilities.evaluation.level1_cognitive_evaluation_run.verifier_v1 _eval_out/level1_cognitive_evaluation_run_boundary_v1/runner_summary_v1.json
cd /Users/luanlei/Desktop/Luna-Core && python -m capabilities.midplatform.core.observation_gateway.run_observation_gateway_controlled_integration_v1
cd /Users/luanlei/Desktop/Luna-Core && python -m capabilities.midplatform.core.cognitive_state_formation.run_cognitive_state_formation_controlled_implementation_v1
cd /Users/luanlei/Desktop/Luna-Core && python -m capabilities.evaluation.a_route_cognitive_whitebox_foundation.runner_v1
cd /Users/luanlei/Desktop/Luna-Core && python -m capabilities.evaluation.a_route_cognitive_whitebox_foundation.verifier_v1
```

Run each line only after the preceding line passes. The boundary Runner is
the only Stage 1 command that writes durable history; its new per-execution
identity makes the command rerun-safe. All other Stage 1 Runners replace only
their declared transient output.

## Stage 2 — controlled replay cognition

```bash
cd /Users/luanlei/Desktop/Luna-Core && python -m capabilities.midplatform.core.a_route_orchestration.run_a_route_controlled_replay_runtime_enablement_v1
cd /Users/luanlei/Desktop/Luna-Core && python -m capabilities.midplatform.core.a_route_orchestration.verify_a_route_controlled_replay_runtime_enablement_v1 _eval_out/a_route_controlled_replay_runtime_enablement_v1/runner_summary_v1.json
```

Runner writes `_eval_out` only; no durable archive; `RERUN_SAFE` transient
replacement. Verifier is `READ_ONLY`. Stop on either failure. This proves
Gateway → A-Route → Cognitive State Formation before archive-writing stages.

## Stage 3 — Evaluation/White-box/Governance

```bash
cd /Users/luanlei/Desktop/Luna-Core && python -m capabilities.evaluation.level1_cognitive_evaluation_run.run_controlled_replay_integration_v1
cd /Users/luanlei/Desktop/Luna-Core && python -m capabilities.evaluation.level1_cognitive_evaluation_run.verify_controlled_replay_integration_v1 _eval_out/level1_replay_evaluation_whitebox_archive_governance_integration_v1/runner_summary_v1.json
```

Runner writes `_eval_out` and one durable archive record using a fresh
execution-instance identity; `RERUN_SAFE`. Verifier writes neither and is
`READ_ONLY`. Stop on failure. The historical fixed-identity integration
record remains untouched and is not reused.

## Stage 4 — minimum sufficient cognition

```bash
cd /Users/luanlei/Desktop/Luna-Core && python -m capabilities.evaluation.level1_cognitive_evaluation_run.run_minimum_sufficient_cognition_loop_controlled_replay_v1
cd /Users/luanlei/Desktop/Luna-Core && python -m capabilities.evaluation.level1_cognitive_evaluation_run.verify_minimum_sufficient_cognition_loop_controlled_replay_v1 _eval_out/level1_minimum_sufficient_cognition_loop_controlled_replay_v1/runner_summary_v1.json
```

Runner writes `_eval_out` and per-case durable archive records using a fresh
execution-instance identity; `RERUN_SAFE`. Verifier is `READ_ONLY`. Stop on
failure. A successful Case A archive is retained if Case B later fails.

## Stage 5 — negative guards

Run the Stage 3 and Stage 4 verifiers already listed above. They cover the
existing live-runtime escalation, invalid replay admission, loop causality,
premature Stop, and post-sufficiency observation guards. These verifiers are
read-only and write neither `_eval_out` nor the durable archive. Stop on any
failure. Archive conflict behavior is audited from history; no collision is
intentionally created.

## Stage 6 — read-only runtime/output/archive audit

```bash
cd /Users/luanlei/Desktop/Luna-Core && python -m capabilities.evaluation.level1_cognitive_evaluation_run.audit_full_regression_v1 --session-manifest _eval_out/level1_internal_full_regression_and_data_conformance_audit_v1/session_manifest_v1.json
```

Writes `_eval_out`: yes, only the audit JSON/Markdown reports. Writes durable
archive: no. Rerun-safe: yes, report replacement only. Stop if required
artifacts cannot be read or the report is blocked. The audit labels outputs and
archive records `CURRENT_SESSION` only when observed metadata changed after the
Stage 0 baseline; otherwise it labels them historical/unchanged.

## Stage 7 — consolidated audit verifier

```bash
cd /Users/luanlei/Desktop/Luna-Core && python -m capabilities.evaluation.level1_cognitive_evaluation_run.verify_full_regression_audit_v1 _eval_out/level1_internal_full_regression_and_data_conformance_audit_v1/full_regression_audit_report_v1.json
```

Writes `_eval_out`: no. Writes durable archive: no. Rerun-safe: `READ_ONLY`.
Stop on failure. It fails closed on missing session evidence, BLOCKER/MAJOR
findings, failed conformance checks, or a blocked decision candidate. It is not
a replacement for component verifiers.
