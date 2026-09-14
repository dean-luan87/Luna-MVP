# Cognitive Loop lifecycle closure contract

This contract extends the existing Cognitive Flow Loop envelope for
`Phase-Luna-Cognitive-Loop-Lifecycle-Closure-And-Assimilation-Bridge-Controlled-Implementation-v1-001`.
The canonical owner remains Brain subject / Cognitive Flow Governance.

## Closure stages

```text
Loop Local State
  -> ClosureAssessmentCandidateV1
  -> ClosureDecisionCandidateV1 (Brain/Cognitive Flow governed)
  -> LifecycleClosureCandidateV1
  -> LoopClosureRecordCandidateV1
  -> CognitiveOutcomeCandidateV1
  -> BrainAssimilationCandidateV1
```

`closure_candidate_created` is only an assessment/record proposal.
`lifecycle_closure_accepted` is a separate governed result. Until acceptance,
the Loop-local closure state remains `OPEN` and no final state is frozen.
The Loop cannot self-authorize either decision.

Accepted closure uses the existing candidate lifecycle vocabulary where it
fits: `COMPLETED`, `STOPPED`, `SUPERSEDED`, `ABANDONED_BY_VALUE`, or `FAILED`.
These are Loop-local candidate dispositions and do not mutate Task, Intent,
World, Memory, Experience, or Brain state.

`STOP_SUFFICIENT` maps to successful `COMPLETED`; unmaterialized remaining
plan candidates are disposed as not required, never recorded as failures.
`FAILED` is a cognitive concern disposition only and does not imply Task
failure.

No accepted closure invokes a Provider, Action, Scheduler, Learning path, or
child Loop.
