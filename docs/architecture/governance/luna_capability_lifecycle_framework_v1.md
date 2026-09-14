# Luna Capability Lifecycle Framework v1

## Purpose

Capability Lifecycle is a governance framework, not a single mandatory state machine. Governance manages authority, compatibility, traceability, lifecycle evidence, and safe extension boundaries; it does not define every future Capability form or operational state.

## Common Lifecycle Markers

The following markers provide a shared governance vocabulary when applicable:

- **Candidate** — proposed identity and non-binding declaration.
- **Registered** — governed identity/lifecycle reference exists or is planned through the existing Registry route.
- **Reviewed** — assessment, compatibility, and risk evidence are available.
- **Approved** — declaration is governance-accepted, without automatic execution authority.
- **Active** — recognized for governed consideration; never Runtime/State/Fact/Decision permission by itself.
- **Frozen** — immutable baseline for reference, validation, comparison, or controlled replacement.
- **Deprecated** — legacy capability subject to sunset and migration rules.
- **Retired** — no longer available for new use; history and trace remain.

These markers are common, not exhaustive. A Capability family may use a subset, repeat review cycles, or add bounded states such as `quarantined`, `suspended`, `limited`, `pilot`, or `migration_pending`.

## Optional-State Rules

An optional lifecycle state must declare:

1. a stable name and owning governance authority;
2. entry/exit evidence and transition authority;
3. allowed operations and explicit denials;
4. mapping to common markers for Registry, Protocol, Permission/Admission, and Diagnostics interoperability;
5. trace/history retention and deprecation/retirement behavior; and
6. proof that it does not weaken L0 Constitution, L1 Protocol, Permission/Admission, or Reducer mutation authority.

An optional state cannot imply Runtime permission, Fact authority, State authority, Decision authority, or self-granted privilege. A Capability cannot create or transition itself into an optional governance state.

## Framework Relationship

The prior Capability Lifecycle Governance state machine remains a reference implementation of the common markers for conventional Capability families. This framework permits future variants while preserving the same authority order: Constitution > Protocol > Permission/Admission > Capability.

