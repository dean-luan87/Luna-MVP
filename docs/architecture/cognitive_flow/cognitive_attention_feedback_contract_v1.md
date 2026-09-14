# Attention Execution Feedback Contract v1

## Purpose

Attention Feedback reports whether an admitted observation requirement received
sufficient governed evidence. It is a feedback candidate for Reality Cognition
and Brain Evaluation, not a Reality judgment or completion decision.

```text
Attention Feedback Candidate
├── Coverage Candidate
├── Evidence Obtained Reference
├── Missing Information Candidate
├── Confidence Candidate
├── Resource Cost Candidate
├── Failure Reason Candidate
└── trace_ref
```

## Failure classification

- Attention Direction Candidate insufficient;
- Requirement Candidate incomplete;
- Capability limitation candidate;
- Resource limitation candidate;
- Environment limitation candidate;
- Unknown.

## Boundary

Attention Feedback Candidate does not correct evidence, create Reality, decide
sufficiency, create an Action, retry a Provider, change Attention strategy, or
mutate State. It preserves missing information and uncertainty for downstream
candidate evaluation.

