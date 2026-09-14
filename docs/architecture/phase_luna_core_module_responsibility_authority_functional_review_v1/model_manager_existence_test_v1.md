# Model Manager Existence Test v1

| Alternative | Finding |
|---|---|
| Capability Governance owns models | Rejected: capability identity must remain portable from assets and weights. |
| Provider Governance owns models | Rejected: Provider executes; it must not own files, checksums, or model lifecycle. |
| Diagnostics owns models | Rejected: Diagnostics observes health, not identity or registration. |
| Filesystem registry only | Rejected: insufficient for versions, provenance, mappings, lifecycle, and retirement. |
| Independent Model Governance | **KEEP**: preserves asset identity, lifecycle, provisioning, mapping, and auditability. |

Independent Model Governance is justified by identity stability, portability,
versioning, provisioning, integrity, dependency declaration, mapping, and
retirement responsibility.
