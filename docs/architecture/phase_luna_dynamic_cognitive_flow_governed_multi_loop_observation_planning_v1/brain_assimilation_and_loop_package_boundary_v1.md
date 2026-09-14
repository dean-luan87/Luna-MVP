# Brain assimilation, Loop Package, and history boundary

## Assimilation boundary

`CognitiveOutcomeCandidateV1` is handed to Brain through
`BrainAssimilationCandidateV1`. Supported candidate dispositions are:

- `ACCEPT_AS_COGNITIVE_REFERENCE`
- `KEEP_AS_LOCAL_RESULT`
- `USE_FOR_REPLANNING`
- `FORWARD_TO_EXPERIENCE_GOVERNANCE`
- `DISCARD_AS_LOW_VALUE`
- `DEFER_ASSIMILATION`

This handoff does not declare World Truth, create a Decision, execute Action,
mutate Intent, create a Task, mutate Memory or Experience, execute Learning,
or automatically create another Loop. Brain remains the assimilation authority.

## Loop Package

`LoopPackageCandidateV1` promotes the existing
`LoopPackageReservationCandidateV1` boundary into a bounded reference surface.
It retains Loop identity, concern, lineage, final disposition/state version,
Need/hypothesis/evidence/capability refs, Context/Field/World, Intent/Task/
Role/Perspective, continuity and pause/wait/resume refs, closure reason,
Cognitive Outcome, trace, and provenance. It does not copy authoritative
state and performs no semantic compression.

## History policy

Runtime trace remains canonical history and is not deleted. The Loop Package
is the bounded handoff surface. Future cognition should normally reference the
package/outcome; deep audit may reference the full trace. This is a reference
policy, not compression or mutation.

## Branch and Experience reservation

Parent/derived/dependency/shared/inherited/merge refs remain read-only
reservations. A branch reservation does not create a child runtime or close the
parent. Parent supersession and merge remain Brain-governed candidates.

The only future Experience path reserved here is:

```text
Runtime Trace -> Loop Closure Record -> Loop Package Candidate
  -> Experience Candidate reference -> Experience Governance
```

Experience, Memory, Learning, Hive, and semantic compression remain deferred.
