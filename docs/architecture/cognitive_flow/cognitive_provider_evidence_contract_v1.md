# Provider Evidence Contract v1

## Purpose

Provider output must be converted into a provenance-rich Evidence Candidate before it can cross the Cognitive Middleware boundary. The contract prevents local model conclusions from becoming direct cognitive facts.

```text
ProviderEvidenceCandidate {
  source,
  provider,
  capability,
  cwo_ref,
  session_ref,
  observation,
  confidence,
  uncertainty,
  scope,
  timestamp,
  reliability_state,
  status,
  conflict_hint,
  trace
}
```

| Field | Meaning |
|---|---|
| `source` | Input/source provenance, not a truth source. |
| `provider` | Specific Provider identity/version candidate. |
| `capability` | Capability role that produced the output. |
| `observation` | Bounded observation payload/representation. |
| `confidence` | Provider-reported support metadata, not correctness. |
| `uncertainty` | Declared ambiguity, coverage limit, or failure scope. |
| `scope` | Time, spatial, contextual, privacy, and task scope. |
| `trace` | CWO/session/provider/evidence provenance lineage. |

## Gateway processing

`Provider output → Evidence Adapter → Provider Evidence Candidate → Evidence Gateway → Middleware Report → Neural Feedback Package`

## Prohibitions

- The contract cannot contain a Truth claim.
- Observation cannot contain a Decision or Action command.
- Confidence cannot be treated as cognitive sufficiency.
- Gateway cannot erase conflict, uncertainty, provider identity, or scope.
- Evidence does not mutate Reality, Brain state, Memory, or Reducer state.
