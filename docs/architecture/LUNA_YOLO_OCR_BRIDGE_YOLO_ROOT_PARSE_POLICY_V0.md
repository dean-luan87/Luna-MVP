# LUNA — YOLO × OCR Bridge YOLO-root Parse Policy v0

## Phase

- **Phase-ModelOCR-YOLO-Bridge-003** — 只做真实证据解析策略冻结。

## Scope（冻结范围）

- 离线证据模式下：`tools/evaluate_yolo_ocr_offline_bridge_v0.py` 使用 `--yolo-root <output_root>` 解析真实 YOLO offline 产物。
- 解析目标：把 YOLO 输出抽取为桥接输入所需的最小字段集合。

## Parse Inputs（输入）

在本仓库的真实 evidence roots 中，至少支持以下两类常见产物结构之一（以实际可读为准）：

1) `stage_outputs/perception/per_sample_results.json`

2) `per_sample_results.json`

3) `per_sample_yolo_perception_replacement_results.json`

## Parse Outputs（输出）

解析后应得到以下桥接输入对象（用于调用 `run_yolo_ocr_bridge_v0(...)`）：

- frame 证据
  - `sample_id`
  - `frame_id`（来自 detection 的 `frame_id`，形如 `..._f<N>`）
  - `image_ref` / `image_path`（本阶段不伪造：必须来自 source video 的真实帧抽取）
  - `image_width` / `image_height`
  - `timestamp_ms`（来自 archive 的 `trace.jsonl`）

- YOLO detections
  - `class_name`
  - `confidence`
  - `bbox`（`[x1,y1,x2,y2]`，用于 proposal clamp）
  - （可选）`detection_id`

## No Fabrication（禁止伪造）

- 如果无法从真实 YOLO root 解析出：
  - `frame_id` 或
  - 对应 `trace.jsonl` 的 `timestamp_ms`，或
  - source video 文件

则必须：

- 输出 `yolo_root_parse_report.json` 中 `yolo_root_parse_status != ok`。
- 在这种情况下不允许把 `sample_matrix.json` 当作真实 root 的证据来源。

## Frame Timestamp Resolution（时间定位）

- archive 中 `trace.jsonl` 必须包含事件 `event_type == "frame_sampled"`。
- 通过 `payload.frame_index == <from frame_id suffix>` 获取 `payload.timestamp_ms`。
- 允许 off-by-one 容错：若找不到 frame_index，则尝试 `frame_index + 1`。

## Audit Requirements（审计字段）

`yolo_root_parse_report.json` 必须包含（冻结字段名）：

- `yolo_root`
- `yolo_root_type`
- `yolo_root_parse_status`
- `parsed_sample_count`
- `parsed_detection_count`
- `parsed_frame_refs`
- `unsupported_or_missing_fields`
- `ocr_worthy_detection_count`

## Governance / closed_v0（治理边界）

- 本阶段不修改 `YOLO closed_v0` 与 `OCR closed_v0`。
- 本阶段不引入语义/导航/执行/TTS。
