---
phase: Phase-DeviceEnv-004
title: Phone Web Camera Controlled Live Adapter Definition v0
status: DEFINITION_FROZEN
version: v0
last_updated: 2026-04-24
scope: definition_only
side_effects_released_default: false
---

## 0. 本阶段定位（只定义，不实现）

本阶段只做一件事：冻结 **Phone/Web（手机浏览器）摄像头作为真实 live input** 的 controlled live adapter 定义，使后续实现阶段可在不扩边界的前提下落地。

禁止（写死）：

- 不写 Phone/Web adapter runtime
- 不执行真实 controlled live run
- 不生成 archive_root
- 不伪造 evidence
- 不进入 full controlled trial
- 不开启默认路径
- 不扩大真实 side effects 面
- 不让模型拿执行权（candidate-only）
- 不做原生 App
- 不做 WebRTC 复杂流媒体

## 1. 目标架构（写死）

手机浏览器打开采集页面
→ `getUserMedia` 调用手机摄像头
→ 按帧/采样间隔通过 **HTTP** 上传到 Mac 本地服务
→ **Mac 接收帧事件并生成 controlled_live archive_root**
→ Mac 运行 validator 校验

必须写死：

- 手机端只做输入采集与上传（device_role=phone_camera_input）
- Mac 是唯一的：session start 入口、archive_root 生成端、validator 运行端
- 手机端不得绕过 session，不得写 manifest/run_evidence 最终结论，不得输出导航执行指令，不得放权

## 2. 与既有资产的关系（复用点）

- 既有手机端 getUserMedia 参考实现存在于：
  - `luna_frontend_package_24files/web_test_server/web_test_server.py`

本阶段不修改/不复用实现，只用于定义合同与边界。

## 3. 关键边界（必须可被机器验证）

- evidence_type：`controlled_live`
- input_source：`phone_web_camera`
- controlled_live：true
- selected_option：`OptionA_sidewalk_short_walk_observe`
- scenario_id：`sidewalk_short_walk_observe_v0`
- candidate-only：true（allows_execute_now=false / model_execution_authority=false）
- default_path_disabled：true

且必须：

- session 未 start → upload 必须拒绝
- stop/abort 后 → upload 必须拒绝
- 禁止公网暴露（默认仅局域网）

## 4. 交付物（DeviceEnv-004 必须产生）

- 手机端输入合同（字段、状态机、禁止事项）
- Mac 接收端合同（API、session 管理、限流、落盘边界）
- archive bridge plan（如何产出 required_files）
- 安全与网络边界（局域网、隐私、权限、HTTPS/HTTP 策略）
- 测试矩阵
- Go/No-Go pack（定义阶段判定）

