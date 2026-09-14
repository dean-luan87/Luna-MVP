# Cognitive Field Representation DryRun Validation Matrix v1

| Area | Required evidence | Failure |
| --- | --- | --- |
| Case coverage | Six fixed Field fixture mappings | Missing/mismatched case |
| Schema/references | Required candidate fields and valid references | Empty or malformed field |
| Concept/Primitive binding | Candidate retains both reference families | Detached cognitive lineage |
| Temporal/spatial | Reference scopes remain explicit | State/time/location assertion |
| Attention | `selection_only` priority status | Attention becomes action authority |
| Traceability | Evidence, binding, capability, matching trace | Broken provenance closure |
| Negative guards | All forbidden-operation flags false | Any boundary violation |
| Determinism | Canonical run1/run2 JSON equality | Comparison differs |

The verifier reads serialized output only and imports neither Runner nor Skeleton.
