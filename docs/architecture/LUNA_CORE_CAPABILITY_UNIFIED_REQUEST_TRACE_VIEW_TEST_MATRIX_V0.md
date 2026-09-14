# Phase-CoreCapability-TRW-Unified-003
# Unified Core RequestTrace View Test Matrix v0

**范围**：只覆盖 unified shadow view 的合并、索引与硬不变量；不触碰 runtime。

---

## A. 输入可读性

- **A1**：core shadow root 可读（含 YOLO/OCR chains）
- **A2**：voice shadow root 可读（含 Voice chains + jsonl）

---

## B. 产物生成

- **B1**：生成 unified summary / chain index / timeline / ns index / matrix / source_root_index / missing report
- **B2**：生成 unified trace/replay/whitebox JSONL 且非空

---

## C. 合并策略（不伪造跨能力关联）

- **C1**：不要求统一 request_id
- **C2**：按 capability 分组输出 unified chain index

---

## D. Stage namespace 与 source refs 保留

- **D1**：保留 YOLO/OCR 的 `core_capability_request_trace_v0`
- **D2**：保留 Voice Phase-005 历史 stage namespace（`voice_output_governance_v0`）与 `request_trace.stage.voice_output.*` stage_name
- **D3**：source_root/refs 索引完整（不补假路径）

---

## E. Hard Audit 不变量

### E1（YOLO）
- runtime_invoked=false
- downstream_invocation_count=0
- navigation_action=null
- real_tts_invoked=false

### E2（OCR）
- semantic_interpretation_enabled=false
- allows_execute_now=false
- downstream_invocation_count=0
- navigation_action=null
- real_tts_invoked=false

### E3（Voice）
- real_tts_invoked=false
- playback_invoked=false
- provider_invoked=false
- navigation_action=null
- downstream_invocation_count=0

