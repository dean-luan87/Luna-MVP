# Canonical Change-Control Rules v1

## Architecture change

The following are architecture changes and require explicit architecture review:

- changing a canonical owner or authority domain;
- changing responsibility, mutation authority or admission authority;
- changing a state ownership class;
- adding/removing/changing a canonical flow edge or transition class;
- changing failure responsibility or return target;
- changing constraint precedence or policy/enforcement separation;
- changing version ownership or invalidation propagation;
- weakening the World Truth boundary or candidate/admission/execution separation;
- expanding the Memory/Experience boundary;
- activating Emotion or changing its deferred status;
- removing historical traceability or creating a second mutable source copy.

## Implementation-only change

Adapter implementation, serialization, performance optimization, Provider implementation, runtime wiring, logging, UI and tests may proceed without reopening architecture only when they preserve this ledger and its negative boundaries.

## Required review evidence

An architecture-changing proposal must identify affected owner rows, state rows, edges, version domains, failure rows and invariants; state the new authority/responsibility pair; and record compatibility/migration impact. No module may grant itself authority through implementation.

## Freeze interpretation

This is a repository architecture record, not an L0 Constitution or runtime scheduler. Runtime readiness must be demonstrated separately and cannot be inferred from this freeze.

