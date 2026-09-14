---
phase: Phase-DeviceEnv-002
title: Controlled Live Adapter Responsibility Matrix v0
status: DEFINITION_FROZEN
version: v0
last_updated: 2026-04-22
scope: definition_only
side_effects_released_default: false
---

## 0. 目的

将 RealScene `archive_root` required_files 与最小 bridge adapters 做一一映射，确保：

- **每个 required file 都有明确责任组件**
- **v0 必须实现 vs 可最小占位** 分界清晰
- 失败处理与禁止事项（不跑真实 run、不造假）写死

## 1. 适配器列表（v0）

### 1.1 输入与落盘链（v0 必须有责任）

- `CameraInputAdapter`（Mac-first）
- `RunEvidenceBuilder`
- `TraceBridge`
- `ReplayBridge`
- `WhiteboxEmitter`
- `ModelCandidateTraceEmitter`
- `OutputCandidateTraceEmitter`
- `OperatorNotesCollector`
- `RiskEventsLogger`
- `PostRunSummaryBuilder`
- `ArchiveManifestBuilder`

### 1.2 Web/Phone 候选（不在 v0 实现）

- `WebCameraInputAdapter`（getUserMedia）
- `WebFrameUploadBridge`（HTTP 上传→frame event）

## 2. Required Files × Adapter 责任矩阵（v0 冻结）

| required file / artifact | 责任 adapter | 输入 | 输出 | v0 必须实现？ | v0 最小允许形态（不造假前提下） | 失败处理（v0） |
|---|---|---|---|---|---|---|
| `run_evidence.json` | `RunEvidenceBuilder` | run 元信息、timebox、人员、断言结果、文件路径 | 结构化 JSON | **必须** | 必须包含 `run_id/mode/option/assertions/files/pending=false`（真实 run 才能为 false） | 若真实 run 未发生：必须标记 `pending_real_device_run=true`，并 **阻断进入 RealScene 扩展** |
| `trace.jsonl` | `TraceBridge` | frame/tick/event 流 | JSONL | **必须** | bridge trace：ENTRY/FRAME/TICK/EXIT/ERROR 最小事件集；可附 `source_trace` | 不得缺文件；写入失败应在 `post_run_summary` 记录并判定 no_go |
| `replay.jsonl` | `ReplayBridge` | frame_ref + ts + seq | JSONL | **必须** | 最小记录帧序号+时间戳+引用；可先不落盘全部帧，但必须可追溯引用策略 | 若无法给出可追溯引用：标记 hard blocker，判定 conditional_go 或 no_go（由 validator 要求决定） |
| `whitebox.jsonl` | `WhiteboxEmitter` | 关键内部状态、候选/抑制/门禁 | JSONL | **必须** | 最小字段：`ts/run_id/tick_seq/gates/suppression`；候选可为空数组但必须解释 | 缺失或空文件：no_go |
| `model_candidate_trace.jsonl` | `ModelCandidateTraceEmitter` | 模型 shadow 调用点或禁用原因 | JSONL | **必须** | 即便未调用模型也必须写：`MODEL_SHADOW_DISABLED` / `NO_MODEL_CANDIDATE` | 缺失：no_go |
| `output_candidate_trace.jsonl` | `OutputCandidateTraceEmitter` | 输出候选、抑制、时窗判定 | JSONL | **必须** | 即便全程 silence 也必须写：`OUTPUT_SILENCE`（含原因） | 缺失：no_go |
| `operator_notes/*` | `OperatorNotesCollector` | 人工填写/模板 | 文件/目录 | **必须** | 目录存在 + 至少 1 文件；允许模板未填满但必须包含“none_observed/aborted”等关键句 | 缺失：no_go |
| `risk_events.jsonl` | `RiskEventsLogger` | 人工/系统风险事件 | JSONL | **必须** | 无风险也必须 1 行：`none_observed=true` | 缺失或空：no_go |
| `post_run_summary.json` | `PostRunSummaryBuilder` | 全部产物路径、计数、断言状态、bridge 状态 | JSON | **必须** | 最小字段：`run_id/result/counts/assertions_status/bridge_status` | 缺失：no_go |
| `archive_manifest.json` | `ArchiveManifestBuilder` | archive_root 文件树 | JSON | **必须** | required_files 全覆盖 + sha256；manifest 自身不做自验 hash | 缺失：no_go |
| `media/frames/*`（可选） | `CameraInputAdapter` + `ReplayBridge` | 原始帧 | jpg/png 或编码视频 | 可选（策略化） | v0 可只做引用，但必须在 replay/manifest 里声明策略 | 若策略导致 replay 不可追溯：升级为 hard blocker |

## 3. 关键不变量（v0 写死）

- **candidate-only**：所有 emitter 只能写“候选/解释”，不得写“执行命令”。
- **side_effects_released 默认 false**：不得在 adapter 中引入任何“默认放权”。
- **不生成伪 archive**：任何自动生成内容都必须来自真实 run 的真实输入；若未 run，必须标明 pending，且不得伪造 required_files 为“已完成态”。

## 4. Mac-first 实施切分（DeviceEnv-003 的 v0 最小可交付）

### 4.1 DeviceEnv-003 v0 必须实现（最小闭环）

- `CameraInputAdapter`（Mac 摄像头真实帧）
- `RunEvidenceBuilder`
- `TraceBridge`（bridge trace 最小事件集）
- `ReplayBridge`（至少 frame_ref/ts/seq）
- `WhiteboxEmitter`（最小 gates/suppression）
- `ModelCandidateTraceEmitter`（至少禁用/未调用说明）
- `OutputCandidateTraceEmitter`（至少 silence/候选说明）
- `RiskEventsLogger`（none_observed）
- `OperatorNotesCollector`（模板落盘）
- `PostRunSummaryBuilder`
- `ArchiveManifestBuilder`

### 4.2 DeviceEnv-003 v0 可延期（不阻塞，但必须记录）

- 桥接 `a3_trace.jsonl` → `trace.jsonl` 的完整字段映射
- 记录所有帧到 `media/frames/`（可先策略化为“引用编码视频 + 映射表”）

## 5. 本阶段判定（Phase-DeviceEnv-002）

当且仅当：

- **Mac-first 决策冻结**
- **required_files 全覆盖且责任归属明确**
- **DeviceEnv-003 v0 最小可交付定义清晰**

则本阶段建议判定为 **GO**。

