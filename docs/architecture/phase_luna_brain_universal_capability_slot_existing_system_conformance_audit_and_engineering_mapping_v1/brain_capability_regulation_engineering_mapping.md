# Brain Capability Regulation Engineering Mapping

## Future handoff

```text
Capability State
 + Resource State
 + Task Context
 + Survival/Safety State
        ↓ read-only inputs
Capability Self View
        ↓
Brain Capability Regulation reasoning
        ↓ candidate only
Capability Regulation Candidate
        ↓
Capability Governance / Admission
        ↓ governed lifecycle transition
Slot / Module state
        ↓ read-only projection
Capability Self View update
```

Brain may evaluate survival pressure, energy, compute, memory, storage,
thermal state, task requirements, usage/contribution, recovery cost,
compatibility, and newly available official Modules.

## Prohibited adapter behavior

Brain must not call direct `slot.disable()`, `uninstall()`, `install()`,
`bind()`, `upgrade()`, `rollback()`, or equivalent mutation APIs. User
requests enter the same candidate/governance boundary.

## Candidate vocabulary

Future candidates may use the existing governance vocabulary where available:
ACQUIRE, DOWNLOAD, INSTALL, BIND, ACTIVATE, SUSPEND, RESUME, RELEASE,
UNLOAD, UNINSTALL_IMPLEMENTATION, RESTORE, REBIND, REPLACE, UPGRADE,
DEGRADE, and ROLLBACK.

These are candidate intents for Capability Governance, not execution commands.

## Constitutional rule

Brain regulation may preserve or improve the minimum survival configuration,
but it cannot reduce the constitutional safety baseline. Low usage or low
historical contribution cannot override `SURVIVAL_BASELINE` protection.
