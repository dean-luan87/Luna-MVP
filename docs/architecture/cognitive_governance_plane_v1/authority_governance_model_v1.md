# Authority Governance Model v1

## Authority questions

For every governed object, the whitebox must answer:

1. Who creates?
2. Who approves?
3. Who modifies?
4. Who runs?
5. Who observes?
6. Who can revoke?

## Frozen authority examples

- Brain creates/approves Goal and final Decision; it does not directly call
  Capability or hardware.
- Constitution approves invariants; it does not run.
- Registry records identity; it does not decide.
- Admission reviews entry; it does not execute.
- Provider supplies Evidence; it has no Goal, Decision, Reality Write, or Brain
  authority.
- Diagnostics observes and classifies; it emits Diagnostic Candidate, not
  Action.
- Reducer remains the sole State mutation authority.

Authority changes require an Authority Proposal, Constitution Check, Risk
Review, Compatibility Review, Approval Candidate, and revocation path. No
authority change is implied by registration or model replacement.

Risk Review is mandatory for an Authority Proposal.
