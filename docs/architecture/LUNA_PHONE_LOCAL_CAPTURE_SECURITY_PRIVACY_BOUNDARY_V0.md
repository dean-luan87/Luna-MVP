---
phase: Phase-DeviceEnv-004
title: Phone Local Capture Security and Privacy Boundary v0
status: BOUNDARY_FROZEN
version: v0
last_updated: 2026-04-24
scope: definition_only
side_effects_released_default: false
---

## 0. 目标

冻结 phone local capture 的安全与隐私边界，确保后续实现不会引入“后台无感采集/敏感区域采集/越权执行/默认上传”。

本文件只定义，不实现。

## 1. 手动采集规则（写死）

- 只能 **手动开始**（必须用户手势/显式按钮）
- 必须 **手动停止** 或 **timebox 自动停止**
- 不允许后台无感采集
- 不允许常驻后台连续运行

## 2. 隐私敏感区域（写死禁止）

不允许采集：

- 卫生间/诊室/私人空间
- 明确禁止拍摄区域
- 未授权拍摄区域
- 任何隐私敏感区域（以 record_owner 判断为准）

若发生：

- 必须立即停止采集（abort_triggered=true）
- 在 risk_events 记录
- bundle 不得标为 ready（或标记为 fail/partial，具体由后续实现阶段策略，但必须可审计）

## 3. 默认上传与外传（写死禁止）

- 不允许默认自动上传
- 采集后必须由用户主动导出 bundle
- Mac 导入前必须用户显式确认

## 4. 执行权与放权（写死禁止）

- 手机端不得产生 execute/release/retry/reopen
- 手机端不得输出强制导航指令
- 手机端不得打开 release window
- 手机端不得绕过 Mac validator

## 5. 证据边界（写死）

- evidence_type 必须为 `phone_local_controlled_capture`
- controlled_live_stream 必须为 false
- 不得伪装成 controlled_live / mac_camera live input / recorded_video_replay

