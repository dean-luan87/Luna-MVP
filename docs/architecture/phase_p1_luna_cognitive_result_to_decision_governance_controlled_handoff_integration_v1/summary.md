# Summary

The integration uses `DecisionGovernanceEngineV1` directly through a small
reference-only handoff adapter. Case A admits after first-cycle Sufficiency
and Stop. Case B rejects cycle 1 and admits only after cycle 2 Sufficiency,
Stop, and Hypothesis Revision. All resulting Decision artifacts remain
candidate-only and downstream Task/Action execution is deferred.

