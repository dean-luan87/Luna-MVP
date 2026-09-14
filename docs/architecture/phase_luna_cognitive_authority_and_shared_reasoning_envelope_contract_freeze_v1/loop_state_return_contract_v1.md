# Loop to A State Return Contract

## Allowed mechanical return fields

Loop may return only:

- current_loop_state;
- current_state_version_ref;
- pending_refs;
- waiting_reason_ref;
- pause_reason_ref;
- recorded_requirement_refs;
- recorded_b_branch_refs;
- closure_state;
- final_freeze_ref;
- trace_refs;
- provenance_refs;
- history_boundary_refs.

These are mechanical facts about recorded state, not semantic conclusions.

## Prohibited inferred conclusions

Loop must not return:

- SUFFICIENT;
- REPLAN;
- REQUEST_MORE_EVIDENCE;
- SHOULD_CONTINUE;
- BEST_CAPABILITY;
- HYPOTHESIS_INVALID;
- BEST_PROVIDER;
- CONCERN_SPLIT;
- CONCERN_MERGE;
- RESULT_ADOPTED.

If A or B supplied one of these as a candidate, Loop may return only the
recorded reference and source owner, for example:

- supplied_sufficiency_ref;
- supplied_replan_ref;
- supplied_hypothesis_invalidation_ref;
- supplied_result_adoption_ref.

The supplied ref remains owned by A, B, Brain or another canonical owner.

## Version integrity

Every state return carries the current state version ref and the trace/
provenance refs created by the mechanical operation. A stale state return
cannot authorize a new semantic decision or Provider invocation.

## Closure integrity

Loop may report closure_state and final_freeze_ref only after receiving the
corresponding governed command. A recorded closure state is not a global
assimilation decision.
