# Runtime Path

The new Runner composes existing owners in this order:

`Observation Demand → Capability Resolution → ProviderRuntimeRequestV1 →`
`canonical YOLO11n admission → bounded raw frame → existing YOLO provider →`
`ProviderRuntimeResultV1 → RuntimeObservationEnvelopeV1 → Observation Gateway`
` → A-Route → Cognitive State Formation`.

The request carries capability/provider/model, bounded source, execution
identity, and provenance references. Full cognitive state is not passed to the
provider. Recorded fixtures remain in the earlier bridge Runner and are not
used by this real-execution Runner.

The shared `RuntimeObservationEnvelopeV1` may carry an optional
provider-specific candidate payload. The verified YOLO path leaves that field
unset; the OCR extension uses it only to preserve native text candidates and
explicit empty-result status for Gateway evidence admission.

The real-provider adapter preserves the canonical FPO
`CapabilityRequirementCandidateV1.requirement_id` (`capability-requirement:...`)
when constructing the provider request, raw-source mapping, and provider
admission. The normalized provider-runtime resolution object may retain its
separate `provider-requirement:...` identity; that identity is not substituted
for the canonical admission reference.

For the local YOLO path, source-image dimensions are read from the selected
image metadata before the raw frame reference is built. YOLO `xyxy` output is
preserved in original-image pixel coordinates; the raw frame dimensions must
describe that same source coordinate space.
