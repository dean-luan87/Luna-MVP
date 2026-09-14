# Role and Relationship Whitebox v1

```text
Social Field
  ↓
Role Assignment Candidate
  ↓
Relationship Context
  ↓
Social Position
  ↓
Behavior Candidate
  ↓
Emotion Interface Placeholder
```

## Control questions

- Who activates Role? Field Context and governed Role Assignment Candidate.
- Who owns Identity? Self Identity; Role cannot mutate it.
- Who evolves Relationship? Interaction Experience, Relationship Memory, and
  Evidence produce Relationship Candidate.
- Who resolves Role Conflict? This phase records Role Conflict Candidate only;
  it does not auto-resolve.
- Who owns Goal and final Decision? Brain.
- Who can execute Social Action? No component in this phase; Action Runtime is
  out of scope.
- Who validates relationship confidence? Evidence, History, Context, Unknown,
  and governance; not a Model judgment.

## Isolation invariants

Role Context → Attention Candidate, Role Context → Behavior Candidate,
Relationship → Relationship Candidate, and Role/Relationship → Emotion State
Candidate placeholder are allowed. Role → Identity Mutation, Relationship →
Emotion Judgment, Role → Decision, Relationship → Social Action, and Model →
Relationship Judgment are forbidden.

This is a Planning Only artifact. No Personality Switching, Face Recognition,
Multi-Agent, Hive, B Route, Prediction, Emotion Runtime, or Action Runtime is
included.

Role/Relationship → Emotion State Candidate is placeholder-only. Relationship →
Emotion Judgment and Model → Relationship Judgment are forbidden. No Face
Recognition. No Multi-Agent. No Hive. No B Route. No Prediction. No Emotion
Runtime. No Action Runtime.

Relationship → Emotion Judgment. No Face Recognition. No Emotion Runtime.
