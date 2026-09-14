# System Diagnostics and Runtime Health Inventory

## Evidence producers

| Evidence | Current asset | Authority classification |
|---|---|---|
| Python/package dependency probe | `probe_yolo11n_python_dependencies_v1.py`, `DependencyProbeResultV1` | Diagnostic evidence; not admission authority |
| Runtime/device health | `runtime_health_checker_v1.py` | Candidate health evidence; returns `health_status` and `routing_eligible`, marked candidate/not-fact |
| Module health and resource diagnostics | `model_manager_health_diagnostics_v1.py` | Diagnostic summary; explicitly candidate-only/not-fact |
| Hardware/resource profiles | `runtime_resource_profile_v1.py` and hardware contracts | Resource evidence/profile; not cognitive authority |
| Health/watchdog signals | `health_watchdog_types_v1.py` and static validators | Health/degradation/recovery recommendation candidates; no restart/process control |
| System maintenance diagnostics | `system_maintenance_diagnostics_v1.py` | Aggregated candidate diagnostics; no write or runtime control |

## What is not currently owned as one contract

The repository has diagnostic evidence for package presence, runtime health,
device/resource compatibility and model readiness, but no single canonical
Runtime Admission result that consumes those evidence refs and is then required
by the logical resolution-to-invocation bridge.

Diagnostics must remain distinct from admission authority:

```text
diagnostic evidence
  → Model/Provider/Capability Admission review
  → executable admission candidate or blocked candidate
```

The diagnostic source does not become the owner of capability value, Need,
Goal, or Provider execution.

