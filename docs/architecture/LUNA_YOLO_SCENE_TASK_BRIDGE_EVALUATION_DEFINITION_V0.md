# LUNA — YOLO Shadow SceneTask Bridge Evaluation Definition v0 (Phase-ModelPerception-007)

## 目标
本阶段只做 **离线 SceneTask bridge evaluation**：
- 输入：Phase-ModelPerception-006 产出的 YOLO perception replacement results
- 输出：离线生成 `scene_state` 与 `task_candidates`（候选-only）

**唯一目的**：验证 YOLO replacement perception results 能否在不越权、不扩能力的前提下进入 SceneTask 候选层，形成可复核的 `scene_state/task_candidate` 结构化产物。

## 严格边界（必须写死）
- 本阶段只是 SceneTask bridge evaluation（离线评测），不是正式下游接入
- 不进入 Fusion/Output
- 不执行导航动作、不真实播报
- 不进入 controlled_live_stream / full controlled trial
- 不扩 Option A
- 不开启默认路径、不扩大 side effects 面
- candidate-only：任何 task_candidate 必须 `allows_execute_now=false`
- YOLO 输出不得被解释为真实导航能力
- SceneContext gates 仍属治理要求，本阶段只做“标记/保守处理”，不宣称已 runtime 完整 enforce

## 输入
- YOLO replacement perception root：
  - `logs/yolo_perception_replacement_eval_option_a_phone_local_001_20260427_1513/`

## 输出
输出根：
- `logs/yolo_scene_task_bridge_eval_option_a_phone_local_001_<timestamp>/`

至少包含：
- `yolo_scene_task_bridge_summary.json`
- `per_sample_yolo_scene_task_results.json`
- `yolo_scene_task_bridge_trace.jsonl`
- `evaluation_notes.md`

## 停止条件
满足即停止（不要进入 Phase-ModelPerception-008）：
- definition 完成
- contract 完成
- evaluation tool 完成
- evaluation result 生成
- matrix 完成
- go/no-go pack 完成
- README 索引完成

