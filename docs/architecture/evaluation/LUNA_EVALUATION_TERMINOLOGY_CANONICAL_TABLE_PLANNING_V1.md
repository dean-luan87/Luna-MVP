# Luna Evaluation — Terminology Canonical Table Planning v1

**Phase**：`Phase-Terminology-Canonical-Table-Planning-v1-001`  
**输出**：`_eval_out/terminology_canonical_table_planning_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_terminology_canonical_table_planning_v1.py
python3 tools/evaluation/governance/verify_terminology_canonical_table_planning_v1.py
```

## 上游依赖

- Roadmap Decision GO：`permission_semantics_canonicalization_roadmap_decision_v1_smoke_v0/`
- `selected_route=Route B — Terminology Canonical Table Planning`
- `ready_for_terminology_canonical_table_planning=true`
- Route C pending P0；Route G blocked

## 通过条件（摘要）

- 10 类核心对象；24 术语全覆盖
- 每术语规划 canonical meaning / forbidden interpretation / required fields / verifier usage
- `canonical_entry_generated_now=false`；`enforced_now=false`
- success claim dependency ≥12 topics；output plan ≥8 artifacts
- final decision 指向 Terminology Canonical Table DryRun

## Smoke 结果

- **verifier**: GO
- **checks**: 420/420
- **boundary_ok**: true
- **final_decision**: `TERMINOLOGY_CANONICAL_TABLE_PLANNING_READY_FOR_DRYRUN`
- **Downstream**: Terminology Canonical Table DryRun **GO**（439/420 checks）→ Post-DryRun Review
