# Loop Mechanical Capability Boundary

## Core

- materialization/identity
- `PERSIST_STATE`
- `RECORD_STATE_VERSION`
- `RECORD_REFS`
- pending refs
- `PAUSE_MECHANICALLY`
- `WAIT_MECHANICALLY`
- `RESUME_RECORDED_STATE`
- `FREEZE_FINAL_STATE`
- `ARCHIVE_HISTORY`
- `APPEND_TRACE`

## Supporting

- `RECORD_NEED_REF`
- `RECORD_REQUIREMENT_REF`
- `RECORD_B_BRANCH_REF`
- `RECORD_OUTCOME_REF`
- closure record persistence
- history/package boundary persistence

## Legacy/compatibility

`RESUME_REPLAN`, `SUPERSEDE_REQUIREMENT`, local disposition and closure-reason helpers may remain for old callers, but their semantic meaning must be supplied by A/Brain and treated as compatibility-only.

## Out of scope

Need selection, hypothesis, sufficiency, reconsideration, continuation, capability/provider selection, B adoption, Concern governance, Truth and final adjudication.
