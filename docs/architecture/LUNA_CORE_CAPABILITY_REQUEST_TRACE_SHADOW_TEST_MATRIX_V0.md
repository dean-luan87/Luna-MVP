# Phase-CoreCapability-TRW-Unified-002
# Core Capability RequestTrace Shadow Adapter Test Matrix v0

**范围**：只覆盖 YOLO/OCR 的离线/shadow adapter 与统一输出；不触碰 runtime。

---

## A. 输入可读性

- **A1**：YOLO root 存在且可读（目录、关键文件可发现）
- **A2**：OCR root 存在且可读（目录、关键文件可发现）

---

## B. 产物生成

- **B1**：生成 `yolo_request_trace_chains.json` 且链条数 > 0
- **B2**：生成 `ocr_request_trace_chains.json` 且链条数 > 0
- **B3**：生成三类 shadow JSONL（trace/replay/whitebox）且非空

---

## C. Stage 完整性

- **C1**：YOLO 5 个 required stages 均出现（至少 1 次）
- **C2**：OCR 7 个 required stages 均出现（至少 1 次）
- **C3**：所有 stage 的 `stage_namespace="core_capability_request_trace_v0"`

---

## D. ID / Missing 策略

- **D1**：`request_id` 存在
- **D2**：`source_run_id` 存在
- **D3**：`trace_id=null` 且 `session_id=null`（不得伪造）
- **D4**：`missing_fields` 显式包含 `trace_id`、`session_id`

---

## E. Local refs 保留

- **E1**：`source_refs` 包含 `trace_ref/replay_ref/whitebox_ref/original_summary_ref/source_root` 键（值允许空但不得补假路径）

---

## F. Hard Audit 不变量

### F1（YOLO）

- `runtime_invoked=false`
- `downstream_invocation_count=0`
- `navigation_action=null`
- `real_tts_invoked=false`

### F2（OCR）

- `semantic_interpretation_enabled=false`
- `allows_execute_now=false`
- `downstream_invocation_count=0`
- `navigation_action=null`
- `real_tts_invoked=false`

---

## G. 禁止项回归

- **G1**：不执行真实 runtime / 不进入中台主链
- **G2**：不执行导航动作
- **G3**：不执行真实 TTS / 不接真实播放
- **G4**：不修改 YOLO/OCR 已有运行逻辑、不修改 OCR provider 默认策略

