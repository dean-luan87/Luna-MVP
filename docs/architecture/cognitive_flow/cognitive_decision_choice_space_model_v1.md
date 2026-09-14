# Decision Choice Space Model v1

## Definition

Choice Space is a bounded, traceable set of current Decision Candidates. It represents possible future selection inputs, not an ordered answer or a policy outcome.

The model supports Multiple Candidate Options, Conflicting Options, Unknown Options, Deferred Options, and Alternative Paths. Each option preserves its own Behavior Candidate, Value Evaluation, uncertainty, conflict, provenance, and trace references.

## Unknown and deferral

Unknown options remain valid when evidence is insufficient. Deferred options represent that an option might be reconsidered after more information, time, or changed Context. Neither unknown nor deferral implies failure, selection, or execution.

Choice Space cannot remove a constrained Behavior Boundary, synthesize a missing option as Fact, or automatically choose the highest apparent value.
