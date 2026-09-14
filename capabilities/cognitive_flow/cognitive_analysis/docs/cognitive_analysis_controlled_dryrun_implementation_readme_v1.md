# Cognitive Analysis Controlled DryRun Implementation v1

This fixture-only DryRun validates the A3 skeleton's eight fixed cases through
object, reference, semantic, permission, and negative-guard checks. It uses
`A3_COGNITIVE_ANALYSIS_FIXTURE_BASELINE_V1`; it does not execute real
analysis, Context runtime, Reducer runtime, model, network, database,
observation, Decision, or State writeback.

The Runner serializes deterministic JSON reports; the Verifier independently
reads those reports and recomputes count, boundary, baseline, Contract, and
negative-guard conditions. Both use fixed flags: runtime false, simulation
true, no model/network/database/observation/decision/writeback.

```text
python3 -m capabilities.cognitive_flow.cognitive_analysis.dryrun.cognitive_analysis_dryrun_runner_v1 --output-dir _eval_out/a3_cognitive_analysis_controlled_dryrun_v1_smoke_v0
python3 -m capabilities.cognitive_flow.cognitive_analysis.dryrun.cognitive_analysis_dryrun_verifier_v1 --input-dir _eval_out/a3_cognitive_analysis_controlled_dryrun_v1_smoke_v0
```

The output directory contains run, case, guard, reference-closure,
verification JSON, and a deterministic summary. This implementation is not
Runtime Ready or Production Ready; Post Review is the next potential phase.
