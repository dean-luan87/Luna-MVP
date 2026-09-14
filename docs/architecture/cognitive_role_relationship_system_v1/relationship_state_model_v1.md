# Relationship State Model v1

Relationship is a contextual, temporal candidate between Participant A and
Participant B. It is not a static label and is never directly inferred by a
Model. It carries Context, History, Confidence, Evidence, and Boundary.

## Evolution states

```text
Initial → Developing → Stable → Changed → Unknown → Archived
```

States are candidates and may regress or become Unknown when current Evidence
conflicts. A relationship can be Colleague in a Work Field and Friend
Candidate in a Private Field without changing Self Identity.

## Evidence path

```text
Interaction Experience
  ↓
Relationship Memory
  ↓
Relationship Candidate
```

Repeated cooperation may support a Cooperation Candidate. It cannot become a
confirmed friendship, emotional judgment, Goal, Decision, or Social Action
without a later governed phase.

## Boundary

Relationship Conflict Candidate is retained rather than automatically solved.
Current Reality > Memory and Evidence > inference. Unknown remains explicit.
Emotion is a placeholder interface only; Emotion Runtime is out of scope.

Friend Candidate remains contextual and provisional.
