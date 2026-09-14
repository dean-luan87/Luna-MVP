# A-Route Attention Scenario Registry v1

## Controlled future cases

| Scenario | Inputs | Required candidate outcome | Negative guard |
|---|---|---|---|
| multi_target_competition | several objects with differing Goal, risk, uncertainty, and cost candidates | traceable Information Prioritization Candidate | no Decision or Provider call |
| dynamic_hazard_change | previously stable condition gains abrupt Temporal Change Candidate | attention transfer candidate | no automatic tempo increase or Action |
| goal_shift | Goal Context changes from route finding to locating an entrance | different Goal Attention candidate | no Goal self-creation |
| constrained_resources | several relevant targets with limited resource-cost envelope | bounded deferred/reduced attention candidate | no actual CPU/GPU allocation |
| self_capability_difference | same world with different Self Capability Context | different self-situated attention candidate | no Self Model mutation |

## Required trace fields

`scenario_id`, `source_candidates`, `target_candidate`, `relevance_candidate`,
`risk_candidate`, `goal_alignment_candidate`, `temporal_change_candidate`,
`uncertainty_candidate`, `resource_cost_candidate`, `selection_candidate`, and
`trace_ref`.

No case may introduce Attention Runtime, automatic model invocation, automatic
visual control, online learning, B Reflection, Scheduler work, Action, or State
mutation.
