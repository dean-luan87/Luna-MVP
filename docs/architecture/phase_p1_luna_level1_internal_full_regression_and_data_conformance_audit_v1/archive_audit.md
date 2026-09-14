# Archive Audit

All JSON under `evaluation_archive/level1_cognitive_runs/` is read without
deletion or repair. Records are classified as `VALID_CURRENT_RUN`,
`VALID_HISTORICAL_RUN`, `VALID_PARTIAL_HISTORY`, `CONFLICTED`,
`INVALID_RECORD`, `ORPHANED_REFERENCE`, or `UNKNOWN`.

A historical partial Case A record remains historical evidence unless its own
contract is malformed. A divergent record under the same immutable identity is
a conflict, not an overwrite candidate. `_eval_out` is never accepted as the
canonical archive.
