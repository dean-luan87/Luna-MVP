# Working Envelope Concern Isolation v1

Each bounded cognitive work context has its own Envelope identity and version.
The binding must prevent cross-Concern source leakage, wrong Grant binding,
wrong Intent/Task refs, shared mutable envelope state, and cross-Loop
contamination.

Shared read-only source refs are permitted only when their scope and
applicability are explicit. A mismatch is an invalidation or admission issue;
the Envelope does not repair or reinterpret the source.
