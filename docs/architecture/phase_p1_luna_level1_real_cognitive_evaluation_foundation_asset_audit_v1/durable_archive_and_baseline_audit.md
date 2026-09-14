# Durable Archive and Baseline Audit

## Existing artifacts

The repository contains `_eval_out/`, `_tmp_eval_out/`, Model Test Lens local job storage, TestBoard manifests/result summaries/artifact refs, `EvaluationReportV0`, Model Test Result Envelope V1, model benchmark records, and various phase-specific JSON outputs.

These assets preserve useful execution evidence. They are not equivalent to a canonical durable archive because the audit found no general owner-controlled record with immutable Evaluation Run identity, Luna version, code/config version, dataset/sample/case versions, trace refs, failure attribution, environment, timestamp, and historical retention semantics.

`EvaluationReportV0` explicitly says it is Evaluation Tools only, not White-box, and must not mutate mainline decisions. The Model Test Lens envelope is candidate-only and model-centered. TestBoard protects artifacts but does not become their semantic source-of-truth.

## Baseline and comparison

The model evaluation engine and dual-route comparison processor provide candidate-only Plane B precedents. They can compare scoped model/provider outputs and trace completeness, but no generic same-Cognitive-Test-Case × changed-Luna-version baseline store or comparison contract was found. There is no evidence for durable statuses such as regression/improvement/unchanged/incomparable with cognitive-process and failure-attribution deltas.

## Readiness

- Durable evaluation archive: `BLOCKED` for the target chain.
- Reproducible historical baseline: `BLOCKED`.
- Comparison: `PARTIAL` for model/provider candidate comparisons; `ABSENT` for primary Luna cognitive comparison.

The next implementation should add an evaluation-owned, append-only archive boundary while reusing existing Trace/Profile, Level-1 case, report, and TestBoard references. It must not make `_eval_out` canonical merely by copying it.

