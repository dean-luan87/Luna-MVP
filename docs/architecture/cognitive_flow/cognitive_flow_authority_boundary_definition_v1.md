# Cognitive Flow Authority Boundary Definition v1

- Candidate is never Fact by itself.
- Field Representation and Current Field View are read-only candidate/query surfaces.
- Field Kernel is not Reducer; it cannot write State, Snapshot, History, or temporal validity.
- Admission owns candidate eligibility; Reducer is the sole State mutation authority.
- Trace/provenance/uncertainty must remain visible across every handoff.
- Confidence, attention, relevance, and model output never grant Fact, Admission, State, Decision, or Action authority.
- L1 Governance owns execution eligibility, permission, protocol/lifecycle integrity, and diagnostics; capabilities cannot self-authorize.
