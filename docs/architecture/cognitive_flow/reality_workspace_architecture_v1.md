# Reality Cognitive Workspace / Fact Layer Architecture v1

## Position

The Reality Cognitive Workspace is the fact layer that provides a stable working
environment for A Route. It is not an extension of A Route and it is not a
decision system.

```text
Evidence
  ↓
Reality Workspace
  ↓
Reality Candidate
  ↓
Reality State Reducer
  ↓
Current World State
  ↓
A Route Understanding
  ↓
Situation Candidate
  ↓
Brain Evaluation
```

Evidence ≠ Fact. Fact ≠ Reality. The workspace maintains the current most
credible reality representation under evidence, time, provenance, confidence,
authority, and conflict constraints; it does not claim absolute truth.
Reality State ≠ Situation: the workspace describes the current world state, while
A Route interprets what that state means for the situated subject.

## Modules

1. **Evidence Intake Layer** receives Vision, Audio, OCR, SLAM, User Input, and
   Capability Output as an Evidence Package. It requires source, timestamp,
   confidence, capability reference, provenance, and uncertainty. Intake cannot
   write World State.
2. **Evidence Assembly Layer** performs Entity Binding, Temporal Alignment, and
   Spatial Association. It combines fragments into a Reality Candidate, never a
   final fact.
3. **Reality State Model** represents Entity, Event, Relation, State, validity,
   provenance, and Unknown.
4. **Reality State Reducer** reconciles updates, conflicts, expiry, evidence
   coverage, and withdrawal. The Reducer remains the sole State mutation
   authority.
5. **Self Reality State** exposes Identity, Capability, Resource, Limitation, and
   Current Condition. Self State ≠ Personality.
6. **Situated Reality Context Interface** supplies Current World State, Self
   State, Goal, and Resource to A Route and returns a Situation Candidate only.

## Fact-layer invariants

The workspace preserves provenance and uncertainty, allows stronger evidence to
supersede weaker evidence, and permits expiry or withdrawal. Latest evidence is
not automatically correct. The workspace cannot produce Action, modify Goal,
change Intent, or bypass Brain.

## Controlled validation boundary

Level 1 validates Evidence Assembly; Level 2 validates Reality State Maintenance;
Level 3 validates Unknown Preservation; Level 4 validates Self–World Coupling;
Level 5 validates Long Running Reality Workspace. All cases are deterministic
fixtures. No real model, OCR Runtime, SLAM Runtime, Hardware, Action, B Route, or
Emotional Engine is used.
