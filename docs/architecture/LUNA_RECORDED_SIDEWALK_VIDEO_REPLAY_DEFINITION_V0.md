---
phase: Phase-RealSceneReplay-001
title: Recorded Sidewalk Video Evidence Replay Definition v0
status: DEFINITION_FROZEN
version: v0
last_updated: 2026-04-24
scope: recorded_video_replay_only
side_effects_released_default: false
---

## 0. 目标（本阶段只做一件事）

将一段**用户已录制的人行道/真实街景视频**转为 `recorded_video_replay` 类型的证据归档（archive_root），以验证：

- recorded video 输入可读
- frame events 可生成
- trace/replay/whitebox 等 required_files 可落盘
- manifest 可生成并通过 hash 校验
- recorded video replay validator 可运行并给出 go/conditional_go/no_go
- 不产生 execute/default-on/side effects 泄漏

## 1. 硬边界（写死）

必须写死并可被 validator 检查：

- `evidence_type = recorded_video_replay`
- `controlled_live = false`
- `pending_real_sidewalk_run = true`（recorded video 不能替代 controlled live）
- `input_source = recorded_video`
- **不得**将 recorded video 标记为 `controlled_live`
- **不得**用 recorded video replay 进入 Review-004 作为“真实人行道 controlled live”证据

## 2. 非目标（明确不做）

- 不执行 controlled live run（不出门、不在真实人行道现场采集 live input）
- 不进入 full controlled trial
- 不开放真实用户测试
- 不开启 default-on
- 不扩大真实 side effects 面
- 不做 Phone/Web adapter（该阶段在 Replay-001 之后另起）

## 3. 与 controlled live 的关系（口径冻结）

- Recorded video replay：验证“真实街景视频”可以进入 archive/evidence/validator 链路（回放/可审计）
- Controlled live：验证“真实现场受控 run”能稳定产出可复审 archive（不可被 replay 替代）

## 4. 交付物（本阶段必须产生）

- recorded replay archive contract（required_files + run_evidence 字段约束）
- 生成工具（读取视频并产出 archive_root）
- 校验工具（强制边界 + required_files + manifest + 安全断言）
- Go/No-Go pack（决策包）
- README 索引更新

