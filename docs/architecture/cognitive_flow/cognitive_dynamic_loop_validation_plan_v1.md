# Cognitive Dynamic Loop Validation Plan v1

- Phase: `Phase-Cognitive-Foundation-Dynamic-Loop-Validation-v1-001`
- Stage / Mode: Controlled DryRun
- Scope: synthetic Field Change, Hypothesis Revision, Experience Influence, Failure Recovery, trace and deterministic replay validation.
- Previous Phase: `Phase-Cognitive-Foundation-Mock-Loop-Validation-v1-001`
- Previous Decision: `COGNITIVE_FOUNDATION_MOCK_LOOP_VALIDATION_READY_WITH_NOTES`

Dynamic cycles use new immutable snapshots and candidate references. They do not modify old Context, Field State, Reducer State, Decision, Action, Permission, Memory, Experience, Constitution, or Runtime.

V0 allows compile/schema/boundary checks. V1 allows only the synthetic runner twice plus validator. V2 is User Terminal only and V3 is ChatGPT only. Stop at `WAITING_FOR_USER_TERMINAL_VERIFICATION`; V0/V1 do not grant GO.

## Reproducible controlled validation commands

```bash
python3 -m cognitive.validation.cognitive_dynamic_loop_runner_v1 --output _tmp_eval_out/cognitive_dynamic_loop_v1/trace_a.json
python3 -m cognitive.validation.cognitive_dynamic_loop_runner_v1 --output _tmp_eval_out/cognitive_dynamic_loop_v1/trace_b.json
python3 -m cognitive.validation.cognitive_dynamic_loop_validator_v1 --input _tmp_eval_out/cognitive_dynamic_loop_v1/trace_a.json --replay _tmp_eval_out/cognitive_dynamic_loop_v1/trace_b.json
```

These are V1 controlled DryRun commands, not a V2 Final Phase Verifier.
