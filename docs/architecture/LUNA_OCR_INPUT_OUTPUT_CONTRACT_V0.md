# LUNA OCR Input/Output Contract v0

## Phase

- Phase-ModelOCR-001（OCR Independent Capability Definition v0）

## Hard boundaries (must be fail-closed)

- candidate-only：OCR 输出只能是候选信号，不得成为结论指令
- `allows_execute_now` 必须为 **false**
- `real_tts_invoked` 必须为 **false**
- 不接 YOLO / 不接中台 / 不接 SceneTask/Fusion/Output（本阶段）
- 不进入 controlled_live_stream / 不进入真实 runtime

## Input boundary (allowed)

允许输入（只作为离线评测上下文）：

- `sample_id`（phone_local controlled capture 样本 id）
- `frame_id`（帧 id）
- `timestamp_ms`（毫秒时间戳）
- 图像输入（二选一或同时提供）：
  - `full_frame`（整帧图像引用/路径/bytes 的抽象引用）
  - `crop_region`（裁剪区域引用/路径/bytes 的抽象引用）
- `crop_regions`（可选，多区域裁剪列表；用于 region_focused）
- `source_metadata`（只读元信息：分辨率、旋转、颜色空间等）
- `task_hint`（可选；只能作为注意力提示，不可强制过滤结论）
- `scene_hint`（可选；不能控制 OCR 结论）
- `ocr_config_id`（配置 id）
- `candidate_only_constraint=true`（显式约束）

## Input boundary (forbidden)

禁止输入（出现即应忽略并在 whitebox 标注风险，必要时 fail-closed）：

- execute permission / release gate / default-on / side effects control
- governance override / hidden execution flags
- 任何可导致 OCR 直接输出导航指令的字段

## Output: `ocr_navigation_signal` (minimum schema)

OCR 输出必须是 candidate，不是结论。

```
ocr_navigation_signal:
{
  "signal_type": "ocr_navigation_signal",
  "signal_status": "available|not_available|partial|low_confidence",
  "sample_id": "...",
  "frame_id": "...",
  "timestamp_ms": 0,
  "ocr_runtime_mode": "ocr_shadow|ocr_baseline|ocr_disabled",
  "text_candidates": [
    {
      "text_id": "txt_001",
      "text": "出口",
      "normalized_text": "出口",
      "bbox": [x1, y1, x2, y2],
      "confidence": 0.91,
      "language": "zh",
      "text_type_candidate": "directional_sign|room_number|facility_label|warning_text|advertisement_text|screen_text|unknown",
      "navigation_relevance": "high|medium|low|unknown",
      "source_region_type": "full_frame|crop|sign_region|doorplate_region|screen_region|unknown",
      "visual_medium_risk": "none|poster|screen|advertisement|reflection|unknown",
      "task_relevance": "target_related|path_context|unrelated|unknown",
      "requires_scene_context_gate": true,
      "allows_execute_now": false,
      "reason_codes": []
    }
  ],
  "unsupported_or_uncertain": {
    "advertisement_filter_not_confirmed": true,
    "visual_medium_not_confirmed": true,
    "spatial_direction_not_confirmed": true
  },
  "allows_execute_now": false,
  "real_tts_invoked": false,
  "hard_blockers": [],
  "soft_followups": []
}
```

### Required invariants

- 顶层 `allows_execute_now=false`
- 顶层 `real_tts_invoked=false`
- 每个 text candidate 的 `allows_execute_now=false`
- `signal_status=not_available` 时必须保持诚实：不得伪造 candidates

## Fallback / not_available policy (fail-closed)

必须支持：

- `ocr_disabled`：明确禁用时输出 `signal_status=not_available`，并标注原因
- `not_available`：输入缺失、解码失败、模型不可用、依赖缺失、违规语义等 → 统一 fail-closed
- `partial/low_confidence`：可输出候选，但必须显式标注不确定性字段与 reason_codes

## Forbidden output semantics (must block)

OCR 输出禁止包含以下语义（出现即 block + fallback/not_available）：

- execute_now / walk_now / turn_now / cross_now
- go_to_text / final_navigation_instruction
- actual_tts / enable_default_path
- release_side_effects / override_governance
- retry_now / reopen_now

