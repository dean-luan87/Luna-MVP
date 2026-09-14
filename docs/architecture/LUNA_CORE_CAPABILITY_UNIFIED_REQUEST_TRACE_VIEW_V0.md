# Phase-CoreCapability-TRW-Unified-003
# Unified Core RequestTrace Extractor View v0

**阶段定位**：本阶段只做 YOLO / OCR / Voice 三条核心能力的统一 RequestTrace **shadow view**（离线/只读合并视图）。  
**不做**：runtime 接线、目录重构、真实播放、真实 TTS、导航动作、世界模型写入、中台主链接入、地图/GPS/点云。

---

## 1. 输入 roots（建议）

- **Core YOLO/OCR shadow root**：Phase-CoreCapability-TRW-Unified-002 output_root  
  例如：`logs/core_capability_request_trace_shadow_002_20260430_160600`
- **Voice shadow root**：Phase-Voice-OutputGovernance-005 output_root  
  例如：`logs/voice_output_request_trace_extractor_005_test_run`

---

## 2. 合并策略（核心约束）

**禁止伪造跨能力请求关联**：本阶段不强行把 YOLO/OCR/Voice 合并成同一个 `request_id`。  
统一视图按 capability 分组，形成统一索引与 timeline：

- capability ∈ {`yolo`, `ocr`, `voice`}
- request_id 来源允许三类：
  - inherited（上游已有 request_id）
  - deterministic_shadow（YOLO/OCR shadow 生成）
  - voice_native（Voice Phase-005 原生 request_id）

若缺 `trace_id/session_id`：**不得伪造**，必须显式缺失（null + missing）。

---

## 3. 统一输出（output_root）

`tools/evaluate_core_capability_unified_request_trace_view_v0.py` 输出：

- `core_capability_unified_request_trace_summary.json`
- `core_capability_unified_request_chains.json`（capability 分组的统一链索引）
- `core_capability_stage_namespace_index.json`（保留原 stage namespace 的索引）
- `core_capability_timeline_index.json`（capability-level timeline）
- `core_capability_observability_matrix.json`（统一可观测矩阵）
- `core_capability_source_root_index.json`（source_root/refs 总索引）
- `core_capability_missing_field_report.json`
- `core_capability_unified_trace.jsonl`
- `core_capability_unified_replay.jsonl`
- `core_capability_unified_whitebox.jsonl`
- `evaluation_notes.md`

---

## 4. Hard Audit 不变量（必须保持）

### YOLO
- `runtime_invoked=false`
- `downstream_invocation_count=0`
- `navigation_action=null`
- `real_tts_invoked=false`

### OCR
- `semantic_interpretation_enabled=false`
- `allows_execute_now=false`
- `downstream_invocation_count=0`
- `navigation_action=null`
- `real_tts_invoked=false`

### Voice
- `real_tts_invoked=false`
- `playback_invoked=false`
- `provider_invoked=false`
- `navigation_action=null`
- `downstream_invocation_count=0`

---

## 5. 边界声明（必须）

- 本阶段只做 Unified Core RequestTrace **shadow view**
- 不接 runtime，不重构，不接真实播放，不执行真实 TTS
- 不接地图/GPS/点云，不进入 SceneTask/Fusion/Output，不执行导航动作
- 不写真实世界模型，不上传蜂巢，不接推荐系统
- 不修改 YOLO/OCR/Voice 已有运行逻辑，不修改 OCR provider 默认策略

