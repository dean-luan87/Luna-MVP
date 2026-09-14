---
phase: Phase-DeviceEnv-002
title: Controlled Live Archive Bridge Definition v0
status: DEFINITION_FROZEN
version: v0
last_updated: 2026-04-22
scope: definition_only
side_effects_released_default: false
---

## 0. 目标（本文件只定义，不实现）

定义一条 **Controlled Live（真实帧输入）→ archive_root（RealScene evidence contract）** 的最小桥接方案（archive bridge），用于后续 Phase-DeviceEnv-003 实现 **Mac Camera Controlled Live Archive Adapter**。

本文件不触发真实 run，不生成伪 archive，不改动 RealScene contract。

## 1. 输入源与桥接原则

### 1.1 输入源（v0 冻结）

- **主输入（Mac-first）**：OpenCV 摄像头（复用 `utils/camera_handler.py` 能力）
- **候选输入（后置，不在本阶段实现）**：浏览器 getUserMedia（`web_test_server.py`）

### 1.2 桥接原则（必须）

- **P0：真实输入 ≠ 真实证据链**。必须产出完整 required_files，且能过 validator。
- **P1：candidate-only**。桥接层只记录、只落盘，不产生执行指令，不触发真实 side effects。
- **P2：明确 entry / exit**。必须有显式开始、显式停止、timebox、abort 记录。
- **P3：每个 required file 必须存在**。即便 “none_observed” 也必须写出文件（尤其 `risk_events.jsonl`）。
- **P4：不绕过 validator**。archive_root 完整性由 manifest + validator 检查。

## 2. archive_root 目录结构（v0 约定）

> 本段只定义“应该长什么样”。实现由 DeviceEnv-003 负责。

```
archive_root/
  run_evidence.json
  trace.jsonl
  replay.jsonl
  whitebox.jsonl
  model_candidate_trace.jsonl
  output_candidate_trace.jsonl
  operator_notes/
    operator_notes.md  (或 .txt；以模板为准)
  risk_events.jsonl
  post_run_summary.json
  archive_manifest.json
  media/
    frames/            (可选：帧文件或编码视频；v0 允许“只引用不落盘大文件”，但必须可追溯)
```

### 2.1 required_files（v0 必须）

以下文件 **必须存在**（可以是最小结构化占位，但不得缺失）：

- `run_evidence.json`
- `trace.jsonl`
- `replay.jsonl`
- `whitebox.jsonl`
- `model_candidate_trace.jsonl`
- `output_candidate_trace.jsonl`
- `operator_notes/`（目录必须存在，且至少 1 个 notes 文件）
- `risk_events.jsonl`
- `post_run_summary.json`
- `archive_manifest.json`

## 3. 每个 evidence 文件的最小内容要求（v0）

> v0 允许“最小字段集”，但必须保留 **run_id / 时间轴 / 禁止执行断言 / 数据来源声明** 等关键要素。

### 3.1 run_evidence.json（RunEvidenceBuilder）

最小字段建议（不得与既有 schema 冲突；以 RealScene 已冻结 schema 为准）：

- `schema_version`
- `run_id`
- `phase_id = "Phase-DeviceEnv-003"`（注意：本文件是 Phase-DeviceEnv-002 定义，但产出由下一阶段实现）
- `mode = "controlled_live"`
- `option = "A"`
- `input_source = { type: "mac_camera", details: { backend, camera_index } }`
- `timebox = { start_ts, end_ts, duration_s }`
- `personnel = { operator_id, observer_id }`
- `assertions = { no_execute_leakage, no_default_on, no_side_effect_expansion, candidate_only }`
- `files = { ... paths ... }`
- `pending_real_device_run = false`（当且仅当确实跑了真实摄像头并写出 evidence）

### 3.2 trace.jsonl（TraceBridge）

目的：对齐 RealScene 的“运行过程可观测性”，不要求完整复刻历史 A3 schema。

最小行结构建议（JSONL，每行一个 event）：

- `ts`（统一时间轴；可用 monotonic 或 wall clock，但必须一致）
- `run_id`
- `event_type`（例如：`ENTRY`/`FRAME`/`PIPELINE_TICK`/`ABORT`/`EXIT`/`ERROR`）
- `seq`（单调递增）
- `payload`（最小必要字段）

桥接策略（允许）：

- **可桥接历史 `logs/a3_trace.jsonl`**：通过转换/复制进入 `archive_root/trace.jsonl`（必须保留来源标记 `source_trace="a3_trace"`）。
- 若桥接成本过高：v0 先写 **bridge trace**（只记录关键 tick、状态与断言），并在 `post_run_summary` 明确 “a3_trace 未桥接”。

