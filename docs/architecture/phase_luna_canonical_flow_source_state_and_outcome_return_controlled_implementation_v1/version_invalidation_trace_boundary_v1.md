# Version, Invalidation and Trace Boundary v1

Every candidate retains source-version refs and reverse-linkable trace/provenance refs. No global version is introduced.

When validation rejects an input because source provenance is missing, the
adapter still emits an edge record with adapter-owned record provenance. The
source omission remains explicit in the failure classification/reason; the
adapter provenance does not promote the rejected source to valid evidence.

The adapter blocks stale Evidence, stale Action Result, source-version mismatch, invalidated Outcome, and stale/revoked Grant candidates. Invalidation is preserved as a ref and does not trigger A Reconsideration or Brain action.

Each output includes an edge observability record with transition identity, producer/consumer, authority/responsibility owners, transition class, input/output refs, versions, status, evidence, invalidation, provenance, failure, next target, mutation flags, runtime flags, and candidate-only status.
