# Luna Cognitive Value & Utility Architecture v1

## Position

Value & Utility Evaluation is the common evaluation layer between a Goal
Candidate and later priority or arbitration. It answers two related questions:
what matters in this Field, and what is worth investing under current finite
resources. It is not a Goal Manager, Decision Engine, Action Runtime, Emotion
Engine, or value-editing mechanism.

```text
Understanding
     ↓
Goal Candidate
     ↓
Value Evaluation Candidate
     ↓
Utility Evaluation Candidate
     ↓
Priority Ranking Candidate
     ↓
Brain / future Decision Arbitration
     ↓
Action Candidate Boundary
```

All outputs in this phase are candidates. Constitution and hard safety
constraints are evaluated before a numerical ranking can be considered.
Value never creates a Goal, executes an Action, changes Reality, or rewrites
Value itself.

## Utility model

The architecture reserves the following model without implementing it:

```text
Utility Score =
  (Expected Benefit × Importance × Probability)
  - (Resource Cost × Risk Factor)
```

Expected Benefit describes the possible gain; Importance is contextual value;
Probability is informed by Belief, Capability, and historical Experience;
Resource Cost is supplied by Self; Risk Factor includes safety, system, and
irreversible-impact risk. A hard constraint can reject a candidate regardless
of its score.

## Authority boundary

Self supplies current resource, health, and rhythm context. Field supplies
current reality. Goal supplies direction. Memory and Schema provide context;
they do not force a ranking. Exploration uses the same layer as an investment
question, with `Expected Information Gain - Exploration Cost` as a reserved
candidate model. Brain retains judgment and future Decision Arbitration owns
the eventual arbitration. No automatic score, Goal adjustment, learning,
Emotion integration, model/provider call, or Runtime behavior is implemented.
