# LUNA — macOS Vision OCR Raw Text Offline Harness v0

## Phase

- **Phase-ModelOCR-004A**
- **Goal:** 仅用 **macOS Vision OCR system provider** 建立 OCR **raw text candidates** 离线 harness；不接 Paddle 推理、不接下游、不做语义。

## Preconditions（上游事实）

| 上游 | 状态 |
|------|------|
| ModelOCR-001 raw text capability | GO |
| ModelOCR-002 candidate inventory | CONDITIONAL_GO |
| ModelOCR-003 manifest/readiness | CONDITIONAL_GO |
| ModelOCR-003-Fix-004 PaddleOCR det+rec | **CONDITIONAL_GO**（`weights_source=pinned_partial`；**本阶段不跑 PaddleOCR**） |
| macOS Vision manifest | ready（`configs/models/ocr/macos_vision_ocr_manifest_v0.json`） |
| PaddleOCR | **不安装、不调用**；依赖就绪属 **004B** |

## Hard boundaries（强边界）

- 只使用 **macOS Vision**；不进入 **PaddleOCR runtime**。
- 不接 YOLO、中台、SceneTask / Fusion / Output。
- 不做文本语义提炼；不执行导航；不真实播报。
- 不进入 `controlled_live_stream`；不扩 Option A。
- `semantic_interpretation_enabled=false`，`allows_execute_now=false`，`real_tts_invoked=false`。
- OCR 输出仅 **raw text candidates**（可含 `text` / `bbox` / `confidence` / `frame_id` / `line_order` / `raw_text_joined`）。

## Implementation（v0）

| 组件 | 路径 |
|------|------|
| Swift 桥 | `tools/macos_vision_ocr_bridge_v0.swift`（`VNRecognizeTextRequest` → JSON） |
| Python adapter | `capabilities/model_ocr/macos_vision_ocr_adapter_v0.py`（统一 envelope + candidates） |
| Harness | `tools/evaluate_macos_vision_ocr_raw_text_v0.py` |
| Verifier | `tools/verify_macos_vision_ocr_raw_text_v0.py` |

**CLI 示例：**

```bash
python3 tools/evaluate_macos_vision_ocr_raw_text_v0.py \
  --input-dir input_videos/ocr_samples \
  --output-root logs/macos_vision_ocr_raw_text_004a_<timestamp> \
  --frame-step 30 \
  --max-sampled-frames 100
```

或单视频：

```bash
python3 tools/evaluate_macos_vision_ocr_raw_text_v0.py \
  --video-path path/to/video.mp4 \
  --output-root logs/macos_vision_ocr_raw_text_004a_<timestamp> \
  --frame-step 30 \
  --max-sampled-frames 100
```

## Per-sample envelope（v0；每条 OCR sample）

每条样本至少包含下列语义字段（实现侧须与 `macos_vision_ocr_adapter_v0` 一致）：

- `sample_id`, `provider_id`=`macos_vision_ocr_system_v0`, `model_config_id`=`macos_vision_ocr_system_v0`
- `ocr_runtime_mode`=`system_provider_offline`
- `provider_method`：`vision_framework` | `bridge` | `unavailable`（当前实现为 Swift 子进程即 **`bridge`**；不可用时 **`unavailable`**）
- `semantic_interpretation_enabled`：**false**
- `raw_text_candidates[]` 每一项：
  - `text_id`, `text`, `normalized_text`
  - `bbox`：`[x1,y1,x2,y2]` 或 **`null`**
  - `bbox_status`：`present` | `not_available`（须与 `bbox` 是否为空一致）
  - `confidence`：float 或 **`null`**
  - `confidence_status`：`present` | `not_available`
  - `frame_id`, `timestamp_ms`, `line_order`, `allows_execute_now`（恒 **false**）
- `raw_text_joined`（字符串，可为空）
- `raw_text_joined_strategy`：`model_order` | `bbox_top_left` | `empty` | `unknown`（当前拼接为 bbox 自上而下 → **`bbox_top_left`**；无字 **`empty`**；错误 **`unknown`**）
- `allows_execute_now`, `real_tts_invoked`：**false**
- `hard_blockers`, `soft_followups`

