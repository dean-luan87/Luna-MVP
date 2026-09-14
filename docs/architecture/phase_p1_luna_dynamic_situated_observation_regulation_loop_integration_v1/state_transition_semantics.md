# State Transition Semantics

The regulation status vocabulary is intentionally small:

- `WAITING_FOR_CONDITION_CHANGE`: Need remains active but current minimum
  conditions are not feasible;
- `OPPORTUNITY_OPEN`: conditions are currently eligible, but this controlled
  step defers execution so a later state can invalidate the opportunity;
- `OBSERVATION_EXECUTED`: the current eligible state entered the existing
  Provider Runtime;
- `INFORMATION_SUFFICIENT`: post-observation cognition reports sufficient
  information;
- `INFORMATION_STILL_MISSING`: post-observation cognition reports an active
  information gap;
- `OBSERVATION_NOT_REQUIRED`: current continuation makes the capability
  unnecessary.

Every state has its own temporal, Situated State, Feasibility, Opportunity,
Eligibility, and admission references. A prior regulation reference provides
lineage only; it does not authorize the next state.

`cycle_index` and `case_id` identify ordering and trace context. They are not
semantic drivers.
