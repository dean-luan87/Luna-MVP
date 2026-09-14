# Owner Boundaries

| Boundary | Owner | Phase relationship |
|---|---|---|
| Cognition | Cognitive State Formation Governance | Reference only |
| Decision Candidate | Decision Governance | Reference only |
| Task admission/state | Task Manager | Produces source state |
| Action admission/candidate | Action Governance / Action Boundary | Consumes Task-derived candidate |
| Runtime Action execution | Runtime Executor / Action execution boundary | Not invoked |

Task Manager does not execute Action. Decision Governance, Brain, and
Cognitive State Formation do not execute Action.
