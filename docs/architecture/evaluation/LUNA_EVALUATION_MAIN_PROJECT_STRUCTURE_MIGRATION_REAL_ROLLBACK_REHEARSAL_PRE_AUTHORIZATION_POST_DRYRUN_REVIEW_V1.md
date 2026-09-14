# Luna Evaluation — Real Rollback Rehearsal Pre-Authorization Post-DryRun Review v1

**Phase**：`Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Post-DryRun-Review-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_real_rollback_rehearsal_pre_authorization_post_dryrun_review_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_post_dryrun_review_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_post_dryrun_review_v1.py
```

## 通过条件（摘要）

- 必须读取上游 Pre-Authorization DryRun 输出，并确认其 `verifier=GO / boundary_ok=true / ready_for_pre_authorization_post_dryrun_review=true`
- 必须生成 10 类 review 对象（含 Completeness / NonRelease / Continuity / BoundaryFreeze / SuccessClaim / NonExecutable / IssueRegister / TerminologyReview / Readiness）
- **AuthorizationNonReleaseReviewMatrix** 与 **BoundaryFreezeReviewMatrix** 必须全 pass
- TerminologyReview 必须覆盖 ≥9 对术语
- final decision 必须指向 Pre-Authorization Roadmap Decision
- Verifier ≥ 420 checks（baseline 340）

## Smoke 结果

- **verifier**: GO
- **checks**: 560/420
- **final_decision**: `MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION`
- **Next**: `Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Roadmap-Decision-v1-001`

