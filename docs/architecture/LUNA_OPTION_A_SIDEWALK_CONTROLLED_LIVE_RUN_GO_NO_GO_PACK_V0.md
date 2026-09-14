---
phase: Phase-RealSceneRun-002A
title: Option A Sidewalk Controlled Live Run Go/No-Go Pack v0
status: PACK
version: v0
last_updated: 2026-04-24
scope: option_a_only
side_effects_released_default: false
---

## 0. 本 pack 的边界

本 pack 汇总 Run-002A 的计划、run record（如未执行则为 pending）、以及验证工具输出，给出本阶段 go/conditional_go/no_go。

禁止：伪造人行道 run 证据；不得用 DeviceEnv-003 的桌面采集冒充真实人行道短距离 run。

## 1. 输入材料（链接）

- Run Plan：`docs/architecture/LUNA_OPTION_A_SIDEWALK_CONTROLLED_LIVE_RUN_PLAN_V0.md`
- Runbook：`docs/architecture/LUNA_OPTION_A_SIDEWALK_CONTROLLED_LIVE_RUNBOOK_V0.md`
- Run Record：`docs/architecture/LUNA_OPTION_A_SIDEWALK_CONTROLLED_LIVE_RUN_RECORD_V0.md`
- Validator Wrapper：`tools/validate_option_a_sidewalk_controlled_live_run_v0.py`

## 2. 复审对象与验证结果（事实）

### 2.1 已存在的真实 controlled live archive（DeviceEnv-003）

- archive_root：`logs/device_env_003_archive_20260424_135440`
- 说明：该 archive 为 **真实 Mac 摄像头 live-input evidence**，用于证明 evidence pipeline 可跑通。
- 重要边界：该 archive **不等价于** “真实人行道短距离受控 run 证据”。

### 2.2 wrapper validator 输出（记录）

对 `logs/device_env_003_archive_20260424_135440` 运行：

- `python3 tools/validate_option_a_sidewalk_controlled_live_run_v0.py --archive_root logs/device_env_003_archive_20260424_135440`
- summary.recommendation=`go`
- hard_blockers=[]

解释：该验证仅说明该 archive 满足 OptionA 字段一致性 + Fix-001 required_files/manifest 规则；不代表已完成“人行道人体现场 run”。

## 3. Run-002A 执行状态（关键门槛）

Run Record 显示：

- `pending_real_sidewalk_run=true`
- `run_executed=false`
- `archive_root_path=null`

因此：**本阶段的“真实人行道短距离 run”尚未执行**。

## 4. Go/Conditional/No-Go 判定

### 4.1 判定：CONDITIONAL_GO

理由：

- evidence pipeline 已在真实输入下被证明可跑通（DeviceEnv-003 + Review-003 已 go）
- Run-002A 所需 plan/runbook/record/validator wrapper 已齐备，可在现场执行后立即产出并验证 archive
- 但 **本阶段核心目标**（真实人行道短距离 controlled live run）尚未发生，因此不能判定 GO

### 4.2 hard_blockers

- `pending_real_sidewalk_run=true`（缺少真实现场 run evidence）

### 4.3 soft_followups（不阻塞进入现场执行，但建议提升）

- frame_ref 可追溯性增强（帧落盘或视频+mapping）
- whitebox 从单行 gate → per-tick 最小白盒

## 5. recommended next step（不在本 pack 内执行）

- 执行一次真实人行道短距离 Option A controlled live run（严格按 Runbook）
- 产出新的 archive_root
- 对新 archive_root 运行：
  - `tools/validate_option_a_sidewalk_controlled_live_run_v0.py`
  - `tools/validate_controlled_live_evidence_collection_execution_v0.py`
- 完成后进入 Review-004（本阶段不进入）

## 6. 明确声明（边界写死）

- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未扩 Option A
- 未开放真实用户测试
- 本阶段不生成伪造的人行道 run evidence

