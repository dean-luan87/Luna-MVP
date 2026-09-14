---
phase: Phase-RealSceneRun-002A
title: Option A Sidewalk Controlled Live Runbook v0
status: RUNBOOK
version: v0
last_updated: 2026-04-24
scope: option_a_only
side_effects_released_default: false
---

## 0. 本 runbook 的用途

指导一次短时 Option A 人行道 controlled live run 的人工操作流程：启动、监控、中止、归档、验证与复审入口。

## 1. Run 前（必须全部满足，否则不得开始）

### 1.1 人员到位

- operator_id 已确认
- safety_observer_id 已确认
- record_owner_id 已确认

### 1.2 场景合法

- 白天、低人流、平整人行道、短距离
- 无过街、无复杂路口、无隐私敏感区域

### 1.3 安全边界确认（candidate-only）

- default_path_disabled=true
- model_execution_authority=false
- 不输出强制导航指令
- side_effects_released=false（默认）

### 1.4 归档配置

- 规划本次 `archive_root`（空目录）
- timebox_ms 设置（短时）
- entry_token 生成（显式 entry）
- validator 可用（本地可运行）

## 2. 启动（显式 entry）

建议命令形态（示例）：

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

记录：

- 命令参数（不含敏感信息）
- start_time

## 3. 运行中监控（持续）

必须持续监控：

- execute/default-on/side effects expansion 风险（任何迹象立即 abort）
- trace/replay/whitebox/model/output 文件是否持续写入
- timebox 是否接近上限
- scope drift（进入不允许环境）
- privacy 风险
- operator/safety observer abort 信号

## 4. abort（触发即执行）

任一出现立即 abort：

- execute/release/retry/reopen leakage
- default-on risk
- side effects expansion
- trace/replay/whitebox broken
- timebox exceeded
- scope drift / privacy violation risk
- operator abort / safety observer abort

abort 后：

- 保全 archive_root（不得覆盖/删除）
- 在 run record 中标记 abort_triggered=true 并填写 abort_reason
- 禁止立即重试（必须先 review）

## 5. 结束与归档

- 确认 controlled_live_input_ended=true
- 确认 required_files 存在
- 生成/确认 archive_manifest.json

## 6. 验证（run 后必须执行）

### 6.1 Option A scope + evidence wrapper（建议）

```bash
python3 tools/validate_option_a_sidewalk_controlled_live_run_v0.py --archive_root <archive_root>
```

### 6.2 Fix-001 validator（必须可跑）

```bash
python3 tools/validate_controlled_live_evidence_collection_execution_v0.py --archive_root <archive_root>
```

## 7. Post-run 复审入口

- 将 validator 输出（go/conditional_go/no_go + blockers）写入 run record
- 进入 Review-004（不在本阶段执行）

