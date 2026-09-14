# LUNA — OCR Module Runtime Governance Standard v0

## Phase

- **Phase-ModelOCR-Governance-001**
- 本阶段只定义治理标准，不实现 OCR runtime，不启用默认 provider chain。

## Scope

适用于所有 OCR provider：
- `rapidocr_onnxruntime_v0`
- `paddleocr_ppocrv5_lightweight_v0`
- `macos_vision_ocr_system_v0`
- 后续 `paddleocr_vl` / `deepseek_ocr` / 其他 provider

## Ownership boundary（归属边界）

本标准采用“**模块产出，中台收口**”：

- **OCR 模块侧负责：**
  - OCR-specific health metrics 原始字段
  - OCR-specific failure/degradation 原始分类
  - OCR-specific fallback 原始记录
  - OCR-specific trace/replay/whitebox 事件字段
- **中台监控层负责：**
  - 统一接收与归一化
  - 跨能力统计、告警、报表
  - 回归对比与 gate 判定
  - 统一健康状态与运行结论

OCR 指标是统一能力监控体系的一个子集，不得建设为孤立监控栈。

## Input normalization（统一输入处理）

每次 OCR 调用输入必须标准化为：
- `source_type`: `video_frame | image_file | crop_region | full_frame`
- `frame_id`
- `timestamp_ms`
- `image_width`
- `image_height`
- `crop_region`（或 `null`）
- `provider_id`
- `model_config_id`
- `ocr_mode`: `full_frame_low_frequency | region_focused | task_hint_guided | offline_batch`
- `semantic_interpretation_enabled=false`
- `allows_execute_now=false`

## Output normalization（统一输出处理）

每次 OCR 调用输出必须包含：
- `raw_text_candidates`
- `bbox` + `bbox_status`
- `confidence` + `confidence_status`
- `line_order`
- `raw_text_joined`
- `raw_text_joined_strategy`
- `provider_latency_ms`
- `provider_success`
- `fallback_used`
- `fallback_reason`
- `not_available_reason`
- `trace_ref`
- `replay_ref`
- `whitebox_ref`

## Governance hard boundaries

- OCR 仅 raw-text：禁止语义提炼。
- 禁止生成导航建议/任务建议。
- 禁止进入 `SceneTask/Fusion/Output`。
- 禁止触发真实 TTS。
- 禁止执行导航动作。
- 禁止把 OCR provider 输出直接用于下游执行。

## Runtime acceptance baseline

运行层面必须同时满足：
1. 有输出（或诚实 not_available）。
2. 输出结构合法。
3. 延迟/吞吐指标可观测。
4. fallback 行为可观测。
5. trace/replay/whitebox 完整。
6. 治理边界无泄漏（语义/导航/下游）。

## Relationship to model-specific phases

- 004A/004C/004B 是 provider-specific。
- 本文是 provider-agnostic 运行治理标准，上层约束所有 provider。

## Relationship to MidPlatform Monitoring

本文件定义 OCR 子域字段；统一归属与统计在：
- **Phase-MidPlatform-Monitoring-001**
- **Unified Capability Runtime Monitoring Definition v0**

该中台阶段将统一覆盖 `Voice/TTS/ASR/OCR/Vision/VLM/Semantic/Decision/TaskChain/Output` 的公共监控范式。
