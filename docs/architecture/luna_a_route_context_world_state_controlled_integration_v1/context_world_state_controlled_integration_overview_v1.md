# A Route Context / World State Controlled Integration v1

This phase closes the controlled handoff chain:

```text
Observation Gateway
 -> Observation Context Handoff Candidate
 -> Context Foundation Candidate
 -> Field Event Candidate
 -> Field Event Admission
 -> Field State Reducer eligibility
 -> Current World Candidate
 -> A Route next cognitive stage candidate
```

The integration reuses existing owners. It does not create a World, Context, or Field super-owner. Context Foundation assembles reference-only context, Field Event Admission remains the admission boundary, Field State Reducer remains the sole Field mutation authority, and Cognitive State Formation owns Current World candidate semantics.

Frozen distinctions include Observation != Context, Observation != Field State, Observation != Current World Truth, Admitted Observation != Fact, Context Candidate != World Truth, Current World != Field State, Field Event != Field State, and Trace / Provenance != semantic authority.

All outputs are synthetic, candidate-only, deterministic, non-persistent, and non-runtime. Contradiction, correction, temporal validity, revocation, expiration, and supersession lineage remain visible. The A Route handoff is candidate-only with `runtime_handoff_ready=false` and `mutation_authority=false`.

Current status: `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
