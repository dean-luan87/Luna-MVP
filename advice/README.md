# Advice Module

## 概述

Advice 模块提供只读的建议生成功能，将系统的中间状态（WAITING / BLOCKED / TIMEOUT）转换为人类可理解的提示文本。

## 核心原则

- ❌ **不执行**任何动作
- ❌ **不触发/影响** C 模块
- ❌ **不改变** Task 状态
- ✅ **只读** Task v2 + 时间
- ✅ **只输出**人类可理解的建议文本 + 证据

## 当前实现（v0）

### 支持的状态

- **WAITING**: 条件未满足，建议等待
- **BLOCKED**: 视野受限，建议调整位置
- **TIMEOUT**: 等待超时，建议确认或更换方案

### 使用方式

```python
from advice import AdviceEngine
from tasks.tasks.traffic_light_task_v2 import TrafficLightTask

engine = AdviceEngine()
advices = engine.generate([task], now=time.time())
```

## 预留功能

### Enhancement-E1：等待时间与预测信息增强（未实现）

**声明**：本能力用于提升用户心理稳定性，不参与任何系统判断或执行逻辑。

**说明**：未来可扩展的功能，包括：
- 等待时间预测（如"预计还需等待 30 秒"）
- 状态变化预测（如"信号灯通常在 60 秒内变化"）
- 历史模式提示（如"类似情况平均等待 45 秒"）

**边界**：
- 所有预测信息仅用于用户提示
- 不参与 Task 状态判断
- 不参与 C 安全决策
- 不触发任何执行动作

## 架构位置

Advice 模块位于系统架构的**只读层**：

```
Dynamic View（事实）
  ↓ 只读
Task v2（状态）
  ↓ 只读
Advice（建议文本）
  ↓ 输出
用户界面 / TTS
```

## 测试

```bash
python3 -m pytest -q advice/tests
```
