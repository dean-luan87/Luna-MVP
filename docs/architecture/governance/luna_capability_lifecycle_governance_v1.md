# Luna Capability Lifecycle Governance v1

## Scope

This planning model governs Capability identity, admission, lifecycle, permission source, upgrades, replacement, and diagnostics. It does not implement a Capability Registry, create a Registry record, activate a Capability, grant Permission, or authorize Runtime.

## Capability Lifecycle

```text
Candidate → Registered → Reviewed → Approved → Active → Frozen → Deprecated → Retired
```

| state | owns | allows | denies | transition authority |
| --- | --- | --- | --- | --- |
| Candidate | proposal intent, declared input/output/dependencies, non-binding assessment | planning and assessment preparation | execution, permission, Registry self-write, Fact/State/Decision authority | Capability owner submits to Governance Core |
| Registered | planned governed identity/lifecycle reference | traceable review intake and dependency declaration | Runtime execution, self-activation, privilege claim | L1 Capability Registry Authority through an approved future write process |
| Reviewed | assessment, compatibility, and risk evidence | authority review and remediation planning | approval by Capability owner, compatibility bypass | L1 Protocol + Permission/Admission review authorities |
| Approved | accepted Capability declaration | controlled activation planning | automatic Runtime, State, Fact, Decision, or Action authority | designated Governance authorities |
| Active | recognized governed Capability identity | use only when a separate Execution Context, Protocol, Permission, and boundary check allow it | Runtime permission by implication, unrestricted service access, self-upgrade | L1 Capability Registry Authority with Protocol/Permission conditions |
| Frozen | immutable implementation/dependency baseline | read, audit, regression comparison, controlled replacement planning | unreviewed implementation/dependency/Contract change | L1 Capability Registry + Protocol Governance after evidence review |
| Deprecated | legacy Capability with migration/sunset record | existing approved compatible use only during sunset | new dependency, feature expansion, automatic activation | L1 Capability Registry + Protocol/Permission review |
| Retired | closed lifecycle and retained history/trace | audit/history reference only | execution, new dependency, reactivation by default | L1 Capability Registry Authority after migration closure |

## Active Is Not Runtime Permission

`Active` means the Capability identity is recognized by governance and may be considered for a separately evaluated execution request. It does not grant `runtime_authorized`, State access, Fact authority, Decision authority, Action authority, database/network/model use, or any bypass of Admission.

## Capability Permission Model

Permission originates only from the governance chain:

```text
Governance Core
        ↓
Protocol compatibility + Permission/Admission eligibility
        ↓
Capability Execution Context
        ↓
bounded Capability operation (future, separately authorized)
```

A Capability may declare required input, expected candidate output, and dependencies. It may not declare privilege, State authority, Decision authority, Fact authority, or a permission grant for itself.

