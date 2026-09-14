# Verification

The user must execute the runner and verifier from the canonical root. The
verifier checks the required cases, one-to-one projection, multiple-candidate
retention, no dedup/merge, zero-route behavior, invalid-input fail-closed
behavior, Scenario 12 opaque capability behavior, deterministic refs, lineage,
and upstream immutability.

It also checks the cross-layer invariants:

- every route references an active Capability Resolution Candidate;
- every route and source candidate reference the same Observation Demand;
- every route preserves Demand, Requirement, Resolution, Strategy, Branch, Gap,
  Need, and Problem lineage;
- no route implies runtime submission.

No verification result is asserted by this document. Status before user
terminal execution remains `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
