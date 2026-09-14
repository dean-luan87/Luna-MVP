# Readiness Evidence Ownership Mapping

| Input | Canonical evidence owner | Admission use | Not owned by |
|---|---|---|---|
| Logical capability ref | Capability Registry/Governance | Identifies logical request target | Brain/A/Loop |
| Capability slot ref | Universal Slot Governance | Confirms slot binding | Provider |
| Model asset/version ref | Model Manager/Model Governance | Resolves admitted model identity | Brain/A |
| Governed model path ref | Model Manifest / Model Governance | Binds physical asset to governed asset | Terminal long-term |
| Declared checksum | Model Manifest / Model Governance | Integrity expectation | Brain/A/Loop |
| Observed integrity evidence | Integrity/provisioning evidence boundary | Verifies current asset against declaration | Brain/A/Loop |
| Dependency health refs | System Diagnostics / dependency evidence | Blocks or supports technical admission | Diagnostics itself as authority |
| Device/runtime health refs | Runtime Health / resource evidence | Blocks or supports executable admission | Provider self-admission |
| Provider compatibility refs | Provider Governance + Model Manager contracts | Confirms adapter/model compatibility | A/Brain |
| Permission refs | Permission/Safety Governance | Admission constraint | Capability Runtime |
| Resource refs | Resource Governance | Budget/device/slot constraint | Loop |
| Safety refs | Safety Governance | Safety boundary | Provider |
| Source/acquisition context | Observation/acquisition owner | Binds input source | Model Manager |
| Source state version | Source owner / governance state | Staleness and validity boundary | Loop semantics |

## Evidence versus decision

Evidence producers report candidate facts or health signals. Capability
Admission Governance decides whether the combined candidate is admitted. No
evidence producer may silently promote its result to executable authority.

