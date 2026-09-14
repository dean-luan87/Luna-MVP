# Cognitive Simulation Branch Model v1

A Simulation Branch Candidate contains Initial Condition, Changed Variable, Transformation Candidate, Possible Outcome, Confidence Candidate, Evidence Requirement, uncertainty, cost, reversibility, provenance, and trace.

Example branches: normal weather + subway -> on-time-arrival candidate; heavy rain + road congestion -> increased-delay-risk candidate.

Branch != Truth, Prediction, Decision, Action, Permission, or State mutation. Branch operations are create, initialize, expand, evaluate, preserve, discard, and close candidates.
