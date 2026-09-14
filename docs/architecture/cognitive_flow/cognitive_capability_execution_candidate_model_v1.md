# Capability Execution Candidate Model v1

## Definition

A Capability Execution Candidate is a Middleware proposal for how a bounded CWO requirement could be served under current contracts, availability, health, and resource limits. It is not an automatically admitted or executed session.

```text
CapabilityExecutionCandidate {
  work_objective_ref,
  capability,
  provider_candidate,
  required_input,
  expected_evidence,
  relationship_coverage,
  resource_estimate,
  reliability_limit,
  risk,
  fallback,
  constraint,
  trace
}
```

| Field | Meaning |
|---|---|
| `capability` | Capability role proposed to answer part of a CWO. |
| `provider_candidate` | Eligible Provider candidate, never a Brain mandate. |
| `resource_estimate` | Expected compute, memory, latency, energy, or availability bounds. |
| `expected_evidence` | Candidate output form and coverage—not truth. |
| `risk` | Execution/coverage/reliability risk candidate. |
| `fallback` | Alternative candidate or declared partial-coverage path. |

## Lifecycle boundary

`Generated → contract/resource evaluated → available for future admission → future execution boundary → Middleware Report`

This phase defines neither admission Runtime nor execution behavior. Candidate creation does not invoke a model, hardware, service, or Provider Session.

## Forbidden authority

Capability Execution Candidates cannot change a Goal, Attention allocation, CWO purpose, Decision, Action, Reality state, Memory, or Reducer state.
