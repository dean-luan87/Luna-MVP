# Closure reason cutover

The existing lifecycle closure engine still contains the compatibility
`CLOSURE_DISPOSITION_BY_REASON` mapping. New closure inputs carry an explicit
reason reference and supplied lifecycle disposition from A or Brain/Cognitive
Flow Governance.

Accepted supplied closure dispositions are mechanically mapped to
`RECORD_OUTCOME_REF`, `CLOSE`, `FREEZE_FINAL_STATE`, and
`ARCHIVE_HISTORY_BOUNDARY`. The Loop never constructs semantic reasons such as
concern resolved, safety termination, or resource value too low.

