# speech_event 数据结构分析报告

## 📋 搜索结果总结

### 1. speech_event 的定义位置

**主要来源**：
- `core/speech/nav_speech_manager.py` - `build_from_nav()` 方法（第 46-176 行）
- `NavigationEngine` 的结果 - `result.get("speech_event")`（在 `tasks/navigation_task.py` 第 269 行）

### 2. speech_event 的数据结构

根据 `nav_speech_manager.py` 的 `_build_event()` 方法（第 155-176 行），`speech_event` 的结构为：

```python
{
    "speak": True,
    "decision": str,        # 决策类型：如 "STOP", "SLIGHT_RIGHT", "HARD_LEFT", "FORWARD" 等
    "text": str,            # 播报文本：如 "前方无法通行，请原地停下。"
    "style": str,           # 语气风格："calm" / "alert"
    "priority": int,        # 优先级：0-3，数字越大优先级越高
    "interruptible": bool,  # 是否可被打断：(priority < 3)
    "category": "navigation"
}
```

### 3. speech_event 的生成逻辑

**路径 1：NavSpeechManager.build_from_nav()**
- 位置：`core/speech/nav_speech_manager.py:46`
- 输入：`nav_result` (dict) + `danger` (bool)
- 输出：`speech_event` (dict) 或 `None`

**路径 2：NavigationEngine**
- 位置：`tasks/navigation_task.py:269`
- 从 `result.get("speech_event")` 获取
- 结构可能相同或类似

### 4. 当前使用方式

**位置**：`tasks/navigation_task.py:292`
```python
if speech_event and self.tts_manager:
    try:
        self.tts_manager.speak(speech_event)  # ⚠️ 这里传入的是字典
    except Exception as e:
        self.logger.warning(f"TTS 播报失败: {e}")
```

**问题**：
- `tts_manager.speak()` 期望的是字符串，但 `speech_event` 是字典
- 需要从字典中提取 `text` 字段，或适配字典输入

### 5. decision 类型映射

根据 `nav_speech_manager.py` 的代码，常见的 `decision` 类型包括：

- `"STOP"` - 停止（最高优先级，priority=3）
- `"HARD_LEFT"` / `"HARD_RIGHT"` - 急转
- `"SLIGHT_LEFT"` / `"SLIGHT_RIGHT"` - 微调
- `"FORWARD"` - 直行

### 6. 关键字段说明

| 字段 | 类型 | 说明 | 迁移用途 |
|------|------|------|----------|
| `text` | str | 播报文本 | 直接使用 |
| `decision` | str | 决策类型 | 判断调用哪个适配器方法 |
| `priority` | int | 优先级 (0-3) | 映射到 TTS 策略的 priority |
| `style` | str | 语气风格 | 可映射到 TTS 的 level |
| `category` | str | 类别 | 通常为 "navigation" |
| `interruptible` | bool | 是否可打断 | 映射到 TTS 的 interrupt |

---

## 🎯 迁移方案

### 方案 1：创建 speech_event 适配器函数

在 `NavigationVoiceAdapter` 中添加一个方法，将 `speech_event` 字典转换为适配器调用：

```python
def handle_speech_event(self, speech_event: Dict[str, Any]) -> None:
    """
    处理来自 NavSpeechManager 或 NavigationEngine 的 speech_event。
    
    Args:
        speech_event: 语音事件字典，包含 text, decision, priority 等字段
    """
    if not speech_event or not speech_event.get("speak"):
        return
    
    text = speech_event.get("text", "")
    decision = speech_event.get("decision", "")
    priority = speech_event.get("priority", 0)
    style = speech_event.get("style", "calm")
    
    # 根据 decision 类型判断调用哪个方法
    if decision == "STOP":
        # STOP 通常是安全相关
        self.announce_obstacle_warning()
    elif "LEFT" in decision or "RIGHT" in decision:
        # 转向提示
        direction = "左转" if "LEFT" in decision else "右转"
        self.announce_turn(direction=direction)
    elif decision == "FORWARD":
        # 直行提示
        self.announce_straight()
    else:
        # 默认使用导航类别
        speak_navigation(text, meta={"decision": decision, "style": style})
```

### 方案 2：直接提取 text 并分类

更简单的方式：直接从 `speech_event` 提取 `text`，根据文本内容判断类别：

```python
def handle_speech_event(self, speech_event: Dict[str, Any]) -> None:
    """
    处理 speech_event，根据文本内容自动分类。
    """
    if not speech_event or not speech_event.get("speak"):
        return
    
    text = speech_event.get("text", "")
    if not text:
        return
    
    # 根据文本内容判断类别
    if any(keyword in text for keyword in ["障碍物", "危险", "停下", "无法通行", "人多", "复杂"]):
        # 安全提示
        speak_safety(text, meta={"source": "speech_event", **speech_event})
    else:
        # 导航提示
        speak_navigation(text, meta={"source": "speech_event", **speech_event})
```

---

## 📝 推荐方案

**推荐使用方案 2（文本分类）**，因为：
1. 更简单，不需要维护 decision 类型映射表
2. 更灵活，可以处理 NavigationEngine 返回的各种格式
3. 向后兼容，即使 speech_event 结构变化也能工作

---

## 🔧 实施步骤

1. 在 `NavigationVoiceAdapter` 中添加 `handle_speech_event()` 方法
2. 在 `tasks/navigation_task.py` 中替换 `self.tts_manager.speak(speech_event)` 为 `voice.handle_speech_event(speech_event)`
3. 创建测试验证迁移正确性

---

**最后更新**: 2025-01-XX












