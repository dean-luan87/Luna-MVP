# Luna Evaluation — Evidence Chain Governance Planning v1

**Phase**：`Phase-Evidence-Chain-Governance-Planning-v1-001`  
**输出**：`_eval_out/evidence_chain_governance_planning_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_evidence_chain_governance_planning_v1.py
python3 tools/evaluation/governance/verify_evidence_chain_governance_planning_v1.py
```

## 上游依赖

- Roadmap Decision GO：`success_claim_gate_canonicalization_roadmap_decision_v1_smoke_v0/`
- `selected_route=Route A — Evidence Chain Governance Planning`
- `ready_for_evidence_chain_governance_planning=true`
- `success_claim_gate_generated_now=false`；`success_claim_allowed=false`

## Smoke 结果

- **verifier**: GO
- **checks**: 502/420
- **boundary_ok**: true
- **final_decision**: `EVIDENCE_CHAIN_GOVERNANCE_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Evidence-Chain-Governance-DryRun-v1-001`
- **Downstream**: DryRun **GO**（428/420）→ Post-DryRun Review
