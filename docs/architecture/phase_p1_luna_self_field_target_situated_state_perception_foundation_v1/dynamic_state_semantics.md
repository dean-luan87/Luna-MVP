# Dynamic State Semantics

Each state assessment has its own `state_id` and `temporal_ref`.  The
controlled cases demonstrate input-driven transitions:

- visibility: `UNSATISFIED` at `t0` → `SATISFIED` at `t1`;
- relation stability: `UNSATISFIED` at `t0` → `SATISFIED` at `t1`;
- the reverse transition is represented by the unstable and inadequate-state
  cases.

`cycle_index` and case identifiers are trace/ordering identifiers only.  The
condition engine does not branch on them.  This phase uses controlled
categorical candidates; it does not claim real camera, IMU, tracking, SLAM, or
geometric measurement.
