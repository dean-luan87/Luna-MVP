# Sufficiency and Continuation Boundary

This phase defines a reference boundary, not a sufficiency algorithm.

Sufficiency statuses: `SUFFICIENT`, `PARTIAL`, `INSUFFICIENT`, `UNKNOWN`.

Continuation dispositions: `STOP_SUFFICIENT`, `CONTINUE`, `REOBSERVE`,
`REPLAN`, `DEFER`.

`STOP_SUFFICIENT` means the current Goal/Need has reached its minimum
information condition. It is not Capability failure, Requirement failure, Task
failure, cancellation, or abandonment. Remaining candidates are explicitly
non-binding, and unexecuted candidates after sufficiency are not failures.
