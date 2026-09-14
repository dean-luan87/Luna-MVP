# LUNA — YOLO Shadow PerceptionEval Replacement Trial Definition v0 (Phase-ModelPerception-006)

## 目标
本阶段只做 **offline replacement trial**：
- 不运行 `PerceptionEval-001` baseline/mock perception 生成器
- 使用已生成的 **YOLO enabled shadow adapter** 输出（Perception-001 五类 signals）作为替代输入
- 生成一份 replacement trial 的 PerceptionEval 形态结果与指标

**唯一目的**：验证“YOLO shadow perception outputs”在 PerceptionEval 层的**可替代性与边界完整性**，不进入下游决策链。

## 严格边界（必须写死）
- 本阶段是 offline replacement trial，不是正式替换
- YOLO 不进入真实 runtime 主链
- YOLO 不进入 SceneTask/Fusion/Output
- YOLO 不触发 execute/release/retry/reopen
- YOLO 不打开 default path
- YOLO 不扩大 side effects
- YOLO 不证明真实导航能力
- YOLO 不证明 depth/OCR/dynamic/collision risk 能力
- 本阶段只验证 PerceptionEval 层可替代性（schema/边界/工件/可复核）

## 输入
- FieldBatch sample_matrix：
  - `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`
- YOLO enabled shadow output root：
  - `logs/yolo_shadow_eval_option_a_phone_local_enabled_smoke_retry_fix002_20260427_1503/`

## 输出（replacement trial artifacts）
输出根：
- `logs/yolo_perception_replacement_eval_option_a_phone_local_001_<timestamp>/`

至少包含：
- `yolo_perception_replacement_summary.json`
- `per_sample_yolo_perception_replacement_results.json`
- `yolo_perception_replacement_trace.jsonl`
- `evaluation_notes.md`

## 每条样本必须记录（最小集合）
- sample_id / archive_root / source_video_path
- yolo_invoked / fallback_used / detection_count / detected_classes
- perception_runtime_mode=`yolo_shadow_replacement`
- 5 类 signal presence（present flags）
- ocr_status=`not_available`
- dynamic_status=`not_available`
- depth_unavailable=true
- collision_risk_not_confirmed=true
- allows_execute_now=false
- execute/default_on/release_retry_reopen/side_effects leakage counters = 0
- evidence_type_preserved / controlled_live_stream_false / phone_local_capture_true
- reason_codes / hard_blockers / soft_followups

## 停止条件
满足即停止（不要进入 Phase-ModelPerception-007）：
- definition 完成
- contract 完成
- evaluation tool 完成
- replacement result 生成
- matrix 完成
- go/no-go pack 完成
- README 索引完成

