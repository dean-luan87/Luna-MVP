---
phase: Phase-DeviceEnv-004
title: Phone Web Camera Mac Receiver Contract v0
status: CONTRACT_FROZEN
version: v0
last_updated: 2026-04-24
scope: definition_only
side_effects_released_default: false
---

## 0. 目标

冻结 Mac 侧“接收手机帧上传 → 生成 controlled_live archive_root”的接收端合同（API、session 管理、拒绝策略、落盘职责）。

本合同只定义，不实现。

## 1. 角色与唯一权责（写死）

Mac 接收端必须负责：

- 创建 archive_root（唯一写入端）
- session start/stop/abort（唯一入口）
- 接收 frame uploads 并落盘为 frame events
- 生成 required_files：
  - `run_evidence.json`
  - `trace.jsonl`
  - `replay.jsonl`
  - `whitebox.jsonl`
  - `model_candidate_trace.jsonl`
  - `output_candidate_trace.jsonl`
  - `operator_notes.md/json`
  - `risk_events.jsonl`
  - `post_run_summary.md/json`
  - `archive_manifest.json`
- 运行 validator（Mac 端）

禁止：

- 允许手机端绕过 start session
- stop/abort 后继续接收帧
- 允许覆盖/合并已有 archive_root
- 允许公网暴露（默认仅局域网）

## 2. API 合同（v0 必须定义）

### 2.1 Start Session

`POST /api/controlled-live/session/start`

输入（JSON）：

- `run_id`
- `scenario_id`（必须 `sidewalk_short_walk_observe_v0`）
- `selected_option`（必须 `OptionA_sidewalk_short_walk_observe`）
- `entry_token`
- `operator_id`
- `safety_observer_id`
- `record_owner_id`
- `timebox_ms`

输出（JSON）：

- `allowed` (bool)
- `session_id`
- `upload_url`（frame upload endpoint）
- `archive_root`（只返回相对路径或句柄；避免泄露系统绝对路径）
- `reason_codes`（allowed=false 时必填）

硬校验（allowed=false）：

- 任一必填字段缺失/为空
- scenario/option 不匹配 Option A
- timebox 超限
- archive_root 非空或路径冲突

### 2.2 Upload Frame

`POST /api/controlled-live/frame`

输入（multipart/form-data 或二进制+header，具体实现阶段定）：

- `session_id`
- `run_id`
- `frame_index`
- `client_timestamp_ms`
- `image_format`（jpeg/webp）
- `frame_blob`
- `frame_width`/`frame_height`（可选：由 Mac 解码校验）
- `camera_facing`

输出（JSON）：

- `accepted` (bool)
- `frame_event_id`（accepted=true 时）
- `reason_codes`（accepted=false 时）

拒绝策略（accepted=false）：

- 未 start session
- session_id/run_id 不匹配
- stop/abort 后上传
- session 超时
- 超出 rate limit
- archive_root 不可写/落盘失败（应触发 abort）

### 2.3 Stop Session

`POST /api/controlled-live/session/stop`

输入（JSON）：

- `session_id`
- `run_id`
- `stop_reason`
- `operator_notes_ref`（可选：指向 notes 内容或上传）
- `risk_events_status`（例如 none_observed）

输出（JSON）：

- `stopped` (bool)
- `archive_root`
- `post_run_summary_ready` (bool)
- `manifest_ready` (bool)
- `validator_ready` (bool)

### 2.4 Abort Session

`POST /api/controlled-live/session/abort`

输入（JSON）：

- `session_id`
- `run_id`
- `abort_reason`

输出（JSON）：

- `aborted` (bool)
- `archive_preserved` (bool)
- `post_run_summary_ready` (bool)

## 3. Session 状态机（v0）

状态：

- `created` → `running` → `stopped`
- `created/running` → `aborted`

写死规则：

- `stopped/aborted` 后不得再接受 frame
- 超时自动 stop 或拒绝（实现阶段选择，但必须可审计）

## 4. controlled_live 证据字段写入（Mac 端写死）

`run_evidence.json` 必须写：

- evidence_type=`controlled_live`
- controlled_live=true
- input_source=`phone_web_camera`
- selected_option/scenario_id 固定为 Option A
- explicit_trial_intent=true
- entry_token
- mode_entry_event_present=true
- controlled_live_input_started/ended=true（基于 session 状态机）

以及三断言全部 true：

- no_execute_leakage_assertion
- no_default_on_assertion
- no_side_effect_expansion_assertion

