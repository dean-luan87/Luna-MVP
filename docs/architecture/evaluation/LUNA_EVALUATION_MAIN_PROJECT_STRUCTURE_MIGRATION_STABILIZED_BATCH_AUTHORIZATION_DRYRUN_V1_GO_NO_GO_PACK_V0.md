# GO / NO-GO Pack — Main Project Structure Migration Stabilized Batch Authorization DryRun v1

## GO

- Batch Authorization Planning verifier=GO，且必要产物齐全
- B0–B7 authorization scope / gates / window / rerun auth / rollback auth / file-op boundary / guard / non-claims dry-run 消费可串联
- `batch_authorization_dryrun_only=true`、`simulated=true`
- request/grant/arming/execution 全为 false；无任何真实 file operation
- 若使用 workspace 输入，明确标记 `source_path_mode=workspace_fallback`
- final decision 指向 Batch Authorization Post-DryRun Review

## NO-GO

- planning 非 GO 或产物缺失
- request sent / grant issued / arming / execution 任一为 true
- final decision 不指向 `Phase-Main-Project-Structure-Migration-Stabilized-Batch-Authorization-Post-DryRun-Review-v1-001`