本阶段**不**强制 `reading_direction_candidate`；不得与后续 Reading Direction / Line Order Contract 冲突。

## Summary（`ocr_raw_text_summary.json`）扩展字段

除 `provider_id`、**`model_config_id`**、**`sample_count_total` / `sample_count_processed`**、各 **metrics**（含 **`downstream_invocation_count`**）、**`recommendation`**、顶层 **`hard_blockers` / `soft_followups`**、**`readiness_status`**、**`harness_verdict`**、**`ok`** 外，正常跑完时 **`governance.downstream_invoked`** 恒为 false。

## 缺输入 / 不可读输入（不得伪造 OCR）

若 `--input-dir` 不存在、非目录、或无图片；或 `--video-path` 不存在、打不开、抽帧为空：

- **不得**写入合成的 OCR 文本结果；`per_sample_ocr_raw_text_results.json` 为 **`[]`**
- `ocr_raw_text_summary.json`：`hard_blockers` 含 **`missing_input_samples`**，`input.missing_input_samples=true`，`readiness_status=not_ready`，`ok=false`
- 仍生成 trace/replay/whitebox（各至少一行 **skip** 记录），便于验收文件完整性
- evaluate **exit code 2**

## `output_root` 产物

| 文件 | 说明 |
|------|------|
| `ocr_raw_text_summary.json` | 汇总、metrics、governance、artifacts 索引 |
| `per_sample_ocr_raw_text_results.json` | 逐样本结果数组 |
| `ocr_raw_text_trace.jsonl` | 轨迹事件 |
| `ocr_raw_text_replay.jsonl` | 可重放输入路径引用 |
| `ocr_raw_text_whitebox.jsonl` | 白盒调试摘要 |
| `evaluation_notes.md` | 边界与后续契约说明 |
| `frames/` | 仅 `--video-path` 时抽帧目录 |

## Summary metrics（`ocr_raw_text_summary.json` → `metrics`）

| 指标 | 含义 |
|------|------|
| `ocr_result_generated_rate` | 无 per-sample `hard_blockers` 的样本占比 |
| `raw_text_candidate_schema_valid_rate` | schema 合法样本占比 |
| `bbox_present_or_declared_rate` | bbox 已填或显式 `null` |
| `confidence_present_or_declared_rate` | confidence 已填或显式 `null` |
| `raw_text_joined_present_rate` | `raw_text_joined` 字段存在（含空串） |
| `semantic_interpretation_disabled_rate` | 恒为 1.0（设计） |
| `allows_execute_now_false_rate` | 恒为 1.0（设计） |
| `real_tts_invoked_false_rate` | 恒为 1.0（设计） |
| `trace_ready_rate` / `replay_ready_rate` / `whitebox_ready_rate` | 对应 jsonl 已生成 |
| `forbidden_semantic_output_count` | 禁止语义键扫描计数（预期 0） |
| `downstream_invocation_count` | 恒为 **0**（本 harness 不调用下游） |

## Reading direction / layout（后续契约，本阶段不冻结）

- 已记录：后续需补 **Reading Direction / Line Order / Layout Order Contract**（LTR/RTL/竖排/多列、`raw_text_joined` 策略）。
- 当前 `line_order` 与 `raw_text_joined` 为 **bbox 启发式**；**阅读顺序不确定时不得进入语义提炼**（与 OCR 主线约定一致）。

## Sandbox note

在 Cursor 沙箱或受限环境下，Vision 可能失败。需在 **macOS 真机、非沙箱**下复现；`adapter.is_available()` 基于 **Darwin + `swift` + 桥接脚本**，不依赖 PyObjC。

## Cross-references

- 测试矩阵：`LUNA_MACOS_VISION_OCR_RAW_TEXT_TEST_MATRIX_V0.md`
- 决策包：`LUNA_MACOS_VISION_OCR_RAW_TEXT_GO_NO_GO_PACK_V0.md`
- Paddle pinned_partial 收口：`LUNA_PADDLEOCR_PINNED_PARTIAL_READINESS_REVIEW_V0.md`
