# LUNA — YOLO Shadow Output Bridge Evaluation Definition v0 (Phase-ModelPerception-009)

## 目标
本阶段只做 **离线 Output bridge evaluation**：
- 输入：Phase-ModelPerception-008 的 `fusion_decision_candidate`
- 输出：离线生成 `navigation_output_candidate`（候选-only）

**唯一目的**：验证 YOLO-driven Fusion candidates 能否在不触发真实 TTS/真实输出 runtime 的前提下生成合规的 output 候选（含 timing/priority/suppression），并保留 source attribution 与边界/安全约束。

## 严格边界（必须写死）
- 本阶段只是 Output bridge evaluation（离线评测），不是正式输出 runtime 接入
- 不触发真实 TTS（`real_tts_invoked=false`）
- 不执行导航动作、不真实播报
- 不进入 controlled_live_stream / full controlled trial
- 不扩 Option A
- candidate-only：`allows_execute_now=false`
- 不证明真实导航能力
- 不宣称真实输出策略能力已验证（v0 仅最小规则）

## 输入
- YOLO Fusion bridge root：
  - `logs/yolo_fusion_bridge_eval_option_a_phone_local_001_20260427_1531/`

## 输出
输出根：
- `logs/yolo_output_bridge_eval_option_a_phone_local_001_<timestamp>/`

至少包含：
- `yolo_output_bridge_summary.json`
- `per_sample_yolo_output_results.json`
- `yolo_output_bridge_trace.jsonl`
- `evaluation_notes.md`

## 停止条件
满足即停止（不要进入 Phase-ModelPerception-010）：
- definition 完成
- contract 完成
- evaluation tool 完成
- evaluation result 生成
- matrix 完成
- go/no-go pack 完成
- README 索引完成

