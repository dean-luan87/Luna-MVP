# TTS 实现分析报告

## 📋 分析时间
2024-12-04

## 🔍 现有 TTS 实现分析

### 1. 主要实现：`modules/voice.py`

**类名**: `Voice`

**关键方法**:
- `speak(text: str)` - 入口方法（第 159 行）
- `_speak_thread(text: str)` - 播报线程（第 196 行）
- `_speak_pyttsx3(text: str)` - pyttsx3 播放（第 210 行）
- `_speak_edge_tts(text: str)` - edge-tts 播放（第 247 行）

### 2. 播放流程分析

#### `speak()` 方法（第 159-194 行）

```python
def speak(self, text: str) -> bool:
    # 1. 检查是否正在播报
    with self._lock:
        if self.speaking:
            logger.warning("正在播报中，跳过新的播报请求")
            return False
        self.speaking = True
    
    # 2. 在新线程中播报
    thread = threading.Thread(target=self._speak_thread, args=(text,))
    thread.daemon = True
    thread.start()
    return True
```

**问题发现**:
- ✅ 已有 `self.speaking` 检查
- ✅ 已有 `self._lock` 锁
- ⚠️ **但检查后立即返回，线程是异步启动的**
- ⚠️ **如果主循环调用很快，可能在 `self.speaking = True` 之前多次进入**

#### `_speak_pyttsx3()` 方法（第 210-245 行）

```python
def _speak_pyttsx3(self, text: str):
    if self.engine:
        # ⚠️ 问题：清空之前的队列（会打断正在播放的）
        self.engine.stop()
        
        # 开始播报
        self.engine.say(text)
        self.engine.runAndWait()  # 阻塞直到播放完成
```

**问题发现**:
- ❌ **`self.engine.stop()` 会打断正在播放的内容**
- ✅ `runAndWait()` 是同步阻塞的，会等待播放完成

#### `_speak_edge_tts()` 方法（第 247-279 行）

```python
def _speak_edge_tts(self, text: str):
    async def _async_speak():
        communicate = edge_tts.Communicate(text, self.voice_name)
        await communicate.save("temp_voice.mp3")
        
        # 播放音频文件
        subprocess.run(['afplay', 'temp_voice.mp3'], check=True)  # 阻塞调用
```

**问题发现**:
- ✅ `subprocess.run()` 是同步阻塞的
- ⚠️ 但如果多次调用，可能同时启动多个 `afplay` 进程

### 3. 根本问题

**问题 1：`self.engine.stop()` 会打断播放**
- 在 `_speak_pyttsx3()` 中，每次调用都会先 `stop()`
- 如果主循环快速调用，新的播报会打断旧的

**问题 2：检查时机问题**
- `speak()` 检查 `self.speaking` 后立即启动线程
- 如果主循环在很短时间内多次调用，可能都通过了检查

**问题 3：线程启动是异步的**
- `thread.start()` 立即返回，不等待线程实际开始执行
- 在 `_speak_thread()` 执行前，可能有多次调用通过检查

## 🎯 修复方案

### 方案：在真正的播放函数上加互斥锁

**不改动线程模型，只在播放函数上加锁**

1. **在 `_speak_pyttsx3()` 和 `_speak_edge_tts()` 上加锁**
2. **移除 `self.engine.stop()` 的自动调用**（或改为条件调用）
3. **添加播放开始/结束日志**

## 📝 下一步

等待用户确认后，应用修复补丁。




