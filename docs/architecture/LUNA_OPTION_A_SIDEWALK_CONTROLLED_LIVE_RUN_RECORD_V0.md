---
phase: Phase-RealSceneRun-002A
title: Option A Sidewalk Controlled Live Run Record v0
status: RUN_RECORD
version: v0
last_updated: 2026-04-24
scope: option_a_only
side_effects_released_default: false
---

## 0. 真实执行状态（写死：不得伪造）

- pending_real_sidewalk_run: **true**

说明：

- 当前 workspace 环境无法代表“真实人行道短距离受控 run”的现场执行（需要线下人员与环境）。
- 本文件只记录：本次 run 尚未被真实执行；不得以 DeviceEnv-003 的室内/桌面摄像头采集冒充人行道 run。

## 1. 计划中的 run 元信息（待线下填写）

- operator_id: TBD
- safety_observer_id: TBD
- record_owner_id: TBD
- date_time_window: TBD
- location_summary: TBD（必须为低人流平整人行道，且无隐私敏感区域）
- timebox_ms: TBD（短时）
- input_source: mac_camera
- camera_index: 0 (default) / TBD
- explicit_entry_token: TBD

## 2. 现场执行结果（pending，待线下填写）

- run_executed: false
- archive_root_path: null
- run_id: null
- camera_opened: null
- frame_count: null
- abort_triggered: null
- abort_reason: null
- fallback_triggered: null
- degraded_triggered: null
- scope_drift_observed: null
- privacy_violation_observed: null

## 3. 证据与验证（pending）

- required_files_complete: null
- archive_manifest_integrity: null
- validator_recommendation: null
- hard_blockers: []
- soft_followups: []

## 4. 明确声明（边界）

- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未扩 Option A
- 未开放真实用户测试
- 本 run record 不包含任何伪造 evidence

