# Luna Global Authority / Responsibility Audit v1

## Purpose

This package consolidates the completed module adjudications into one system-wide authority ledger. It is an architecture audit, not a runtime design or implementation plan.

## Adjudication

Luna is **AUTHORITY_MODEL_COHERENT_WITH_GAPS**. The principal owner splits are mutually consistent: Brain governs global cognitive work and final assimilation; A governs local semantic reasoning; source modules own their state; execution modules own admission or invocation at their boundary; Diagnostics observes and classifies; Loop persists references mechanically; Protocol Governance governs representation and compatibility.

The remaining gaps are explicit contract/admission/invalidation gaps, not permission for a new Manager or a second owner.

## Hard rules used

1. Authority implies responsibility.
2. Candidate production does not imply admission authority.
3. Read access does not imply mutation authority.
4. Derived state does not own source state.
5. Protocol ownership does not imply source ownership.
6. Diagnostics ownership does not imply remediation authority.
7. Policy ownership and enforcement are separate.
8. Execution infrastructure does not own semantic decisions.
9. Mechanical persistence does not own semantic lifecycle.
10. Shared contracts do not imply shared final mutation authority.
11. Cross-owner changes propagate through refs, versions and invalidation.
12. No module may grant itself authority.

## Scope and evidence

Primary evidence is the completed module adjudication package at `docs/architecture/phase_luna_core_module_responsibility_authority_functional_review_v1/`. Historical assets are listed only where they create an observable overlap or bypass risk. No runtime, canonical type, enum, protocol, owner, model, provider, probe or legacy asset was changed.

## Documents

- [Canonical owner registry](canonical_owner_registry_v1.md)
- [Global state ownership ledger](global_state_ownership_ledger_v1.md)
- [Mutation and admission authority matrix](global_mutation_admission_authority_matrix_v1.md)
- [Policy versus enforcement matrix](global_policy_enforcement_matrix_v1.md)
- [Candidate to authority matrix](global_candidate_authority_matrix_v1.md)
- [Conflict and vacuum audit](global_authority_conflict_vacuum_audit_v1.md)
- [Version and invalidation map](global_version_invalidation_map_v1.md)
- [Canonical end-to-end authority flow](canonical_end_to_end_authority_flow_v1.md)
- [Legacy conflict register](legacy_conflict_register_v1.md)
- [Global gap register](global_gap_register_v1.md)
- [Audit summary](global_authority_audit_summary_v1.md)

## Online documentation sections

This package supplies sections 03.8.1 through 03.8.10 for the architecture ledger. It does not authorize implementation. User review is required before any subsequent phase.

