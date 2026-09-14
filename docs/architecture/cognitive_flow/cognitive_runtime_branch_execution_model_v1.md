# Cognitive Runtime Branch Execution Model v1

One Runtime Instance may hold Branch Candidate sets such as vehicle stops, continues, or turns. Each branch carries assumption, evidence references, confidence candidate, uncertainty, evaluation reference, resource cost, and provenance.

Branch operations are create, preserve, weaken, strengthen, merge, suspend, and discard candidates. Branch != Truth, Prediction, Decision, Action, or State mutation. Simulation / possible-world exploration != future confirmation.

Multi-branch execution is a candidate-space model, not parallel Runtime implementation.
