# Phase-CoreCapability-StatusReview-001
# Core Capability TRW / Observability Matrix v0（观测矩阵）

**目的**：对比 YOLO/OCR/Voice 三条核心能力线的观测面，明确哪些已经进入统一请求链视图，哪些仍停留在“各自文件输出”。

---

## 1. 观测层级枚举

- `none`
- `local`（本能力链自有 trace/replay/whitebox 输出）
- `adapter`（已有 TRW adapter records）
- `request_trace_shadow`（已有 RequestTraceChain shadow mapping）

---

## 2. 观测矩阵（核心）

| capability | trace/replay/whitebox | TRW adapter | RequestTrace shadow | whitebox dictionary |
|---|---|---|---|---|
| yolo | local | none | none | partial（分散文档/工具） |
| ocr | local | none | none | partial（分散文档/工具） |
| voice | request_trace_shadow | adapter（已完成） | done | done（V1 字典齐全） |

---

## 3. 关键缺口（跨线）

- YOLO/OCR 尚未形成与 Voice 同等级别的 `RequestTraceChain shadow mapping`。
- 三条线尚未统一 stage namespace（Voice 已有 `voice_output_governance_v0`，但未扩展到 YOLO/OCR）。
- `trace_id/session_id/candidate_text_hash` 的统一注入仍是 future branch。

