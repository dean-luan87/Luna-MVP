# Evaluation: Task Manager Controlled Skeleton Implementation DryRun v1

The evaluation runs a static and sample dry-run over the Task Manager skeleton.

## Inputs

- Task Manager skeleton implementation planning output.
- Task Manager mount dry-run and review output.
- Health Watchdog frozen foundation handoff output.
- Decision Center frozen foundation handoff output.

## Required Checks

- Upstream planning is GO.
- Three skeleton files exist.
- `task_manager_files_created_now=true`.
- All runtime/model/provider/write/output/mount/task/tool flags remain false.
- `TaskState`, `TaskReadiness`, six candidate dataclasses, ten pure functions, and twelve static validators exist.
- Seven sample dry-runs pass without task execution or user output.

## Commands

```bash
python3 tools/evaluation/midplatform/run_midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1.py
```
