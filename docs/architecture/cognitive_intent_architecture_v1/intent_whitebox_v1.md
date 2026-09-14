# Intent Whitebox v1

## Authority questions

1. Who creates an Intent Candidate? A permitted Intent source through the
   Intent Source Contract; no Provider or Model creates one.
2. Who qualifies it? Intent Governance checks source, context, provenance,
   risk, unknowns, and compatibility.
3. Who binds it to a Field? The Field Binding Contract projects an existing
   Field; it does not create or mutate a Field.
4. Who owns Goal and Task continuity? Existing Goal/Task owners retain that
   authority; Intent supplies references and alignment candidates.
5. Who allocates Attention? Attention Governance; Intent only supplies an
   attention influence candidate.
6. Who evaluates options? A Route/Option Governance; Intent only supplies
   relevance and purpose context.
7. Who owns final Decision? Brain retains final Decision authority.
8. Who can request clarification? Brain or an authorized user-facing
   interface; the request remains a candidate until reviewed.
9. Who can revoke an Intent? Governance or the owning source, subject to
   provenance and lifecycle rules.

## Allowed information flow

```text
Drive / Value + Source Evidence
        ↓
Intent Candidate
        ↓
Field / Role / Relationship / Self / Situation Binding
        ↓
Attention Influence + Option Relevance + Goal Alignment Candidate
        ↓
Brain Intent Review
        ↓
Existing Goal / Task Interface
```

The Intent Layer references Reality and Field state but never writes Reality.
It references Goal and Task but does not create or mutate them. It may expose
Unknown, Risk, Constraint, Confidence, and Provenance to Brain.

## Negative paths

- Provider → Intent: forbidden.
- Model → Intent: forbidden.
- Capability → Goal: forbidden.
- Intent → Goal mutation: forbidden without Goal authority and review.
- Intent → Decision: forbidden; Brain review is required.
- Intent → Action: forbidden; Action Boundary remains separate.
- Intent → Reality write: forbidden.
- Personality → automatic intent: forbidden.
- Emotion → Decision: forbidden in this phase.
- B Route Snapshot → live Intent mutation: forbidden.

## Boundary inventory

The whitebox must preserve Intent Candidate status, Field binding,
source identity, lifecycle state, time validity, Unknown, Risk, Constraint,
Confidence, and Provenance. Absence of an interpretation is represented as
Unknown, not silently completed. A conflict remains an Intent Conflict
Candidate until Brain review or an explicit governance outcome.

The unresolved record is an Intent Conflict Candidate and remains a governed
candidate.
