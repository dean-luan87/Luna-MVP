# Local disposition cutover

The legacy `_local_disposition()` helper remains unchanged for old fixtures.
At the new boundary, `SUFFICIENT`, `INSUFFICIENT`, `RECONSIDER`, or `DEFER`
must be supplied by A and are recorded as a pending semantic reference through
the existing mechanical `RECORD_REFS` representation
(`RECORD_PENDING_CANDIDATE`).

The Loop does not calculate local disposition from lifecycle, sufficiency, or
resume fields.

