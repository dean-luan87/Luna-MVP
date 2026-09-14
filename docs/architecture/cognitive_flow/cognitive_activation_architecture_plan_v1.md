# Cognitive Activation Architecture Plan v1

- Phase: `Phase-Cognitive-Activation-Architecture-Planning-v1-001`
- Stage: Planning Only
- Previous Phase: `Phase-Cognitive-Retention-and-Activation-Architecture-Planning-v1-001`
- Previous Decision: `COGNITIVE_RETENTION_AND_ACTIVATION_ARCHITECTURE_PLANNING_READY_WITH_NOTES`

## Position

`Task / Field / Experience / Retention -> Cognitive Activation Candidate -> Attention Allocation Candidate -> Current Cognitive Runtime`.

Activation is the continuity scheduler that decides which retained cognitive candidates should re-enter the current candidate space. It is not Attention Selection, Memory Retrieval, Decision, Action, Rule Engine, Scheduler, or Storage.

## Inputs and output

Inputs: Current Field, Current Context, Task State, Goal, Time, Risk, Experience Match, and Resource Availability candidates.

Output: Activation Candidate with Target Representation, Activation Reason, Priority Candidate, Expected Value, Resource Cost Candidate, validity reference, and provenance.

No Runtime, State mutation, Memory mutation, Decision, Action, or Reducer modification is authorized.
