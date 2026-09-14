# Luna — GO / NO_GO Pack: Return To Vision Mainline Planning v1

## GO 条件

- `preplan_input_loaded=true`
- `ocr_final_closure_loaded=true`
- `minimal_runtime_integration_closure_loaded=true`
- `formal_mainline_name=Task-Aware Perception Orchestration`
- `planning_report_generated=true`
- `roadmap_generated=true`
- `adopted_preplan_principles_generated=true`
- `rejected_patterns_register_generated=true`
- `midplatform_reuse_commitment_generated=true`
- `duplicate_module_ban_list_generated=true`
- `governance_boundary_matrix_generated=true`
- `first_batch_phase_definitions_generated=true`
- `deferred_capability_register_generated=true`
- `deferred_worldmodel_memory_library_boundary_generated=true`
- `worldmodel_memory_library_placeholder_plan_generated=true`
- `non_claims_register_generated=true`
- `formal_readiness_gate_generated=true`
- `entity_resolution_deferred=true`
- `fact_admission_deferred=true`
- `memory_consolidation_deferred=true`
- `library_experience_governance_deferred=true`
- `worldmodel_handoff_candidate_allowed=true`
- `memory_handoff_candidate_allowed=true`
- `library_handoff_placeholder_allowed=true`
- `no_runtime_executed=true`
- `no_new_capability_implemented=true`
- `world_model_written=false`
- `memory_written=false`
- `library_write_allowed=false`
- `fact_written=false`
- `entity_fusion_runtime_allowed=false`
- `fact_admission_runtime_allowed=false`
- `handoff_candidate_not_fact=true`
- `placeholder_not_runtime=true`
- `boundary_ok=true`
- `final_decision=RETURN_TO_VISION_MAINLINE_PLANNING_READY_FOR_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY`
- `recommended_next_phase=Phase-MidPlatform-Perception-Orchestration-Policy-v1-001`

## NO_GO 条件

- 未加载 `preplan`
- 未加载 `OCR final closure`
- 未加载 `Minimal Runtime Integration closure`
- 建议直接进入 runtime
- 建议 `full-scene tracking`
- 建议 `full-frame OCR`
- 建议直接接地图 API
- 建议直接写 `WorldModel / Memory / Fact`
- 建议在视觉主线内执行 `Entity Resolution / Fact Admission / Memory Consolidation / Library Experience Commit`
- 建议新建重复 `STC / TTL / Evidence / Memory / Task / Speech / runtime framework`
- 未冻结下一阶段

## 判定语义

### GO

说明视觉主线已经从 preplan 进入正式 planning freeze，下一阶段应切入：

- `Phase-MidPlatform-Perception-Orchestration-Policy-v1-001`

### NO_GO

说明当前仍停留在 planning review，必须先补齐缺失输入、复用承诺、禁建清单、边界矩阵或第一批 phase 定义。

## 明确边界

即使 `GO`，本阶段也 **不等于**：

- 视觉 runtime 已启用
- OCR provider 已接入
- tracking runtime 已启用
- camera 已接入
- map API 已接入
- `WorldModel / Memory / Fact` 可写
- `Library` 经验治理已生效
- `Entity Resolution / Fact Admission / Memory Consolidation` 已在视觉主线内启用
- navigation action 可触发

本阶段 `GO` 只表示：

- 视觉主线正式回归
- 主线原则已冻结
- 工程路线图已冻结
- 下一刀应切中台 policy，而不是视觉算法 runtime
