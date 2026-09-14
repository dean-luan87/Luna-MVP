# Closure reason mapping

| Closure reason | Candidate lifecycle disposition | Meaning |
|---|---|---|
| `STOP_SUFFICIENT` | `COMPLETED` | Goal sufficiency terminates this Loop only |
| `COGNITIVE_CONCERN_RESOLVED` | `COMPLETED` | Local concern resolved |
| `INTENT_SUPERSEDED` | `SUPERSEDED` | Intent owner superseded the concern |
| `TASK_OR_BEHAVIOR_COMPLETED` | `COMPLETED` | Task/Behavior owner no longer needs this concern |
| `CONTEXT_INVALIDATED_CONCERN` | `STOPPED` | Current context invalidates continued pursuit |
| `BRAIN_GOVERNED_STOP` | `STOPPED` | Brain governance stops the local process |
| `RESOURCE_VALUE_TOO_LOW` | `ABANDONED_BY_VALUE` | Expected value no longer justifies growth |
| `CONTINUITY_STALE` | `SUPERSEDED` | Continuity no longer supports the old concern path |
| `UNRECOVERABLE_CAPABILITY_GAP` | `FAILED` | The concern cannot proceed through available capability paths |
| `SAFETY_GOVERNED_TERMINATION` | `STOPPED` | Safety governance terminates the local process |
| `PARENT_SUPERSEDED_BY_BRANCH_OR_MERGE` | `SUPERSEDED` | Brain accepts a parent/branch/merge supersession |

The table is a candidate mapping, not a new global enum. A closure reason is
not a universal failure signal. In particular, `STOPPED`, `SUPERSEDED`, and
`ABANDONED_BY_VALUE` remain distinct from `FAILED`, and none implies Task
failure.

Branch reservation alone has no closure effect. Parent supersession requires a
separate Brain-governed closure decision.
