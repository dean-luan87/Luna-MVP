# Recommended Minimal Future Change

## Recommendation

Adopt **Option B: Semantic Cognitive Requirement + Alternative Satisfaction
Basis**.

This is a recommendation only. No implementation is included in this review.

## Minimal boundary

### Input

- governed objective / intent / concern semantics;
- one semantic cognitive requirement candidate;
- explicit alternative satisfaction-basis references;
- current selected cognitive coverage;
- current validity/provenance of the basis references.

### Formation responsibility

The existing A-Route Required Cognitive Condition / Cognitive Coverage boundary
should determine whether at least one governed alternative basis satisfies the
same requirement. It should not infer a basis from strings, scenario IDs,
question text, or acquisition strategy names.

### Output

Preserve the existing conceptual outputs:

- active required condition refs;
- satisfied requirement refs;
- necessary unknown refs for Need Formation;
- provenance showing which basis satisfied a requirement.

The smallest schema adjustment is an explicit requirement-to-alternative-basis
relation or equivalent governed field. Keep existing `minimum_set_ref` semantics
for requirement selection; do not overload it to mean alternative evidence
satisfaction.

### Non-goals

- no new Meaning Framework;
- no Boolean DSL or confidence algebra;
- no evidence fusion;
- no acquisition strategy ranking;
- no Strategy Coordination;
- no Attention or Observation Demand;
- no resource scheduling or merge;
- no Branch lifecycle changes;
- no Truth, Field, World, Memory, Identity, Decision, Task, or Action change.

## Stop condition

Stop after a controlled semantic proof shows:

```text
same requirement
+ basis A covered
→ requirement satisfied, no Need for basis B

same requirement
+ no valid basis covered
→ Need remains

same requirement
+ accepted basis invalidated
→ Need can be formed/reopened again
```

The proof must preserve multiple acquisition strategy candidates as downstream
options without making them Required Cognitive Conditions.

## Required future review order

1. Correct the affected fixture semantics.
2. Specify the smallest governed alternative-basis contract.
3. Update Required Condition / Coverage satisfaction evaluation.
4. Re-check Information Need subtraction without changing its owner.
5. Only then reassess readiness for Strategy Coordination.
