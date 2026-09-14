# Phase-CoreCapability-StatusReview-001
# Core Capability Next Phase Options v0（下一阶段选项）

**目的**：列出下一阶段可选路线，并保持“不自动进入、不接 runtime”的约束。

---

## Option A. YOLO Core Closure（仅当缺失时）

- 现状：YOLO offline perception source 已有 closure review（closed_v0）。
- 何时需要：若要把 YOLO 的输出统一纳入 RequestTrace 视图（而不是再做新的 closure），建议优先走 Option B/C。

---

## Option B. OCR / YOLO TRW RequestTrace Mapping（shadow）

- 目标：把 OCR/YOLO 的离线 trace/replay/whitebox 适配成类似 voice 的 TRW adapter records，并产出 RequestTraceChain shadow mapping。
- 风险：需要统一 stage namespace 与字段语义，否则会出现“映射有了但不可比较”。

---

## Option C. Unified Core Capability TRW（统一核心能力 TRW）

- 目标：统一 YOLO/OCR/Voice 的 stage namespace、硬审计字段、以及 request-level chain 视图。
- 价值：减少“各自为政”的观测碎片，提升跨链排障与治理一致性。

---

## Option D. Voice governed_submit shadow（仍不真实播放）

- 目标：在不改变真实输出路径的前提下，模拟“治理若接入会如何”，验证 wiring contract 与审计字段是否足够。

---

## Option E. Real runtime readiness review（只做定义）

- 目标：仅定义“进入真实 runtime 需要哪些 gates、哪些证据、哪些 kill switch”，不做接线。

