---
phase: Phase-DeviceEnv-004
title: Phone Local Capture Archive Bridge Plan v0
status: PLAN_FROZEN
version: v0
last_updated: 2026-04-24
scope: definition_only
side_effects_released_default: false
---

## 0. 目标

定义：phone local capture bundle 如何桥接到 RealScene archive_root required_files（由 Mac import 生成）。

本文件只定义，不实现、不生成 archive。

## 1. 两段校验（写死）

### 1.1 bundle_valid（手机端产物自洽）

由 Mac 在导入前校验：

- bundle_manifest integrity_status=pass
- required_files 完整
- file_hashes 全部匹配
- capture_metadata 边界字段正确（evidence_type / input_source / controlled_live_stream=false）

### 1.2 archive_valid（Mac 侧归档可复审）

由 Mac 导入后生成 archive_root 并运行 archive validator：

- required_files complete
- archive_manifest hash pass
- evidence_type 不被误标为 controlled_live
- 三断言 true

## 2. bundle → archive 的字段映射（v0）

### 2.1 run_evidence.json（Mac 生成）

来源：

- `capture_metadata.json`（bundle）
- `bundle_manifest.json`（bundle）
- 导入时刻的 Mac 时间戳

必须写入（关键差异点）：

- evidence_type = phone_local_controlled_capture
- input_source = phone_local_camera
- controlled_live_stream = false
- phone_local_capture = true
- source_bundle_id
- source_bundle_manifest_path
- imported_on_mac = true
- archive_generated_from_phone_bundle = true

同时保留 Option A 字段：

- selected_option = OptionA_sidewalk_short_walk_observe
- scenario_id = sidewalk_short_walk_observe_v0

并保持：

- pending_real_sidewalk_run 不被误改（本阶段不授权置 false）

### 2.2 trace.jsonl / replay.jsonl

最小要求：

- trace：run_started / bundle_verified / import_started / media_indexed / run_completed(or failed) / safety assertion event
- replay：frame_index + timestamp + frame_ref

frame_ref v0 建议：

- `phone_local://bundle/<bundle_id>#frame/<n>`（若为 frames）
- `phone_local://bundle/<bundle_id>#video/<filename>#frame/<n>`（若为 video + frame index）

### 2.3 whitebox/model/output

最小 gate（必须）：

- candidate_only=true
- default_path_disabled=true
- allows_execute_now=false
- model_execution_authority=false
- full_controlled_trial=false

### 2.4 operator_notes / risk_events / post_run_summary

规则：

- 从 bundle 导入（notes/risk_events）并在 archive 里保留一份
- risk_events 若无：必须 none_observed（bundle 与 archive 均不得缺文件）
- post_run_summary 需记录：bundle_valid 结果 + archive_valid 结果 + validator 输出摘要

## 3. 禁止事项（写死）

- 任何情况下不得将 phone_local_capture 导入结果标为 `controlled_live`
- 不得丢失 source_bundle_id
- 不得丢失对原始 media 的可追溯引用

