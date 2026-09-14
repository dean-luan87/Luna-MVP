# Grant contract

`RuntimeExecutionGrantInputV1` accepts immutable preparation candidate
collections and explicit governed refs/statuses. The resolver validates type
shape, complete cross-layer lineage, candidate-only upstream flags, authority
and responsibility refs, permission assessment, safety and constitution
status, resource feasibility, runtime boundary, freshness, and validity.

`RuntimeExecutionGrantDecisionV1` contains:

- stable `grant_ref`, request/owner/authority/responsibility refs;
- the source provider binding, allocation preparation, and execution
  preparation refs;
- permission, safety, protocol, governance, constraint, validity and
  revocation refs;
- observation/cognitive lineage carried forward without reinterpretation;
- `GRANTED`, `DENIED`, `DEFERRED`, or `REVOKED`;
- `authoritative=true`, `candidate_only=false`, `read_only=true`, and false
  runtime/truth side-effect flags.

Grant refs are deterministic hashes of the stable request ref and execution
preparation ref. Multiple independent preparation candidates produce multiple
independent decisions; none is ranked or selected.

Validity is minimal and explicit: `FRESH`, `STALE`, `EXPIRED`, or `REVOKED`.
Stale and expired grants are denied; revoked grants are marked `REVOKED`.
No runtime interrupt or retry scheduler is implemented.
