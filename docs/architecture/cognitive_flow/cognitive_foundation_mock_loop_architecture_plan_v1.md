# Cognitive Foundation Mock Loop Architecture Plan v1

## Phase contract

- Phase: `Phase-Cognitive-Foundation-Mock-Loop-Validation-v1-001`
- Stage: Controlled DryRun
- Execution Mode: Controlled DryRun
- Previous Phase: `Phase-Cognitive-Foundation-Skeleton-Implementation-v1-001`
- Previous Phase Decision: `COGNITIVE_FOUNDATION_SKELETON_IMPLEMENTATION_READY_WITH_NOTES`

## Scope

Validate one synthetic, deterministic A-route cognitive cycle:

`Field Observation -> Perception -> Situation -> Context -> Attention -> Sufficiency -> B Route -> Future Space -> Evaluation -> Decision Candidate -> Commitment Candidate`.

The runner emits candidate-only signals and an inspectable Cognitive Trace. Replay means rerunning the identical synthetic input and comparing trace signatures; it does not retrieve Experience, change routing from history, or implement evolution.

## Out of scope

No camera, OCR, SLAM, LLM, Emotion, World Model, Memory, Experience retrieval, Field Runtime, scheduler, Decision selection, Action, permission, Human control, State mutation, or Reducer modification.

## Verification authority

- V0: Agent may compile/import files and inspect schema/boundary keywords.
- V1: Agent may run the synthetic mock-loop runner twice and validate both traces with `cognitive_trace_validator_v1.py`.
- V2: User Terminal only; Agent must not run a Final Phase Verifier.
- V3: ChatGPT only.

## Negative guards

- Synthetic Field Input != reality observation.
- Perception != risk conclusion or action suggestion.
- Situation != Decision.
- Sufficiency != Permission.
- B Route != better answer or Decision.
- Future Branch != prediction truth.
- Evaluation / Decision / Commitment Candidate != Action.
- Trace != Memory, Experience write, or State mutation.
- Replay != Learning or Evolution.

## Agent stop point

After V0 and authorized V1 controlled validation, stop at `WAITING_FOR_USER_TERMINAL_VERIFICATION`. Neither result grants GO.

## Reproducible controlled validation commands

```bash
python3 -m cognitive.validation.run_cognitive_foundation_mock_loop_dryrun_v1 --output _tmp_eval_out/cognitive_foundation_mock_loop_v1/trace_a.json
python3 -m cognitive.validation.run_cognitive_foundation_mock_loop_dryrun_v1 --output _tmp_eval_out/cognitive_foundation_mock_loop_v1/trace_b.json
python3 -m cognitive.validation.cognitive_trace_validator_v1 --input _tmp_eval_out/cognitive_foundation_mock_loop_v1/trace_a.json --replay _tmp_eval_out/cognitive_foundation_mock_loop_v1/trace_b.json
```

These are controlled V1 DryRun commands only. They are not a V2 Final Phase Verifier and cannot grant GO.