### 3.3 replay.jsonl（ReplayBridge）

目的：让后续可以在“无真实摄像头”情况下回放同一条输入序列，复现关键路径。

最小行结构建议：

- `ts`
- `run_id`
- `frame_seq`
- `frame_ref`（例如：`media/frames/frame_000123.jpg` 或 hash 引用）
- `frame_meta`（w/h/encoding）
- `notes`（可选）

v0 可选策略：

- **不强制落盘所有帧**（避免巨大空间），但必须提供可重放引用（例如：编码视频 + 时间戳映射，或帧 hash + 外部存储指针）。
- 如果无法提供稳定引用：则本阶段判定应倾向 **CONDITIONAL_GO**，并把它作为 DeviceEnv-003 的 hard blocker。

### 3.4 whitebox.jsonl（WhiteboxEmitter）

目的：记录 “候选生成/抑制/门禁/降级” 的内部可解释状态，支撑 Review 时的因果追溯。

最小行结构建议：

- `ts`
- `run_id`
- `tick_seq`
- `state`（只读内部状态摘要）
- `candidates`（候选摘要；若无则空数组）
- `suppression`（抑制原因；若无则明确 `none`）
- `gates`（关键门禁结论：candidate-only、execute禁止、side_effects_released=false）

### 3.5 model_candidate_trace.jsonl（ModelCandidateTraceEmitter）

目的：即便本次未调用模型，也必须落盘说明原因，确保文件存在且可审计。

最小行结构建议：

- `ts`
- `run_id`
- `event_type`：`MODEL_SHADOW_DISABLED` / `MODEL_CANDIDATE` / `MODEL_FALLBACK`
- `input_digest`（可选：脱敏摘要）
- `candidate_digest`（可选）
- `admission`（`go/conditional_go/no_go` + reason）

### 3.6 output_candidate_trace.jsonl（OutputCandidateTraceEmitter）

目的：记录“输出候选被生成但未执行/被抑制/过期”的全过程。

最小行结构建议：

- `ts`
- `run_id`
- `event_type`：`OUTPUT_CANDIDATE` / `OUTPUT_SUPPRESSED` / `OUTPUT_SILENCE`
- `candidate`（摘要；必须包含 `allows_execute_now=false` 等关键字段）
- `policy`（优先级/抑制/时窗判定结果摘要）

### 3.7 operator_notes（OperatorNotesCollector）

目的：把人工观察与过程说明纳入证据链。

v0 规则：

- 目录必须存在
- 至少 1 个 notes 文件
- 必须包含：地点/时间窗/是否中止/是否有异常/是否观察到风险事件（可为 none_observed）

### 3.8 risk_events.jsonl（RiskEventsLogger）

v0 规则（强制）：

- 文件必须存在
- 若无风险事件：也必须写入 1 行 `none_observed=true` 的结构化记录（不得空文件）

### 3.9 post_run_summary.json（PostRunSummaryBuilder）

最小字段建议：

- `run_id`
- `result`：`completed/aborted/error`
- `timebox`
- `counts`：frame_count, tick_count, candidate_count, suppressed_count
- `assertions_status`：各断言 pass/fail/unknown
- `bridge_status`：哪些桥接完成、哪些仅最小占位
- `validator`：validator 路径 + 运行结果摘要（仅记录，不替代）

### 3.10 archive_manifest.json（ArchiveManifestBuilder）

按 `LUNA_REAL_SCENE_ARCHIVE_MANIFEST_SCHEMA_V0.md`：

- required_files 列表
- 每个文件 sha256（允许对大媒体文件做策略化处理，但必须声明）
- `archive_manifest.json` 本身不做自验 hash（遵循已修复规则）

## 4. Go/Conditional/No-Go（本桥接定义的判定）

### 4.1 GO（本定义可用）

满足：

- required_files 全覆盖且每个都有明确责任组件
- 明确 Mac-first；网页后置不阻塞
- v0 最小字段集不会与既有 RealScene contract 冲突
- 明确禁止生成伪 evidence、禁止 fixture 冒充 live

### 4.2 CONDITIONAL_GO

允许：

- `trace/replay/whitebox` 先以 bridge 最小字段落盘
- `a3_trace` 暂不桥接（但必须在 `post_run_summary.bridge_status` 里明确）

但必须：

- required_files 文件都存在且非空（risk_events 必须含 none_observed 行）
- 不影响现有 validator 对 required_files 的硬性检查

### 4.3 NO_GO

出现任一：

- required_files 缺失或无责任归属
- 计划用 fixture 冒充 controlled live
- 计划绕过/跳过 validator

