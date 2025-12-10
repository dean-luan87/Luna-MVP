# Voice 模块替换总结

## ✅ 已完成

### 1. 替换 `modules/voice.py`
- ✅ 已完全替换为用户提供的新版本
- ✅ 使用单通道队列模式
- ✅ 支持停止播放和清空队列
- ✅ 内置同句冷却机制（默认 3 秒）

### 2. 修改 `Luna_Badge/core/tts_manager.py`
- ✅ 修改输出文件扩展名为 `.wav`
- ⚠️ 需要验证 edge-tts 是否能直接生成 WAV

## 🔍 关键改进

### 解决的问题

1. **播报停不下来**
   - ✅ 使用队列 + 单一工作线程
   - ✅ `stop()` 方法可以终止当前播放并清空队列
   - ✅ 不再使用 pydub（无法停止）

2. **同一句话反复播**
   - ✅ 内置冷却机制（默认 3 秒）
   - ✅ 相同文本在冷却期内会被跳过

3. **多路语音叠加**
   - ✅ 所有播放请求进入队列
   - ✅ 单一后台线程串行处理
   - ✅ 不会出现并发播放

## 📝 使用说明

### 初始化
```python
from modules.voice import Voice
from Luna_Badge.core.tts_manager import TTSManager

voice = Voice()
tts_manager = TTSManager()
```

### 播报
```python
# 基本播报
voice.speak("Luna 已启动", tts_manager)

# 自定义冷却时间
voice.speak("已到达目的地", tts_manager, cooldown=5.0)
```

### 停止
```python
# 停止当前播放并清空队列
voice.stop()
```

### 程序退出
```python
# 程序退出前调用
voice.shutdown()
```

## ⚠️ 注意事项

1. **WAV 格式要求**
   - 新的 Voice 模块只支持 WAV 文件
   - TTSManager 已修改为生成 `.wav` 文件
   - 需要验证 edge-tts 是否能直接生成 WAV（如果不能，需要添加转换逻辑）

2. **冷却时间**
   - 默认冷却时间为 3 秒
   - 可以通过 `cooldown` 参数自定义
   - 导航模块的重复播报问题应该已经解决

3. **停止机制**
   - `stop()` 会立即停止当前播放
   - 会清空队列中所有待播放的文件
   - 导航模块在到达目的地时可以调用 `voice.stop()`

## 🧪 测试建议

1. **测试停止功能**
   ```python
   voice.speak("这是一段很长的测试语音...", tts_manager)
   time.sleep(2)
   voice.stop()  # 应该立即停止
   ```

2. **测试冷却机制**
   ```python
   voice.speak("测试", tts_manager)
   voice.speak("测试", tts_manager)  # 应该被跳过（3秒内）
   time.sleep(4)
   voice.speak("测试", tts_manager)  # 应该正常播放
   ```

3. **测试队列**
   ```python
   voice.speak("第一句", tts_manager)
   voice.speak("第二句", tts_manager)
   voice.speak("第三句", tts_manager)
   # 应该按顺序播放，不会叠加
   ```

## 📋 下一步

1. 验证 edge-tts 是否能直接生成 WAV
2. 如果不能，添加 MP3 到 WAV 的转换逻辑
3. 测试实际场景（导航播报、停止功能等）
4. 根据测试结果调整冷却时间




