# Terminal Trial Compatibility Mapping

| Real trial CLI | Candidate seam mapping | Long-term owner |
|---|---|---|
| `--source` | `source_acquisition_context_ref` | Observation/acquisition context |
| `--model-path` | `governed_model_path_ref` | Model Manager / Model Manifest |
| `--dependency-status` | `dependency_status_ref` + dependency health refs | System Diagnostics |
| `--declared-checksum` | `declared_checksum_ref` | Model Manifest / Model Governance |
| `--observed-checksum` | `observed_integrity_evidence_ref` | Integrity evidence boundary |

This is a mapping record only. The Real Capability Single Invocation Trial is
not changed, and terminal values are not promoted to canonical authority.

