# Capability Availability and Degradation v1

| State | Meaning | Typical owner |
|---|---|---|
| logically supported | scope/resolution can satisfy the requirement | Capability Governance |
| logically unsupported | no registered scope/module/contract can satisfy it | Capability Governance |
| available | required implementation evidence is admissible for use | Runtime Admission/Provider boundary |
| unavailable | asset, slot, implementation or runtime prerequisite unavailable | Model Manager/Runtime Admission |
| degraded | usable only under explicit degraded policy | Capability/Runtime Admission governance |
| blocked | governance, asset, integrity, dependency, resource, permission or safety block | corresponding owner/admission boundary |
| stale | source/version/admission evidence no longer valid | Runtime Admission/source owner |

Example: object detection may be logically supported while the YOLO model is
missing. Logical Resolution succeeds; Runtime Admission blocks execution and no
Executable Capability Candidate is created.
