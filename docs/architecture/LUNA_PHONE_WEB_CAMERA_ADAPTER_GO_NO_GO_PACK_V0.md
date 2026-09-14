---
phase: Phase-DeviceEnv-004
title: Phone Web Camera Controlled Live Adapter Go/No-Go Pack v0
status: PACK
version: v0
last_updated: 2026-04-24
scope: definition_only
side_effects_released_default: false
---

## 0. 本 pack 的边界（写死）

本 pack 仅对 **DeviceEnv-004 定义阶段**做 go/conditional_go/no_go 判定。

禁止：

- 不实现 runtime
- 不执行 controlled live run
- 不生成 archive_root
- 不伪造 evidence

## 1. 输入材料（本阶段交付物）

- Definition：`docs/architecture/LUNA_PHONE_WEB_CAMERA_CONTROLLED_LIVE_ADAPTER_DEFINITION_V0.md`
- Phone Input Contract：`docs/architecture/LUNA_PHONE_WEB_CAMERA_INPUT_CONTRACT_V0.md`
- Mac Receiver Contract：`docs/architecture/LUNA_PHONE_WEB_CAMERA_MAC_RECEIVER_CONTRACT_V0.md`
- Archive Bridge Plan：`docs/architecture/LUNA_PHONE_WEB_CONTROLLED_LIVE_ARCHIVE_BRIDGE_PLAN_V0.md`
- Security & Network Boundary：`docs/architecture/LUNA_PHONE_WEB_CAMERA_SECURITY_AND_NETWORK_BOUNDARY_V0.md`
- Test Matrix：`docs/architecture/LUNA_PHONE_WEB_CAMERA_ADAPTER_TEST_MATRIX_V0.md`

## 2. 目标架构（冻结复述）

手机浏览器 getUserMedia 采集
→ HTTP 上传帧到 Mac（局域网）
→ Mac start session 为唯一入口
→ Mac 生成 controlled_live archive_root + manifest
→ Mac 运行 validator

## 3. 关键硬边界检查（定义级）

### 3.1 不能把 replay 当 controlled_live

- recorded_video_replay 与 controlled_live 的边界已写死（本阶段定义未混淆）

### 3.2 手机端不得越权

已写死：

- 手机端不得生成 run_evidence/manifest 最终结论
- 手机端不得输出强制导航指令
- 手机端不得放权/不得绕过 candidate-only

### 3.3 Mac 端唯一入口与拒绝策略

已写死：

- start session 是唯一入口
- 未 start 上传拒绝
- stop/abort 后上传拒绝
- 禁止 archive_root 覆盖/合并

### 3.4 网络安全边界

已写死：

- 默认局域网
- 禁止公网暴露
- 明示采集状态与 run/session 标识

## 4. go / conditional_go / no_go 判定

### 4.1 判定：GO

满足：

- Phone/Web 架构定义完整
- 手机输入合同完整
- Mac 接收端合同完整（含 4 个 API + 状态机 + 拒绝策略）
- archive bridge plan 覆盖 required_files 与完结规则（stop/abort）
- 安全/网络边界完整
- 测试矩阵覆盖 A–N 场景
- 本阶段未实现 runtime、未生成 archive、未伪造 evidence

### 4.2 hard_blockers

无（定义阶段）。

### 4.3 soft_followups

可后置到实现阶段再定：

- image_format 选型（jpeg vs webp）
- HTTP/HTTPS 策略细化（在不引入公网暴露前提下）
- UI 文案/展示细节

## 5. recommended next phase

进入：

- **Phase-DeviceEnv-005：Phone Web Camera Controlled Live Adapter Implementation v0**

注意：实现阶段仍须维持 candidate-only、默认路径禁用、局域网边界、严禁公网暴露。

## 6. 明确声明（边界重申）

- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled live run
- 本阶段只定义 Phone/Web camera adapter，不实现

