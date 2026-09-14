# Observation feasibility, window, and capability eligibility

Feasibility compares the current Self and Relative Observation candidates with
the requirement-specific minimum conditions. It records satisfied and
unsatisfied condition references and emits one of the controlled statuses:
`NOT_OBSERVABLE`, `APPROACHING_OBSERVABLE`, `OBSERVABLE_UNSTABLE`,
`OBSERVABLE`, or `LOSING_OBSERVABILITY`.

An Observation Window is `OPEN` only when observation is `REQUIRED`, feasibility
is `OBSERVABLE`, and no requirement condition is unsatisfied. It is `CLOSED`
otherwise, or `UNSTABLE` when the only blocking state is stability.

Capability eligibility is true only when the window is open and the canonical
capability is available. `eligible_now = true` never means provider invocation;
this phase invokes no provider.

Condition gaps and relative adjustment needs are candidate descriptions such
as `TARGET_TOO_SMALL` / `NEED_LARGER_TARGET_SCALE` and `OCCLUDED` /
`NEED_CLEAR_LINE_OF_SIGHT`. They do not contain movement commands.

