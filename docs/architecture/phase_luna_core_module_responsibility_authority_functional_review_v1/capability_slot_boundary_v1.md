# Capability Slot Boundary v1

Capability Slot is the stable abstraction between a functional capability and
one or more compatible implementations. Examples include object detection,
segmentation, text recognition, speaker recognition, depth estimation,
localization and scene understanding.

Capability Governance owns slot identity, taxonomy, slot version, lifecycle
metadata, input/output contract references and binding candidates. A slot may
reference multiple module/model/provider candidates; a binding is not an
invocation.

The existing `UniversalCapabilitySlotV1` carries lifecycle, compatibility,
resource, permission, health, provenance and history refs while remaining
candidate-only and explicitly having no semantic or World Truth authority.

Slot compatibility does not prove model availability, dependency health,
checksum integrity, device readiness or Provider admission. Those are later
Runtime Admission/Provider boundaries.
