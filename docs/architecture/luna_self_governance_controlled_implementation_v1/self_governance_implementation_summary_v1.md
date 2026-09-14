# Implementation Summary

Self Governance is implemented as a narrow candidate lifecycle owner. A `SelfReferenceCandidateV1` carries source owner, source/evidence/provenance refs, temporal validity, uncertainty, sensitivity, boundary class, and explicit `candidate_only=True`, `fact_admitted=False`, and `persisted=False` flags.

`SelfAttributionCandidateV1` supports identity, role, relationship-position, capability, limitation, preference, habitual tendency, agency, responsibility, resource-condition, interaction-style, autobiographical, intent, memory, learning, regulation, emotional, personality-evidence, action-history, and uncertain-self domains. It preserves contradiction, revision, revocation, supersession, and sensitivity lineage.

Boundary classes are `SELF`, `OTHER`, `SHARED`, `ENVIRONMENT`, `SYSTEM`, `UNKNOWN`, and `CONTESTED`. Stability remains partitioned into `STRUCTURAL_SELF`, `SEMI_STABLE_SELF`, `TRANSIENT_SELF`, and deferred `FUTURE_PERSONALITY_DERIVED_SELF`; it is never flattened.

Continuity is a change-tolerant candidate with stable, changed, unresolved, revision, revocation, temporal, trace, and provenance refs. Revision, revocation, supersession, and expiration preserve prior lineage. Explicit user correction is represented and has precedence without producing a persisted fact.

PCN, Memory, Learning, Intent, Dynamic Regulation, Personality, and Emotion remain read-only or deferred boundaries. Memory semantic compression is not implemented. No prior module is modified.

The 34 frozen planning scenarios are represented exactly in the fixture. The runner emits per-case expected/actual checks and summary flags; the final verifier checks source contracts and the user-generated runner artifacts. This report is not a GO decision.
