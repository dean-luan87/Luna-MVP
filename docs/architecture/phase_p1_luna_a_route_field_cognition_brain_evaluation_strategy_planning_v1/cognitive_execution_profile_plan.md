# Luna Cognitive Execution Profile Plan

## Primary profile

The primary future profile is `LunaCognitiveExecutionProfileV1`, not a
ModelFitProfile.

## Planned groups

- **Task**: goal, concern, role, environment, task identity;
- **Cognitive Entry**: prior context, initial field candidate, available knowledge;
- **Attention**: selected/ignored targets and transitions;
- **Observation**: information need, demand/request, capability requirement,
  ROI, cycle refs;
- **Evidence**: received, relevant, irrelevant, conflicting, uncertain, missing;
- **World Cognition**: Current World and Field Cognition candidate revisions;
- **Hypothesis**: creation, revision, supersession, invalidation;
- **Sufficiency**: status transitions, premature/delayed/false insufficiency;
- **Information Gap**: creation, persistence, resolution;
- **Re-observation**: count, reason, target, capability/ROI changes;
- **Termination**: stop reason, completion reason, Decision handoff;
- **Performance**: cycles, cognitive transitions, observable latency/resource signals;
- **Outcome**: field cognition goal completed, incomplete, wrong, unsafe, unresolved.

## Semantics

The profile is evaluation evidence/candidate only. Missing instrumentation is
`unavailable` or `planned`, never zero. It references existing Model Test
Envelope, Trace, Evaluation Report, and TestBoard artifacts.
