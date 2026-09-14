# Phase-CoreCapability-TRW-Unified-001
# Local TRW → RequestTrace Mapping Policy v0（通用映射原则）

**目的**：定义 local trace/replay/whitebox（原始观测产物）到 RequestTrace（请求链视图）的通用映射原则，适用于 YOLO/OCR/Voice。  
**边界**：RequestTrace 是“视图”，不替代 local TRW；映射必须保留原始 refs；不得伪造 runtime 状态。

---

## 1. 核心原则（必须）

1. **local TRW 是原始证据**：trace/replay/whitebox 是可回溯原始产物，不可丢弃。
2. **RequestTrace 是请求链视图**：用于统一观察与调试，不替代 local TRW。
3. **映射必须保留 refs**：`trace_ref/replay_ref/whitebox_ref/raw_observation_refs` 至少一类必须存在。
4. **缺字段必须显式 missing**：不得用推断填充 `trace_id/session_id/runtime_invoked`。
5. **不得伪造 runtime 状态**：shadow/offline 映射不得被当作 runtime 接入证明。
6. **不得扩大副作用面**：映射层不得引入执行、不得触发下游动作。

---

## 2. 典型映射输出（建议）

- Stage records（有序）：
  - `stage_name` / `stage_order`
  - `status` / `reason`
  - `key_fields`（含 hard audit fields 与 why_* whitebox 扩展）
- Request-level chain summary：
  - `chain_type` / `status`
  - `hard_audit` 聚合

---

## 3. 禁止项（硬规则）

- 不允许复制后丢失来源（refs）
- 不允许把 shadow mapping 当 runtime 接入
- 不允许把离线候选当作真实世界事实/执行信号

