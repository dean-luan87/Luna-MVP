# Owner Gap Analysis

| Responsibility | Current owner | Target owner | Gap type | Severity | Migration action |
|---|---|---|---|---|---|
| Cognitive capability request | A/Brain governance | A/Brain governance | NO_GAP | — | Preserve |
| Logical capability identity | Capability Registry | Capability Registry | NO_GAP | — | Preserve |
| Scope assessment | Capability Scope Governance | Capability Scope Governance | NO_GAP | — | Preserve |
| Logical resolution | Universal Slot/Capability Governance | Same | NO_GAP | — | Preserve, clarify result meaning |
| Model asset/path metadata | Model Manager | Model Manager | ADAPTER_GAP | Medium | Replace raw trial path with governed asset ref at a later boundary |
| Declared checksum | Model Manifest/Model Governance, incomplete for YOLO11n | Same | CONTRACT_GAP | Medium | Establish governed metadata source before real canonicalization |
| Observed checksum | Terminal/provisioning candidate | Integrity evidence boundary reviewed by Admission | ADAPTER_GAP | Medium | Preserve evidence provenance; do not move into Brain/A/Loop |
| Dependency status | Terminal/probe candidate | System Diagnostics evidence consumed by Admission | TRIAL_ONLY_GAP | High | Define evidence handoff; do not let diagnostic evidence self-admit |
| Runtime/device health | Runtime health checker candidate | Capability Admission coordination | CONTRACT_GAP | Medium | Require health evidence in executable admission assessment |
| Executable capability admission | Distributed Model/Provider/Capability assets | Capability Admission coordination | CONTRACT_GAP | High | Add logical-resolution-to-admission contract seam, no new Manager |
| Provider invocation | FPO/Provider adapter after admission | Same | NO_GAP | — | Preserve |
| Observation/evidence return | Observation Gateway/FPO | Same | NO_GAP | — | Preserve |
| Loop recording | Loop mechanical boundary | Same | NO_GAP | — | Preserve |
| Canonical failure namespace | Multiple existing status/error vocabularies | Existing namespaces reconciled at adapter boundary | TERMINOLOGY_GAP | Medium | Map, do not add duplicate enums in this review |

