# Luna Evaluation — Terminology Canonical Table Roadmap Decision v1

**Phase**：`Phase-Terminology-Canonical-Table-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/terminology_canonical_table_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_terminology_canonical_table_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_terminology_canonical_table_roadmap_decision_v1.py
```

## 上游依赖

- Post-DryRun Review GO：`terminology_canonical_table_post_dryrun_review_v1_smoke_v0/`
- `ready_for_terminology_canonical_table_roadmap_decision=true`
- `ready_for_success_claim_gate_planning=false`（上游须保持冻结）

## 通过条件（摘要）

- Route **C** `selected_now=true`；仅 planning allowed
- Route **G** `blocked_now=true`；Route **A/B/D** `deferred=true`
- 9 类 roadmap 对象；≥12 success claim topics；≥12 entry risks
- `success_claim_allowed=false`；`success_claim_gate_generated_now=false`
- final decision 指向 Success Claim Gate Canonicalization Planning

## Smoke 结果

- **verifier**: GO
- **checks**: 460/420
- **boundary_ok**: true
- **selected_route**: `Route C — Success Claim Gate Canonicalization Planning`
- **final_decision**: `TERMINOLOGY_CANONICAL_TABLE_ROADMAP_DECISION_READY_FOR_SUCCESS_CLAIM_GATE_CANONICALIZATION_PLANNING`
- **Downstream**: Success Claim Gate Canonicalization Planning **GO**（515/420）→ DryRun
