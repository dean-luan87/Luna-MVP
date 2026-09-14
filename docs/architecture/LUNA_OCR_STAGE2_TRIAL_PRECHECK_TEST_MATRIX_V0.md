# LUNA — OCR Stage-2 Dry-run Precheck Test Matrix v0

## Phase

- **Phase-Mainline-GuardedTrial-008**

## Test matrix（precheck only）

### A. YOLO closure gate

- 输入 `--yolo-closure-root` 可读
- `yolo_stage1_offline_trial_status == closed_v0`

### B. Source policy readiness

- `capabilities/model_ocr/offline_source_policy_v0.py` 可 import
- `source_policy_id` 匹配 `ocr_default_offline_raw_text_source_policy_v0`

### C. Provider readiness static

- `configs/models/ocr/*_manifest_v0.json` 存在且可解析
- 不触发任何 provider 推理/联网

### D. Raw text candidate schema

- schema 合同非空、字段齐全

### E. Output paths

- output_root 可写
- RequestTrace dir 可写
- trace/replay/whitebox dir 可写
- trace/replay/whitebox 文件非空

### F. Governance boundaries

- provider_invoked=false
- semantic_interpretation_enabled=false
- midplatform/scene_delta/world_context=false
- qwen/tts/playback/nav/world_write/hive_upload 全 false

