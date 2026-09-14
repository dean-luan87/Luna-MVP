# Luna Capability Lifecycle Governance Go/No-Go v1

## v2 Framework Revision

This record now also covers `Phase-L1-Capability-Lifecycle-Governance-Planning-v2-001`. The existing linear lifecycle model remains a reference track, while the v2 framework defines common markers, optional states, extension rules, contextual availability, and assessment dimensions. No prior governance boundary is removed or weakened.

## Replacement and Deprecation Strategy

An old Capability is replaced through a governed successor Candidate, compatibility assessment, coexistence window, dependency migration, validation evidence, and explicit sunset. Existing approved consumers may use a Deprecated Capability only during its declared migration window. New consumers may not depend on it. Retirement preserves identity, lifecycle history, Protocol/Contract references, provenance, and trace; governance records are never directly deleted.

## Diagnostics Boundary

Diagnostics may detect Capability drift, Contract mismatch, dependency risk, and Deprecated usage. Diagnostics may expose validation, lifecycle, and compatibility evidence. Diagnostics may not automatically activate, upgrade, grant Permission to, register, or retire a Capability.

## Planning Completion

- Capability lifecycle states and transition authorities are defined.
- Admission flow and non-authorizing Registration boundary are defined.
- Permission source is limited to Governance Core through a future Capability Execution Context.
- Upgrade, replacement, coexistence, deprecation, rollback, and diagnostics rules are defined.
- Lifecycle is explicitly a framework, not a fixed unique state flow.
- Common states, optional-state extension rules, evolution impact levels, contextual governance, and assessment dimensions are defined.

## Counts

- `blocker_count: 0`
- `warning_count: 2`
- `followup_count: 2`

## Warnings

1. This is lifecycle planning only; no Capability Registry Runtime, Registry write, activation, Permission Runtime, contextual evaluation engine, or Runtime Integration exists.
2. Existing A3 registration/admission work remains a candidate/reference mapping; optional state extensions and assessment dimensions do not establish an active Capability or execution authority.

## Final Candidate Decision

`CAPABILITY_LIFECYCLE_FRAMEWORK_PLANNING_READY_WITH_NOTES`

No final GO is declared. Runtime remains unauthorized.
