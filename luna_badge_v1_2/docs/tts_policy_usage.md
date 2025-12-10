# TTS 策略使用指南（v1.4.6c）

本文档介绍如何使用 v1.4.6c 新增的 TTS 策略映射系统。

---

## 快速开始

### 1. 使用快捷函数（推荐）

最简单的方式是使用预定义的快捷函数：

```python
from task_engine.tts import speak_safety, speak_navigation, speak_task, speak_chat

# 安全播报（高优先级 + 打断）
speak_safety("前方有障碍物，请减速！")

# 导航播报（高优先级，不打断）
speak_navigation("前方50米，请向左转")

# 任务反馈（中等优先级）
speak_task("已为您规划到医院的路线")

# 闲聊（低优先级）
speak_chat("今天天气不错")
```

### 2. 使用策略映射

如果需要更细粒度的控制，可以使用 `make_utterance`：

```python
from task_engine.tts import make_utterance, TTSCategory

# 使用策略自动填充 priority / interrupt
utter = make_utterance("前方有障碍物", TTSCategory.SAFETY)
# utter.priority == 90
# utter.interrupt == True

# 允许覆盖策略值
utter = make_utterance(
    "特殊导航提示",
    TTSCategory.NAVIGATION,
    priority=80,  # 覆盖默认的 75
    interrupt=True,  # 覆盖默认的 False
)
```

---

## 策略类别

| 类别 | 优先级 | 打断 | 默认 Level | 用途 |
|------|--------|------|------------|------|
| `SAFETY` | 90 | ✅ | warning | 障碍物、危险环境、施工提醒 |
| `NAVIGATION` | 75 | ❌ | info | 路线/方向播报 |
| `SYSTEM` | 65 | ❌ | system | 系统错误、模块异常 |
| `TASK` | 50 | ❌ | info | 任务执行反馈 |
| `CHAT` | 25 | ❌ | info | 闲聊、陪伴、非刚需内容 |

---

## 使用场景示例

### 导航模块

```python
# navigation/voice_feedback.py
from task_engine.tts import speak_navigation, speak_task

def on_route_planned_success(destination_name: str) -> None:
    speak_task(f"已为您规划到 {destination_name} 的路线。")

def on_turn_instruction(distance_m: int, direction: str) -> None:
    speak_navigation(f"前方{distance_m}米，请向{direction}转弯。")

def on_reroute_due_to_deviation() -> None:
    speak_navigation("您已偏离路线，我正在为您重新规划。")
```

### 安全模块

```python
# safety/voice_feedback.py
from task_engine.tts import speak_safety

def on_obstacle_detected(direction: str, distance_m: int) -> None:
    speak_safety(f"注意，{direction}方向约{distance_m}米处有障碍物，请减速。")

def on_dangerous_zone(zone_type: str) -> None:
    if zone_type == "water":
        speak_safety("前方有水域，请远离。")
    elif zone_type == "construction":
        speak_safety("前方有施工区域，请绕行。")
    else:
        speak_safety("前方环境复杂，请提高警惕。")
```

### 任务链模块

```python
# task_chain/task_chain_manager.py
from task_engine.tts import speak_task, speak_system

def on_task_started(task_name: str) -> None:
    speak_task(f"开始执行任务：{task_name}")

def on_task_completed(task_name: str) -> None:
    speak_task(f"任务 {task_name} 已完成")

def on_task_error(error_msg: str) -> None:
    speak_system(f"任务执行出错：{error_msg}")
```

---

## 高级用法

### 在已有 Utterance 上应用策略

如果已经创建了 `Utterance` 对象但没有设置优先级，可以使用 `apply_policy_to_utterance`：

```python
from task_engine.tts import apply_policy_to_utterance, TTSCategory, Utterance

# 创建一个没有策略的 Utterance
original = Utterance(text="前方有障碍物", priority=0)

# 应用安全策略
new_utter = apply_policy_to_utterance(original, TTSCategory.SAFETY)
# new_utter.priority == 90
# new_utter.interrupt == True
```

### 自定义策略值

所有快捷函数和 `make_utterance` 都支持覆盖策略值：

```python
# 覆盖 priority
speak_safety("紧急警告", priority=95)

# 覆盖 interrupt
speak_navigation("重要导航", interrupt=True)

# 覆盖 meta
speak_task("任务完成", meta={"custom": "value"})
```

---

## 优先级顺序

优先级从高到低：

```
SAFETY (90) > NAVIGATION (75) > SYSTEM (65) > TASK (50) > CHAT (25)
```

在 `TtsManager.pop_all()` 时，会按 priority 降序 + created_at 升序排序。

---

## 打断语义

- **`interrupt=True`**: 当队列中存在 `interrupt=True` 的项时，`TTSRuntimeDriver.process_once()` 只会播报最高优先级的那一条，其余项会被丢弃（被打断）。
- **`interrupt=False`**: 按排序结果依次播报全部项。

示例：

```python
# 队列：普通 -> interrupt -> 普通
speak_task("普通提示1", priority=50, interrupt=False)
speak_safety("紧急警告", priority=90, interrupt=True)  # 会打断其他项
speak_task("普通提示2", priority=50, interrupt=False)

# process_once() 后，只会播报"紧急警告"，其他两项被丢弃
```

---

## 最佳实践

1. **优先使用快捷函数**：`speak_safety`、`speak_navigation` 等，避免手写 priority / interrupt
2. **合理选择类别**：根据播报内容选择合适的类别，让系统自动应用正确的策略
3. **避免过度覆盖**：除非有特殊需求，否则不要覆盖策略值
4. **安全优先**：安全相关的播报必须使用 `SAFETY` 类别，确保高优先级和打断语义

---

## 测试

运行 TTS 策略相关测试：

```bash
cd luna_badge_tests
pytest tests/v1_4_6b/test_tts_policy.py -v
```

---

## 相关文档

- `task_engine/tts/tts_policy.py`: 策略定义和工具函数
- `task_engine/tts/tts_shortcuts.py`: 快捷函数实现
- `task_engine/tts/tts_manager.py`: 队列管理器
- `task_engine/tts/runtime_driver.py`: 运行时驱动

