# Luna Midplatform — Module Integration Planning v1

## Purpose

Plan Task Manager / Midplatform module integration: boundaries, candidate lifecycle, evidence/record/approval/permission alignment, orchestration skeleton positioning.

This phase does **not** implement runtime, execute integration tests, or create real records/grants.

## Status

- `midplatform_overall_status`: `construction_consolidation`
- Foundation consolidated ≠ midplatform completed
- Owner Approval Request chain closed — do not reopen

## Module Integration View

```
governance_constraints ──cross_cut──► all modules
file_size_governance ──cross_cut──► engineering files
protocol_registry ──► module_boundary_registry ──► candidate_lifecycle_manager
  ──► task_manager_core_orchestration_skeleton ──► evidence/record/approval/permission alignment
  ──► owner_approval_request_closed_module (downstream handoff)
```

## Selected Next Route

**A. Module Boundary Registry Planning** — foundational prerequisite

## Commands

```bash
python3 tools/evaluation/midplatform/run_task_manager_module_integration_planning_v1.py
python3 tools/evaluation/midplatform/verify_task_manager_module_integration_planning_v1.py
```

## Output

`_tmp_eval_out/task_manager_module_integration_planning_v1_smoke_v0/`
