# Cognitive Neural Coordination Candidate Model v1

## Definition

A Neural Coordination Candidate states which capability **roles** should cooperate to cover a Cognitive Intent. It is the demand-side organization proposal passed to Middleware; it is not Middleware resolution or Provider selection.

```text
NeuralCoordinationCandidate {
  parent_mission_ref,
  required_capability_roles,
  required_evidence_coverage,
  relation_dependencies,
  priority_candidate,
  depth_candidate,
  resource_constraints,
  fallback_requirements,
  trace
}
```

## Example

```text
Need: understand road-crossing risk

Capability-role candidates:
- Vision Scene / Object Understanding
- Spatial Relationship Understanding
- Text / Traffic Guidance Understanding
- Audio Risk Evidence
```

This means the Brain's intent may need scene, spatial, text, and audio evidence coverage. It does not mean Neural selected OCR, a VLM, a camera, or any other Provider.

## Boundary with Middleware

| Neural Governance | Middleware |
|---|---|
| Proposes capability roles, coverage, dependencies, and fallback requirements. | Resolves available capability/provider candidates under contracts and resource state. |
| Emits coordination candidate. | Creates/maintains future Provider Session boundary. |
| Monitors returned signal completeness. | Reports session/delivery/degradation status. |

## Constraints

- Candidate ≠ capability resolution.
- Capability role ≠ provider/model identifier.
- Fallback requirement ≠ retry command.
- Coordination may be reduced, deferred, or unavailable; that result returns through Feedback Aggregation.
