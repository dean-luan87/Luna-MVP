## Phase

- **Phase ID**: `Phase-Luna-Project-Structure-Governance-and-Modularization-Planning-v1-001`
- **Capability module**: `capabilities/governance/luna_project_structure_governance_and_modularization_planning_v1.py`
- **Status**: planning-only

## Intent

这不是普通 refactor，也不是代码搬家。本阶段的目标是把 Luna 从“阶段产物堆叠”提升为“长期工程体系”，以 **项目结构治理** 的视角完成一次全局盘点与模块化规划：

- **全项目结构盘点**：仅做目录层级与数量级审计（非事实、非证明）。
- **模块归类与边界重画（规划）**：给出目标结构模型与模块域分类。
- **版本与变更治理（规划）**：提出模块级版本/变更日志/接口契约/非主张的统一要求。
- **文档重组（规划）**：把 architecture / phase records / module specs / evaluation 索引结构化。
- **Developer Backend 抽离（规划）**：明确白盒、测试中心、仿真、评测与仪表盘不进入 client runtime。
- **中台器官化（规划）**：给出 midplatform 子系统器官模型与后续治理路径。
- **未来模块占位**：WorldModel/Memory/Library/Emotion/Hardware 等仅做占位，不做实现与启用。

## Hard Boundaries (Non-Negotiable)

本阶段必须满足 **planning-only**，并严格遵守以下硬边界（任何违反均应 NO-GO）：

- **No runtime**：不启用任何运行时能力（相机、视觉模型、OCR、跟踪、跨越执行、导航动作等）。
- **No real file ops for user media**：不打开/读取用户媒体文件，不做 EXIF/视频探测/哈希计算。
- **No persistent writes**：不得写入 `WorldModel/Memory/Fact/Library` 等持久层。
- **No destructive changes**：不得移动/重命名/删除生产代码与文档；仅允许在 `_eval_out` 输出结构化规划产物。

## Inputs (Upstream)

该 phase 的 runner 会加载上游 smoke 产物（主要用于“链路一致性校验”，不把内容当作事实）：

- `gate_taxonomy_and_requirement_framework_planning_v1_smoke_v0`
- `post_file_stat_roadmap_decision_v1_smoke_v0`
- `controlled_frame_file_stat_guarded_closure_v1_smoke_v0`
- `controlled_frame_file_existence_check_guarded_closure_v1_smoke_v0`
- `controlled_frame_file_metadata_boundary_closure_v1_smoke_v0`
- `controlled_frame_sample_closure_v1_smoke_v0`
- `controlled_frame_input_closure_v1_smoke_v0`
- `crossing_decision_closure_v1_smoke_v0`
- `luna_safety_constitution_policy_v1_smoke_v0`

## Outputs (Artifacts)

所有输出均为 **规划对象**（`fact_status=not_fact`），并落在：

- `_eval_out/luna_project_structure_governance_and_modularization_planning_v1_smoke_v0/`

关键产物（JSON）：

- `summary.json`
- `input_root_matrix.json`
- `luna_project_structure_governance_planning_policy.json`
- `current_project_structure_audit.json`
- `target_project_structure_model.json`
- `module_domain_taxonomy.json`
- `module_versioning_and_changelog_policy.json`
- `document_reorganization_policy.json`
- `midplatform_organ_system_model.json`
- `developer_backend_extraction_plan.json`
- `hardware_management_consolidation_plan.json`
- `future_module_placeholder_plan.json`
- `module_consolidation_candidate_register.json`
- `client_boundary_policy.json`
- `project_governance_debt_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `no_action_boundary_report.json`
- `no_file_operation_boundary_report.json`
- `verifier_report.json`

## Final Decision Contract

当且仅当上游输入齐全且边界无违反时，本阶段允许输出：

- **`final_decision`**: `LUNA_PROJECT_STRUCTURE_GOVERNANCE_AND_MODULARIZATION_PLANNING_READY_FOR_STRUCTURE_MAP_DRYRUN`
- **`recommended_next_phase`**: `Phase-Luna-Project-Module-Inventory-and-Structure-Map-DryRun-v1-001`

## Non-Claims

- 不声称已经完成任何实际模块拆分、文件迁移、接口重构或行为变更。
- 不声称当前审计统计能作为真实资产清单或准确度量（仅用于 planning 信号）。
- 不声称任何 runtime 能力已经被批准或启用。

