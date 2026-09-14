# Owner Boundaries

| Responsibility | Owner | Boundary |
| --- | --- | --- |
| Cognition and Sufficiency/Stop | Existing Cognitive State Formation owners | Upstream proof only. |
| Decision semantics | Decision Governance | Supplies selected Decision Candidate; does not execute Action. |
| Task admission/lifecycle | Task Manager | Supplies admitted planned Task; does not execute Action. |
| Action candidate, permission/safety admission, readiness | Action Governance | Canonical Action owner. |
| Runtime execution | Runtime Executor | Future execution authority only; not invoked in this phase. |
| Integration composition | This narrow adapter | Carries canonical refs and observes results; owns no cognition, Task, or Action semantics. |

Brain, Cognitive State Formation, Decision Governance, and Task Manager do not
execute Action. The adapter has no mutation authority.

