# speech_event 迁移总结报告（v1.4.6d）

## 📋 搜索结果总结

### 1. speech_event 的定义位置

**主要来源**：
- ✅ `core/speech/nav_speech_manager.py` - `build_from_nav()` 方法（第 46-176 行）
- ✅ `NavigationEngine` 的结果 - `result.get("speech_event")`（在 `tasks/navigation_task.py` 第 269 行）

### 2. speech_event 的数据结构

根据 `nav_speech_manager.py` 的 `_build_event()` 方法，`speech_event` 的结构为：

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

### 4. 关键 decision 类型

根据 `nav_speech_config.py`，常见的 `decision` 类型包括：

| Decision | 优先级 | 语气 | 说明 |
|----------|--------|------|------|
| `STOP` | 3 | alert | 停止（最高优先级） |
| `REPLAN` | 3 | alert | 重新规划 |
| `HARD_LEFT` / `HARD_RIGHT` | 2 | alert | 急转 |
| `SLIGHT_LEFT` / `SLIGHT_RIGHT` | 1 | calm | 微调 |
| `FORWARD` | 0 | calm | 直行 |

---

## ✅ 已完成的迁移

### 1. NavigationVoiceAdapter 增强

**新增方法**：`handle_speech_event()`

**功能**：
- 兼容字典格式的 `speech_event`
- 兼容字符串格式的 `speech_event`（向后兼容）
- 根据 `decision` 类型自动映射到对应的适配器方法
- 根据文本内容自动分类（安全 vs 导航）

**映射规则**：
- `STOP` → `announce_obstacle_warning()` (SAFETY)
- `HARD_LEFT` / `LEFT` → `announce_turn(direction="左转")` (NAVIGATION)
- `HARD_RIGHT` / `RIGHT` → `announce_turn(direction="右转")` (NAVIGATION)
- `SLIGHT_LEFT` → `announce_turn(direction="左转")` (NAVIGATION)
- `SLIGHT_RIGHT` → `announce_turn(direction="右转")` (NAVIGATION)
- `FORWARD` / `GO` → `announce_straight()` (NAVIGATION)
- 其他 → 根据文本内容自动分类

### 2. tasks/navigation_task.py 迁移

**位置**：第 290-294 行

**旧代码**：
```python
if speech_event and self.tts_manager:
    try:
        self.tts_manager.speak(speech_event)  # ⚠️ 传入字典
    except Exception as e:
        self.logger.warning(f"TTS 播报失败: {e}")
```

**新代码**：
```python
if speech_event:
    try:
        from task_engine.navigation import NavigationVoiceAdapter
        voice = NavigationVoiceAdapter()
        voice.handle_speech_event(speech_event)
    except Exception as e:
        self.logger.warning(f"TTS 播报失败: {e}")
```

### 3. 测试覆盖

**新增测试文件**：`tests/v1_4_6d/test_speech_event_migration.py`

**测试用例**（10 个，全部通过）：
- ✅ STOP decision → SAFETY 类别
- ✅ 转向 decision → NAVIGATION 类别
- ✅ FORWARD decision → NAVIGATION 类别
- ✅ 根据文本内容自动分类为 SAFETY
- ✅ 根据文本内容自动分类为 NAVIGATION
- ✅ 字符串类型兼容性
- ✅ Meta 数据保留
- ✅ speak=False 时跳过
- ✅ 空文本时跳过
- ✅ None 输入安全处理

---

## 📊 迁移效果

### 迁移前

```python
# 旧代码：直接传入字典，可能导致类型错误
self.tts_manager.speak(speech_event)  # speech_event 是 dict
```

**问题**：
- `tts_manager.speak()` 期望字符串，但收到字典
- 没有应用 TTS 策略体系（priority / interrupt）
- 无法自动分类（安全 vs 导航）

### 迁移后

```python
# 新代码：自动转换并应用策略
voice.handle_speech_event(speech_event)
```

**优势**：
- ✅ 自动提取 `text` 字段
- ✅ 根据 `decision` 类型自动映射到正确的适配器方法
- ✅ 自动应用 TTS 策略体系（priority / interrupt）
- ✅ 自动分类（SAFETY / NAVIGATION / TASK）
- ✅ 保留原始 meta 数据
- ✅ 向后兼容字符串类型

---

## 🎯 迁移验证

### 测试结果

- **v1.4.6d 测试套件**: 30 个测试用例全部通过
  - `test_navigation_voice_adapter.py`: 20 个测试用例
  - `test_speech_event_migration.py`: 10 个测试用例
- **无 linter 错误**
- **向后兼容**: 支持字符串和字典两种格式

### 功能验证

1. ✅ **字典格式处理**: 正确提取 `text` 和 `decision`
2. ✅ **字符串格式兼容**: 向后兼容旧版本
3. ✅ **决策类型映射**: STOP / LEFT / RIGHT / FORWARD 正确映射
4. ✅ **文本内容分类**: 根据关键词自动分类为 SAFETY / NAVIGATION
5. ✅ **Meta 数据保留**: 原始字段和自定义 meta 都保留

---

## 📝 其他需要迁移的文件

### 已迁移 ✅
- `tasks/navigation_task.py` - 已迁移

### 待检查（可能不需要迁移）

以下文件中的 `tts_manager.speak()` 调用属于系统级功能，**不需要**迁移到 `NavigationVoiceAdapter`：

- `task_chain/task_chain_manager.py` (5 处) - 任务生命周期管理
- `decision_core/decision_core.py` (3 处) - 决策核心
- `task_engine/ask/ask_runtime.py` (8 处) - AskChain 问询
- `task_engine/scene/scene_runtime.py` (3 处) - 场景切换
- `core/flow_engine/runtime.py` (4 处) - 流程运行时

这些调用可以**可选优化**为使用 `speak_task()` 或 `speak_system()`，但不强制迁移。

---

## ✅ 迁移完成检查清单

- [x] 分析 `speech_event` 的数据结构
- [x] 创建 `handle_speech_event()` 方法
- [x] 实现决策类型映射逻辑
- [x] 实现文本内容自动分类
- [x] 替换 `tasks/navigation_task.py` 中的调用
- [x] 创建测试用例验证功能
- [x] 运行测试确保全部通过
- [x] 验证向后兼容性

---

## 🎉 迁移完成

**v1.4.6d 的 speech_event 迁移已完成！**

现在导航任务中的所有语音播报都通过 `NavigationVoiceAdapter` 统一管理，自动应用 TTS 策略体系。

---

**最后更新**: 2025-01-XX












