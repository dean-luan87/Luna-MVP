# Capability identity, versioning, and binding

## Identity layers

- Slot identity: stable host/binding identity, for example `slot-017`.
- Capability Module identity: the semantic ability identity.
- Capability Implementation identity: the concrete implementation revision.
- Model identity: a model asset/resource identity owned by Model Manager.
- Provider identity: an adapter/provider identity owned by Provider Governance.

## Version decisions

An implementation/model/provider upgrade may preserve Module identity when
the capability contract, evidence boundary, compatibility, and governance
semantics remain compatible. A new Module identity is required when purpose,
problem classes, semantic contract, requirement classification, or authority
boundary changes.

Slot rebinding requires compatibility assessment, admission, provenance,
permission, resource checks, and historical binding recording. No rebinding
is automatic.
