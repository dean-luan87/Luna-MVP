# LUNA — OCR Stage-2 Source Policy & Provider Readiness (Static) v0

## Phase

- **Phase-Mainline-GuardedTrial-008**

## Source policy（only）

OCR Stage-2 仅允许引用 **离线 raw_text source policy**：

- `docs/architecture/LUNA_OCR_DEFAULT_OFFLINE_SOURCE_POLICY_V0.md`
- selector 实现：`capabilities/model_ocr/offline_source_policy_v0.py`

要求：

- `source_policy_id = ocr_default_offline_raw_text_source_policy_v0`
- `semantic_interpretation_enabled=false`
- `downstream_invocation_allowed=false`
- `real_tts_allowed=false`
- `controlled_live_stream=false`

## Provider readiness（static only）

本阶段 readiness 只做 **静态检查**：

- `configs/models/ocr/*_manifest_v0.json` 存在且可解析
- manifest 至少包含一个可识别的 id（`provider_id`/`model_id`/`id`/`name`）

禁止：

- import/执行任何真实 provider SDK 进行推理或联网
- 读取实时 camera 或在线 runtime

