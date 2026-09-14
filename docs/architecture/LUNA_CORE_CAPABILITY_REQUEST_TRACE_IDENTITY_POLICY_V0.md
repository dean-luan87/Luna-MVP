# Phase-CoreCapability-TRW-Unified-001
# Core Capability RequestTrace Identity Policy v0（统一 ID 规范）

**目标**：定义跨 YOLO/OCR/Voice 的 RequestTrace 统一引用规范，避免 adapter 映射时伪造 trace/session 信息。  
**原则**：`request_id` 是最小统一主键；其余 ID 允许为空，但必须显式 missing。

---

## 1. 字段定义（v0）

- `request_id`：一次用户/系统请求的主链 ID（最小统一主键）
- `trace_id`：跨模块链路追踪 ID（可空）
- `session_id`：用户交互会话 ID（可空）
- `source_run_id`：离线评估 run ID（离线链必须存在）
- `frame_id`：视觉帧 ID（YOLO/OCR 常用；可空）
- `evidence_id`：中台证据 ID（后续治理链）
- `decision_id`：治理决策 ID（如 voice output decision）
- `audit_id`：审计 envelope ID

---

## 2. 规则（必须）

- `request_id` 必须存在于所有 stage（否则该记录不可进入统一请求链视图）
- `trace_id/session_id` 可为空，但必须在 record/summary 中显式记录 missing（不得伪造）
- 离线链必须携带 `source_run_id`
- 不同模块 ID 必须通过 `source_reference_chain` 或等价引用链连接（不得凭空联想）

---

## 3. 禁止项（硬规则）

- local TRW 适配 RequestTrace 时不得伪造 `trace_id/session_id`
- 不得把 shadow mapping 当作 runtime 接入证明
- 不得把离线候选输出升级为真实执行/真实世界模型写入证据

