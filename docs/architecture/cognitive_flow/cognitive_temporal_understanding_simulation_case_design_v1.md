# Temporal Understanding Controlled Case Design v1

## Test posture

These are future controlled A-route simulation cases, not a Temporal Runtime,
prediction benchmark, hardware test, or intelligence score. They evaluate
whether temporal information remains candidate-only and improves situated
understanding without violating A Core boundaries.

| Case | Input distinction | Required candidate evidence | Boundary check |
|---|---|---|---|
| Static vs dynamic | same current traffic density; one stable, one rapidly increasing | transition and change-relevance candidates differ | no automatic route choice |
| Trend change | energy reserve decreases across governed observations | bounded resource-pressure possibility and uncertainty | no frequency change or resource allocation |
| Cyclic change | same route under day and night illumination references | cyclic pattern and low-light capability coupling candidate | no prediction written as fact |
| Abrupt change | represented environment changes between observations | abrupt-change and additional-observation need candidate | no automatic provider call or action |
| Self difference | same declining illumination for different visual capability contexts | Situation Enhancement Candidate differs by Self capability | no change to capability facts |

## Trace requirements

Each future case must retain `past_reference`, `current_state_reference`,
`change_evidence`, `temporal_uncertainty`, `situation_enhancement_candidate`,
`decision_support_candidate`, and `trace_ref`. It must record that no real Action,
Scheduler, Provider execution, state mutation, B Reflection, or online learning
occurred.

## Regression requirement

Any later implementation must rerun the frozen seven A-route baseline fixtures
and add these temporal cases without replacing baseline metrics for Self
Awareness, Reality Grounding, Situation Quality, Decision Reasoning, and
Feedback Quality.
