# Verification

Runner:

```bash
python3 -m capabilities.evaluation.self_field_target_situated_state_perception_foundation.self_field_target_situated_state_perception_runner_v1
```

Verifier:

```bash
python3 -m capabilities.evaluation.self_field_target_situated_state_perception_foundation.self_field_target_situated_state_perception_verifier_v1
```

The Agent did not execute either command.  The verifier is prepared to check:

- condition statuses are derived from situated inputs rather than fixture
  `satisfied_condition_refs`;
- unknown conditions do not pass as satisfied;
- visibility and relation changes alter derived conditions and feasibility;
- minimum conditions are consumed by existing Feasibility;
- gaps trace to the derived situated state;
- no provider/model/action/runtime execution or state mutation occurs;
- candidate-only and traceability invariants hold.

## Closure

The first terminal verification was `27/28`; the only failure was
`no_device_control`, caused by a missing false output projection.  After the
contract repair, the user terminal reported:

- `30/30` checks;
- `all_checks_passed=true`;
- `controlled_logic_result=PASS`;
- `failed_checks=[]`;
- `validation_errors=[]`.

Final status: `CONTROLLED LOGIC VERIFIED — PHASE CLOSED FOR DECLARED SCOPE`.

## Post-verification contract repair

The first terminal run produced `27/28` passing checks; the sole failure was
`no_device_control`.  Static review showed a missing
`forbidden_behaviors.device_control=false` projection, not a device-control
execution.  The repaired output now exposes `device_control=false` at the
top-level, Situated State Perception behavior, and downstream precondition
result behavior layers.  This is classified as
`VERIFIER_OUTPUT_CONTRACT_GAP`; no condition derivation or feasibility logic
was changed.  A new terminal Runner/Verifier run is required.
