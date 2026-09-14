---
phase: Phase-DeviceEnv-004
title: Phone Local Controlled Capture Bundle Definition v0
status: DEFINITION_FROZEN
version: v0
last_updated: 2026-04-24
scope: definition_only
side_effects_released_default: false
---

## 0. 本阶段定位（只定义，不实现）

本阶段只做一件事：定义 **Phone Local Controlled Capture Bundle** 的证据结构与边界：

- 手机出门在真实场景中本地受控采集，形成 bundle
- 回到 Mac 后由 Mac 导入 bundle → 生成 RealScene archive_root → 运行 validator

禁止（写死）：

- 不写手机端采集 runtime
- 不写 Mac 导入 runtime
- 不执行真实采集
- 不生成 archive_root
- 不伪造 evidence
- 不做实时 Phone→Mac 上传
- 不做公网 tunnel/VPN/ngrok/cloudflare tunnel
- 不做原生 App
- 不做后台无感采集
- 不进入 full controlled trial / 不开放用户测试 / 不开启 default-on / 不扩大 side effects / 不放权

## 1. 新证据类型（写死）

定义新的 evidence_type：

- `evidence_type = phone_local_controlled_capture`

它不是：

- controlled_live_stream（实时流式）
- Mac camera live input
- recorded_video_replay
- fixture

它是：

- 手机端按受控流程采集 “本地媒体 + 元数据 + notes + risk events”
- Mac 端导入后生成 archive_root（Mac 侧负责 required_files + manifest + validator）

## 2. 必须写死的边界（不可混淆）

- phone_local_controlled_capture **不能冒充**：
  - `controlled_live`（Mac live 或实时手机上传）
  - `recorded_video_replay`
- 不能自动把 `pending_real_sidewalk_run` 改为 false（本阶段不授权这一语义）
- 后续实现阶段必须区分：
  - `bundle_valid`（bundle 自洽、hash pass）
  - `archive_valid`（导入后 archive_root validator pass）

## 3. 总体流程（定义级）

1) Phone 端：手动开始采集 → timebox 或手动停止 → 生成 bundle（含 manifest）
2) Phone 端：用户主动导出 bundle（无默认上传）
3) Mac 端：用户显式确认导入 → Mac 校验 bundle manifest/hash → 生成 archive_root → 运行 validator

## 4. 本阶段交付物

- bundle 定义与 contract（目录结构/字段/校验）
- Mac import contract（导入规则与边界保真）
- archive bridge plan（bundle → archive_root required_files）
- 安全/隐私边界（手动开始/停止、敏感区域禁止、无后台采集）
- 测试矩阵
- go/no-go pack（定义阶段判定）
- README 索引更新

