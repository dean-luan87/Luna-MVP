---
phase: Phase-RealSceneReview-003
title: Mac Camera Live Archive Branch Decision Pack v0
status: DECISION_PACK
version: v0
last_updated: 2026-04-24
scope: decision_only
---

## 0. 输入（本次决策依据）

- DeviceEnv-003 真实 Mac camera live archive：
  - archive_root: `logs/device_env_003_archive_20260424_135440`
  - run_id: `live_beb8d78211`
  - camera_opened: true
  - frame_count: 30
- Validator：
  - `validate_controlled_live_evidence_collection_execution_v0.py` → recommendation=`go`，hard_blockers=[]
- Review artifacts：
  - `docs/architecture/LUNA_MAC_CAMERA_LIVE_ARCHIVE_EVIDENCE_REVIEW_V0.md`
  - `docs/architecture/LUNA_MAC_CAMERA_LIVE_ARCHIVE_EVIDENCE_QUALITY_MATRIX_V0.md`
  - `docs/architecture/LUNA_OPTION_A_SIDEWALK_CONTROLLED_LIVE_RUN_ELIGIBILITY_CHECKLIST_V0.md`

## 1. 结论（分流决策）

### 1.1 决策

- **branch_decision = GO**

进入：

- **Phase-RealSceneRun-002A**
  - Option A Sidewalk Controlled Live Run With Mac Camera Evidence v0

### 1.2 决策理由（高信号）

满足进入人行道短距离 controlled live run 的核心硬门槛：

- 真实 live input（Mac 摄像头打开 + 捕帧）
- required_files 完整
- manifest 完整且 hash 校验通过
- validator 输出 `go`
- 三条安全断言为 true，candidate-only 与 default_path_disabled 已在 whitebox/断言口径内成立

## 2. 风险与软跟进（不阻塞 GO，但必须记录）

### 2.1 soft_followups

- **frame_ref_traceability（partial）**
  - 当前 replay 使用 `controlled_live://frame/N` 事件级引用，不含帧字节的稳定引用。
  - 建议在进入人行道 run 前或 run 同步升级：落盘帧或视频+映射表（不要求产品级）。

- **whitebox_per_tick_auditability（partial）**
  - 当前 whitebox 为最小 gate 单行，不足以支撑更细粒度复盘解释。
  - 建议在下一次 run 扩展为按 tick 最小白盒行（仍 candidate-only）。

### 2.2 不变量重申（写死）

- 不进入 full controlled trial
- 不开放真实用户测试
- 不开启默认路径
- 不扩大 side effects 面
- 不让模型获得执行权
- 不实现 Phone/Web adapter

## 3. 若后续出现异常的回退分流规则（预案）

若 Phase-RealSceneRun-002A 中出现任一：

- validator 不再 `go`
- required_files 缺失 / manifest fail
- safety assertions 任一失败
- 发生 execute/default-on/side effects 扩张风险

则立即中止并分流到：

- **Phase-DeviceEnvFix-004**（证据链修复冲刺）或
- **Phase-RealScenePause-003**（暂停与整改）

