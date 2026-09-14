# Reality Cognition Simulation Scenario Registry v1

## Controlled fixture structure

```text
Scenario
├── Initial World State
├── Self Capability State
├── Goal
├── Resource Context
├── Unknown Factors
├── Expected Cognitive Trace
└── Evaluation Criteria
```

## v1 scenario set

| Scenario | Level | Architectural assertion |
|---|---|---|
| `level1_gully_child` | basic | a capability-limited child forms a different Situation from the same gully |
| `level1_gully_cattle` | basic | a higher-capability subject has different situated meaning for the same gully |
| `level1_low_resource_navigation` | basic | Resource Context is visible in the decision trace |
| `level2_risk_route_choice` | decision | risk/survival/resource factors remain explicit in option evaluation |
| `level2_information_insufficient` | decision | unknown is recognized and a non-forced information candidate is formed |
| `level3_prediction_error_environment_change` | complex feedback | outcome deviation localizes environment-change candidate |
| `level3_capability_constraint` | complex feedback | outcome failure can localize Self Capability constraint |

All scenarios are static local fixtures. They are not world simulations,
model benchmarks, hardware tests, or action executions.
