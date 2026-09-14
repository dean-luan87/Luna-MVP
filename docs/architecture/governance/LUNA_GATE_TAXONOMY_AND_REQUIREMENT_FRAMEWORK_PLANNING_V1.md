# Luna — Gate Taxonomy and Requirement Framework Planning v1

**Phase**：`Phase-Gate-Taxonomy-and-Requirement-Framework-Planning-v1-001`  
**性质**：planning-only（治理收敛：只定义全局 gate 分类与要求框架；不做实现、不改既有 gate、不合并 gate、不进入 runtime）  
**输出目录**：`_eval_out/gate_taxonomy_and_requirement_framework_planning_v1_smoke_v0/`

## 阶段目标

在 `Post File Stat Roadmap Decision v1` 明确“先做 Gate Taxonomy”之后，本阶段冻结：

- Luna 全局 **GateTypeTaxonomy**（gate 类型分类）
- **GateLevelModel**（gate 等级）
- **GateDecisionVocabulary**（统一决策词汇表）
- **GateRequirementFramework**（统一最低要求）
- **GateAuthorityAndVetoPolicy**（权威/veto/override 规则）
- **GateDependencyGraph**（典型链路依赖图）
- **GateFailureRecoveryPolicy**（失败/恢复/降级/冻结规则）
- **GateAuditTraceRequirement**（审计要求）
- **GateVerifierRequirementTemplate**（verifier 模板最低要求）
- **GateConsolidationRiskRegister**（治理债务与收敛风险登记）

## 强边界（必须压死）

- **planning_only=true**
- **不实现 gate runtime**
- **不修改既有 gate 行为**
- **不合并 gate / 不做 consolidation 实现**
- **不进入真实文件链**（不调用 `stat/exists/open/read/hash/EXIF/probe`）
- **不进入任何 runtime**（camera / OCR provider / tracking / map / crossing / speech）
- **不写** `WorldModel / Memory / Fact / Library`，不触发 action

## Luna Gate Constitution

**定位**：`Gate Constitution` 是 **Gate Taxonomy 之上的设计约束（design constraint）**，用于规定未来所有 gate 设计必须遵守的基本原则。它 **不是新 phase**，不是 runtime，不改变现有 gate 行为，不合并 gate，不启用任何真实文件链，且 **不替代** Safety Constitution。

**层级关系（必须明确）**：

`Safety Constitution`  
> `Gate Constitution`  
> `Gate Taxonomy / Gate Requirement Framework`  
> `Specific Gate Policy`

**12 条宪法条款（摘要）**：

- Article 1：Safety Supremacy（Safety Constitution 永远最高；用户/地图/OCR/视觉/记忆/任务目标均不可覆盖 safety）  
- Article 2：Gate Ownership（所有 gate 必须有 owner_layer；ownerless gate 禁止进入主链）  
- Article 3：No Self-Escalation（禁止自我扩权；capability/output/simulation/map-location 等不得升级授权）  
- Article 4：Candidate Is Not Fact（candidate 不得直写事实/记忆/库；必须走 admission gate）  
- Article 5：Simulation Does Not Grant Runtime（dryrun/closure 的 GO 不代表 runtime/production readiness）  
- Article 6：Final Release Gate Required（runtime/write/action/speech 必须有最终 release/admission gate）  
- Article 7：Auditability（gate 最小审计字段集必须成立）  
- Article 8：Conservative Failure Default（缺失/冲突/超时/证据不足等默认保守）  
- Article 9：Gate Dependency Declaration（必须声明依赖/效果/veto/override/failure/recovery）  
- Article 10：No Duplicate Gate Creation（限制平行新建 gate；必须复用评审与 risk register 登记）  
- Article 11：Layered Authority Boundary（分层边界：governance/midplatform/capability/runtime/evaluation）  
- Article 12：Human and Review Boundary（不假设人工确认；review 结果默认非事实）

**Non-claims**：

- 不实现 gate runtime
- 不改变现有 gate
- 不合并 gate
- 不开启真实文件链
- 不产生事实/行动/写入权限

## 结构化产物（概览）

`_eval_out/gate_taxonomy_and_requirement_framework_planning_v1_smoke_v0/`：

- `luna_gate_taxonomy_planning_policy.json`
- `gate_constitution.json`
- `gate_type_taxonomy.json`
- `gate_level_model.json`
- `gate_decision_vocabulary.json`
- `gate_requirement_framework.json`
- `gate_input_output_contract_template.json`
- `gate_authority_and_veto_policy.json`
- `gate_dependency_graph.json`
- `gate_failure_recovery_policy.json`
- `gate_audit_trace_requirement.json`
- `gate_verifier_requirement_template.json`
- `gate_consolidation_risk_register.json`
- `future_governance_handoff_plan.json`
- `no_runtime_boundary_report.json` / `no_write_boundary_report.json` / `no_action_boundary_report.json`
- `next_phase_recommendation.json`
- `verifier_report.json`

## 通过判定（概念级）

当 verifier=GO 时：

- `final_decision=GATE_TAXONOMY_AND_REQUIREMENT_FRAMEWORK_PLANNING_READY_FOR_MIDPLATFORM_FUNCTION_GOVERNANCE`
- `recommended_next_phase=Phase-MidPlatform-Function-Governance-and-Consolidation-Planning-v1-001`

