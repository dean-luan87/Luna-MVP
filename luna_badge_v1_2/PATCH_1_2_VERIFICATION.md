# PATCH 1 & 2 验证指南

## ✅ 补丁应用状态

**PATCH 1**: `modules/voice.py` - ✅ 已替换为统一播放器  
**PATCH 2**: `Luna_Badge/core/tts_manager.py` - ✅ 已替换为音频生成器

## 📋 核心变更总结

### modules/voice.py

**新架构**:
- ✅ 只依赖 `simpleaudio`，不依赖 pyttsx3 / edge-tts / pydub
- ✅ 提供 `play_audio(file_path)` - 播放 wav 文件
- ✅ 提供 `speak(text, tts_manager)` - 统一播报入口
- ✅ 提供 `is_speaking()` - 检查播放状态
- ✅ 锁保护，防止并发播放

### Luna_Badge/core/tts_manager.py

**新架构**:
- ✅ 只负责生成 wav 文件，不播放
- ✅ 提供 `synthesize(text)` - 生成音频文件，返回路径
- ✅ 提供 `speak(text)` - 兼容接口（只生成，不播放）
- ✅ 不再调用任何系统命令（afplay / say / mpg123）

## 🧪 验证步骤

### 1. 检查依赖

```bash
pip install simpleaudio edge-tts
```

### 2. 运行主程序

```bash
cd luna_badge_v1_2
python3 main.py
```

### 3. 观察日志

**应该看到**:
- ✅ `[Voice] 初始化成功` 或类似日志
- ✅ `[TTS] 开始合成文本` 日志
- ✅ `[Voice] 播放音频文件` 日志
- ✅ `[Voice] 播放完成` 日志

**不应该看到**:
- ❌ pyttsx3 相关日志
- ❌ `afplay` 或 `say` 系统命令调用
- ❌ "播放只播前 1-2 个字" 的问题

### 4. 测试播报

等待系统启动后（约 2 秒），应该能听到：
- ✅ "Luna 已启动" 完整播报
- ✅ 导航提示完整播报
- ✅ 无杂音、无卡顿、无中断

## 📝 当前调用状态

### main.py 中的调用

**当前实现**（已正确）:
```python
# 所有调用都使用统一接口
voice.speak(text, tts_manager)
```

**这是正确的**，因为：
- `voice.speak()` 内部会调用 `tts_manager.synthesize()`
- 然后调用 `voice.play_audio()` 播放

### 如果需要分步调用

```python
# 方式 1：使用便捷方法（当前 main.py 使用的方式）
voice.speak("文本", tts_manager)

# 方式 2：分步调用（更灵活）
audio_path = tts_manager.synthesize("文本")
if audio_path:
    voice.play_audio(audio_path)
```

## ⚠️ 注意事项

1. **simpleaudio 依赖**
   - 需要安装 `simpleaudio`
   - macOS 可能需要额外依赖

2. **临时文件**
   - 生成的 `tts_*.wav` 文件会在播放完成后自动清理
   - 如果播放失败，文件可能残留

3. **错误处理**
   - `synthesize()` 失败返回 `None`
   - `play_audio()` 会检查文件是否存在
   - 所有错误都有日志记录

## 🎯 下一步

如果验证通过（能正常完整播音），可以继续：
1. 启动静音保护 + 异步初始化（PATCH D 落地版）
2. PATCH E（YOLO/OCR/调度优化）

如果还有问题，请检查：
- simpleaudio 是否正确安装
- edge-tts 网络连接是否正常
- 日志中的错误信息




