# Capability History and Recovery Mapping

Existing Self and Memory/Experience contracts provide capability memory,
performance evidence, limitations, provenance, and historical references.
System Maintenance provides diagnostics, dependency impact, model asset
issues, remediation candidates, and trace replay.

## Missing generic concept

No canonical record was found that binds these references to a persistent Slot
history. A future extension should preserve:

- Slot identity
- Module identity and historical version
- Implementation/model/provider references
- usage and contribution references
- removal/suspension reason
- recoverability
- compatibility evidence
- estimated restoration cost reference
- rollback/recovery linkage

This should be a governed reference projection, not an autonomous Memory
write. Memory/Experience remains responsible for persistence and consolidation
where its existing contracts permit.

## Recovery semantics

Historical presence is not current availability. Restoration requires a new
admission, compatibility, integrity, permission, resource, safety, and
rollback assessment. A recovery candidate may be rejected without deleting
history.
