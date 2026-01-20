# TTS Router Time Window Gate 文档

## 概述

Patch-H (v1.4.6d-TW) 为导航语音路由器增加了时间窗口节流（Time Window Gate）功能，用于避免重复播报，提升用户体验。

## 目标

1. **避免重复播报**：防止连续多帧重复播报相同内容（例如连续 10 帧都说"前方有障碍物"）
2. **保留实时性**：为高优先级（安全类）保留极短窗口，保证实时性
3. **自然频率**：为导航播报（转弯/距离提示）设置自然频率，避免"话密"
4. **统一控制**：提供路由级统一控制，不影响各模块逻辑

## 架构设计

### 为什么在 Router 层实现？

| 方案 | 问题 |
|------|------|
| 在 voice adapter 层节流 | 无法区分来源（导航 / 安全） |
| 在 tts_manager 层节流 | tts_manager 不理解导航语义，不知道优先级差异 |
| 在导航模块节流 | 会污染导航逻辑，破坏模块边界 |
| **在 router 层节流（推荐）** | **这是 TTS 行为决策层，应该由 router 管理输出频率** |

→ 完全符合系统分层结构（决策 → 语义 → router → TTS）

## 实现细节

### 1. TimeWindowGate 类

**位置**：`task_engine/tts/routers/time_window_gate.py`

**核心功能**：
- `safety_window`: 安全播报时间窗口（默认 0.8s）
- `navigation_window`: 导航播报时间窗口（默认 2.0s）
- `allow(category)`: 检查某类别是否可以播报

**特点**：
- 不同类别的时间窗口相互独立
- TASK / CHAT / SYSTEM 等类别不受限制
- 提供 `reset()` 方法用于测试

### 2. NavigationVoiceRouter 集成

**修改点**：
- 在 `__init__` 中初始化 `TimeWindowGate`
- 在 `route_batch` 中应用时间窗口节流
- 在 `reset` 中重置时间窗口状态

**路由逻辑**：
1. 安全播报：先检查时间窗口，如果被节流则记录安全时间但不播报
2. 导航播报：在正常流程中应用时间窗口节流
3. 其他类别：不受时间窗口限制

### 3. 与安全静默窗口的关系

时间窗口节流与安全静默窗口（Step 5）是**独立且互补**的：

- **安全静默窗口**（3.0s）：安全播报后抑制导航播报
- **时间窗口节流**（0.8s / 2.0s）：防止同一类别的重复播报

两者协同工作：
1. 安全播报触发安全静默窗口（3.0s），在这期间导航播报被抑制
2. 时间窗口节流防止安全播报（0.8s）和导航播报（2.0s）的重复

## 效果（可量化）

| 分类 | 原播报频率 | 现在 |
|------|-----------|------|
| 安全播报（障碍物） | 连续每帧1次（30次/sec） | 每 0.8 秒最多 1 次 |
| 转弯提示 | 每帧重播 | 每 2 秒最多 1 次 |
| 直行提示 | 重复播报 | 每 2 秒最多 1 次 |

**明显提升体验，避免"说话太密"**

## 配置

### 当前版本（v1.4.6d）

时间窗口大小硬编码在 `TimeWindowGate` 类中：
- `safety_window`: 0.8s
- `navigation_window`: 2.0s

### 未来版本（v1.4.7+）

可在配置文件中加入：

```yaml
tts:
  time_window:
    safety_window: 0.8
    navigation_window: 2.0
```

## 测试

### 单元测试

**文件**：`tests/v1_4_6d/test_time_window_gate.py`

**覆盖**：
- 安全播报时间窗口节流
- 导航播报时间窗口节流
- 不同类别的时间窗口相互独立
- 其他类别不受限制
- reset 功能
- 自定义窗口大小

### 集成测试

**文件**：`tests/v1_4_6d/test_navigation_voice_router_window.py`

**覆盖**：
- 安全播报被时间窗口节流
- 导航播报被时间窗口节流
- 安全播报和导航播报的时间窗口相互独立
- 安全播报的优先级仍然高于导航播报
- route_and_speak 与时间窗口的集成

## 使用示例

```python
from task_engine.navigation.navigation_voice_router import NavigationVoiceRouter
from task_engine.tts.routers.time_window_gate import TimeWindowGate
from task_engine.navigation.navigation_voice_adapter import NavigationVoiceAdapter
from task_engine.tts import tts_manager

# 创建带时间窗口的 router
gate = TimeWindowGate(safety_window=0.8, navigation_window=2.0)
router = NavigationVoiceRouter(time_window_gate=gate)

# 创建适配器
adapter = NavigationVoiceAdapter()

# 处理 speech_event
speech_event = {'decision': 'STOP', 'text': '前方有障碍物', 'category': 'safety'}
utterances = adapter.handle_speech_event(speech_event)
router.route_and_speak(utterances)

# 立即再次播报：会被时间窗口节流
speech_event2 = {'decision': 'STOP', 'text': '前方有台阶', 'category': 'safety'}
utterances2 = adapter.handle_speech_event(speech_event2)
router.route_and_speak(utterances2)  # 被节流，不会播报
```

## 完整链路

```
NavigationEngineV13.evaluate()
  ↓
struct_events
  ↓ (Step 4)
NavigationEventPostProcessor.process()
  ↓
filtered_events
  ↓ (Step 3)
NavPhraseMapper.convert_events()
  ↓
speech_event dict
  ↓ (Step 6)
NavigationVoiceAdapter.handle_speech_event()
  ↓
Utterance 列表
  ↓ (Step 5 + Patch-H)
NavigationVoiceRouter.route_batch()
  ├─ 安全静默窗口检查
  └─ 时间窗口节流（Patch-H）
  ↓
filtered Utterances
  ↓
TTS Policy (SAFETY / NAVIGATION)
  ↓
TTS Runtime
```

## 总结

Patch-H 成功实现了时间窗口节流功能，与现有的安全静默窗口机制协同工作，显著提升了导航语音播报的用户体验。所有测试通过，代码无 linter 错误。












