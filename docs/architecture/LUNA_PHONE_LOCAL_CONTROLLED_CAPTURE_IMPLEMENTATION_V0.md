---
phase: Phase-DeviceEnv-005
title: Phone Local Controlled Capture Bundle Implementation v0
status: IMPLEMENTED_V0
version: v0
last_updated: 2026-04-24
scope: v0_mac_side_builder_and_import
side_effects_released_default: false
---

## 0. 本阶段定位

本阶段实现 **phone_local_controlled_capture** 的最小闭环：

手机端（v0）：

- 使用系统相机拍摄视频（不实现手机端 runtime）
- 通过任意方式把视频文件传回 Mac（不实现实时上传）

Mac 端（v0）：

- 基于视频文件生成 bundle（metadata/notes/risk/device_info/summary/manifest）
- 校验 bundle（bundle_valid）
- 导入 bundle 生成 archive_root（archive_valid）
- 校验 archive（archive manifest/hash + evidence_type 边界 + required_files）

明确不是：

- 实时 Phone→Mac 上传
- controlled_live_stream
- full controlled trial / 开放用户测试
- 默认路径开启 / side effects 扩张 / 模型放权 / 手机端执行决策

## 1. v0 采用的实现路线（写死）

### 方案 A：手机拍视频 + Mac bundle builder（v0）

1) Phone：系统相机拍摄视频（人行道短距离、合规环境）
2) Transfer：将 `video.mp4` 传到 Mac
3) Mac：运行 bundle builder 生成 `phone_capture_bundle/`
4) Mac：运行 bundle validator 确认 bundle_ready
5) Mac：运行 import tool 生成 archive_root

## 2. 实现文件与入口

### 2.1 核心能力模块

- `capabilities/device_env/phone_local_capture_bundle_v0.py`
  - build bundle
  - validate bundle
  - import bundle → archive_root
  - validate archive_root

### 2.2 CLI 工具

- `tools/build_phone_local_capture_bundle_v0.py`
- `tools/validate_phone_local_capture_bundle_v0.py`
- `tools/import_phone_local_capture_bundle_v0.py`
- `tools/verify_phone_local_capture_bundle_v0.py`

## 3. 证据类型边界（实现级强约束）

### 3.1 bundle

- `capture_metadata.json.evidence_type = phone_local_controlled_capture`
- `controlled_live_stream = false`
- `phone_local_capture = true`

### 3.2 archive_root（import 生成）

- `run_evidence.json.evidence_type = phone_local_controlled_capture`
- 禁止改写为 `controlled_live`
- 必须保留：
  - `source_bundle_id`
  - `source_bundle_manifest_path`

## 4. 最小使用示例（v0）

### 4.1 build bundle

```bash
python3 tools/build_phone_local_capture_bundle_v0.py \
  --video-path /path/to/phone_video.mp4 \
  --bundle-root logs/phone_bundle_$(date +%Y%m%d_%H%M%S) \
  --operator-id dean \
  --safety-observer-id observer \
  --record-owner-id dean \
  --entry-token entry_$(date +%s) \
  --timebox-ms 30000
```

### 4.2 validate bundle

```bash
python3 tools/validate_phone_local_capture_bundle_v0.py --bundle-root <bundle_root>
```

### 4.3 import bundle → archive_root

```bash
python3 tools/import_phone_local_capture_bundle_v0.py \
  --bundle-root <bundle_root> \
  --archive-root logs/phone_archive_$(date +%Y%m%d_%H%M%S)
```

### 4.4 verify（A–L）

```bash
python3 tools/verify_phone_local_capture_bundle_v0.py
```

## 5. 边界声明

- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 本阶段实现的是 phone_local_controlled_capture（bundle→import→archive→validator），不等价于 controlled_live

