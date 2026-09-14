# Luna Evaluation — Gate Taxonomy and Requirement Framework Planning v1

**Phase**：`Phase-Gate-Taxonomy-and-Requirement-Framework-Planning-v1-001`  
**输出目录**：`_eval_out/gate_taxonomy_and_requirement_framework_planning_v1_smoke_v0/`

## 目标

验证 planning-only 产物结构、输入 roots 加载状态、taxonomy/requirements/authority/依赖图等对象定义完整性，以及 no-runtime/no-write/no-action 边界冻结。并验证新增上位约束 **Gate Constitution** 已被定义且不改变任何 runtime/既有 gate 行为。

## 运行命令（smoke）

运行 runner：

```bash
python tools/evaluation/governance/run_gate_taxonomy_and_requirement_framework_planning_v1.py
```

运行 verifier：

```bash
python tools/evaluation/governance/verify_gate_taxonomy_and_requirement_framework_planning_v1.py
```

## 通过判定

verifier 必须输出：

- `verifier=GO`
- `final_decision=GATE_TAXONOMY_AND_REQUIREMENT_FRAMEWORK_PLANNING_READY_FOR_MIDPLATFORM_FUNCTION_GOVERNANCE`
- `recommended_next_phase=Phase-MidPlatform-Function-Governance-and-Consolidation-Planning-v1-001`

