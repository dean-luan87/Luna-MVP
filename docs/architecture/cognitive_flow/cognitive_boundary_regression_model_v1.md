# Cognitive Boundary Regression Model v1

## Regression purpose

Future integration changes must preserve these negative constraints:

- Simulation != Reality.
- Hypothesis != Fact.
- Experience != Rule.
- Experience != Reality Override.
- Schema != Truth.
- Schema != Action.
- Feedback != Automatic System Mutation.
- Feedback != Genome Mutation.
- Feedback != Culture Mutation.
- B Interface != B Route Execution.
- Runtime != Reducer.
- Reducer remains the only State Mutation Authority.

## Regression method

For each trace edge, verify that its declared output is a candidate and inspect that it does not grant state, decision, execution, truth, or learning authority. A failed guard produces a boundary-violation finding and requires architecture review; it cannot be repaired by silently changing a candidate’s confidence.
