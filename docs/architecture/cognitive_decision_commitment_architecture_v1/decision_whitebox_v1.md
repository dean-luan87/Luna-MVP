# Decision Commitment Whitebox v1

## Authority questions

1. Who creates a Decision Commitment Candidate? Brain output through the
   Decision Candidate Contract.
2. Who validates freshness and constraints? Decision Commitment Governance
   using Reality, Evidence, Constitution, Value, Safety, and Governance.
3. Who owns Capability status? Capability Governance; Commitment only checks
   status and does not invoke a Capability.
4. Who owns Attention? Attention; Commitment emits a Validation Requirement
   and Attention Request only.
5. Who owns Expected Outcome? Expectation; Commitment references its
   condition and consumes Feedback.
6. Who owns Goal and Intent? Existing Goal and Intent contracts; Commitment
   checks alignment and does not mutate them.
7. Who owns Action permission and execution? Action Boundary and Runtime;
   Commitment produces only an Action Request Candidate.
8. Who can override? Human Review is a reserved interface for high-risk or
   uncertain commitments.
9. Who owns revision? Brain and Decision Governance review Revision
   Candidates; no automatic replacement is allowed.

## Allowed flow

```text
Brain Decision Candidate
          ↓
Reality Freshness + Evidence Sufficiency + Constraint Check
          ↓
Intent Alignment + Capability Availability Check
          ↓
Decision Commitment Candidate
          ↓
Expected Outcome / Validation Requirement
          ↓
Action Request Candidate → Action Boundary
```

## Negative paths

- Brain → Action Execution: forbidden.
- Decision Candidate → direct Action Request: forbidden.
- Commitment → Reality mutation: forbidden.
- Commitment → Goal mutation: forbidden.
- Commitment → Value mutation: forbidden.
- Commitment → Capability invocation: forbidden.
- Commitment → Model Runtime or Hardware Control: forbidden.
- Commitment → automatic planning: forbidden.
- Commitment → automatic execution: forbidden.
- Commitment → Prediction Runtime or B Simulation Runtime: forbidden.
- Learning → automatic strategy modification: forbidden.
- Conflict → silent selection: forbidden.

## Preserved fields

Every commitment preserves source Decision Candidate, Field, Task, Intent,
Evidence, Confidence, Risk Level, Constraint Check, Resource Requirement,
Expiration Condition, Expected Outcome, Unknown, Conflict, Review Trace,
Human Override status, and Provenance.

