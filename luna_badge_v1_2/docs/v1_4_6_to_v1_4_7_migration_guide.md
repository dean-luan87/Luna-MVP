# v1.4.6 → v1.4.7 迁移指南

**来源版本**: v1.4.6 – Dynamic Safety Broadcast Orchestrator  
**目标版本**: v1.4.7 – 任务链问询系统（规划中）

---

## 一、迁移概述

v1.4.7 将在 v1.4.6 的 TTS 调度系统基础上，引入**任务链问询系统**，包括：

- 主任务确认机制
- 插入任务问询逻辑
- 播报主动问询模块（基于 v1.4.6 Router）

---

## 二、v1.4.7 预期变更

### 2.1 新增模块（预期）

- `task_engine/query/`：问询系统模块
  - `query_manager.py`：问询管理器
  - `query_chain.py`：问询链
  - `query_runtime.py`：问询运行时

### 2.2 增强模块（预期）

- `task_chain/task_chain_manager.py`：
  - 集成问询系统
  - 支持任务确认流程

- `task_engine/tts/router_facade.py`：
  - 新增问询相关播报接口

---

## 三、迁移准备

### 3.1 代码检查

在开始 v1.4.7 开发前，请确保：

1. ✅ v1.4.6 的所有 TTS 调用已迁移到 `TTSRouterFacade`
2. ✅ 所有测试通过
3. ✅ 无已知严重 bug

### 3.2 依赖检查

v1.4.7 将依赖以下 v1.4.6 模块：

- `TTSRouterFacade`：统一播报入口
- `PriorityScheduler`：优先级调度
- `SafetyQueue`：安全播报队列
- `TimeWindowGate`：时间窗口节流

---

## 四、迁移步骤（待 v1.4.7 开发时补充）

本指南将在 v1.4.7 开发时更新。

---

## 五、兼容性说明

v1.4.7 将保持与 v1.4.6 的向后兼容性：

- 所有 v1.4.6 的 API 将继续工作
- 问询系统作为可选功能添加
- 现有任务链无需修改即可使用

---

**本指南将在 v1.4.7 开发时更新**












