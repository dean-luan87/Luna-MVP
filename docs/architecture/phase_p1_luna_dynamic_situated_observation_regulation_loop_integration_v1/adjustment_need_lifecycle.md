# Adjustment Need Lifecycle

Adjustment Needs are derived from the current Capability Condition Gaps using
the existing Situated Capability Preconditions evaluator.

When a gap disappears at a later Situated State, its corresponding adjustment
is no longer active. Historical references remain in the prior state's trace,
but the current state exposes only adjustments for current unsatisfied or
unknown conditions.

The output remains abstract, such as `NEED_TARGET_SCALE`,
`NEED_BETTER_VISIBILITY`, or `NEED_STABLE_RELATION`. It never becomes a move,
turn, zoom, camera-control, navigation, Decision, Task, or Action command.
