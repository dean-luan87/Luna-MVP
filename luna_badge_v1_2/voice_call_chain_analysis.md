# Voice 调用链分析报告

## 🔍 全局搜索结果

### 1. 所有 `.speak(` 调用位置

#### ✅ 正确调用（使用 Voice.speak(text, tts_manager)）
- `luna_badge_v1_2/main.py:59` - `self.voice.speak(text, self.tts_manager)` ✅
- `luna_badge_v1_2/main.py:80` - `self.voice.speak(text, self.tts_manager)` ✅
- `luna_badge_v1_2/main.py:107` - `self.voice.speak(text, self.tts_manager)` ✅
- `luna_badge_v1_2/main.py:142` - `self.voice.speak("好的，已结束任务。", self.tts_manager)` ✅
- `luna_badge_v1_2/main.py:145` - `self.voice.speak("好的，我会继续保持导航。", self.tts_manager)` ✅
- `luna_badge_v1_2/main.py:147` - `self.voice.speak("我没有听清楚，就先继续导航。", self.tts_manager)` ✅
- `luna_badge_v1_2/main.py:193` - `self.voice.speak("Luna 已启动", self.tts_manager)` ✅

#### ⚠️ 可疑调用（需要检查）
- `main.py:45` - `self.voice.speak("Luna 已启动")` - **缺少 tts_manager 参数！**

### 2. TTSManager 直接调用
- ❌ **未发现** `tts_manager.speak()` 或 `tts_manager.speak_sync()` 的直接调用
- ✅ `Luna_Badge/core/tts_manager.py` 已修改为只生成，不播放

### 3. 系统命令调用（afplay/say）
- ❌ **未发现** `os.system("afplay")` 在业务代码中
- ⚠️ 只在文档和测试脚本中发现（非业务代码）

### 4. Voice 实例化
- ✅ `luna_badge_v1_2/main.py:41` - `self.voice = Voice()` ✅
- ✅ `luna_badge_v1_2/main.py:140` - `self.voice = Voice()` ✅

## 🚨 关键发现

### 问题 1：main.py 中有两个不同的文件！

1. **`luna_badge_v1_2/main.py`** (v1.4.2 版本)
   - ✅ 使用 `voice.speak(text, tts_manager)` - 正确
   - ✅ 这是我们应该使用的版本

2. **`main.py`** (旧 MVP 版本)
   - ⚠️ 使用 `voice.speak("Luna 已启动")` - 缺少 tts_manager
   - ⚠️ 使用 `self.voice.is_available` - 新 Voice 没有这个属性

### 问题 2：Voice 模块缺少 `is_available` 属性

从 `main.py:42` 看：
```python
if self.voice.is_available:  # ❌ 新 Voice 没有这个属性
    self.voice.speak("Luna 已启动")  # ❌ 缺少 tts_manager
```

新 Voice 模块只有 `get_status()` 方法，没有 `is_available` 属性。

## 📋 需要修复的问题

### 1. 确认运行的是哪个 main.py
- 如果运行的是 `luna_badge_v1_2/main.py` → 调用方式正确
- 如果运行的是 `main.py` → 需要修复

### 2. 检查 Voice 模块是否有 `is_available` 属性
- 新 Voice 模块使用 `get_status()['available']`
- 需要检查是否有兼容性问题

### 3. 检查是否有其他调用路径
- 需要检查 `navigation_controller.py`、`query_bus.py` 等模块
- 确认它们都使用 `tts_say` 回调，而不是直接调用

## 🎯 下一步行动

1. 确认实际运行的 main.py 文件
2. 检查 Voice 模块的接口兼容性
3. 修复所有不正确的调用















