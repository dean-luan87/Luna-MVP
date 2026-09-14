# LUNA — Offline SceneContext Gates Implementation v0 (Phase-EngineeringFlow-003)

## 目标（本阶段唯一目标）
把 SceneContext-001/002/003 中定义的三道防线，落成 **offline evaluation 内可执行的最小 gate**：
- Visual Medium / Depicted Scene Filter
- Physics-Aware Perception Consistency
- Scene Continuity / Zone Reasoning

输出只包含：
- `scene_context_gate_result`（结构化 gate 输出）
- `gated_perception_result`（候选态 perception 透传/门控结果）
- trace/summary/per-sample 产物

## 严格边界（确认）
- 只在 offline evaluation 运行，不进入真实 runtime
- 不产生 task_candidate / fusion_candidate / output_candidate
- candidate-only；`allows_execute_now=false`；`real_tts_invoked=false`
- 不改变 `evidence_type`
- 不关闭 `pending_real_sidewalk_run`
- depicted/ad/screen/poster 等不得触发 macro_scene 迁移或 task 触发
- depth/motion 不可用时必须保守：不确认 passable / collision risk

## 实现位置
- gates runtime：`capabilities/scene_context/offline_scene_context_gates_v0.py`
  - `visual_medium_gate_v0`
  - `physics_consistency_gate_v0`
  - `scene_continuity_zone_gate_v0`
  - `run_offline_scene_context_gates_v0`
- 评测工具：`tools/evaluate_offline_scene_context_gates_v0.py`
- 验证工具：`tools/verify_offline_scene_context_gates_v0.py`

## v0 最小行为说明
### Visual Medium Gate v0
- 默认：`visual_medium_detected=false`（未接 OCR/medium detector）
- 支持测试 hint：若提供 `scene_context_test_hint.visual_medium_type`（screen/poster/ad/photo/...）：
  - `depicted_scene_blocked=true`
  - `task_trigger_allowed=false`
  - `macro_scene_transition_allowed=false`

### Physics Gate v0
- 固定保守输出：
  - `depth_status=not_available`
  - `motion_status=not_available`
  - `collision_risk_status=not_confirmed`
  - `physical_plausibility=uncertain`

### Continuity/Zone Gate v0
- 只输出 candidate，不确认：
  - `macro_scene_confirmed=false`
  - `macro_scene_candidate`（phone_local 兼容时给 `outdoor_sidewalk`，否则 unknown）
  - `zone_type_candidate`（兼容时 `sidewalk_path`）
- depicted_scene 被标记时：
  - `macro_scene_transition_state=blocked`
- `degraded_or_uncertain=true`（v0 保守默认）

## Evidence run（本次）
- 输入 PerceptionEval output_root：
  - `logs/perception_eval_yolo_default_source_policy_ef002_20260428_102332`
- 评测输出：
  - `logs/scene_context_gates_offline_ef003_20260428_103623`
- verifier 输出：
  - `logs/offline_scene_context_gates_verify_002_20260428_1038.json`

