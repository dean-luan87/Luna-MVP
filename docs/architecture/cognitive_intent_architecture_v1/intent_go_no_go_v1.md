# Intent Go / No-Go v1

## Readiness checks

- Intent Layer is documented between Drive/Value and Goal/Task.
- User Intent, Self Intent, Survival Intent, Task Intent, and Field
  Requirement are represented as governed sources.
- Every Intent is an Intent Candidate with Context, Confidence, Unknown, and
  Provenance.
- Field, Role, Relationship, Self, Situation, Goal, and Task bindings are
  reference-only and do not mutate their owners.
- Intent influences Attention, Option, and Decision Candidate context but does
  not allocate resources or decide.
- Intent Conflict Candidate is preserved and escalated to Brain review.
- Existing Goal/Task contracts remain authoritative for continuity.
- Intent lifecycle and governance preserve provenance and expiry.
- B Route is a placeholder only and has no Simulation Runtime.

## Required negative guards

No automatic goal generation; no autonomous will; no personality-driven
intent; no Emotion Decision; no Action; no Action Runtime; no model or
hardware invocation; no Reality mutation; no Provider-created Intent; no
silent Unknown completion; no automatic conflict resolution.

Guard keywords: Field Requirement; no personality-driven intent; no model or
hardware invocation; no silent Unknown completion.
Guard keyword: no model or hardware invocation.

## Decision authority

V0 static checks are Agent-only readiness checks. V1 is not authorized in
Planning Only mode. V2 Final Phase Verification is User Terminal Only. V3
Final Audit and Decision is ChatGPT Only. V0 does not grant GO, and this
phase stops at WAITING_FOR_USER_TERMINAL_VERIFICATION.

## No-go conditions

The phase is blocked if a required artifact is missing, a JSON contract does
not parse, a required boundary term is absent, an Intent source bypasses
governance, a Provider or Model gains Intent/Goal/Decision authority, a
Workspace/Field/Goal/Task owner is mutated, or the verifier output contract
is incomplete.
