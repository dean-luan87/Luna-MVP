---
phase: Phase-DeviceEnv-004
title: Phone Web Camera Security and Network Boundary v0
status: BOUNDARY_FROZEN
version: v0
last_updated: 2026-04-24
scope: definition_only
side_effects_released_default: false
---

## 0. 目标

冻结 Phone/Web（手机浏览器）→ Mac 接收端 的网络、安全、隐私边界，确保后续实现不会引入“默认开放/公网暴露/无感采集/放权”。

本文件只定义，不实现。

## 1. 网络边界（写死）

- **默认只允许局域网访问**（同 Wi‑Fi 或手机热点）
- **禁止公网暴露服务**（不得对 0.0.0.0 公网端口开放；不得做端口映射/公网隧道作为默认路径）
- 建议实现阶段只 bind 到局域网网卡，或提供 allowlist（手机 IP）

## 2. HTTPS/HTTP 策略（v0）

- v0 允许 HTTP（局域网内）以降低复杂度
- HTTPS 作为后续增强（不得因 HTTPS 缺失而扩大其它风险边界）
- 手机端若因浏览器策略要求 HTTPS（部分 iOS/Safari 场景）：必须通过“本地自签证书 + 明示安装步骤”方式解决，禁止引入公网托管

## 3. 权限与可见性（写死）

手机端必须：

- 通过用户手势触发 getUserMedia
- 页面显著显示采集状态（started/running/stopped/aborted）
- 显示 run_id/session_id/entry_token（可显示摘要）
- 明示“受控采集，禁止进入隐私敏感区域”

禁止：

- 后台无感采集
- 页面隐藏采集状态

## 4. Session gate（写死）

- **Mac start session 是唯一入口**
- 未 start session 的任何 frame upload 必须拒绝
- session 超时必须拒绝或自动 stop/abort（必须写入 trace/summary 可审计）
- stop/abort 后必须拒绝一切后续上传

## 5. 限流与资源保护（写死）

Mac 接收端必须：

- frame upload rate limit（例如上限 fps 或每秒最大请求数）
- 单 session 最大帧数上限（与 timebox 对齐）
- archive_root 不可覆盖、不可复用（拒绝非空目录）

## 6. 隐私边界（写死）

- 禁止在隐私敏感区域采集
- 若进入隐私敏感区域或出现合规风险：必须 abort，并保全 archive（不得继续上传）
- risk_events 必须可记录 none_observed 或具体事件

## 7. 安全不变量（写死）

- candidate-only
- 不让手机端模型拿执行权
- 不输出强制导航指令
- 不开启默认路径
- 不扩大真实 side effects 面

