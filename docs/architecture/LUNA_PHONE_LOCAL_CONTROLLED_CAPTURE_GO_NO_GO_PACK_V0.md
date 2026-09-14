---
phase: Phase-DeviceEnv-004
title: Phone Local Controlled Capture Bundle Go/No-Go Pack v0
status: PACK
version: v0
last_updated: 2026-04-24
scope: definition_only
side_effects_released_default: false
---

## 0. 本 pack 的边界（写死）

本 pack 仅对 **Phone Local Controlled Capture Bundle Definition v0**（定义阶段）做 go/conditional_go/no_go 判定。

禁止：

- 不实现手机端采集 runtime
- 不实现 Mac 导入 runtime
- 不执行真实采集
- 不生成 archive_root
- 不伪造 evidence

## 1. 输入材料（本阶段交付物）

- Definition：`docs/architecture/LUNA_PHONE_LOCAL_CONTROLLED_CAPTURE_BUNDLE_DEFINITION_V0.md`
- Bundle Contract：`docs/architecture/LUNA_PHONE_LOCAL_CAPTURE_BUNDLE_CONTRACT_V0.md`
- Mac Import Contract：`docs/architecture/LUNA_PHONE_LOCAL_CAPTURE_MAC_IMPORT_CONTRACT_V0.md`
- Archive Bridge Plan：`docs/architecture/LUNA_PHONE_LOCAL_CAPTURE_ARCHIVE_BRIDGE_PLAN_V0.md`
- Security/Privacy Boundary：`docs/architecture/LUNA_PHONE_LOCAL_CAPTURE_SECURITY_PRIVACY_BOUNDARY_V0.md`
- Test Matrix：`docs/architecture/LUNA_PHONE_LOCAL_CAPTURE_TEST_MATRIX_V0.md`

## 2. 关键硬边界检查（定义级）

### 2.1 证据类型不混淆

已写死：

- evidence_type=phone_local_controlled_capture
- controlled_live_stream=false
- 不得冒充 controlled_live / recorded_video_replay / mac_camera_live

### 2.2 导入边界不漂移

已写死：

- Mac import 必须保留 source_bundle_id / source_bundle_manifest_path
- 禁止导入后改写 evidence_type=controlled_live
- pending_real_sidewalk_run 不得在本阶段自动置 false

### 2.3 隐私与权限边界

已写死：

- 手动开始/停止或 timebox 停止
- 禁止后台无感采集
- 禁止隐私敏感区域采集
- 禁止默认自动上传
- 禁止手机端生成 execute/release/retry/reopen

## 3. go / conditional_go / no_go 判定

### 3.1 判定：GO

满足：

- bundle definition 完整
- bundle contract 完整（required_files + capture_metadata + bundle_manifest）
- Mac import contract 完整（拒绝策略 + source 保真 + 不混淆）
- archive bridge plan 完整（bundle_valid / archive_valid 两段校验）
- security/privacy boundary 完整
- test matrix 覆盖 A–L
- 本阶段未实现 runtime、未执行采集、未生成 archive_root、未伪造 evidence

### 3.2 hard_blockers

无（定义阶段）。

### 3.3 soft_followups

可后置到实现阶段再定：

- media 形态选择：video vs frames
- iOS/Android 兼容性细节
- bundle 导出/导入的具体 UX（仍需显式确认）

## 4. recommended next phase

进入：

- **Phase-DeviceEnv-005：Phone Local Controlled Capture Bundle Implementation v0**

实现阶段才允许开始实现：

- 手机端本地采集（PWA/网页/系统相机+脚本等实现形态后定）
- bundle 生成与 manifest/hash
- Mac 导入、archive_root 生成、validator

## 5. 明确声明（边界重申）

- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled live run
- 本阶段只定义 Phone Local Controlled Capture Bundle，不实现

