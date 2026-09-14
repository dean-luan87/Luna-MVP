# Phase-Voice-OutputGovernance-009
# Governed Submit Shadow Unified Query/Export Integration v0

**阶段定位**：把 Phase-008 的 `governed_submit_shadow_gate` 可观察阶段并入“可查/可筛/可导出”的离线体系；不接真实 submit、不真实播报、不执行真实 TTS。

---

## 输入（只读）

- Phase-008 output_root（enhanced chains）：
  - `voice_governed_submit_enhanced_request_chains.json`

---

## Query（离线查询）

工具：`tools/query_voice_governed_submit_unified_view_v0.py`

必须支持过滤：
- `submit_shadow_result`
- `submit_gate_position`
- `submit_allowed`
- `request_id`
- `hard_audit_only`

输出：
- `voice_governed_submit_unified_query_summary.json`
- `voice_governed_submit_unified_query_results.json`
- `voice_governed_submit_unified_query_results.jsonl`
- `voice_governed_submit_unified_query_report.md`

---

## Export（离线导出包）

工具：`tools/export_voice_governed_submit_unified_view_v0.py`

输出：
- gate position table
- submit result distribution table
- request matrix（两位置一致性）
- hard audit table
- field mapping report
- markdown export report

---

## 边界声明（必须）

- 不修改 Phase-008 原始产物
- 不接真实 submit，不真实播报，不执行真实 TTS
- 不接新 provider，不删 legacy voice，不改 env 语义

