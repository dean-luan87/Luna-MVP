---
phase: Phase-DeviceEnv-003
title: Mac Camera Controlled Live Archive Adapter Implementation v0
status: IMPLEMENTED_V0
version: v0
last_updated: 2026-04-22
side_effects_released_default: false
---

## 0. 本阶段定位

本阶段实现 **Mac Camera Controlled Live Archive Adapter v0**，目标是：

- 使用 **Mac 摄像头真实帧输入**（短 timebox）
- 产出符合 Fix-001 validator 的 `archive_root` required_files
- 调用 validator 验证（工具只验证，不运行 trial）

**明确不是**：开放真实用户测试 / full controlled trial / 产品发布 / 默认路径开启 / 模型放权 / 扩 Option A / 手机网页方案。

## 1. 实现入口与文件

### 1.1 核心实现

- `capabilities/device_env/mac_camera_archive_adapter_v0.py`
  - 输入：Mac 摄像头（OpenCV `CameraHandler`）
  - 输出：`archive_root/` required_files（Fix-001 兼容）
  - 约束：candidate-only，不产生执行权，不扩 side effects 面

### 1.2 CLI 入口

- `tools/run_mac_camera_controlled_live_archive_v0.py`

运行示例：

```bash
python3 tools/run_mac_camera_controlled_live_archive_v0.py \
  --archive-root <archive_root> \
  --operator-id <operator_id> \
  --safety-observer-id <safety_observer_id> \
  --record-owner-id <record_owner_id> \
  --timebox-ms <timebox_ms> \
  --camera-index 0 \
  --explicit-entry-token <entry_token>
```

入口硬约束：

- `archive_root` 必须为空目录或不存在（拒绝合并/覆盖 evidence）
- `explicit_entry_token` 必填（写入 `run_evidence.json`）
- `timebox_ms` 必填，且 v0 上限为 60_000ms（短运行）

### 1.3 Verifier

- `tools/verify_mac_camera_archive_adapter_v0.py`
  - 检查：缺参失败
  - 检查：摄像头不可用时不伪造 controlled_live archive（只写 `failed_run_report.json`）
  - 若本机摄像头可用：生成短 timebox archive 并跑 validator，要求 recommendation=go

## 2. required_files（Fix-001 兼容）

成功路径必须生成以下文件（与 validator `REQUIRED_RELATIVE_FILES_V0` 对齐）：

- `run_evidence.json`
- `trace.jsonl`
- `replay.jsonl`
- `whitebox.jsonl`
- `model_candidate_trace.jsonl`
- `output_candidate_trace.jsonl`
- `operator_notes.md`
- `risk_events.jsonl`（首行允许 `risk_events_status=none_observed`）
- `post_run_summary.md`
- `archive_manifest.json`

## 3. 失败路径（摄像头不可用 / 无帧）规则

若摄像头无法打开或 timebox 内未捕获任何帧：

- **不得生成**上述 required_files（不得伪装成 controlled_live evidence archive）
- 允许生成：`failed_run_report.json`（用于明确失败原因与 pending 状态）
- CLI 返回非 0 退出码

## 4. 安全与治理不变量（写死）

- candidate-only：不产生任何可执行命令
- `no_execute_leakage_assertion=true`
- `no_default_on_assertion=true`
- `no_side_effect_expansion_assertion=true`
- 不进入 full controlled trial，不开启 default-on，不扩大 side effects 面

## 5. Validator 对接

建议在生成真实 `archive_root` 后运行：

```bash
python3 tools/validate_controlled_live_evidence_collection_execution_v0.py --archive_root <archive_root>
```

目标：summary.recommendation == `go`。

