# Attention Axis and Observation Requirement Scenario Registry v1

| Scenario | Inputs | Required candidate result | Guard |
|---|---|---|---|
| multi_object_competition | task need, possible safety risk, temporal change, and limited cost envelope | traceable Attention Priority Candidate / requirement ordering | no Decision or automatic Provider call |
| goal_change_axis_shift | Goal Context changes | Attention Axis Candidate direction/region/entity changes | no self-created Goal |
| constrained_observation | incomplete resource feasibility | compressed or deferred Attention Requirement Candidate | no actual allocation or frequency change |
| observation_failure | evidence coverage is insufficient | Attention Feedback Candidate carries missing information and failure reason | no automatic retry or strategy mutation |
| self_difference | same world with different Self Capability Context | differing Attention Requirement Candidate | no Self Model change |

## Required trace fields

`intent_ref`, `requirement_ref`, `axis_ref`, `priority_candidate`,
`resource_cost_candidate`, `observation_candidate_ref`, `evidence_ref`,
`feedback_ref`, `missing_information`, and `trace_ref`.

These are future controlled cases only. No Attention Runtime, automatic visual
control, automatic model invocation, Scheduler, online learning, B Reflection,
Action, or State mutation is authorized.

