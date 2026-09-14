# Model and Provider Dependency Mapping

The existing separation is conformant with the Universal Slot Standard:

```text
Capability Module
  → Model Manager model options/resources/compatibility
  → Provider Governance adapter qualification
  → Runtime qualification where applicable
  → Evidence Gateway boundary
```

Model Manager owns Model Identity, Version, Resource Requirement, Runtime
Compatibility, and Deployment Status. Provider Governance owns provider
adapter qualification and provider health evidence. Neither owns capability
meaning, Slot identity, Self identity, Decision, or Reality.

## Mapping rule

Slot/Module admission may reference Model Manager and Provider Governance
evidence, but must not duplicate their registries or infer capability identity
from a model/provider name.

## Gap

The future Module Implementation record needs an explicit reference envelope
for model/provider candidates, integrity, compatibility, and provenance. This
is an extension/mapping concern, not a reason to change Model Manager or
Provider Governance ownership.
