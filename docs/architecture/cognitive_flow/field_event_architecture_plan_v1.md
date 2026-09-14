# Field Event Architecture Plan v1

## Position

`FieldEventCandidateV1` represents a possible current-world change derived from bounded, traceable references. It is not Fact, State, History, Memory, Decision, or an event accepted by Reducer.

```text
Current Field View / Field Representation / Primitive / Concept references
 -> Field Event Candidate
 -> existing Field Event Admission + Temporal Validity
 -> Admitted Event
 -> existing Reducer (sole State mutation authority)
```

Field Kernel may expose a Current Field View reference but is not Event Authority: it cannot create truth, admit an Event, or write State.

## Candidate event types

- State Transition Candidate
- Entity Appearance Candidate
- Entity Disappearance Candidate
- Relationship Change Candidate
- Environment Change Candidate
- Task Context Change Candidate

Each type is a possible change pattern, not a fact claim or a State transition command. Conflicting, unknown, stale, or incomplete references remain explicit for Admission/Temporal Validity to assess later.
