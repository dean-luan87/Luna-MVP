# Phase-DeviceEnv-001 — Option A Controlled Live Device Setup Checklist v0（设备/系统准备清单冻结）

**目的**：列出 Option A 开跑前必须满足的设备/系统/路径/权限/人员 checklist。任一不满足：继续 pending，不得开跑。  

---

## 1) 设备与输入源

- `camera_input_available=true`
- `camera_permission_granted=true`
- `camera_preview_ok=true`（能看到实时画面）

---

## 2) 运行环境

- `runtime_environment_available=true`（设备端或笔记本端可执行）
- `python3_available=true`（用于 validator）
- `repo_accessible=true`（能拷贝 archive_root 到本仓库或能在同环境运行 validator）

---

## 3) 归档与写权限

- `archive_root_configured=true`（例如 `runs/controlled_live/option_a/<run_id>/`）
- `write_permission_ready=true`（能写入 required_files）
- `disk_space_sufficient=true`（最小可用空间足够）

---

## 4) 采集开关（必须）

- `replay_capture_enabled=true`（真实 run 仍必须可回放）
- `trace_capture_enabled=true`
- `whitebox_capture_enabled=true`

---

## 5) 人员与监督

- `operator_id_configured=true`
- `safety_observer_id_configured=true`
- `record_owner_id_configured=true`
- `operator_present=true`
- `safety_observer_present=true`
- `record_owner_present=true`

---

## 6) Timebox 与中止

- `timebox_configured=true`
- `abort_key_or_abort_method_ready=true`（操作员与观察员均可中止）
- `abort_triggers_configured=true`

---

## 7) Validator 就绪

- `validator_available=true`
- `validator_command_ready=true`：
  - `python3 tools/validate_controlled_live_evidence_collection_execution_v0.py --archive_root "<archive_root>"`

---

## 8) 隐私与环境

- `privacy_area_checked=true`
- `environment_allowed=true`（白天、低人流、平整路段、短距离）
- `no_high_risk_area=true`
- `no_unauthorized_filming=true`

---

## 9) 边界断言（开跑前必须确认）

- `default_path_disabled=true`
- `full_controlled_trial=false`
- `side_effects_expansion=false`
- `model_execution_authority=false`
- `candidate_only=true`

