# A-Route Simulation Baseline Contract v1

## Frozen baseline

The seven controlled fixtures in `reality_cognition_simulation_scenarios_v1.json` are the A-route simulation baseline.

- `level1_gully_child`; `level1_gully_cattle`; `level1_low_resource_navigation`.
- `level2_risk_route_choice`; `level2_information_insufficient`.
- `level3_prediction_error_environment_change`; `level3_capability_constraint`.

## Regression invariants

Future changes to World Model, Self Model, Situation, Decision, Experience, or Evidence integration must revalidate:

- Self Awareness;
- Reality Grounding;
- Situation Quality;
- Decision Reasoning;
- Feedback Quality;
- Candidate-only authority and deterministic replay.

The baseline is engineering governance evidence.
It is not a Runtime input, reward dataset, model-training corpus, or proof of real-world intelligence.
