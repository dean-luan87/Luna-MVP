# LUNA — Offline Mainline Runner Implementation v0 (Phase-EngineeringFlow-004)

## 目标（本阶段唯一目标）
实现一键离线主链 runner，把已通过的离线模块串成可复现的工程链：

FieldBatch `sample_matrix`  
→ PerceptionEval（source policy：YOLO pinned_local / fallback baseline）  
→ SceneContext gates（offline minimal runtime v0）  
→ SceneTask（offline minimal candidate v0）  
→ Fusion（offline minimal candidate v0）  
→ Output candidate（offline minimal v0；no-real-TTS）  
→ unified summary / trace / replay / whitebox index

## 严格边界（确认）
- 只运行 offline evaluation，不进入 controlled_live_stream，不进入真实 runtime
- 不执行导航动作，不真实播报
- 不关闭 `pending_real_sidewalk_run`；不改 `evidence_type`
- 全链路 candidate-only；`allows_execute_now=false`；`real_tts_invoked=false`
- 任一阶段失败必须 fail-closed（记录 hard_blockers，保持保守输出，不伪造执行成功）

## 实现与入口
- runner core：`capabilities/offline_mainline/offline_mainline_runner_v0.py`
- CLI：`tools/run_offline_mainline_v0.py`
- verifier：`tools/verify_offline_mainline_runner_v0.py`

## 产物目录结构（输出）
`logs/offline_mainline_<timestamp>/`
- `mainline_summary.json`
- `per_sample_mainline_results.json`
- `mainline_trace.jsonl`
- `mainline_replay_index.json`
- `mainline_whitebox_index.json`
- `stage_outputs/`
  - `perception/`（PerceptionEval 原始产物）
  - `scene_context/`（gates 产物）
  - `scene_task/`（每 sample 一个 json）
  - `fusion/`（每 sample 一个 json）
  - `output/`（每 sample 一个 json）
- `evaluation_notes.md`

## 复用关系（不复制大量逻辑）
- PerceptionEval：复用 `tools/evaluate_option_a_phone_local_perception_v0.py`
- SceneContext gates：复用 `tools/evaluate_offline_scene_context_gates_v0.py`
- Fusion / Output：复用既有工具中的映射/选择 helper（仅 import helper，不进入其 runtime）

## Evidence runs（本次）
- normal（disable_yolo=false）：
  - `logs/offline_mainline_ef004_20260428_105303`
- fallback（disable_yolo=true）：
  - `logs/offline_mainline_ef004_fallback_20260428_105303`
- verifier report：
  - `logs/offline_mainline_runner_verify_001_20260428_1058.json`

