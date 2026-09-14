# Attention Drift Detection Model v1

## Drift purpose

Attention Drift Candidate identifies a mismatch between current cognitive
purpose and long-term attention allocation. It does not directly correct the
allocation.

## Drift classes

- Attraction Drift: irrelevant stimuli repeatedly capture attention;
- Persistence Drift: attention remains after the requirement is complete;
- Narrowing Drift: attention repeatedly covers too little of the relevant Field;
- Omission Drift: important sources are consistently missed;
- Overgeneralization Drift: a local pattern is applied outside its scope;
- Resource Drift: attention cost grows without Information Value.

## Detection chain

```text
Attention Pattern Candidate
      ↓
Current Field / Reality / Goal comparison
      ↓
Attention Drift Candidate
      ↓
Validation
      ↓
Future Allocation Candidate
```

Drift detection preserves Unknown and provenance. It cannot modify Brain, Goal,
Decision, Reality, or Attention Policy directly. A single event is not enough
to adopt a drift correction.

Drift detection cannot modify Goal and cannot modify Reality.
