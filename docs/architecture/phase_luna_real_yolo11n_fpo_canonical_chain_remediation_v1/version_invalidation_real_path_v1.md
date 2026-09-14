# Version / Invalidation Real Path v1

The seam preserves separate domains for:

- Capability↔Model binding;
- Model and weights;
- Runtime Admission;
- Model↔Provider binding;
- executable source state;
- trace/provenance.

Any binding invalidation, executable staleness, or source-version mismatch
blocks the adapted Provider admission input. No automatic refresh is added.

The remaining limitation is that upstream production construction of these
canonical records is not implemented by this phase; callers must supply the
context explicitly.

