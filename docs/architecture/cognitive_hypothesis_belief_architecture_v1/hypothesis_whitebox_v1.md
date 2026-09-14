# Hypothesis Whitebox v1

## Authority and flow questions

1. Who creates a Hypothesis Candidate? An admitted Evidence, Field Rule,
   validated Experience, or Human Feedback source.
2. Who owns Reality? Reality Workspace and its Reducer; Hypothesis cannot
   write Reality.
3. Who owns the Field binding? The existing Field contract; Hypothesis only
   references an existing Field.
4. Who qualifies confidence? Hypothesis Governance with source, support,
   contradiction, uncertainty, and provenance checks.
5. Who allocates validation resources? Attention; Hypothesis emits a
   validation requirement and Attention Request only.
6. Who executes Observation? Capability Governance and the existing
   Observation/Provider boundary.
7. Who receives Validation Result? Learning and Memory as governed inputs;
   neither may silently solidify a Belief Candidate.
8. Who admits a Belief Candidate? Governance after validated-pattern review.
9. Who resolves material conflicts? Brain Evaluation; multiple candidates
   may remain active.
10. Who owns final judgment? Brain retains final decision authority.

## Allowed flow

```text
Evidence / Field Rule / Experience / Human Feedback
                         ↓
              Hypothesis Candidate
                         ↓
       Field + Situation + Confidence + Unknown
                         ↓
              Validation Requirement
                         ↓
                Attention Request
                         ↓
                  Evidence Update
                         ↓
            Validation Result / Experience
                         ↓
              Belief Candidate (admitted)
                         ↓
                 Brain Context Package
```

## Negative paths

- Hypothesis → Reality write: forbidden.
- Belief → Evidence override: forbidden.
- Hypothesis → Decision: forbidden.
- Belief → automatic Decision: forbidden.
- Attention → Hypothesis selection: forbidden; Attention only allocates
  validation resources.
- Learning → automatic belief solidification: forbidden.
- Provider/Model → Belief: forbidden without Evidence Gateway and Governance.
- Hypothesis → Prediction Runtime: forbidden.
- Hypothesis → B Simulation Runtime: forbidden in this phase.
- Hypothesis → Action Runtime: forbidden.

## Required preserved fields

Every candidate preserves Unknown, Confidence, Uncertainty, Supporting
Evidence, Contradicting Evidence, Validation Status, Lifecycle State,
Field Context, Situation Context, Risk, Constraint, Time Validity, and
Provenance. A conflict remains a Hypothesis Conflict and is never silently
collapsed to one explanation.

Contract keyword: Supporting Evidence.
