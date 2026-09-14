---
phase: Phase-DeviceEnv-004
title: Phone Web Controlled Live Archive Bridge Plan v0
status: PLAN_FROZEN
version: v0
last_updated: 2026-04-24
scope: definition_only
side_effects_released_default: false
---

## 0. 目标

定义：手机浏览器帧上传如何桥接到 **RealScene controlled_live archive_root required_files**（由 Mac 生成）。

本文件只定义，不实现、不生成 archive。

## 1. bridge 总览（写死）

1) Mac `Start Session` 创建 archive_root + 初始化 run_evidence（entry/人员/timebox/断言占位= true，待 stop/abort 完结）
2) 手机 `Upload Frame` → Mac 接收并写入：
   - `trace.jsonl`：frame_captured 事件
   - `replay.jsonl`：frame_ref（建议 v0 使用 `phone_web://session/<sid>#frame/<n>`）
3) Mac 在运行中/结束时写入最小：
   - `whitebox.jsonl`：candidate-only gates（可先最小）
   - `model_candidate_trace.jsonl`：若未调用模型也必须写 disabled/not_used
   - `output_candidate_trace.jsonl`：至少 silence/状态确认候选（allows_execute_now=false）
4) `Stop/Abort Session` 结束后写：
   - `operator_notes.md/json`（由 operator 提供）
   - `risk_events.jsonl`（无风险也必须 none_observed）
   - `post_run_summary.md/json`
   - `archive_manifest.json`（sha256；self-hash 规则同 Fix-001）
5) Mac 运行 validator 并把结果写入 post_run_summary（记录，不改变 validator 本体）

## 2. required_files（controlled_live，v0 必须）

必须生成：

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

## 3. run_evidence.json（controlled_live 必须字段要点）

除 Fix-001 既定字段外，本桥接明确新增/强调：

- `input_source = phone_web_camera`
- `controlled_live = true`（可显式字段，若沿用 Fix-001 口径则以 evidence_type=controlled_live 为准）
- `pending_real_sidewalk_run` 仅当“真实 Option A sidewalk run 已完成且 validator go”才允许为 false

写死不变量：

- no_execute_leakage_assertion=true
- no_default_on_assertion=true
- no_side_effect_expansion_assertion=true
- candidate-only（whitebox/output_candidate 必须体现 allows_execute_now=false）

## 4. frame_ref 与可回放策略（v0）

v0 允许事件级引用，但必须可追溯：

- `replay.jsonl.frame_ref = phone_web://session/<session_id>#frame/<frame_index>`
- `replay.jsonl` 必须同时记录：client_timestamp_ms + server_timestamp_ms（server 可写在 trace）

建议（不强制）在实现阶段提供：

- 可选的 `media/frames/` 或 `media/video`（用于增强回放与审计）

## 5. stop/abort 与证据完结规则（写死）

### stop

- 必须写：controlled_live_input_ended=true
- 生成 manifest + validator 可运行

### abort

- abort_triggered=true + abort_reason 非空
- archive_preserved=true
- stop 接收帧
- post_run_summary 必须解释：禁止立即重试（需 review）

