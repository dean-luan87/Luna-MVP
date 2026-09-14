# Luna Evaluation — Evidence Chain Governance DryRun v1

**Phase**：`Phase-Evidence-Chain-Governance-DryRun-v1-001`  
**输出**：`_eval_out/evidence_chain_governance_dryrun_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_evidence_chain_governance_dryrun_v1.py
python3 tools/evaluation/governance/verify_evidence_chain_governance_dryrun_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 428/420
- **boundary_ok**: true
- **final_decision**: `EVIDENCE_CHAIN_GOVERNANCE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**: `Phase-Evidence-Chain-Governance-Post-DryRun-Review-v1-001`
- **Downstream**: Post-DryRun Review **GO**（434/420）→ Roadmap Decision
