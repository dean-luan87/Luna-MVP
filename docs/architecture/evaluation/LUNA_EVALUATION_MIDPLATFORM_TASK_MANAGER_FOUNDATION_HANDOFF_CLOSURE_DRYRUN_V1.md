# Evaluation: Task Manager Foundation Handoff Closure DryRun v1

The evaluation validates closure planning readiness for post-dryrun review and records the Closure Channel Governance governance debt.

## Commands

```bash
python3 tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_closure_dryrun_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_closure_dryrun_v1.py
```

## GO Criteria

- Closure planning package GO with `passed_checks>=420`
- `freeze_candidate_preserved=true`
- `closure_candidate_preserved=true`
- `closure_channel_governance_debt_recorded=true`
- `l1_closure_protocol_not_implemented=true`
- `closure_dryrun_only=true`
