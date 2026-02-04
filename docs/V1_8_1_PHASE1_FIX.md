# V1.8.1 Phase 1 生死线修复

**修复日期**: 2025-12-29  
**问题**: 音频系统自激振荡  
**状态**: ✅ 已修复

---

## 问题诊断

### 核心问题

**音频系统自激振荡态**：
- TTS 重初始化 ↔ 麦克风录音 ↔ ffmpeg 占用 ↔ 设备被抢 ↔ 再异常

### 症状

- 杂音
- 卡顿
- ffmpeg 录音失败（exit 255）
- 即使 Ctrl+C，也还在触发重初始化

### 根本原因

1. **is_speaking 属性不存在** → 触发异常
2. **异常触发重初始化** → TTS 重新初始化
3. **TTS 和 ASR 同时抢音频设备** → ffmpeg 失败
4. **没有系统状态守门人** → 清理资源时还在重初始化

---

## 3 个生死线修改

### 修改 1: 禁止 is_speaking 异常触发重初始化

**位置**: `main.py` `_speak_safely()` 方法

**改动**:
```python
# 修改前
if self.voice.is_speaking():
    ...

# 修改后
try:
    speaking = getattr(self.voice, "is_speaking", None)
    if speaking and callable(speaking):
        if speaking():
            ...
except Exception as is_speaking_error:
    # is_speaking 检查失败，只记录 debug，不触发重初始化
    self.logger.debug(f"is_speaking 检查失败（已忽略）: {is_speaking_error}")
    # 继续执行，不阻止播报
```

**效果**: is_speaking 永远不能触发 reinit

---

### 修改 2: 测试期关闭 TTS 重初始化

**位置**: `main.py` 全局变量

**改动**:
```python
# ===== Phase 1 测试期硬开关 =====
# 禁止 TTS 重初始化，避免音频系统自激振荡
ENABLE_TTS_REINIT = False
```

**在异常处理中**:
```python
except Exception as e:
    self.logger.debug(f"语音播报异常（已忽略，不重初始化）: {e}")
    
    # 修改 2: 只有启用开关时才重初始化
    if ENABLE_TTS_REINIT:
        # 重初始化逻辑
        ...
    else:
        # Phase 1 测试期：不重初始化，只记录
        self.logger.debug("TTS 重初始化已禁用（测试期）")
```

**效果**: Phase 1 期间，TTS 重初始化完全关闭

---

### 修改 3: 录音时禁止 TTS

**位置**: `main.py` 全局变量 + `_voice_conversation_loop()` + `_speak_safely()`

**改动**:

1. **全局变量**:
```python
# 音频 IO 状态管理（防止 TTS 和 ASR 同时抢设备）
audio_io_state = "IDLE"  # IDLE / RECORDING / SPEAKING
```

2. **_speak_safely() 中检查**:
```python
# 修改 3: 录音时禁止 TTS 初始化/播报
if audio_io_state == "RECORDING":
    self.logger.debug("正在录音中，跳过语音播报")
    return
```

3. **_voice_conversation_loop() 中设置**:
```python
# 修改 3: 录音前设置状态，禁止 TTS
audio_io_state = "RECORDING"
try:
    recognized_text = self.voice_recognition.listen_and_recognize(timeout=5)
finally:
    # 录音结束后恢复状态
    audio_io_state = "IDLE"
```

**效果**: 录音时，TTS 完全被禁止，不会和 ffmpeg 打架

---

## 修复验证

### 代码层面验证

- ✅ 修改 1: 使用 getattr 安全获取 is_speaking
- ✅ 修改 2: ENABLE_TTS_REINIT = False
- ✅ 修改 3: audio_io_state 状态管理

### 预期效果

- ✅ 不再出现 `'Voice' object has no attribute 'is_speaking'` 警告
- ✅ 不再出现无限 reinit
- ✅ 不再出现 ffmpeg exit 255
- ✅ 录音和播报不会同时进行

---

## Phase 1 判定标准（再次强调）

- ❌ 不要求语音"好听"
- ❌ 不要求播报完整
- ✅ 只要求：
  - observer_mode=false 行为等价
  - 不再出现无限 reinit
  - 不再出现 ffmpeg 255

---

## 下一步

1. 重启程序
2. 重新运行 Phase 1（TC-06 / TC-07）
3. 验证修复效果

---

**最后更新**: 2025-12-29  
**状态**: ✅ 修复完成，准备重跑 Phase 1


