# Synthetic Fixture and Verification v1

## Fixture coverage

`fixtures_v1.py` adds `rf_detr_normalization_cases_v1()` with:

The cases use the observed one-image `model_output_3.predictions` envelope and
cover:

1. normal detection;
2. multiple detections;
3. empty predictions;
4. malformed prediction missing observed geometry;
5. low-confidence candidate;
6. unknown provider-only extra field;
7. missing `model_output_3`;
8. missing `predictions`;
9. `predictions` with the wrong type.

The fixture supplies raw provider-shaped input only. It does not create World
Truth, a Decision, a Task, or an Action.

## Runner

The existing Roboflow PoC `runner_v1.py` now includes:

- repository declaration checks;
- RF-DETR normalization case records;
- deterministic provider/model/workflow/trace/provenance checks;
- no-runtime flags;
- existing cognitive structural cases and negative cases.

The Runner does not call the SDK in structural mode. It uses
`native_payload` only as a synthetic adapter input.

## Verifier

The existing `verifier_v1.py` now requires:

- RF-DETR model declaration;
- object-detection Capability↔Model binding;
- Roboflow Provider/workflow binding;
- `inference_sdk` transport declaration;
- `image` input and `$[0].model_output_3.predictions` output mapping;
- no embedded credential;
- candidate-only normalization;
- raw schema isolation;
- provenance/trace/model identity retention;
- existing Observation Gateway handoff construction for non-empty normalized
  Evidence;
- no model loading, Provider invocation, network, Observation, Action, source
  mutation, or World Truth.

The helper `rf_detr_declaration_validator_v1.py` reads owner-controlled
registries and returns diagnostics; it does not synthesize declarations.

## Structural versus real verification

The verifier is mode-scoped. In `structural` mode, the RF-DETR normalization
regression aggregate, Observation Gateway handoff regression aggregate, and
negative fixture aggregate are required checks. Their checks remain strict;
they are exposed as not applicable in `real` mode rather than being treated
as successful fixture results.

In `real` mode, the verifier checks the current provider response directly:
successful normalization or a legal empty result, the real Observation
Gateway handoff boundary, provenance, and the no-truth/no-mutation guards.
The real case does not need to replay the structural fixture aggregates.

The real cognitive boundary also remains ownership-preserving. When the
Luna-side sufficiency candidate is `SUFFICIENT`, this adapter may stop with
`next_target = "Decision Governance"` and no Decision candidate. If a
Decision candidate is present, its owner must be `Decision Governance`. When
sufficiency is `INSUFFICIENT`, a Next Observation candidate is required and
the current adapter must not create a Decision.

## Required terminal commands

Do not run during agent implementation. The user may run after review:

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 -m capabilities.midplatform.field_perception_orchestrator.integration.roboflow_provider_poc.runner_v1 --mode structural --output _tmp_eval_out/roboflow_provider_poc/rf_detr_structural_summary_v1.json
cd /Users/luanlei/Desktop/Luna-Core
python3 -m capabilities.midplatform.field_perception_orchestrator.integration.roboflow_provider_poc.verifier_v1 _tmp_eval_out/roboflow_provider_poc/rf_detr_structural_summary_v1.json
```

These commands are structural only. They do not constitute a real Roboflow
smoke and do not install `inference_sdk`.
