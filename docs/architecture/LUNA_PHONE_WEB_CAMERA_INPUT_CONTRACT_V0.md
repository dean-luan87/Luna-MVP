---
phase: Phase-DeviceEnv-004
title: Phone Web Camera Input Contract v0
status: CONTRACT_FROZEN
version: v0
last_updated: 2026-04-24
scope: definition_only
---

## 0. 目标

冻结手机浏览器侧“摄像头采集与上传”的输入合同（字段、状态机、禁止事项）。

本合同只定义，不实现。

## 1. 角色与禁止事项（写死）

- device_role = `phone_camera_input`

禁止：

- 手机端直接写 `archive_manifest.json`
- 手机端直接写 `run_evidence.json` 最终结论/最终断言
- 手机端生成 execute/release/retry/reopen 语义
- 手机端输出强制导航指令
- 手机端绕过 Mac session start 直接上传

## 2. 输入字段合同（v0 必须包含）

### 2.1 session/run 标识

- `session_id`（由 Mac start session 返回）
- `run_id`（由 operator 在 Mac start session 时提交；手机端只回传）
- `entry_token`（由 operator 在 Mac start session 时提交；手机端只回传）

### 2.2 固定边界字段（必须回传，且值必须匹配 session）

- `device_role = phone_camera_input`
- `evidence_type = controlled_live`
- `controlled_live = true`
- `input_source = phone_web_camera`
- `selected_option = OptionA_sidewalk_short_walk_observe`
- `scenario_id = sidewalk_short_walk_observe_v0`

### 2.3 frame 上传字段（每帧）

- `frame_index`（单调递增，从 1 开始）
- `client_timestamp_ms`
- `upload_timestamp_ms`（由 Mac 接收端填充；手机端可不填）
- `image_format`：`jpeg` 或 `webp`（二选一；实现阶段定）
- `frame_blob`（二进制）
- `frame_width`
- `frame_height`
- `camera_facing`：`environment` 或 `user`

### 2.4 capture 状态机字段

- `capture_state`：`started` | `running` | `stopped` | `aborted`

## 3. getUserMedia 约束（定义级）

必须：

- 明示用户正在采集（页面显著提示）
- 必须通过用户手势启动采集（避免后台无感）
- 优先 `environment`（后置），失败回退 `user`

## 4. 采样与限流（合同级）

手机端必须支持（由实现阶段选择参数）：

- 采样间隔（例如每 200–500ms 一帧）
- 最大上传频率上限（配合 Mac 限流）

## 5. 隐私边界（手机端必须声明）

手机端 UI 必须显示：

- 当前 `run_id / session_id / entry_token`（只显示摘要亦可）
- 当前 `capture_state`
- 明确“仅局域网/仅受控试验，禁止进入隐私敏感区域采集”

