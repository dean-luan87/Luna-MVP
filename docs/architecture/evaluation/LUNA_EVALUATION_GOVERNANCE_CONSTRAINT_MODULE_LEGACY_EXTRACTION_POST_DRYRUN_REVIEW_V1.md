# Luna Evaluation — Governance Constraint Module Legacy Extraction Post-DryRun Review v1

**Phase**：`Phase-Governance-Constraint-Module-Legacy-Extraction-Post-DryRun-Review-v1-001`  
**输出**：`_eval_out/governance_constraint_module_legacy_extraction_post_dryrun_review_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_governance_constraint_module_legacy_extraction_post_dryrun_review_v1.py
python3 tools/evaluation/governance/verify_governance_constraint_module_legacy_extraction_post_dryrun_review_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 421/420
- **boundary_ok**: true
- **final_decision**: `GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION`
- **Next**: `Phase-Governance-Constraint-Module-Legacy-Extraction-Roadmap-Decision-v1-001`（**已完成 GO**；见 Roadmap Decision evaluation doc）
- **main_migration_chain_resumed_now**: false

## 核心对象（10 类）

| 对象 | 产物 |
|------|------|
| LegacyExtractionPostDryRunReviewPolicy | `legacy_extraction_post_dryrun_review_policy_v1.json` |
| LegacyExtractionDryRunCompletenessReview | `legacy_extraction_dryrun_completeness_review_v1.json` |
| LegacyAssetNonModificationReview | `legacy_asset_non_modification_review_v1.json` |
| LegacyChainStatusReview | `legacy_chain_status_review_v1.json` |
| ConstraintMappingQualityReview | `constraint_mapping_quality_review_v1.json` |
| CanonicalFrozenFieldExtractionReview | `canonical_frozen_field_extraction_review_v1.json` |
| DomainConstraintPreservationReview | `domain_constraint_preservation_review_v1.json` |
| InheritanceAndAbsorptionPolicyReview | `inheritance_and_absorption_policy_review_v1.json` |
| ConstraintModuleOutputNonGenerationReview | `constraint_module_output_non_generation_review_v1.json` |
| LegacyExtractionPostDryRunReviewReadinessDecision | `legacy_extraction_post_dryrun_review_readiness_decision_v1.json` |

## 审查结论

| 审查维度 | 结果 |
|---------|------|
| Dry-run completeness（10 objects） | pass |
| Legacy asset non-modification | pass |
| Legacy chain status（12 chains） | pass |
| Constraint mapping quality（14 domains） | pass |
| Frozen field extraction（25 patterns） | pass |
| Domain constraint preservation（12 domains） | pass |
| Inheritance / absorption policy | pass |
| Output non-generation（12 artifacts） | pass |

## 边界冻结

- `legacy_as_source_evidence=true`；`legacy_as_template_source=false`
- 旧链路未 deprecated、未 rewrite、未作为模板来源
- 正式 constraint module / canonical template 未生成；主线未恢复
