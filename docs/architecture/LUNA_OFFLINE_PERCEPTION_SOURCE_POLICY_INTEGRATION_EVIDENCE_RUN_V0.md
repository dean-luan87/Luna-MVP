# LUNA — Offline Perception Source Policy Integration Evidence Run v0 (Phase-EngineeringFlow-002-Fix)

## 目的
补齐 EF-002 的“PerceptionEval 集成运行证据”，覆盖 H/I/J：
- H：YOLO 输出合同校验（五类 signal schema 完整）
- I：forbidden scan / safety boundary 成立（无 execute/no-real-TTS/无 default-on 泄漏）
- J：审计字段在真实产物中齐全，且 fallback path 可产出

## 输入
- sample_matrix（FieldBatch-002）：`logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`
- yolo manifest：`configs/models/yolo/yolo_model_manifest_v0.json`
- source policy：`yolo_default_offline_perception_source_v0`

## Evidence Run #1 — YOLO selected path（disable_yolo=false）
### Command（实际）
```bash
python3 tools/evaluate_option_a_phone_local_perception_v0.py \
  --sample-matrix logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json \
  --output-root logs/perception_eval_yolo_default_source_policy_ef002_20260428_102332 \
  --source-policy yolo_default_offline_perception_source_v0 \
  --offline-evaluation true \
  --disable-yolo false \
  --yolo-manifest configs/models/yolo/yolo_model_manifest_v0.json
```

### output_root
- `logs/perception_eval_yolo_default_source_policy_ef002_20260428_102332`

### Key summary assertions（来自 summary.json）
- yolo_selected_rate=1.0
- yolo_invoked_rate=1.0
- signal_completeness 五类=1.0
- safety leakage=0
- evidence boundary rates=1.0

## Evidence Run #2 — Fallback path（disable_yolo=true）
### Command（实际）
```bash
python3 tools/evaluate_option_a_phone_local_perception_v0.py \
  --sample-matrix logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json \
  --output-root logs/perception_eval_yolo_default_source_policy_fallback_ef002_20260428_102332 \
  --source-policy yolo_default_offline_perception_source_v0 \
  --offline-evaluation true \
  --disable-yolo true \
  --yolo-manifest configs/models/yolo/yolo_model_manifest_v0.json
```

### output_root
- `logs/perception_eval_yolo_default_source_policy_fallback_ef002_20260428_102332`

### Key summary assertions（来自 summary.json）
- baseline_fallback_rate=1.0
- fallback_reason_present_rate=1.0
- yolo_invoked_rate=0.0
- signal_completeness 五类=1.0
- safety leakage=0
- evidence boundary rates=1.0

## 边界声明
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- 本阶段只补 PerceptionEval source policy integration evidence，不进入下游

