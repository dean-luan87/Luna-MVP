# Loop Capability Boundary

## Intrinsic mechanical capabilities

Loop has an intrinsic mechanical capability boundary containing:

- PERSIST_STATE;
- RECORD_STATE_VERSION;
- RECORD_REFS;
- PAUSE_MECHANICALLY;
- WAIT_MECHANICALLY;
- RESUME_RECORDED_STATE;
- FREEZE_FINAL_STATE;
- ARCHIVE_HISTORY;
- APPEND_TRACE.

These capabilities are still exercised only under a scoped Runtime Authority
Grant. Intrinsic capability does not mean autonomous authority.

## Immutable forbidden capabilities

Loop can never be granted:

- JUDGE_SUFFICIENCY;
- SELECT_NEED;
- GENERATE_HYPOTHESIS;
- SELECT_CAPABILITY;
- REQUEST_B;
- SPLIT_CONCERN;
- MERGE_CONCERN;
- ADOPT_RESULT;
- DECLARE_TRUTH.

These are Capability Boundary violations, not merely missing runtime
permissions. A grant cannot override them.

## Mechanical command relationship

The existing A-to-Loop mechanical command contract remains the source shape.
The Runtime Authority Grant authorizes the Loop to perform an allowed
mechanical operation for the scoped Work and state version. Loop does not infer
the command or semantic reason.

## Mechanical failure boundary

Loop may report a mechanical failure for persistence, trace or lifecycle
recording. It must not reinterpret that failure as cognitive failure, Task
failure, Goal failure or Capability failure.

## Closure

Loop can execute CLOSE or FREEZE_FINAL_STATE only after a governed semantic
closure decision has been supplied. Loop self-authorized closure remains
forbidden.
