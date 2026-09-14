# Recommended Implementation Sequence

This sequence is a future engineering plan, not an implementation performed
by this audit.

1. Review and approve this conformance matrix and cardinality policy.
2. Add a narrow Universal Slot identity/binding contract under existing
   Capability Registry/Governance ownership.
3. Map existing capability IDs into Module identity without duplicating the
   Registry.
4. Add Slot compatibility and binding candidates that reference existing
   admission, Model Manager, Provider, resource, permission, integrity, and
   safety evidence.
5. Separate Module lifecycle, Implementation qualification, and Slot binding
   lifecycle through additive references.
6. Add read-only history/recovery projection using Memory/Experience and
   System Maintenance references.
7. Add Capability Self projection for current, degraded, suspended,
   historical, recoverable, potential, and unavailable states.
8. Add Brain Capability Regulation candidate handoff; retain Capability
   Governance as the only lifecycle writer.
9. Review and map `SURVIVAL_BASELINE`, `SYSTEM_REQUIRED`, and `OPTIONAL`
   without silently renaming legacy states.
10. Perform a separate visual conformance/remediation phase. Only then decide
    whether visual candidate types need adapters or narrow additive changes.

No step authorizes provider execution, installation, activation, download,
rollback, Memory mutation, Learning, or runtime behavior.
