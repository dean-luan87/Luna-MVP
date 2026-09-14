# Model Provider Isolation Contract v1

## Input isolation

Provider receives only model_reference, capability_request_reference, scoped
input Evidence, resource envelope, deadline, output schema, and provenance
requirements. It does not receive Goal, Brain Intent, full Field, full Self,
Identity, Value, Decision, Authority, Task list, or Action Request.

## Output isolation

Provider returns Raw Evidence Candidate or Model Failure Candidate with source,
confidence, limitation, Unknown, provenance, timestamp, and capability
reference. Evidence Gateway validates it before Reality Update Candidate.

Provider cannot create a Field, Goal, Situation, Decision, Action, or Reality
Write. Provider is not Brain and not Authority. Provider replacement must be
transparent to A Route and Self Identity.

No direct Provider-to-Brain, Provider-to-Decision, Provider-to-Goal,
Provider-to-Reality, or Provider-to-Action path is permitted.

The scoped input Evidence and capability reference are explicit.
