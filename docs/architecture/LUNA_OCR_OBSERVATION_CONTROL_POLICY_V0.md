# LUNA OCR Observation Control Policy v0

## Phase

- Phase-ModelOCR-001（OCR Independent Capability Definition v0）

## Goal

定义 OCR 的观察控制方案（只定义，不实现 runtime），确保：

- OCR 作为独立感知能力可离线评测
- 支持多种观测模式（全帧低频/区域聚焦/task_hint 引导）
- 具备禁用与 fallback/not_available（fail-closed）
- task_hint/scene_hint 仅作提示，不得强制控制结论

## Observation modes (v0 definitions)

### 1) `full_frame_low_frequency`

低频全帧 OCR，用于探索与异常发现。

建议控制参数：

- `frame_sample_rate`（例如每 N 帧采样）
- `max_frames`
- `confidence_threshold`
- `emit_low_confidence`
- `language_hint`

### 2) `region_focused`

对指定区域进行 OCR（未来区域可能来自 YOLO 或中台 observation plan）。

本阶段仅定义接口，不接 YOLO：

- `crop_regions`: `[[x1,y1,x2,y2], ...]`
- `source_region_type`: `crop|sign_region|doorplate_region|screen_region|unknown`
- `allow_full_frame_fallback`: true/false（区域失败时是否允许回退全帧低频）

### 3) `task_hint_guided`

根据 `task_hint` 提高相关文字优先级（例如门牌/出口/科室/站台方向），但：

- 不得强行过滤掉其它安全相关信息
- 不得把 task_hint 变成“指令注入”通道

建议控制参数：

- `task_hint`（可选字符串或结构化提示）
- `boost_text_type_candidates`（仅影响排序/标注，不影响允许输出的类别集合）

## Control parameters (recommended v0)

建议配置字段（后续实现阶段映射到 adapter）：

- `ocr_mode`（三种模式之一）
- `frame_sample_rate`
- `max_frames`
- `crop_regions`
- `language_hint`
- `task_hint`
- `scene_hint`
- `confidence_threshold`
- `emit_low_confidence`
- `allow_full_frame_fallback`
- `disable_ocr`
- `ocr_config_id`

## Fail-closed rules

- `disable_ocr=true` → 必须输出 `signal_status=not_available`
- 任意依赖/模型不可用/输入解码失败/违规语义 → `not_available`（不得伪造可用）
- 任何禁止 token/语义（见 I/O contract）→ block + `not_available`

## Anti-false-positive considerations (definition-only)

OCR 必须显式保留“视觉介质风险”候选字段（非结论）：

- `visual_medium_risk`: none|poster|screen|advertisement|reflection|unknown

并在 `unsupported_or_uncertain` 中默认保守：

- `advertisement_filter_not_confirmed=true`
- `visual_medium_not_confirmed=true`

说明：本阶段仅定义字段与保守默认，不实现分类器/过滤器。

