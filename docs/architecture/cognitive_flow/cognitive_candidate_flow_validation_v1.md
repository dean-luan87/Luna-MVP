# Cognitive Candidate Flow Validation v1

## Candidate-first path

```text
Observation -> Candidate -> Evaluation -> Validation -> Adoption Candidate
```

The complete integration trace may add intermediate candidate types, but may not bypass this path.

## Static validation requirements

For every candidate handoff, confirm:

1. source and provenance are available;
2. contextual boundaries are present;
3. evidence references and unknowns are retained;
4. confidence is represented as a candidate rather than truth;
5. receiving modules do not turn the candidate into a fact, rule, permission, Decision, Action, or State mutation; and
6. any adoption remains a separately validated adoption candidate.

## Prohibited shortcuts

- Observation -> Belief -> Action;
- Schema -> Truth;
- Experience -> Rule;
- Evaluation -> Decision authority;
- Feedback -> automatic system change.

Candidate flow validates cognition support, not reality confirmation.
