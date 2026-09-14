# Five Readiness Fields — Ownership Matrix

| Field | Current source | Target owner/source | Authoritative? | Long-term terminal ownership |
|---|---|---|---|---|
| `source` | Real trial `--source`; frame/source ref | Observation/acquisition context, then Observation Gateway | Input reference, not model readiness | Test adapter only; not canonical long-term |
| `model_path` | Real trial `--model-path`; provisioning candidate | Model Manager / Model Manifest governed asset path ref | Model asset metadata; not Brain/A choice | No; terminal may provide a test input during transition |
| `dependency_status` | Real trial CLI, passed to model/readiness resolver | System Diagnostics/dependency probe evidence, consumed by Model/Capability Admission | Evidence, not admission by itself | No; terminal status is temporary test input |
| `declared_checksum` | Real trial CLI or model manifest if present | Model Manifest / Model Governance asset metadata | Declared integrity expectation | No; current YOLO11n manifest lacks a stable value |
| `observed_checksum` | Real trial CLI/provisioning candidate | Integrity verification evidence at Model Manager/Runtime Admission boundary | Observed integrity evidence | No; terminal should not be the permanent integrity authority |

## Key distinction

The terminal currently owns delivery of values required by the controlled
trial. That is an execution/test input ownership fact, not evidence that the
terminal is the canonical owner. The current repository supports the target
semantic mapping for four of the five fields, but their unified handoff is
partially missing.

