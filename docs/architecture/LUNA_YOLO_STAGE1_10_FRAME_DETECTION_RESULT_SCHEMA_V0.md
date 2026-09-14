# LUNA YOLO Stage-1 10-Frame Detection Result Schema v0

**Phase**：Phase-Mainline-GuardedTrial-005

---

## 1. 校验函数

`validate_yolo_detection_result_schema_v0(det)` — 对每个 detection dict 校验；任一 invalid 即累计 `schema_invalid_count` 并 **立即 abort**（`abort_reason=schema_validation_failed_first_invalid`）。

---

## 2. 单条 detection 必填字段

| 字段 | 类型 / 约束 |
|------|-------------|
| `bbox` | `list` 或 `tuple`，长度 **4**（数值可转为 float） |
| `confidence` | 可 `float(...)` |
| `class_id` | 可选；若存在须可 `int(...)` |
| `class_name` | 非空字符串（strip 后非空） |
| `frame_id` | 非空字符串（与当前帧 planned id 对齐） |

---

## 3. 规范化补充字段

`normalize_yolo_detection_result_v0(...)` 可附加：

- `ts`：浮点时间戳（记录用）

规范化后的对象须仍通过 §2 校验。

---

## 4. 失败原因码（`reason`）

包含但不限于：`bbox_invalid`、`confidence_invalid`、`class_id_invalid`、`class_name_missing`、`frame_id_missing`。

---

## 5. 持久化

逐帧结果写入 `yolo_stage1_10_frame_detection_results.json`（`detection_results_by_frame`）；逐条 schema 记录在 `yolo_stage1_10_frame_detection_schema_validation.json` 的 `checks` 数组中聚合。
