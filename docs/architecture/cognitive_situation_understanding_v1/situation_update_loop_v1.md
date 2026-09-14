# Situation Update Loop v1

## Reassessment chain

```text
New Evidence
    ↓
Reality Update Candidate
    ↓
Cognitive Field Update Candidate
    ↓
Situation Reassessment Candidate
    ↓
Situation Confidence / Unknown Update
    ↓
A Route Input
```

An update is candidate-only until the applicable Reducer validates state. A
material change in location, entity, relation, Self State, Capability State,
Goal Context, or Unknown must be able to produce a new Situation Candidate.
stale Situation must not be retained merely because a previous interpretation
was confident.

## Reassessment rules

New Reality Evidence has priority over stale Experience Reference. If evidence
is insufficient, the loop preserves Unknown and may lower Situation
Confidence. If Self Capability or Self State degrades, the Situation may gain
a capability constraint without changing Reality. If the Field changes, the
Situation is re-evaluated against the new Field Context.

Situation Update does not execute Action, make Decision, alter Goal, or mutate
Reality directly. It does not mutate Reality directly. It produces a traceable
Situation Reassessment Candidate.
