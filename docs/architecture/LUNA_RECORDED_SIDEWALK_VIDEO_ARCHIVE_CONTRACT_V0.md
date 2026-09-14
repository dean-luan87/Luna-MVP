---
phase: Phase-RealSceneReplay-001
title: Recorded Sidewalk Video Replay Archive Contract v0
status: CONTRACT_FROZEN
version: v0
last_updated: 2026-04-24
scope: recorded_video_replay_only
side_effects_released_default: false
---

## 0. 目的

冻结 recorded sidewalk/real-world 视频的 **recorded_video_replay** 证据归档合同（archive_root 形态 + `run_evidence.json` 字段 + 安全边界）。

## 1. 硬边界字段（必须可机器校验）

- `run_evidence.json.evidence_type = recorded_video_replay`
- `run_evidence.json.controlled_live = false`
- `run_evidence.json.pending_real_sidewalk_run = true`
- `run_evidence.json.input_source = recorded_video`
- **禁止** `evidence_type=controlled_live`

## 2. required_files（v0 必须全部生成）

archive_root 下必须包含（与 controlled live 相同的“文件集合”，但字段语义不同）：

- `run_evidence.json`
- `trace.jsonl`
- `replay.jsonl`
- `whitebox.jsonl`
- `model_candidate_trace.jsonl`
- `output_candidate_trace.jsonl`
- `operator_notes.md`
- `risk_events.jsonl`（无风险也必须写 `risk_events_status=none_observed`）
- `post_run_summary.md`
- `archive_manifest.json`

## 3. run_evidence.json（v0 字段最小集）

必须包含：

- `run_id`
- `scenario_id = recorded_sidewalk_video_replay_v0`
- `selected_option = OptionA_sidewalk_short_walk_observe_replay`
- `evidence_type = recorded_video_replay`
- `controlled_live = false`
- `pending_real_sidewalk_run = true`
- `input_source = recorded_video`
- `video_path`（原视频路径）
- `video_filename`
- `video_duration_ms`（可为 `null` 或 `unknown`，但必须有字段）
- `frame_count`（原视频帧数可获取则填，否则 `null`）
- `sampled_frame_count`（本次写入 replay/trace 的抽帧数）
- `operator_id`
- `record_owner_id`
- `start_time_ms`
- `end_time_ms`
- `duration_ms`

文件路径字段（必须存在且非空）：

- `trace_file_path`
- `replay_file_path`
- `whitebox_file_path`
- `model_candidate_trace_path`
- `output_candidate_trace_path`
- `operator_notes_path`
- `risk_events_path`
- `archive_manifest_path`
- `post_run_summary_path`

安全断言（必须全部为 true）：

- `no_execute_leakage_assertion=true`
- `no_default_on_assertion=true`
- `no_side_effect_expansion_assertion=true`

run 状态字段（必须存在）：

- `overall_run_status`（completed / failed）

## 4. trace/replay 最小要求

### 4.1 trace.jsonl

至少包含事件：

- `run_started`
- `video_opened`
- `frame_sampled`（多条）
- `run_completed` 或 `run_failed`
- `no_execute_leakage_assertion`（事件）

### 4.2 replay.jsonl

至少包含字段：

- `frame_index`
- `timestamp_ms`（基于视频时间或抽样时间）
- `frame_ref`
- `input_source=recorded_video`
- `replay_available=true`

frame_ref v0 允许：

- `recorded_video://<video_filename>#frame/<N>`
- 或 `video_path + frame_index`（以字段表示，不强制落盘帧图片）

## 5. whitebox/model/output（最小要求）

必须明确：

- `candidate_only=true`
- `default_path_disabled=true`
- `model_execution_authority=false`
- `allows_execute_now=false`
- `full_controlled_trial=false`

## 6. manifest（必须）

`archive_manifest.json` 必须列出 required_files，并对每个文件计算 sha256，满足：

- `missing_files=[]`
- `hash_mismatches=[]`
- `integrity_status=pass`

