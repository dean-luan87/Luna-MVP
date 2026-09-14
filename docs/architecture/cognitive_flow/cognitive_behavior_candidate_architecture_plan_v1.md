# Cognitive Behavior Candidate Architecture Plan v1

## Position

Behavior Candidate Layer creates a managed set of possible behaviors inside an existing Behavior Boundary. Its path is:

`Behavior Boundary Candidate -> Cognitive Behavior Candidate -> Future Decision Candidate -> Future Action Candidate`.

The layer answers “what behavior may be considered under current constraints?” It does not select a final behavior, grant permission, execute an Action, or mutate State.

## Inputs and output

Inputs are governed references to Survival, Current Cognitive Context, Field Identity/Affordance, Minimum Sufficient Field Understanding, Attention, Information Value, Strategy, Cognitive Depth, Hypothesis, Belief, Reasoning Lifecycle, Behavior Boundary, Goal, provenance, and trace. The output is a candidate-only `CognitiveBehaviorCandidateV1`.

## Responsibility boundary

| Layer | Responsibility | Excluded authority |
| --- | --- | --- |
| Behavior Boundary | Constrains behavior space | Selection, permission, execution |
| Behavior Candidate | Expresses individual possible behaviors | Decision and Action |
| Future Decision | Selects only from an admitted candidate space | Execution and State mutation |
| Future Action | Separately governed execution candidate | Admission or State mutation |
| Reducer | Sole State mutation authority | Behavior generation or execution |

This is Planning Only. No Runtime, provider, model, Field Kernel/Reducer integration, Memory, Learning, Hive, permission, Decision, or Action implementation is authorized.
