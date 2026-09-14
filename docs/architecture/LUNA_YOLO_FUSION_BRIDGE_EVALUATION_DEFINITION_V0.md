# LUNA — YOLO Shadow Fusion Bridge Evaluation Definition v0 (Phase-ModelPerception-008)

## 目标
本阶段只做 **离线 Fusion bridge evaluation**：
- 输入：Phase-ModelPerception-007 的 `scene_state` / `task_candidates`
- 输出：离线生成 `fusion_decision_candidate`（候选-only）

**唯一目的**：验证 YOLO-driven SceneTask outputs 能否在不进入真实 Output runtime 的前提下进入 Fusion 候选层，生成可复核的 `fusion_decision_candidate`，并保持边界/安全/证据语义。

## 严格边界（必须写死）
- 本阶段只是 Fusion bridge evaluation（离线评测），不是正式下游接入
- 不进入真实 Output runtime
- 不执行导航动作、不真实播报
- 不进入 controlled_live_stream / full controlled trial
- 不扩 Option A
- candidate-only：fusion candidate 必须 `allows_execute_now=false`
- 不证明真实导航能力
- 不宣称真实融合能力已验证（规则仍为最小 v0）

## 输入
- YOLO SceneTask bridge root：
  - `logs/yolo_scene_task_bridge_eval_option_a_phone_local_001_20260427_1522/`

## 输出
输出根：
- `logs/yolo_fusion_bridge_eval_option_a_phone_local_001_<timestamp>/`

至少包含：
- `yolo_fusion_bridge_summary.json`
- `per_sample_yolo_fusion_results.json`
- `yolo_fusion_bridge_trace.jsonl`
- `evaluation_notes.md`

## 停止条件
满足即停止（不要进入 Phase-ModelPerception-009）：
- definition 完成
- contract 完成
- evaluation tool 完成
- evaluation result 生成
- matrix 完成
- go/no-go pack 完成
- README 索引完成

