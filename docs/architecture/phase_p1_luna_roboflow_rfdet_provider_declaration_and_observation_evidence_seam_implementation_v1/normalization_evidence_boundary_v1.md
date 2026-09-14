# Normalization and Evidence Boundary v1

## Reused types

The integration reuses:

- `RoboflowProviderRequestV1`
- `RoboflowNativeResultV1` (adapter-private payload)
- `RoboflowNormalizedProviderResultV1`
- `VisualDetectionEvidenceCandidateV1`
- `ObservationGatewayEvidenceHandoffCandidateV1`

No Roboflow-specific canonical Evidence type was added.

## Mapping

```text
native workflow payload
  → governed output path `$[0].model_output_3.predictions`
  → normalized prediction records
  → VisualDetectionEvidenceCandidateV1
```

The observed prediction fields are `class`, `class_id`, `confidence`,
`detection_id`, `height`, `parent_id`, `width`, `x`, and `y`. The adapter maps
the observed `x/y/width/height` geometry to the existing canonical bbox field;
an optional provider `id` or `detection_id` becomes a detection correlation
ref. Unknown extra provider fields are ignored and cannot leak into the
normalized dataclass.

Each normalized candidate preserves:

- Provider ref
- Model asset ref
- frame ref
- ROI ref
- bbox
- confidence candidate
- trace ref
- provenance refs including Provider, workflow, model, and source refs
- candidate-only and no-truth/no-mutation flags

The normalizer now rejects a missing/malformed prediction rather than silently
creating an empty geometry candidate. Empty `predictions` is a valid accepted
empty candidate result.

## Boundary rules

```text
Raw Roboflow result
  ≠ Luna Evidence candidate
  ≠ World Truth
  ≠ Field mutation
  ≠ Decision / Task / Action
```

For non-empty accepted evidence, the adapter now builds the existing
`ObservationGatewayEvidenceHandoffCandidateV1`.  Its `raw_output_refs` carry
the normalized result correlation ref, not the native payload.  Empty accepted
predictions produce no handoff because there are no Evidence refs to hand off.
The handoff remains candidate-only: this phase does not execute Gateway
admission or any source-state mutation.

## Evidence ownership

The adapter owns only provider-result translation correctness. Evidence
admission, Current World candidate lifecycle, Field admission/reduction, and
semantic interpretation remain with their existing owners.
