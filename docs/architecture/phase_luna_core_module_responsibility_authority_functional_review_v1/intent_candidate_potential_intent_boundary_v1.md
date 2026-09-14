# Potential Intent / Intent Candidate Boundary v1

## Definitions

- **Potential Intent**: a source-supported indication that a directed
  orientation may exist. It preserves unknowns and is never an admitted
  commitment.
- **Intent Candidate**: a structured proposal with source/context refs,
  direction/future-state candidates, alternatives, uncertainty, lifecycle
  candidate, provenance and optional interaction/carryover information.
- **Admitted Intent**: a governed identity/version returned by Intent
  Governance after ownership, provenance, conflict, scope and lifecycle checks.

Source modules, Brain, A or Task may produce proposal inputs. The controlled
`IntentGovernanceSkeletonV1` is the canonical candidate assembly seam. Its
outputs explicitly remain `candidate_only` and `reference_only`; ownership
guards reject decision/action/task output and source mutation.

An Intent Candidate cannot directly trigger Concern admission, Task creation,
Capability resolution, Observation, Provider invocation or Loop persistence.
It may carry a candidate handoff; the receiving owner and Brain still govern
the next transition.
