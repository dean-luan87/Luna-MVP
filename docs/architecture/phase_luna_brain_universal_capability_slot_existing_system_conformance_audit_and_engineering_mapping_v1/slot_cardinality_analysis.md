# Slot Cardinality Analysis

## Recommended canonical rules

1. One Slot has zero or one active Module binding at a time. Historical
   bindings are references/events and do not count as active bindings.
2. One Capability Module may bind to multiple Slot instances when the Module
   declares multi-instance support and each binding passes compatibility,
   resource, permission, and safety checks.
3. One Module may have multiple Implementation candidates. A Slot has at most
   one active Implementation selection for its active Module binding.
4. Compatible Implementation, Model, or Provider replacement preserves Module
   identity. The replacement receives its own implementation/resource record.
5. Removing a Module unbinds the active relationship; it does not delete Slot
   identity or historical binding records. The Slot becomes EMPTY, AVAILABLE,
   or RECOVERY_CANDIDATE according to governance evidence.
6. Restoration references a historical Module and a new compatibility
   assessment. Historical presence does not make a capability currently usable.
7. Concurrent versions may exist as candidates or on separate Slots. They may
   not silently compete as two active bindings on one Slot.
8. Conflicting bindings are rejected or deferred as a governance conflict;
   there is no implicit last-write-wins rule.
9. An empty Slot is a valid generic resource with no current capability. Self
   may expose historical or recoverable information without reporting a
   current usable capability.

## Rationale

This preserves Slot identity across lifecycle changes while keeping Module
identity and Implementation identity separate. It also prevents concurrent
state ambiguity and allows resource-isolated multi-instance capability use
without specializing the Slot type.

## Ambiguities requiring future decision

- Whether all Slots are persistent physical/logical identities or whether a
  subset may be ephemeral must be decided by Capability Governance.
- Whether a test Implementation may be active on a dedicated Slot requires a
  qualification policy.
- The retention period and storage owner for binding history requires Memory /
  Experience Governance input.

No runtime cardinality behavior is implemented in this phase.
