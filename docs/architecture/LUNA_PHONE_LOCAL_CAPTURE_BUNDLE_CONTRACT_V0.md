---
phase: Phase-DeviceEnv-004
title: Phone Local Capture Bundle Contract v0
status: CONTRACT_FROZEN
version: v0
last_updated: 2026-04-24
scope: definition_only
---

## 0. 目的

冻结 phone local capture 的 bundle 目录结构、必需文件、字段与校验要求。

本合同只定义，不实现，不产生 bundle。

## 1. bundle 目录结构（v0）

建议 bundle 根目录：

```
phone_capture_bundle/
  bundle_manifest.json
  capture_metadata.json
  device_info.json
  capture_summary.json
  operator_notes.md (或 operator_notes.json)
  risk_events.jsonl
  media/
    video.mp4
    # 或 frames/ (可选实现形态)
```

## 2. bundle required_files（v0 必须）

bundle 必须至少包含：

- `bundle_manifest.json`
- `capture_metadata.json`
- `device_info.json`
- `capture_summary.json`
- `operator_notes.md` 或 `operator_notes.json`
- `risk_events.jsonl`（无风险也必须写 none_observed，不得缺文件）
- `media/video.mp4` 或 `media/frames/*`（至少一种）

## 3. capture_metadata.json（v0 必须字段）

必须包含：

- `bundle_id`
- `run_id`
- `evidence_type = phone_local_controlled_capture`
- `input_source = phone_local_camera`
- `controlled_live_stream = false`
- `phone_local_capture = true`
- `selected_option = OptionA_sidewalk_short_walk_observe`
- `scenario_id = sidewalk_short_walk_observe_v0`
- `explicit_trial_intent = true`
- `entry_token`
- `capture_started = true`
- `capture_ended = true`
- `start_time_ms`
- `end_time_ms`
- `duration_ms`
- `timebox_ms`
- `operator_id`
- `safety_observer_id`
- `record_owner_id`
- `device_id_or_label`
- `camera_facing`（environment/user）
- `media_type`（video/frames）
- `media_path`（相对 bundle 根）
- `privacy_area_checked = true`
- `environment_allowed = true`
- 安全断言（必须 true）：
  - `no_execute_leakage_assertion=true`
  - `no_default_on_assertion=true`
  - `no_side_effect_expansion_assertion=true`
- `abort_triggered`（bool）
- `abort_reason`（abort_triggered=true 时必须非空）
- `fallback_triggered`（bool）
- `degraded_triggered`（bool）
- `pending_mac_import = true`

## 4. bundle_manifest.json（v0 必须字段）

必须包含：

- `manifest_id`
- `bundle_id`
- `generated_at_ms`
- `required_files`（数组）
- `file_hashes`（map：相对路径 → sha256）
- `missing_files`（数组）
- `hash_mismatches`（数组）
- `integrity_status`（pass/partial/fail）
- `bundle_ready`（bool；仅当 integrity_status=pass 才允许 true）

要求：

- required_files 中列出的每个文件都必须在 `file_hashes` 中有 hash
- 任一关键文件缺失 → integrity_status=fail
- 任一 hash mismatch → integrity_status=fail

## 5. risk_events.jsonl（强制规则）

- 文件必须存在
- 若无风险事件：也必须至少 1 行：
  - `risk_events_status = none_observed`

