---
phase: Phase-DeviceEnv-004
title: Phone Local Capture Mac Import Contract v0
status: CONTRACT_FROZEN
version: v0
last_updated: 2026-04-24
scope: definition_only
side_effects_released_default: false
---

## 0. 目标

定义 Mac 端如何导入 phone capture bundle、转换为 archive_root，并保持 evidence_type 与边界不混淆。

本合同只定义，不实现。

## 1. 导入前置条件（写死）

Mac import 必须：

- 用户显式确认导入（不能自动后台导入）
- 校验 bundle_manifest.json：
  - required_files 完整
  - sha256 hash 全部匹配
  - integrity_status=pass 且 bundle_ready=true
- 校验 capture_metadata.json 的硬边界字段：
  - evidence_type=phone_local_controlled_capture
  - controlled_live_stream=false
  - phone_local_capture=true

若任一失败：必须拒绝导入（不得生成伪 archive_root）。

## 2. 导入后的 archive_root（必须由 Mac 生成）

Mac 导入后生成 archive_root，并必须生成 RealScene required_files（与 Fix-001 file set 对齐）：

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

## 3. 导入后 run_evidence.json 的边界（写死）

Mac 生成的 `run_evidence.json` 必须包含：

- `evidence_type = phone_local_controlled_capture`
- `input_source = phone_local_camera`
- `controlled_live_stream = false`
- `phone_local_capture = true`
- `imported_on_mac = true`
- `archive_generated_from_phone_bundle = true`
- `source_bundle_id`
- `source_bundle_manifest_path`（相对或绝对均可，但必须可追溯）

并且必须保留 Option A 语义：

- `selected_option = OptionA_sidewalk_short_walk_observe`
- `scenario_id = sidewalk_short_walk_observe_v0`

关于 `pending_real_sidewalk_run`：

- 本阶段不授予“自动置 false”的权限
- 默认必须保持 `pending_real_sidewalk_run` 不被误改（建议：仍为 true，除非后续治理明确允许在 phone_local 模式下置 false）

禁止：

- 将 evidence_type 改写为 `controlled_live`
- 将 phone bundle 伪装成 Mac live input
- 丢失 source_bundle_id 或丢失对原始 media 的引用

## 4. media 引用规则（写死）

导入后 archive 必须：

- 引用或复制原始 media（video/frames）到 archive_root 可追溯位置
- replay.jsonl 必须能追溯回：
  - source bundle
  - 原始 media
  - frame_index / timestamp

实现可选策略（后续实现阶段决定）：

- “复制 media 到 archive_root/media/ …”
- 或 “archive_root 仅引用 bundle 路径 + hash”（但必须防止 bundle 被篡改；需要强制 bundle_manifest 作为证据链一部分）

## 5. validator 规则（写死）

Mac import 完成后必须运行 validator，并在 post_run_summary 中记录：

- bundle 校验结果
- import 结果
- archive validator 结果（go/conditional_go/no_go + blockers）

