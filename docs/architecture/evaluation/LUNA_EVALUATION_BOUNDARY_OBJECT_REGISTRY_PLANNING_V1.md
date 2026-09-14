# Luna Evaluation — Boundary Object Registry Planning v1

**Phase**：`Phase-Boundary-Object-Registry-Planning-v1-001`  
**输出**：`_eval_out/boundary_object_registry_planning_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_boundary_object_registry_planning_v1.py
python3 tools/evaluation/governance/verify_boundary_object_registry_planning_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 420/420
- **boundary_ok**: true
- **final_decision**: `BOUNDARY_OBJECT_REGISTRY_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Boundary-Object-Registry-DryRun-v1-001`
- **Downstream**: Boundary Object Registry DryRun **GO**（420/420）→ Post-DryRun Review
