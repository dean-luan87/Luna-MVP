# Phase-CoreCapability-StatusReview-001
# Core Capability Gap Register v0（缺口登记）

**目的**：登记 YOLO/OCR/Voice 三条核心能力线的硬缺口与软缺口，并明确哪些属于 future branch。

---

## 1. Hard gaps（硬缺口：不能忽略）

- **统一请求链观察面不一致**：Voice 已进入 RequestTraceChain shadow 视图；YOLO/OCR 仍缺同等级统一视图。
- **统一 stage namespace 缺失（跨线）**：Voice 仅在 voice_output_governance_v0 内完成；YOLO/OCR 尚未统一纳入核心 stage namespace。

---

## 2. Soft follow-ups（软缺口：可排期）

- `trace_id/session_id` 注入（跨线）：当前多为 null（shadow/offline），后续需主链注入与映射。
- `candidate_text_hash` 标准化：已被 voice chain 登记为 future branch，但未形成全链统一方案。

---

## 3. Future branches（明确暂停/未来分支）

- Map/GPS/POI/PointCloud/Depth：attachment/enhancement layer，当前暂停，不参与核心能力闭包完成判断。
- Voice real playback / real submit wiring：当前明确禁止，必须另开受控阶段治理变更。
- OCR/YOLO real runtime 与中台主链接线：当前不在允许范围。

