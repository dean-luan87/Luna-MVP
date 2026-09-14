## Phase-ModelOCR-003

OCR Model Manifest Schema v0

### 0. 目标

冻结 OCR model manifest 的最小 schema，用于“可追踪、可校验、可回退”的候选资产管理。

### 1. schema 版本

- `manifest_version`: `"v0"`（变更需升级版本）

### 2. 顶层字段（最小集合，v0）

- **manifest_version**: `string`
- **model_config_id**: `string`
- **model_family**: `string`
- **model_name**: `string`
- **model_variant**: `string`
- **model_task**: `string`（固定：`ocr_raw_text_candidates`）
- **candidate_tier**: `string`
  - `lightweight_navigation_ocr`
  - `complex_layout_ocr`
  - `system_fallback`
  - `comparison_only`
- **provider_kind**: `string`
  - `local_model`
  - `system_provider`
  - `online_or_service`
  - `unavailable`
- **weights_source**: `string`
  - `pinned_local`
  - `system_builtin`
  - `manual_download_required`
  - `unavailable`

### 3. 权重字段（v0）

- **weights_paths**: `object`
  - `det_model_path`: `string|null`
  - `rec_model_path`: `string|null`
  - `cls_model_path`: `string|null`
  - `tokenizer_path`: `string|null`
  - `other_assets`: `array[string]`
- **weights_sha256**: `object`（key=weights_paths 的 key；value=sha256；仅当文件存在时填写）
- **weights_file_size_bytes**: `object`（key=weights_paths 的 key；value=size；仅当文件存在时填写）

约束：

- 路径不存在时 **不得伪造** sha256/size
- `weights_source=pinned_local` 时，readiness 必须要求路径存在且 hash/size 可验证

### 4. 依赖与环境快照（v0）

- `dependency_profile_id`: `string|null`
- `python_version`: `string|null`
- `paddleocr_version`: `string|null`
- `paddlepaddle_version`: `string|null`
- `opencv_version`: `string|null`
- `numpy_version`: `string|null`
- `pillow_version`: `string|null`
- `platform`: `string|null`

### 5. 能力声明（v0）

- `supported_languages`: `array[string]`
- `supports_chinese`: `bool|\"unknown\"`
- `supports_english`: `bool|\"unknown\"`
- `supports_digits`: `bool|\"unknown\"`
- `supports_bbox`: `bool|\"unknown\"`
- `supports_confidence`: `bool|\"unknown\"`
- `supports_orientation`: `bool|\"unknown\"`
- `supports_layout`: `bool|\"unknown\"`
- `supports_video_frame_input`: `bool`
- `expected_input_format`: `string`
- `expected_output_format`: `string`

### 6. 禁止项与硬边界（必须）

以下字段必须在 manifest 中显式声明并受 readiness 检查：

- `raw_text_only=true`
- `semantic_interpretation_enabled=false`
- `allows_execute_now=false`
- `real_tts_invoked=false`

### 7. 审计字段（v0）

- `created_at`: `string|null`（ISO8601）
- `verified_at`: `string|null`（ISO8601）
- `verification_status`: `string`（`pass|partial|fail|pending`）
- `fallback_policy`: `object`
- `risks`: `array[string]`
- `notes`: `string`

