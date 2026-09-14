# Controlled dynamic cases

The evaluation contains four cases:

1. `OBSERVATION_NOT_NECESSARY`: an unknown remains, but continuation is
   possible. Necessity is `NOT_REQUIRED`; there is no adjustment and no
   provider invocation.
2. `NECESSARY_BUT_CONDITIONS_NOT_MET`: the transit-sign text is required, but
   the target is `SMALL`. The window is closed and a
   `TARGET_TOO_SMALL` / `NEED_LARGER_TARGET_SCALE` pair is emitted.
3. `DYNAMIC_STATE_REACHES_OBSERVABLE`: the same requirement, target, and field
   move from partial/small at `t0` to visible/complete/adequate at `t1`.
   Window and eligibility change from closed/false to open/true.
4. `OBSERVATION_WINDOW_LOST`: the same open state becomes `OCCLUDED` at `t1`.
   Feasibility becomes `LOSING_OBSERVABILITY`, window closes, and eligibility
   becomes false.

`case_id` and `cycle_index` are identity/order fields only. They are not read
by the semantic predicates.

