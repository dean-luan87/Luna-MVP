# Luna Evaluation — Evidence Chain Governance Roadmap Decision v1

**Phase**：`Phase-Evidence-Chain-Governance-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/evidence_chain_governance_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_evidence_chain_governance_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_evidence_chain_governance_roadmap_decision_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 521/420
- **boundary_ok**: true
- **selected_route**: Route A — Owner/Operator Approval Protocol Planning
- **final_decision**: `EVIDENCE_CHAIN_GOVERNANCE_ROADMAP_DECISION_READY_FOR_OWNER_OPERATOR_APPROVAL_PROTOCOL_PLANNING`
- **Next**: `Phase-Owner-Operator-Approval-Protocol-Planning-v1-001`
- **Downstream**: Owner/Operator Planning **GO**（488/420）→ DryRun
