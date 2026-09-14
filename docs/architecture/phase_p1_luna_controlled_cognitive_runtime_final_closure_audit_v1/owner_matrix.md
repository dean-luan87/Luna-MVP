# Owner matrix result

| Surface | Canonical owner | Audit relationship |
|---|---|---|
| Observation admission | Observation Gateway | ingress/admission |
| Cognitive coordination | A-Route Orchestration | route coordination only |
| Cognition, Sufficiency, Gap, Revision, Stop | Cognitive State Formation Governance | semantic production |
| Decision Candidate | Decision Governance | decision semantics |
| Controlled Task state | Task Manager | task admission/lifecycle |
| Action Candidate/readiness | Action Governance | action admission and candidate eligibility |
| Real execution | Runtime Executor | deferred future authority |
| Memory mutation | Memory Governance | outside this baseline |
| Experience mutation | Experience Governance | outside this baseline |
| Learning mutation | Learning Governance | outside this baseline |
| Brain | responsibility domain | coordination; not a monolithic mutation owner |

The audit requires Brain, CState, Decision, and Task Manager takeover flags to
remain false. Existing unresolved Brain coordination authorities remain
non-blocking architecture debt unless they prevent the controlled path.

