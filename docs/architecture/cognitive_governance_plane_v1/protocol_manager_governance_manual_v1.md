# Protocol Manager Governance Manual v1

## Protocol lifecycle

Protocol Manager governs protocol creation, registration, versioning,
compatibility, deprecation, migration, and archival.

```text
Change Proposal → Compatibility Review → Version Candidate → Admission
→ Active → Deprecated → Archived
```

## When to create a protocol

Create a new Protocol when a new boundary, data contract, authority, or
Evidence type cannot be represented without ambiguity by an existing protocol.
The proposal must state owner, consumers, schema, provenance, failure behavior,
security boundary, and Constitution checks.

## When to modify

Modify an existing Protocol only when compatibility impact, migration plan,
version semantics, rollback, and affected Registry/Admission entries are
reviewed. A breaking change requires a new version and explicit activation.

## When to deprecate

Deprecate when a replacement is admitted, migration is available, and active
consumers are identified. Deprecated protocols remain readable for migration;
they are not silently deleted.

Protocol Manager does not interpret Reality, create a Goal, make a Decision,
call a Provider, or execute an Action.

Protocol Manager does not create a Goal, does not make a Decision, does not
call a Provider, and does not execute an Action.

Protocol Manager does not call a Provider.
