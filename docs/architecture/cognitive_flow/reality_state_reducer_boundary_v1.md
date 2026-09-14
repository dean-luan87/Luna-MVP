# Reality State Reducer Boundary v1

## Sole state authority

The Reality State Reducer remains the sole State mutation authority for Current
World State and Self Reality State projections. Intake, Assembly, Capability,
Provider, A Route, and Brain may submit candidates or evaluations, but they cannot
write state directly.

## Reconciliation rules

The Reducer evaluates:

- temporal freshness and validity windows;
- source provenance and authority;
- confidence and uncertainty;
- supporting and conflicting evidence;
- expiry, withdrawal, and explicit invalidation;
- whether a candidate belongs to an existing Entity, Event, Relation, or State.

Latest evidence is not automatically correct. A newer low-quality candidate may
remain conflicted or be rejected in favor of stronger valid evidence. Expired or
withdrawn content is not silently treated as current.

## Authority boundary

The Reducer does not own Goal, Intent, Situation, Decision, Action, or value
judgment. It maintains fact-layer state only. It cannot bypass Evidence
Validation, invent missing evidence, or turn Unknown into a fact.
