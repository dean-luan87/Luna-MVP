# NavigationVoiceRouter 架构说明

## 概述

v1.4.6d 中存在两个 `NavigationVoiceRouter` 实现，分别服务于不同的使用场景：

1. **Navigation 层 Router**：`task_engine/navigation/navigation_voice_router.py`
2. **TTS Routers 层 Router**：`task_engine/tts/routers/navigation_voice_router.py`

## 两个实现的关系

### Navigation 层 Router（Step 5-6）

**位置**：`task_engine/navigation/navigation_voice_router.py`

**特点**：
- 与 `NavigationVoiceAdapter` 紧密集成
- 使用 `route_batch` 统一处理 Utterance 列表
- 支持安全静默窗口（Step 5）
- 支持时间窗口节流（Patch-H）

**使用场景**：
- `NavigationTask` 中的导航语音处理
- 需要批量处理多个 Utterance 的场景
- 需要安全静默窗口的场景

**导入方式**：
```python
from task_engine.navigation.navigation_voice_router import NavigationVoiceRouter, navigation_voice_router
```

### TTS Routers 层 Router（Patch-H，按用户 diff）

**位置**：`task_engine/tts/routers/navigation_voice_router.py`

**特点**：
- 提供语义化的路由方法（`route_turn`, `route_straight`, `route_obstacle_warning`, `route_generic`）
- 每个方法内部应用时间窗口节流
- 直接调用 `NavigationVoiceAdapter` 的 `announce_*` 方法
- 更符合 TTS 路由层的职责

**使用场景**：
- 需要语义化接口的场景
- 需要直接调用 `route_turn`、`route_straight` 等方法的场景
- 新的代码应该优先使用这个实现

**导入方式**：
```python
from task_engine.tts.routers.navigation_voice_router import NavigationVoiceRouter, navigation_voice_router
```

## 迁移建议

### 当前状态

- **NavigationTask**：使用 Navigation 层 Router（`task_engine/navigation/`）
- **新代码**：建议使用 TTS Routers 层 Router（`task_engine/tts/routers/`）

### 未来计划

1. **短期**：两个实现并存，新代码使用 TTS Routers 层
2. **中期**：逐步迁移 `NavigationTask` 到 TTS Routers 层
3. **长期**：考虑合并两个实现，或明确职责分工

## 功能对比

| 功能 | Navigation 层 Router | TTS Routers 层 Router |
|------|---------------------|----------------------|
| 安全静默窗口 | ✅ | ❌（由 Navigation 层处理） |
| 时间窗口节流 | ✅ | ✅ |
| 批量处理 | ✅ (`route_batch`) | ❌ |
| 语义化接口 | ❌ | ✅ (`route_turn`, `route_straight` 等) |
| 优先级路由 | ✅ | ❌（由 Navigation 层处理） |

## 使用示例

### Navigation 层 Router（当前 NavigationTask 使用）

```python
from task_engine.navigation.navigation_voice_adapter import NavigationVoiceAdapter
from task_engine.navigation.navigation_voice_router import navigation_voice_router

adapter = NavigationVoiceAdapter()
speech_event = {'decision': 'STOP', 'text': '前方有障碍物', 'category': 'safety'}
utterances = adapter.handle_speech_event(speech_event)
navigation_voice_router.route_and_speak(utterances)
```

### TTS Routers 层 Router（推荐新代码使用）

```python
from task_engine.tts.routers.navigation_voice_router import navigation_voice_router

# 语义化接口
navigation_voice_router.route_turn("左转", distance=50)
navigation_voice_router.route_obstacle_warning(direction="前方", distance_m=10)
navigation_voice_router.route_generic("SAFETY", "前方有危险")
```

## 总结

两个实现各有优势，当前阶段建议：
- **新代码**：使用 TTS Routers 层 Router（语义化接口，更清晰）
- **现有代码**：继续使用 Navigation 层 Router（保持兼容性）
- **未来**：逐步统一到 TTS Routers 层，或明确职责分工

