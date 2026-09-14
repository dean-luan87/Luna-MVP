# Capability Self Engineering Mapping

Capability Registry state must be projected into the existing Cognitive Self
Model / Capability Awareness boundary. The Registry remains the source of
capability definitions and lifecycle evidence; Capability Self remains the
read-only cognitive representation of ability state.

| Future Self view | Source mapping | Meaning |
|---|---|---|
| CURRENT | Active/Available admitted Module plus usable Implementation evidence | Luna may currently use the declared capability boundary. |
| DEGRADED | Degraded/Limited capability health | A restricted or less reliable boundary is visible; identity remains. |
| SUSPENDED | Suspended lifecycle evidence | Capability is known but not currently usable. |
| HISTORICAL | Slot binding history and Memory/Experience references | Luna possessed or used the capability previously. |
| RECOVERABLE | Historical Module plus valid recovery/compatibility/resource references | Capability may be restored, not currently available. |
| POTENTIAL | Official Module definition/admission candidate and resource/compatibility evidence | Capability may be considered; it is not possessed or active. |
| UNAVAILABLE | Not installed, incompatible, retired, or no admissible implementation | Capability is not currently usable. |

Existing Self vocabulary (`Available`, `Degraded`, `Limited`, `Unavailable`,
`Unknown`) should be preserved through a future adapter rather than silently
renamed. `CURRENT`, `HISTORICAL`, and `RECOVERABLE` are view dimensions and
may require a separate projection from lifecycle state.

Capability Self does not admit, bind, install, activate, suspend, or remove a
capability. Its state update remains governed by existing Self/State
reduction and Memory/Experience boundaries.
