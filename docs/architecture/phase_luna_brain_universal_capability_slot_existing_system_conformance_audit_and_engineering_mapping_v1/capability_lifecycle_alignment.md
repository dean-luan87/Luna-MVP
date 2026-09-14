# Capability Lifecycle Alignment

## Existing lifecycle

Canonical Capability Governance defines:

`Candidate → Registered → Testing → Active → Degraded/Suspended → Retired`

with admission required before Active and no automatic transition.

## Alignment finding

The existing lifecycle is reusable for Module/capability state but is not a
complete Slot lifecycle. Future mapping should keep three concerns distinct:

1. Module definition/admission lifecycle.
2. Implementation/model/provider qualification lifecycle.
3. Slot binding/availability lifecycle.

The visual lifecycle values `NOT_INSTALLED`, `INSTALLING`, `INSTALLED`,
`INCOMPATIBLE`, and `RETIRED` are useful reference vocabulary but are not yet
canonical Universal Slot states.

## Required future extension

Add a narrow mapping/reference layer rather than changing existing lifecycle
meaning. It must prevent `AVAILABLE` from implying `INSTALLED`, `BOUND`, or
`ACTIVE`, and must preserve candidate-only transitions and admission gates.
