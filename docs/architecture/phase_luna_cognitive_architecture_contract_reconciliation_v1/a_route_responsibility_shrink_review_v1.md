# A Route Responsibility Shrink Review

## Target definition

A Route is the Reality Thinking Engine for one active Cognitive Concern. It
owns reasoning direction, current reality evaluation, cognitive-gap judgment,
sufficiency judgment, evidence request, B contingency request and reasoning
continuation/pause/resume/closure request semantics.

A Route is not the owner of every stage it currently orchestrates.

| Current component | Current status | Target conceptual status |
|---|---|---|
| Observation Gateway | Admission/evidence boundary | External governed service consumed/requested by A |
| Active Observation Control / FPO | Need/admission/provider boundary | External governed capability |
| Model Manager / Provider | Resolution/provider mapping | External Capability/Provider Governance |
| Context Foundation | Context assembly | External canonical owner |
| Field / Current World | Field reduction and World candidate | External authoritative/reference owner |
| Attention | Relevance/allocation candidate | External cognitive input |
| Intent Governance | Intent governance | External owner; A consumes constraints |
| Decision Governance | Decision authority | Downstream governance after A result |
| Task Manager | Task lifecycle/readiness | Downstream execution organization |
| Action Governance | Action candidate/admission | Downstream action boundary |
| Runtime Executor | Runtime admission/result | Outside cognition |
| Outcome Evaluation | Comparison/feedback | External feedback owner |
| Memory / Learning | Candidate/admission | External owners; not A semantics |
| Loop Engine | Persistence/lifecycle mechanics | Shared A/B mechanics |

## Genuine A capabilities

- active concern reasoning direction;
- current reality interpretation under Field/Context/Role;
- cognitive gap and evidence relevance judgment;
- local sufficiency judgment;
- current minimum Need request;
- governed Capability/Observation request;
- bounded B contingency request;
- A/B candidate consolidation;
- continuation, pause, resume, replan or closure request.

## Narrowing rule

Current A stage names for Decision, Task, Action, Runtime, Memory/Experience,
Learning, Self and Personality are handoff targets, not A semantic ownership.
Existing implementation remains untouched.

## Risk

Sufficiency, reconsideration and lifecycle callbacks are high-risk boundaries
because existing Dynamic Flow and Loop fixtures assert them. Migration should
retain candidate envelopes and change authority declarations before field or
type removal.
