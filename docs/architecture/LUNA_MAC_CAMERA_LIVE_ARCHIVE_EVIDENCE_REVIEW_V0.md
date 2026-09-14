---
phase: Phase-RealSceneReview-003
title: Mac Camera Live Archive Evidence Review v0
status: REVIEW
version: v0
last_updated: 2026-04-24
scope: review_only
side_effects_released_default: false
---

## 0. 本阶段定位（写死边界）

本阶段只做一件事：**基于 DeviceEnv-003 生成的真实 Mac 摄像头 live-input archive，进行正式 evidence review**。

禁止：

- 不执行新的 live run
- 不扩 Option A，不进入 Option B/C/D
- 不进入 full controlled trial
- 不开放真实用户测试
- 不开启 default-on
- 不扩大真实 side effects 面
- 不让模型拿执行权
- 不实现 Phone/Web adapter

## 1. 本次复审对象（事实冻结）

- **archive_root**：`logs/device_env_003_archive_20260424_135440`
- **run_id**：`live_beb8d78211`
- **evidence_type**：`controlled_live`
- **input_source**：`mac_camera`
- **camera_opened**：true（见 `trace.jsonl` 的 `camera_opened` 事件）
- **frame_count**：30（见 `run_evidence.json` 与 `trace.jsonl`）

## 2. 必须回答的问题（逐条结论）

### 2.1 本次真实 archive_root 是什么路径？

`logs/device_env_003_archive_20260424_135440`

### 2.2 是否为真实 live input，而非 fixture？

**是**。证据：

- `run_evidence.json.evidence_type=controlled_live`
- `trace.jsonl` 存在 `camera_opened=true`、`controlled_live_input_started=true`、连续 `frame_captured`（frame_index 1..30）
- `replay.jsonl` 记录 frame_ref（`controlled_live://frame/N`）与 timestamp_ms，与 trace 的 frame 事件同一时间轴范围

> 说明：此处“真实”指 **真实摄像头打开与帧事件产生**。它不等价于“真实佩戴视角/最终硬件链路”。

### 2.3 required_files 是否完整？

**是**。`archive_manifest.json.required_files` 列出 10 个文件，且 `missing_files=[]`。

### 2.4 manifest 是否通过 hash 校验？

**是**。`archive_manifest.json.integrity_status=pass`，`hash_mismatches=[]`。

### 2.5 validator 是否输出 go？

**是**。对该 archive_root 运行 `validate_controlled_live_evidence_collection_execution_v0.py`，summary.recommendation=`go`，hard_blockers=`[]`。

### 2.6 是否存在 execute/default-on/side effects 泄漏？

在本次证据链口径下，**未发现**。证据：

- `run_evidence.json` 三条断言为 true：
  - `no_execute_leakage_assertion=true`
  - `no_default_on_assertion=true`
  - `no_side_effect_expansion_assertion=true`
- `whitebox.jsonl` 明确：
  - `candidate_only=true`
  - `default_path_disabled=true`
  - `allows_execute_now=false`

### 2.7 frame_ref 追溯策略是否足以支撑下一阶段？

**结论：partial（soft follow-up）**。

- 当前 `replay.jsonl.frame_ref=controlled_live://frame/N` 可用于“事件级回放索引”，但不包含真实帧字节的稳定引用（例如帧文件/编码视频 + 映射表）。
- 若下一阶段的“人行道短距离 run”需要更强的复现与审计（例如后续重跑感知/对齐时间线），建议升级为：
  - `media/frames/*.jpg` 或 `media/video.mp4` + `frame_index→timestamp` 映射（仍不要求产品级）

该项目前不构成 hard blocker（validator 已 go），但属于进入“真实人行道 run”前的质量增强建议。

### 2.8 whitebox v0 最小字段是否足以支撑下一阶段？

**结论：partial（soft follow-up）**。

- 当前 whitebox 只有 1 行最小 gate 声明，足以证明 candidate-only 与默认路径禁用，但不足以支持更细粒度的“每 tick 抑制原因/候选生成链路”审计。
- 建议在进入真实人行道 run 前，白盒至少扩展为：按 tick 写入（即使候选为空）：
  - gates + suppression_reason_codes + candidate_count + degraded/help prompt 状态（仍不引入执行权）

### 2.9 这份证据是否能支持进入 Option A sidewalk controlled live run？

**建议：GO（允许进入）**，理由：

- 证据链关键硬门槛已满足：真实 live input、required_files 完整、manifest pass、validator go、三断言 true
- 当前不足项（frame_ref/whitebox 丰富度）属于 soft follow-up，可在下一阶段 run 中用更严格 timebox + 运行中记录策略补齐，或在进入前做一个极小 fix（见分流包）

### 2.10 这份证据不能支持哪些结论？

明确不能证明：

- 这不是开放真实用户测试
- 这不是 full controlled trial
- 这不是最终硬件/佩戴视角验证（非手机/徽章第一视角）
- 这不证明“导航能力正确/可用/安全”，只证明 **controlled live evidence pipeline** 在真实输入下可跑通并可被 validator 接受

## 3. 本阶段结论（review recommendation）

- **recommendation**：GO（进入下一次 Option A 人行道短距离 controlled live run 的资格成立）
- **hard_blockers**：无（以当前 evidence contract 与 validator 口径）
- **soft_followups**：
  - frame_ref 可追溯策略增强（帧落盘或编码视频+映射）
  - whitebox 从“单行 gate”升级为“每 tick 最小白盒”以提升复盘可解释性

