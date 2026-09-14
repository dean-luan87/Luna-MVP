# Phase-CoreCapability-TRW-Unified-002
# Core Capability RequestTrace Shadow Adapter Go/No-Go Pack v0

**阶段目标**：把 YOLO/OCR 的 local TRW/benchmark/offline policy 观测产物映射为统一 RequestTrace shadow chain，使其进入同一观察面（shadow-only）。

**硬边界**：不接 runtime、不重构目录、不接真实播放、不执行真实 TTS、不执行导航动作、不写真实世界模型、不进入 SceneTask/Fusion/Output。

---

## GO 条件（全部满足）

- YOLO root 可读
- OCR root 可读
- YOLO chains 生成且 > 0
- OCR chains 生成且 > 0
- YOLO required stages 完整
- OCR required stages 完整
- stage_namespace 使用 `core_capability_request_trace_v0`
- local TRW refs 关键键保留（不得丢失/覆盖）
- `trace_id/session_id` 缺失被显式记录（不得伪造）
- hard audit 不变量全部保持（见下）
- shadow trace/replay/whitebox JSONL 非空
- verifier 通过

---

## CONDITIONAL_GO（允许但必须记录）

- 部分 local refs 值缺失，但 **键存在** 且 missing report 可追溯
- 部分字段无法映射，但 mapping/missing report 完整披露

---

## NO_GO（任一触发即失败）

- 伪造 `trace_id` 或 `session_id`
- 丢失 `source_root` 或关键 `source_refs` 键
- hard audit 字段缺失或被置为“可能触发 runtime”的值（例如 `semantic_interpretation_enabled=true`）
- `real_tts_invoked=true`
- `navigation_action` 非空
- 本阶段接入 runtime 或修改 YOLO/OCR 原始逻辑
- 目录级重构

---

## Hard Audit 不变量（验收点）

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

