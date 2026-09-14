# Luna 评测 — OCR Mainline Final Closure v1

**Phase**：`Phase-OCR-Mainline-Final-Closure-v1-001`  
**类型**：closure / consolidation / handoff only  
**目标**：在**不**运行 OCR、**不**接真实 provider、**不**写事实层的前提下，对 OCR 主线做最终收口并正式交回视角强化主线。

## 评测目标

本评测回答以下问题：

1. OCR 主线当前完成到什么程度  
2. 哪些能力已经通过 policy / dry-run / reference / gated / readonly / regression 验证  
3. 哪些能力仍停留在 candidate / reference-only / no-fact  
4. OCR 是否具备支撑未来视觉主线的辅助边界  
5. OCR 是否允许继续扩展  
6. OCR 是否允许真实 provider runtime  
7. OCR 是否允许写 `WorldModel` / `Memory` / `Fact`  
8. OCR 与 `Static Reading` / `Poster` / `RealVideo` / `Minimal Runtime Integration` 的关系是否清楚  
9. 主线是否可以回到视角强化  
10. 下一阶段应否进入 `Phase-Return-To-Vision-Mainline-Planning-v1-001`

## 输入根

优先加载以下产物；存在则 `loaded`，不存在则 `optional_missing`，**不得伪造**：

- `_eval_out/ocr_staticreading_poster_realvideo_regression_route_compliance_v1_smoke_v0/`
- `_eval_out/roi_to_ocrrequest_reference_v1_smoke_v0/`
- `_eval_out/ocr_evidence_pack_adapter_v1_scan_observation_alignment_v0/`
- `_eval_out/mixed_video_poster_batch_smoke_v2_gated_path_only_v0/`
- `_eval_out/realvideo_ocr_text_bearing_sample_planning_smoke_v0/`
- `_eval_out/static_readable_region_discovery_guidance_policy_v1_smoke_v0/`
- `_eval_out/worldmodel_lookup_for_reading_framework_v1_smoke_v0/`
- `_eval_out/minimal_runtime_integration_closure_v1_smoke_v0/`

如存在，也加载：

- `_eval_out/roi_crop_execution_dryrun_v1_rerun_better_frames_smoke_v0/`
- `_eval_out/roi_bbox_expansion_proposal_v1_smoke_v0/`
- `_eval_out/better_frame_extraction_dryrun_v1_smoke_v0/`
- `_eval_out/bbox_adjustment_proposal_v2_multiframe_smoke_v0/`
- `_eval_out/hardware_camera_control_contract_v1_smoke_v0/`
- `_eval_out/voice_interruption_governance_dryrun_v1_smoke_v0/`
- `_eval_out/basic_navigation_guidance_loop_stabilization_test_v1_smoke_v0/`

文档输入同样按 `loaded / optional_missing` 处理；其中以下两项为收口硬依赖：

- `docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md`
- `_eval_out/minimal_runtime_integration_closure_v1_smoke_v0/summary.json`

## 输出目录

Runner 输出目录：

- `_eval_out/ocr_mainline_final_closure_v1_smoke_v0/`

必须包含：

- `summary.json`
- `input_root_matrix.json`
- `ocr_mainline_final_closure_report.json`
- `ocr_completed_phase_matrix.json`
- `ocr_validated_capability_summary.json`
- `ocr_runtime_disabled_summary.json`
- `ocr_non_claims_register.json`
- `deferred_ocr_capability_pool.json`
- `ocr_to_vision_handoff_plan.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## 核心检查点

### 输入

- `minimal_runtime_integration_closure_loaded=true`
- `ocr_phase_verdict_table_loaded=true`
- `loaded_phase_count >= 5`

### 收口对象

- `ocr_completed_phase_matrix_generated=true`
- `ocr_validated_capability_summary_generated=true`
- `ocr_runtime_disabled_summary_generated=true`
- `ocr_non_claims_register_generated=true`
- `deferred_ocr_capability_pool_generated=true`
- `ocr_to_vision_handoff_plan_generated=true`

### OCR 边界

- `ocr_runtime_allowed=false`
- `ocr_provider_allowed=false`
- `ocrrequest_submission_allowed=false`
- `fact_write_allowed=false`
- `worldmodel_write_allowed=false`
- `memory_write_allowed=false`
- `scene_delta_allowed=false`
- `new_runtime_enabled=false`
- `full_frame_ocr_default_forbidden=true`
- `direct_provider_bypass_forbidden=true`
- `scan_observation_not_text_evidence=true`
- `evidence_pack_not_fact=true`
- `semantic_candidate_not_fact=true`

### 禁用项

- `ocr_runtime_invoked=false`
- `ocr_provider_invoked=false`
- `ocrrequest_submitted=false`
- `paddleocr_invoked=false`
- `rapidocr_invoked=false`
- `deepseek_ocr_invoked=false`
- `camera_invoked=false`
- `frame_sampled=false`
- `new_crop_generated=false`
- `detector_invoked=false`
- `segmentation_invoked=false`
- `tracking_invoked=false`
- `benchmark_accuracy_updated=false`
- `world_model_written=false`
- `memory_written=false`
- `fact_written=false`
- `scene_delta_generated=false`
- `navigation_action_triggered=false`
- `task_state_committed_now=false`
- `map_api_invoked=false`
- `boundary_ok=true`
- `violations=[]`

### Non-claims

必须显式声明：

- OCR closure 不等于 production OCR runtime
- OCRRequest reference 不等于 submitted request
- Evidence Pack candidate 不等于 fact
- semantic candidate 不等于 `WorldModel` write
- readable region candidate 不等于 detected text fact
- static reading handoff 不等于 camera capture
- RealVideo planning 不等于 benchmark
- 不发生 `Memory` / `WorldModel` / `Fact` write

### Handoff

必须存在 OCR → Vision handoff，且包含：

- viewpoint segmentation / view slicing
- object tracking
- visual candidate stabilization
- map / route / location context integration
- basic navigation loop strengthening

并且**不得**把以下内容推荐为下一阶段：

- OCR provider runtime
- OCR benchmark execution
- `Memory` / `WorldModel` write
- map API

## Verifier

- `tools/evaluation/ocr/verify_ocr_mainline_final_closure_v1.py`
- 实际检查数：`331`
- 最低目标：`100`
- baseline requirement：`80`

## 最终判定

通过时必须输出：

- `verifier=GO`
- `closure_verdict=GO`
- `final_decision=OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE`
- `next_phase_recommendation=Phase-Return-To-Vision-Mainline-Planning-v1-001`

## 结论口径

本阶段只允许把 OCR 主线表述为：

> 已完成到 governance / gated / reference / candidate / readonly / no-write baseline，可作为未来视觉主线的辅助证据层，但**不**等于生产 OCR runtime，**不**等于 OCR provider 已启用，**不**等于事实层写入已开启。
