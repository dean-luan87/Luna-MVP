# 导航语音迁移指南（v1.4.6d）

本文档说明如何将现有导航模块中的 TTS 调用迁移到新的 `NavigationVoiceAdapter`。

---

## 迁移目标

将所有导航相关的语音输出统一到 TTS 策略体系：
- **导航指引** → `speak_navigation` (priority=75)
- **任务反馈** → `speak_task` (priority=50)
- **安全提示** → `speak_safety` (priority=90, interrupt=True)

---

## 迁移步骤

### 步骤 1: 导入 NavigationVoiceAdapter

```python
from task_engine.navigation import NavigationVoiceAdapter

# 创建适配器实例（建议作为模块级单例）
_voice = NavigationVoiceAdapter()
```

### 步骤 2: 替换现有 TTS 调用

#### 示例 1: 路线规划完成

**旧代码：**
```python
from task_engine.tts import tts_manager

def on_route_planned(destination: str, eta: int):
    tts_manager.speak(
        f"已为您规划到 {destination} 的路线，预计用时 {eta} 分钟。",
        level="info",
        priority=70,
        interrupt=False,
    )
```

**新代码：**
```python
def on_route_planned(destination: str, eta: int):
    _voice.announce_route_planned(destination, eta_minutes=eta)
```

#### 示例 2: 转向提示

**旧代码：**
```python
def on_turn_event(distance_m: int, direction: str):
    tts_manager.speak(
        f"前方 {distance_m} 米，请向{direction}转弯。",
        level="info",
        priority=70,
        interrupt=False,
    )
```

**新代码：**
```python
def on_turn_event(distance_m: int, direction: str):
    # direction 统一成文案："左转" / "右转" / "调头"
    _voice.announce_turn(distance_m=distance_m, direction=direction)
```

#### 示例 3: 偏航纠正

**旧代码：**
```python
def on_deviation_detected():
    tts_manager.speak(
        "您已偏离路线，我正在为您重新规划。",
        priority=75,
        interrupt=False,
    )
```

**新代码：**
```python
def on_deviation_detected():
    _voice.announce_reroute(reason="偏离路线")
```

#### 示例 4: 到达目的地

**旧代码：**
```python
def on_arrival(name: str):
    tts_manager.speak(
        f"已到达{name}附近。",
        priority=60,
        interrupt=False,
    )
```

**新代码：**
```python
def on_arrival(name: str):
    _voice.announce_arrival(destination_name=name)
```

#### 示例 5: 安全提示

**旧代码：**
```python
def on_obstacle_detected(direction: str, distance: int):
    tts_manager.speak(
        f"{direction}方向约 {distance} 米处有障碍物，请注意避让。",
        level="warning",
        priority=90,
        interrupt=True,
    )
```

**新代码：**
```python
def on_obstacle_detected(direction: str, distance: int):
    _voice.announce_obstacle_warning(
        direction=direction,
        distance_m=distance,
    )
```

---

## 完整映射表

| 导航事件类型 | 旧调用方式 | 新调用方式 | Category |
|------------|-----------|-----------|----------|
| 路线规划完成 | `tts_manager.speak(..., priority=70)` | `announce_route_planned()` | TASK |
| 导航开始 | `tts_manager.speak(..., priority=50)` | `announce_navigation_started()` | TASK |
| 导航结束 | `tts_manager.speak(..., priority=50)` | `announce_navigation_finished()` | TASK |
| 转向提示 | `tts_manager.speak(..., priority=70)` | `announce_turn()` | NAVIGATION |
| 直行提示 | `tts_manager.speak(..., priority=70)` | `announce_straight()` | NAVIGATION |
| 重新规划 | `tts_manager.speak(..., priority=75)` | `announce_reroute()` | NAVIGATION |
| 到达目的地 | `tts_manager.speak(..., priority=60)` | `announce_arrival()` | NAVIGATION |
| 人群拥挤 | `tts_manager.speak(..., priority=90, interrupt=True)` | `announce_crowded_ahead()` | SAFETY |
| 环境复杂 | `tts_manager.speak(..., priority=90, interrupt=True)` | `announce_complex_environment()` | SAFETY |
| 障碍物警告 | `tts_manager.speak(..., priority=90, interrupt=True)` | `announce_obstacle_warning()` | SAFETY |

---

## 安全提示识别规则

以下情况应使用 `SAFETY` 类别（`speak_safety`）：

- ✅ 障碍物检测
- ✅ 人群拥挤
- ✅ 环境复杂（地铁口、商场等）
- ✅ 施工区域
- ✅ 危险区域
- ✅ 红灯/交通信号
- ✅ 水域/危险地形

以下情况应使用 `NAVIGATION` 类别（`speak_navigation`）：

- ✅ 方向指引（左转/右转/直行）
- ✅ 距离提示
- ✅ 偏航纠正
- ✅ 到达提示

以下情况应使用 `TASK` 类别（`speak_task`）：

- ✅ 路线规划完成
- ✅ 导航开始/结束
- ✅ 任务状态反馈

---

## 自定义 Meta 数据

如果需要传递额外的元数据，可以通过 `meta` 参数：

```python
_voice.announce_turn(
    distance_m=50,
    direction="左转",
    meta={
        "route_id": "route_123",
        "step_index": 3,
        "custom": "value",
    },
)
```

这些 meta 数据会与策略的默认 meta 合并，并保留在最终的 `Utterance` 中。

---

## 测试验证

迁移后，运行测试确保功能正常：

```bash
cd luna_badge_tests
pytest tests/v1_4_6d/test_navigation_voice_adapter.py -v
```

---

## 注意事项

1. **不要混用新旧方式**：迁移后，同一模块内应统一使用 `NavigationVoiceAdapter`，避免同时使用 `tts_manager.speak()`。

2. **方向文案统一**：`announce_turn()` 的 `direction` 参数建议使用标准文案：
   - "左转"
   - "右转"
   - "调头"
   - "直行"

3. **优先级自动管理**：迁移后无需手动设置 `priority` 和 `interrupt`，策略层会自动处理。

4. **向后兼容**：`NavigationVoiceAdapter` 不会破坏现有的 TTS 管线，可以逐步迁移。

---

## 迁移检查清单

- [ ] 导入 `NavigationVoiceAdapter`
- [ ] 创建适配器实例
- [ ] 替换所有路线规划相关的 TTS 调用
- [ ] 替换所有转向/直行相关的 TTS 调用
- [ ] 替换所有偏航/重新规划相关的 TTS 调用
- [ ] 替换所有到达相关的 TTS 调用
- [ ] 替换所有安全提示相关的 TTS 调用
- [ ] 运行测试验证
- [ ] 运行 demo 脚本验证流程

---

## 相关文档

- `task_engine/navigation/navigation_voice_adapter.py`: 适配器实现
- `docs/tts_policy_usage.md`: TTS 策略使用指南
- `scripts/demo_navigation_voice.py`: 演示脚本

