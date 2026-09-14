# Provider Isolation Contract v1

## Least-privilege input

Provider receives only:

- request_reference and capability_id;
- scoped input Evidence references;
- capability parameters;
- resource envelope and deadline;
- expected output Evidence schema.

Provider does not receive Goal, Brain Intent, full Cognitive Field, Identity,
Value, Decision Candidate, Action Request, or complete Self Model. Provider
does not know the whole cognitive state.

## Least-privilege output

Provider returns a Raw Evidence Candidate or an explicit Failure Candidate.
Output must carry provenance, confidence, uncertainty, timestamp, capability
reference, and schema status. Provider output is not Fact, Reality, Situation,
Decision, Goal, or Action.

The Evidence Gateway validates and normalizes output. The Reducer remains the
sole State mutation authority. Provider replacement is allowed at the
Capability boundary; it cannot change A Route logic, Self Identity, Goal, or
Brain authority.

## Prohibitions

No Provider-to-Brain, Provider-to-Decision, Provider-to-Goal, Provider-to-Field,
Provider-to-Reality, Provider-to-Action, direct model call from cognition, or
automatic external operation is permitted.

The capability reference is explicit. Reducer remains the sole State mutation
authority.

Reducer remains the sole State mutation authority.
