# Universal Capability Slot design standard

## Purpose

A Slot is a persistent, capability-neutral binding surface through which a
Capability Module may be admitted, bound, recognized, activated, suspended,
released, restored, replaced, governed, and traced.

## Required semantic groups

- stable `slot_id` and `slot_version`
- slot lifecycle state and binding state
- current bound Capability Module reference, if any
- compatibility boundary
- resource allocation boundary
- permission/admission boundary
- health/degradation state
- provenance and trace references
- usage/history reference
- recovery reference
- current availability
- last-known capability reference
- Brain Self visibility
- governance status

## Authority

Capability Registry owns Slot identity and registry metadata. Capability
Governance/Admission owns binding eligibility. Model Manager owns model
resource admission. Provider Governance owns provider qualification. Runtime
owns execution only after admission. Brain and user produce governed
requests/candidates; neither directly mutates a Slot.

## Persistence

Slot identity and binding history may persist across unbinding or implementation
removal. A Slot does not become a Capability Module merely because it has a
history entry.
