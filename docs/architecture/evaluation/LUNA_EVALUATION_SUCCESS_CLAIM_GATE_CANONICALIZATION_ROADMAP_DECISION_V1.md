# Luna Evaluation — Success Claim Gate Canonicalization Roadmap Decision v1

**Phase**：`Phase-Success-Claim-Gate-Canonicalization-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/success_claim_gate_canonicalization_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_success_claim_gate_canonicalization_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_success_claim_gate_canonicalization_roadmap_decision_v1.py
```

## 上游依赖

- Post-DryRun Review GO：`success_claim_gate_canonicalization_post_dryrun_review_v1_smoke_v0/`
- `ready_for_success_claim_gate_canonicalization_roadmap_decision=true`
- `success_claim_gate_generated_now=false`；`success_claim_allowed=false`
- verifier_report / summary / candidate evidence 不可支撑 success claim
- source chain 为 evidence chain 组成部分，但不可单独推出 success claim

## 通过条件（摘要）

- 9 类 roadmap decision 对象；三段 success claim gate chain GO
- Route A selected；Route D deferred；Route H blocked
- Evidence chain dependency ≥12；planning scope ≥14 topics；risk matrix ≥14
- 所有 success claim / evidence / execution 权限继续冻结

## Smoke 结果

- **verifier**: GO
- **checks**: 466/420
- **boundary_ok**: true
- **selected_route**: `Route A — Evidence Chain Governance Planning`
- **final_decision**: `SUCCESS_CLAIM_GATE_CANONICALIZATION_ROADMAP_DECISION_READY_FOR_EVIDENCE_CHAIN_GOVERNANCE_PLANNING`
- **Next**: `Phase-Evidence-Chain-Governance-Planning-v1-001`
- **Downstream**: Evidence Chain Governance Planning **GO**（502/420）→ DryRun
