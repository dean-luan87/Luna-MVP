# Phase-CoreCapability-TRW-Unified-004
# Unified Query / Filter / Export View v0

**阶段定位**：在 Phase-CoreCapability-TRW-Unified-003 的 unified shadow view 之上，新增离线查询、过滤、导出能力；不接 runtime、不重构目录。

---

## 1. 输入

- Phase-003 unified view output_root，例如：
  - `logs/core_capability_unified_request_trace_view_003_20260430_163000`

---

## 2. 查询能力（query）

工具：`tools/query_core_capability_unified_request_trace_view_v0.py`

支持过滤：
- capability：`yolo|ocr|voice|all`
- stage_name：精确匹配
- missing_field：如 `timestamp_ms`
- hard_audit_only：仅返回 hard_audit 异常记录（不变量违规）
- request_id：精确匹配

导出：
- `core_capability_unified_query_summary.json`
- `core_capability_unified_query_results.json`
- `core_capability_unified_query_results.jsonl`
- `core_capability_unified_query_report.md`

---

## 3. 导出能力（export）

工具：`tools/export_core_capability_unified_observability_view_v0.py`

导出产物：
- capability table / stage table / hard audit table / missing fields table
- field-level mapping report（字段级映射表）
- markdown export report

---

## 4. 边界声明（必须）

- 只读输入 root，不修改 YOLO/OCR/Voice 原始链路
- 不接 runtime，不执行真实 TTS，不接真实播放
- 不执行导航动作，不写真实世界模型
- 不接地图/GPS/点云，不进入 SceneTask/Fusion/Output

