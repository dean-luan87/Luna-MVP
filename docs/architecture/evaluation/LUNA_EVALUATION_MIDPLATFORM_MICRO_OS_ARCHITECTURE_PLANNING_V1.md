# Luna Evaluation — Midplatform Micro-OS Architecture Planning v1

**Phase**：`Phase-Midplatform-Micro-OS-Architecture-Planning-v1-001`  
**Verifier**：`verify_midplatform_micro_os_architecture_planning_v1.py`  
**MIN_CHECKS**：≥ 280

## 验证目标

确认 Luna Midplatform 1.0 已被正式定义为 **Micro-OS 九层架构**，且既有 Constitution、Governance、Health、Module Binding、Model Profile、Output Gate、Task Chain、WorldModel/Memory Bridge 等成果均已归位。

## 必检项

1. L0–L8 九层齐全
2. L0 全局治理约束存在（constitution_kernel）
3. L8 全局监管旁路存在（health_supervisor_bypass）
4. relocation matrix 收纳 Constitution / Governance / Validation / Whitebox / Health / Module Binding / Model Profile / Output Gate / Task Chain / WorldModel / Memory
5. Working Memory ≠ Memory / WorldModel
6. information lifecycle 完整（raw_output → … → discarded）
7. model / rule / algorithm placement matrix 完整
8. health metric scope 覆盖中台自身指标
9. failure mode matrix 覆盖 timeout / long pending / health tag missing / queue backlog / schema invalid / stale state / resource overload / recovery failed 等
10. degraded / recovery mode policy 五模式完整
11. WorldModel / Memory 双向边界明确
12. local / cloud model routing boundary 明确
13. 全部 runtime / model / memory / worldmodel / output / task execution flags 为 false
14. non-claims 完整

## 运行方式

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 tools/evaluation/midplatform/run_midplatform_micro_os_architecture_planning_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_micro_os_architecture_planning_v1.py
```

## 预期结果

- `summary.json` → `planning_pass: true`
- `final_decision` → `MIDPLATFORM_MICRO_OS_ARCHITECTURE_PLANNING_READY_FOR_DRYRUN_AND_REVIEW`
- `verifier_report.json` → `verifier: GO`

## Non-Claims

- Micro-OS planning ≠ real operating system
- Micro-OS planning ≠ runtime enabled
- Micro-OS planning ≠ model selected or invoked
- Micro-OS planning ≠ Memory / WorldModel write allowed
- Micro-OS planning ≠ Output to user allowed
