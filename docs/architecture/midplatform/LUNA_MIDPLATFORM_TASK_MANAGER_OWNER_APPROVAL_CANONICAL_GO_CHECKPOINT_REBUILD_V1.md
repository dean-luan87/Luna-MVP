# Task Manager / Owner Approval Canonical GO Checkpoint Rebuild v1

Independent checkpoint rebuild layer — does **not** modify original stage business logic or overwrite original `summary.json` / `verifier_report.json`.

## Purpose

Top-down scan of Task Manager / Owner Approval chain; generate per-stage `canonical_go_checkpoint_v1.json`, mapping tables, and centralized gap/repair reports. Stops adding per-HOLD issue review stages.

## Modes

```bash
# Default: run original runner/verifier top-down (F-group readiness stages scan-only)
python3 tools/evaluation/midplatform/run_task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1.py --mode topdown-rerun

# Scan existing artifacts only
python3 tools/evaluation/midplatform/run_task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1.py --mode scan-only

python3 tools/evaluation/midplatform/verify_task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1.py
```

Output: `_tmp_eval_out/task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1_smoke_v0/`

Per-stage checkpoints: `checkpoints/<stage_key>/canonical_go_checkpoint_v1.json`

Forbidden: modifying original stages, fake GO, new issue review stages, World Model, Scene Graph, SLAM model execution, Field Simulation, Task Reasoning.
