# Capability Module and Implementation Mapping

## Existing mapping

The canonical Registry `capability_id` is the closest existing Module
identity. It already carries purpose/need semantics and provider/model
references, but it mixes capability definition with implementation options.

The existing Model Manager correctly treats models as resources and keeps
capability identity separate. Provider Governance similarly treats providers
as isolated implementation adapters whose output must enter an evidence
gateway.

## Recommended future mapping

```text
Universal Capability Slot
        ↓ governed binding
Capability Module identity
        ↓ selects compatible implementation
Capability Implementation
        ↓ depends on
Model / Provider / Runtime resources
```

The Module definition should own purpose, problem classes, input/output
contracts, requirement class, safety classification, and capability boundary.
Implementation records should own implementation version, asset integrity,
resource profile, model/provider choices, and runtime compatibility.

## Migration caution

The existing Registry and visual manifest shapes can be adapted, but they must
not be copied into a second registry. A future extension should preserve old
`capability_id` references where they are canonical, add explicit Module and
Slot references only where the current contract cannot represent them, and
keep Model Manager/provider ownership unchanged.

## Identity rule

Implementation/model/provider replacement preserves Module identity only when
the capability contract and authority boundary remain compatible. A change in
purpose, problem class, output authority, requirement class, or semantic
scope requires a new Module identity review.
