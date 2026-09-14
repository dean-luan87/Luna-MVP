# LUNA — Scene Delta Signature Comparison Policy v0

## Phase

- **Phase-MidPlatform-SceneDelta-001**

## Purpose

冻结 Scene Delta 的签名优先级、比较语义与比较结果类别，确保“对比机制可解释、可审计、可复现”。

本阶段只定义，不实现。

## Signature priority（按输入类型）

### OCR 文本（ocr_evidence）

- `text_signature`
- `layout_signature`
- `crop_signature`

### YOLO 对象（yolo_detection）

- `object_signature`
- `crop_signature`
- `scene_signature`

### YOLO × OCR（yolo_ocr_bridge_result）

- `object_signature + text_signature + crop_signature`

### 商业/世界上下文候选（world_context_candidate / ambient_context_candidate）

- `text_signature + spatiotemporal_anchor + ttl_policy`

### 视觉符号（visual_symbol_candidate）

- `symbol_signature + spatiotemporal_anchor + meaning_status/confirmation_status`

## Comparison result classes（冻结）

- `exact_match`：签名完全一致
- `near_match`：内容一致但位置/布局轻微变化（不改变核心含义）
- `changed`：内容或对象明显变化
- `unstable`：低置信度反复变化（抖动/模糊/碎片）
- `expired`：时间有效性失效（TTL 到期）
- `contradicted`：新证据与旧证据冲突（不等于真假裁决）

## Mapping to delta_status / delta_action（默认映射）

- `exact_match` → `delta_status=unchanged` → `delta_action=reuse_previous`
- `near_match` → `delta_status=changed` → `delta_action=partial_update`
- `changed` → `delta_status=changed` → `delta_action=full_reprocess`
- `unstable` → `delta_status=uncertain` → `delta_action=hold_uncertain`
- `expired` → `delta_status=expired` → `delta_action=expire_and_reprocess`
- `contradicted` → `delta_status=contradicted` → `delta_action=hold_uncertain | full_reprocess`（由治理与确认策略决定；本阶段只冻结“不得当作事实”）

## Threshold suggestions（v0 只冻结建议值，不实现）

- `spatial_shift_threshold = 0.10`
- `duplicate_iou_threshold = 0.85`
- `confidence_delta_threshold = 0.20`
- `same_text_window_ms = 3000`
- `scene_local_ttl_default = 30min`
- `commercial_short_ttl_default = 24h`（或由信息内容决定）
- `uncertain_hold_window_ms = 3000..10000`

