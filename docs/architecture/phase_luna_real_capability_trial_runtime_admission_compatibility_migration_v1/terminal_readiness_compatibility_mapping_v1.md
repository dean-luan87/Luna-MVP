# Terminal Readiness Compatibility Mapping

| CLI input | Candidate mapping | Canonical target owner |
|---|---|---|
| `--source` | `source_acquisition_context_ref` and terminal evidence ref | Observation/acquisition context |
| `--model-path` | governed model path candidate ref | Model Manager / Model Manifest |
| `--dependency-status` | dependency health/status candidate ref | System Diagnostics |
| `--declared-checksum` | declared integrity metadata ref | Model Manager / Model Manifest |
| `--observed-checksum` | observed integrity evidence ref | Integrity evidence boundary |

Provenance includes `TERMINAL_CONTROLLED_TRIAL_INPUT`; terminal ownership is
not promoted to canonical authority.

