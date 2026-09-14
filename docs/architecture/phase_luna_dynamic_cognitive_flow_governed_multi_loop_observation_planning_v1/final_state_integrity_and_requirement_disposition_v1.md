# Final-state integrity and outstanding disposition

When closure is accepted, `FinalStateFreezeCandidateV1` freezes the existing
state-version reference; it does not copy or mutate authoritative state.
The freeze preserves references to:

- current Need and Need lineage;
- hypothesis lineage and evidence;
- Context, Field, Current World;
- Intent, Task/Behavior, Role, and Perspective;
- capability path, trace, and provenance.

Outstanding Requirements receive explicit candidate dispositions such as
`NOT_REQUIRED_AFTER_SUFFICIENCY`, `CLOSED_STALE`, `CLOSED`, or `DEFERRED`.
Outstanding Observation Candidates receive `NOT_REQUIRED_AFTER_SUFFICIENCY`,
`SUPERSEDED`, `CLOSED`, or `DEFERRED`. A stale Requirement is never
invocation-eligible after closure.

Remaining provisional plan candidates after `STOP_SUFFICIENT` are
non-materialized or marked not required, not failed. Closure freezes the final
state version and does not imply that the full provisional plan was executed.

For a rejected closure assessment, the local closure state remains `OPEN`, no
final-state freeze is created, and the candidate does not authorize an
invocation or assimilation.
