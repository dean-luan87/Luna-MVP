# Evidence → Context / Field / Current World Controlled Integration v1

This phase integrates an already admitted `PerceptionEvidenceV1` into the
existing Field boundary. It does not create a second world owner or a direct
Evidence-to-State write path.

The repository's canonical controlled path is:

```text
PerceptionEvidenceV1
  → FieldEventCandidateV1
  → admit_field_event
  → FieldKernelReducerAdapterV1
  → FieldStateReducerModuleV1
  → FieldStateV1 read representation
  → CurrentWorldCandidateV1
```

The current Field State Reducer module is explicitly a candidate-only
skeleton: it produces a reducer candidate and does not persist a Field State.
`FieldStateV1` and `CurrentWorldCandidateV1` in this evaluation therefore
remain controlled, immutable representations. They are not absolute World
Truth and do not mutate Current World storage.

The phase consumes an existing evidence contract. No Provider, Model, Gateway,
Memory, Experience, Decision, Task, Action, Field, or World runtime is called.
