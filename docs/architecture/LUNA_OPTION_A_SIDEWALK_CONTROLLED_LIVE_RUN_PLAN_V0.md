---
phase: Phase-RealSceneRun-002A
title: Option A Sidewalk Controlled Live Run Plan v0
status: PLAN
version: v0
last_updated: 2026-04-24
scope: option_a_only
side_effects_released_default: false
---

## 0. 本阶段定位（边界写死）

本阶段执行 **Option A：人行道短距离 controlled live run**，使用 **Mac Camera evidence 链**，产出可复审 `archive_root`。

不是：开放真实用户测试 / full controlled trial / 产品发布 / 默认路径开启 / side effects 扩张 / 手机网页方案 / 徽章佩戴视角验证。

## 1. 唯一目标

在真实人行道短距离环境中（白天、低人流、平整）执行一次或少量短时 run，并产出：

- `archive_root` required_files 完整
- manifest hash 校验通过
- validator 输出 go 或 conditional_go
- 无 execute/default-on/side effects leakage
- scope 无漂移、无隐私违规

## 2. 唯一允许场景（Option A）

- 白天
- 低人流
- 平整人行道
- 短距离（严格 timebox）
- 操作员在场 + safety observer 在场 + record owner 在场
- candidate-only
- Mac 摄像头作为 controlled live input
- 可随时 abort

禁止：

- 过街/复杂路口/高密人流/夜间雨天/长距离连续
- 单人测试
- 隐私敏感区域/未授权拍摄区域

## 3. 人员与职责（写死）

- operator_id：负责启动/停止/监控/归档
- safety_observer_id：负责安全边界监控与强制中止
- record_owner_id：负责证据归属、隐私合规、归档保全

## 4. 运行输入与证据链

### 4.1 输入源

- input_source：`mac_camera`

### 4.2 archive_root（run 前规划）

- 每次 run 一个全新空目录：`logs/real_scene_run_002A_<timestamp>/archive_root`
- CLI 必须拒绝向非空目录写入

## 5. 显式 entry 与 timebox（硬门槛）

- 必须 explicit entry token（写入 run_evidence）
- 必须 timebox_ms（上限短时；不得长时间连续运行）

## 6. abort triggers（任一出现立即 abort）

- execute/release/retry/reopen leakage
- default-on risk
- side effects expansion
- trace/replay/whitebox 写入中断
- timebox exceeded
- operator abort / safety observer abort
- scope drift / 进入隐私敏感区域
- 高风险交通环境遭遇

abort 后必须：

- 标记 abort_triggered=true + abort_reason
- 保全 archive_root（不要覆盖/删除）
- post-run summary 说明禁止立即重试（需 review）

