# Luna Protocol Lifecycle Governance v1

## Scope

This model governs Protocol lifecycle, version, change, admission, and deprecation planning. A Protocol is a governed Contract/compatibility boundary. `Active` means eligible for governed reference only; it never activates a Capability, grants Permission, authorizes Runtime, or writes a Registry.

## Lifecycle States

```text
Draft → Review → Approved → Active → Frozen → Deprecated → Retired
```

| state | owns | allows | denies | transition authority |
| --- | --- | --- | --- | --- |
| Draft | proposal intent and non-binding design | authoring and impact preparation | production reference, activation, capability dependency | protocol owner submits to L1 Protocol Governance |
| Review | review evidence, unresolved issues, impact record | compatibility/authority review | activation, self-approval, silent scope expansion | L1 Protocol Governance with L0 compatibility check |
| Approved | accepted immutable proposal revision | scheduled activation planning and migration preparation | automatic Runtime/Capability/permission activation | designated L1 Protocol Governance authority |
| Active | governed reference version and declared compatibility | compatible Capability use through admission checks | version bypass, self-upgrade, incompatible dependency | L1 Protocol Governance; Permission/Admission remains separate |
| Frozen | immutable baseline/version evidence | read/reference and regression comparison | unreviewed modification or automatic upgrade | L1 Protocol Governance after validation evidence |
| Deprecated | legacy version with sunset/migration record | existing approved dependencies only, under compatibility policy | new Capability dependency and feature expansion | L1 Protocol Governance with Registry/lifecycle evidence |
| Retired | closed Protocol record and migration outcome | audit/history reference only | new use, activation, or dependency | L1 Protocol Governance after migration completion |

## Lifecycle Rules

- All transitions require Protocol Governance evidence; no Capability can alter Protocol state.
- Constitution incompatibility blocks Review, Approval, Activation, and migration.
- Permission/Admission determines a request's eligibility under an Active Protocol; lifecycle state alone is not Permission.
- Diagnostics may report drift and risk but cannot transition state automatically.
- Frozen and Deprecated versions retain traceable version identity and migration history.

## Capability Relationship

Capabilities use only compatible, governed Protocol versions. They cannot modify a Protocol, self-upgrade a version, bypass version checks, redefine input/output semantics, or treat Deprecated as Active without explicit compatibility handling. Every future Capability Execution Context references its selected Protocol version and denied operations.

