## GO

- DryRun 链审查通过；全部 post-review pass；`ready_for_closure=true`
- 无 sandbox/branch/evidence/verifier rerun 真实执行；success claim 阻断

## NO-GO

- DryRun 未 ready 或任一 post-review 未 pass
- `sandbox_created_now=true` 或 `rollback_success_claim_allowed=true`

## Smoke

- **Next**：`Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Closure-v1-001`
