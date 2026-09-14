---
phase: Phase-DeviceEnv-002
title: Existing Camera Input Adapter Decision v0
status: FROZEN_DECISION
version: v0
last_updated: 2026-04-22
scope: decision_only
side_effects_released_default: false
---

## 0. 背景与问题定义

本阶段的核心问题不是“能否打开摄像头”，而是：

- **是否存在可复用的真实输入源**（Mac 摄像头 / 手机浏览器摄像头）
- **如何把真实帧输入接入当前 RealScene evidence archive 链（archive_root 合同）**

结论来自 Phase-DeviceEnv-002 的 inventory：当前已有可复用输入源，但尚未形成 `archive_root` 的证据产出链。

本文件冻结本阶段的正式决策：**优先 Mac 摄像头路径**，网页方案后置为候选。

## 1. 严格边界（本阶段宪法）

### 1.1 禁止

- 不执行真实 Option A controlled live run
- 不生成伪造 `run_evidence`/`trace`/`replay`/`whitebox` 等证据文件
- 不使用 fixture 冒充 controlled live
- 不同时实现 Mac 与网页两条输入路径
- 不扩 Option A scope，不进入 full controlled trial，不进入 Review-003
- 不开启默认路径，不扩大真实 side effects 面
- 不让模型获得执行权（candidate-only 维持不变）
- 不修改既有 RealScene evidence contract（包含 required_files、断言语义、validator 预期）

### 1.2 允许

- 新增“决策/定义/矩阵/计划”类文档
- 更新 `docs/architecture/README.md` 的索引链接

## 2. 已知可复用输入源（只记录事实，不做实现）

### 2.1 Mac / OpenCV 摄像头

- `utils/camera_handler.py`
- `check_camera.py`

已确认能力：

- 可打开真实 Mac 摄像头（OpenCV `VideoCapture`，可选 `CAP_AVFOUNDATION`）
- 可按帧读取并返回图像矩阵

### 2.2 浏览器 / 手机摄像头（getUserMedia）

- `luna_frontend_package_24files/web_test_server/web_test_server.py`

已确认能力：

- 浏览器侧 `navigator.mediaDevices.getUserMedia` 可开启摄像头（优先后置 environment，失败回退 user）
- 可通过 `canvas` 抓帧并通过 HTTP 上传到 Python 后端

### 2.3 既有 trace/replay 能力（非 RealScene archive_root 口径）

- `runtime/a3_logger.py`（`logs/a3_trace.jsonl`）
- `tools/run_video_a3_trace.py`
- `tools/run_video_replay.py`

已确认能力：

- 存在历史落盘 trace / replay 的能力，但文件名、schema 与 RealScene `archive_root` 合同不同，需 bridge。

## 3. 正式决策（冻结）

### 3.1 第一接入路径（本阶段冻结）

- **第一优先级：Mac Camera Archive Adapter（DeviceEnv-003 实现）**
  - 理由：输入链更短、更稳定、无需移动端部署；更适合先把 `archive_root` 证据链跑通。

### 3.2 第二接入路径（候选，不在本阶段实现）

- **第二优先级：Phone/Web getUserMedia Archive Adapter（后续候选）**
  - 理由：更接近手机第一视角，但引入 HTTPS/权限/前后端联调等额外不确定性。
  - 约束：必须在 Mac-first 的 `archive_root` bridge 跑通之后再进入。

### 3.3 明确不做

- 不做原生 App
- 不做双路径同时实现
- 不在本阶段把网页方案接入 RealScene archive 链

## 4. 进入下一阶段的必要输出（DeviceEnv-003 的唯一输入）

本决策要求下一阶段（DeviceEnv-003）以 **Mac-first** 实现最小 `archive_root` bridge：

- 必须能产出 required files（见 `LUNA_CONTROLLED_LIVE_ARCHIVE_BRIDGE_DEFINITION_V0.md`）
- 必须能通过现有 archive validator（不得绕过）
- 必须维持 candidate-only 与 side_effects_released 默认 false

## 5. 本阶段 Go/No-Go

### 5.1 GO

满足：

- 已明确选择 **Mac-first**
- 已将 Phone/Web 方案登记为后续候选且不阻塞本阶段
- 已定义最小 archive bridge adapters 与责任矩阵（由本阶段其余文档给出）

### 5.2 CONDITIONAL_GO / NO_GO

本文件本身不承诺实现，只冻结决策；本阶段总体判定以 “bridge definition + responsibility matrix + impl plan” 是否完整为准。

