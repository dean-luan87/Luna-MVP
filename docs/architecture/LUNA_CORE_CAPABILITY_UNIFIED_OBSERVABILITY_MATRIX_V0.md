# Phase-CoreCapability-TRW-Unified-003
# Core Capability Unified Observability Matrix v0（shadow）

**目的**：以统一表格形式展示 YOLO / OCR / Voice 在 shadow/offline 统一观察面中的可观测状态与关键缺失项。  
**注意**：该矩阵不声称三条链属于同一个真实用户任务；只表示“同一套抽链视图可观察”。

---

## 矩阵字段（v0）

- capability
- chain_count
- stage_per_chain
- trace/replay/whitebox（local / adapter-to-shadow）
- request_trace_shadow（bool）
- missing_trace_id（bool）
- missing_session_id（bool）
- hard_audit_ok（bool）

---

## 版本边界

- offline/shadow only
- 不接 runtime、不执行真实 TTS、不执行导航动作、不写世界模型

