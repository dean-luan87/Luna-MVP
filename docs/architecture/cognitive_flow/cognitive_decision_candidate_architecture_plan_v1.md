# Decision Candidate Formation Architecture Plan v1

## Position

Decision Candidate Formation Layer builds a traceable choice space from Behavior Candidates and their Cognitive Value Evaluations. Its flow is:

`Behavior Candidate -> Cognitive Value Evaluation -> Decision Candidate Formation -> Future Decision -> Future Action Candidate`.

It answers “which options are sufficiently represented to enter a future decision stage?” It does not make a Decision, select an option, issue a command, grant Permission, execute behavior, or mutate State.

## Inputs and output

The layer may consume governed references to Survival, Mission, Context, Field/View, Attention, Information Value, Strategy, Cognitive Depth, Hypothesis, Belief, Reasoning Lifecycle, Cognitive Constraint, Behavior Boundary, Behavior Candidate, Cognitive Value Evaluation, Experience/Library pattern, provenance, and trace.

Output is a candidate-only `CognitiveDecisionCandidateV1` within a Choice Space. It remains explicitly non-Fact, non-State, non-Decision, non-Action, non-Permission, and non-Memory.

## Responsibility separation

| Layer | Responsibility | Excluded authority |
| --- | --- | --- |
| Behavior Candidate | Express possible behaviors | Choice admission or selection |
| Value Evaluation | Describe trade-off dimensions | Final ranking or Decision |
| Decision Candidate Formation | Form candidate choice space | Decision or Action |
| Future Decision | Separately select from eligible candidates | State mutation or Action execution |
| Reducer | Sole State Mutation Authority | Candidate formation |
