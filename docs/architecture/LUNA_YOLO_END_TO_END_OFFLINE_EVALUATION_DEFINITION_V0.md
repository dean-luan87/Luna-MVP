# LUNA — YOLO Shadow End-to-End Offline Evaluation Definition v0 (Phase-ModelPerception-010)

## 目标
本阶段只做 **YOLO shadow 端到端离线机制验收**：

phone_local archive  
→ YOLO shadow perception replacement  
→ YOLO SceneTask bridge  
→ YOLO Fusion bridge  
→ YOLO Output bridge  

**唯一目的**：复核整条 YOLO shadow 候选链路在离线条件下是否闭合、可追溯、candidate-only、no-real-TTS、零泄漏、证据边界保持。

## 严格边界（必须写死）
- offline only；不是 live run
- 不执行导航动作
- 不真实播报
- 不进入 controlled_live_stream / full controlled trial
- 不扩 Option A
- 不开启默认路径、不扩大 side effects 面
- 不得关闭 `pending_real_sidewalk_run`
- 不得改写 `evidence_type`
- YOLO shadow 仍不得进入真实 runtime
- 不得声称真实导航能力已验证

## 输入（本次验收使用）
- FieldBatch root：
  - `logs/phone_local_field_batch_002_20260427_111431/`
- YOLO perception replacement root：
  - `logs/yolo_perception_replacement_eval_option_a_phone_local_001_20260427_1558/`
- YOLO SceneTask bridge root：
  - `logs/yolo_scene_task_bridge_eval_option_a_phone_local_001_20260427_1558/`
- YOLO Fusion bridge root：
  - `logs/yolo_fusion_bridge_eval_option_a_phone_local_001_20260427_1558/`
- YOLO Output bridge root：
  - `logs/yolo_output_bridge_eval_option_a_phone_local_001_20260427_1558/`

## 输出
输出根：
- `logs/yolo_e2e_offline_eval_option_a_phone_local_001_<timestamp>/`

至少包含：
- `yolo_e2e_offline_evaluation_summary.json`
- `per_sample_yolo_chain_results.json`
- `yolo_chain_trace_consistency.json`
- `evaluation_notes.md`

## 停止条件
满足即停止（不要进入 Phase-ModelPerception-011）：
- definition 完成
- eval contract 完成
- evaluation tool 完成
- evaluation result 生成
- matrix 完成
- go/no-go pack 完成
- README 索引完成

