# Registry Plane Architecture v1

## Registry family

Registry Plane answers “what exists” and “what state is declared”. It does not
answer “what should Luna do”.

- **Capability Registry**: capability identity, evidence contract, limitations.
- **Model Registry**: model asset, version, provider mapping, resource profile.
- **Hardware Registry**: sensor/actuator identity, health, capability mapping.
- **Field Registry**: Field identity, lifecycle, owner reference, boundaries.
- **Authority Registry**: subject, permission, scope, expiration, revocation.

## Registry entry lifecycle

Every entry follows Draft, Review, Admission, Active, Deprecated, Archived.
Registry registration does not grant permission, execute a Provider, mutate
Reality, or create a Goal.

## Invariants

Registry entries preserve provenance, version, owner, limitations, validity,
health, and unknowns. Model Registry cannot define cognition. Hardware Registry
cannot control hardware. Capability Registry cannot become A Route. Field
Registry cannot decide a Goal. Authority Registry records permissions but does
not perform Actions.

The Evidence contract is registered, not interpreted. A Model asset is
registered, not used to decide. Registry does not decide, does not execute,
and does not create a Goal.
