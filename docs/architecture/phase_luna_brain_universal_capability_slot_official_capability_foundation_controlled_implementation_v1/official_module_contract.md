# Official Capability Module Contract

`CapabilityModuleV1` represents capability semantics and dependencies.
`OfficialCapabilityModuleV1` constrains origin to `OFFICIAL`.

The Module preserves purpose, problem classes, requirement class, version,
implementation references, input/output contracts, Model/Provider references,
resource and permission references, compatibility, integrity, provenance,
degradation, rollback, Self visibility, and optional knowledge references.

Requirement classes remain independent from origin:

- `MANDATORY_SAFETY`
- `SYSTEM_REQUIRED`
- `OPTIONAL`

`MARKET` is retained only for schema compatibility and is rejected by the
current Official admission flow.
