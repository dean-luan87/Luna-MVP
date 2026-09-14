---
phase: Phase-DeviceEnv-002
title: Mac Camera Controlled Live Archive Adapter Implementation Plan v0
status: PLAN_FROZEN
version: v0
last_updated: 2026-04-22
scope: plan_only
side_effects_released_default: false
---

## 0. 本文件定位（强边界）

本文件属于 **Phase-DeviceEnv-002** 的交付物，只做下一阶段 **Phase-DeviceEnv-003** 的实现计划冻结：

- 不进入 DeviceEnv-003
- 不实现 Mac Camera Adapter
- 不执行真实 run
- 不生成任何 `archive_root`
- 不生成伪 evidence
- 不扩 Option A，不进入 full controlled trial
- 不开启默认路径，不扩大真实 side effects 面
- 不让模型获得执行权（candidate-only）

## 1. 下一阶段（DeviceEnv-003）阶段目标（仅规划）

### 1.1 DeviceEnv-003 要实现的最小交付（v0）

实现 **Mac Camera Controlled Live Archive Adapter v0**：

- 从 **Mac 摄像头真实帧输入**（OpenCV）产生 RealScene `archive_root` 的 required_files：
  - `run_evidence.json`
  - `trace.jsonl`
  - `replay.jsonl`
  - `whitebox.jsonl`
  - `model_candidate_trace.jsonl`
  - `output_candidate_trace.jsonl`
  - `operator_notes/`（至少 1 文件）
  - `risk_events.jsonl`（至少 1 行 `none_observed=true`）
  - `post_run_summary.json`
  - `archive_manifest.json`
- 以 **candidate-only** 方式记录：不产生执行权、不触发真实 side effects
- 能对接并通过现有 evidence validator（不得绕过）

### 1.2 DeviceEnv-003 明确不做（v0 非目标）

- 不做网页/手机方案
- 不做 full controlled trial
- 不要求产品级帧率/性能/稳定性
- 不要求完整 A3 trace 字段桥接
- 不要求全量视觉模型推理
- 不要求真实导航决策或任何“可执行”输出
- 不做情感表达/个性化语言

## 2. 输入依赖（DeviceEnv-003 允许使用的复用点）

### 2.1 复用输入源（已盘点）

- `../Luna-Core/utils/camera_handler.py`
- `../Luna-Core/check_camera.py`

### 2.2 契约与定义（不得修改）

- RealScene evidence contract（required_files、断言语义、validator 预期）
- `docs/architecture/LUNA_CONTROLLED_LIVE_ARCHIVE_BRIDGE_DEFINITION_V0.md`
- `docs/architecture/LUNA_CONTROLLED_LIVE_ADAPTER_RESPONSIBILITY_MATRIX_V0.md`
- Fix-001 证据链 validator：
  - `tools/validate_controlled_live_run_evidence_capture_v0.py`
  -（以及 RealSceneTrial-002 wrapper，如仍作为执行对接入口）

## 3. 建议新增实现文件（DeviceEnv-003 规划；本阶段不创建）

> 仅规划路径/职责，不在 DeviceEnv-002 落代码。

- `capabilities/device_env/mac_camera_archive_adapter_v0.py`
  - 负责：主编排（打开摄像头、timebox 循环、产出事件流、协调各 emitter/bridge）
- `tools/run_mac_camera_controlled_live_archive_v0.py`
  - 负责：命令行入口（参数校验、显式 entry、调用 adapter、退出码）
- `tools/verify_mac_camera_archive_adapter_v0.py`
  - 负责：对 `archive_root` 运行 validator（不生产数据，仅验证）
- `docs/architecture/LUNA_MAC_CAMERA_ARCHIVE_ADAPTER_IMPLEMENTATION_V0.md`
  - 负责：记录 DeviceEnv-003 实现细节与已知限制（实现后再写）

## 4. 运行入口设计（DeviceEnv-003 入口冻结）

下一阶段建议入口（示例）：

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

入口硬约束（建议写死在脚本参数校验中）：

- `--explicit-entry-token` 必填且必须被写入 `run_evidence.json`（防止“默认启动即采集”）
- `--timebox-ms` 必填且上限受控（防止无限采集）
- `--archive-root` 必须为空目录或允许创建（禁止覆盖已有 evidence）

## 5. DeviceEnv-003 v0 必须实现的 adapters（清单冻结）

- `CameraInputAdapter`
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

## 6. v0 可最小化的内容（允许最小，但不得破坏 validator）

允许最小化：

- `trace.jsonl`：先写 bridge trace（ENTRY/FRAME/TICK/EXIT/ERROR），不要求完整 A3 字段映射
- `whitebox.jsonl`：先写最小 gates/suppression/candidate 摘要字段
- `model_candidate_trace.jsonl`：未调用模型时写 `MODEL_SHADOW_DISABLED` / `NO_MODEL_CANDIDATE`
- `output_candidate_trace.jsonl`：全程 silence 时写 `OUTPUT_SILENCE` + 原因
- `replay.jsonl`：先保证 frame_seq/ts/frame_ref 可追溯，不要求全量帧落盘（但必须声明引用策略）

但必须满足（硬约束）：

- required_files **全部存在**
- `archive_manifest.json` sha256 可计算且符合 schema（manifest 自身不做自验 hash）
- `risk_events.jsonl` 至少 1 行 `none_observed=true`
- 三条安全断言为 true：
  - `no_execute_leakage=true`
  - `no_default_on=true`
  - `no_side_effect_expansion=true`
- 不出现 execute/default-on/side effects expansion
- evidence validator 可跑且可复现

## 7. 成功标准（DeviceEnv-003 完成条件）

DeviceEnv-003 v0 视为完成（GO）的条件：

- 能打开 Mac 摄像头；若失败，必须输出明确失败原因（权限/占用/索引/后端），并在 `post_run_summary` 记录
- 能在 timebox 内采集真实帧事件（至少 >0 帧）
- 能生成完整 `archive_root` required_files（全部存在且非空，符合最小字段要求）
- 能生成 `archive_manifest.json`（sha256 完整，且能被 validator 接受）
- 能通过 evidence validator（不得绕过）
- 全程不生成伪 evidence、不放权、不扩 scope

## 8. NO_GO 条件（DeviceEnv-003 任一出现即 no_go）

- 摄像头不可用且没有明确 pending/失败原因记录（“静默失败”）
- required_files 任一缺失或空文件（尤其 `risk_events.jsonl`）
- manifest hash 失败或 schema 不符合
- validator 失败且不可复现
- 安全断言任一为 false
- 用 fixture 冒充 live
- 输出触发 execute/default-on/side effects

## 9. 与 Phone/Web 候选路径的关系（写死）

- Phone/Web（getUserMedia）仅为后续候选
- 只有当 Mac-first 的 `archive_root` bridge 跑通并可被 validator 接受后，才进入 Phone/Web 适配
- 不做原生 App

