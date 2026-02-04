# TTS 播报无法停止问题分析

## 🔴 问题描述

**现象**：强制关闭播报时，音频无法停止，持续播放直到结束。

## 🔍 根本原因

### 问题代码段 1：`pydub.playback.play()` 阻塞调用

```67:110:modules/voice.py
def play_audio(self, file_path: Optional[str]) -> bool:
    """
    播放已经生成好的音频文件（wav/mp3）
    """
    if not file_path:
        self.logger.warning("[Voice] play_audio 收到空路径，跳过")
        return False

    try:
        self._set_speaking(True)
        self.logger.info(f"[Voice] 播放音频文件: {file_path}")

        # 优先使用 pydub（支持多种格式：mp3, wav, etc.）
        if self._pydub_available:
            audio = AudioSegment.from_file(file_path)
            # 使用非阻塞播放，避免长时间阻塞
            play(audio)  # ❌ 问题：这是阻塞调用，无法中断！
            # 注意：pydub.playback.play() 是阻塞的，会等待播放完成
        elif self._simpleaudio_available:
            # 备用方案：simpleaudio（仅支持 WAV）
            if not file_path.endswith('.wav'):
                self.logger.error(f"[Voice] simpleaudio 仅支持 WAV 格式，当前文件: {file_path}，请安装 pydub: pip install pydub")
                return False
            wave_obj = sa.WaveObject.from_wave_file(file_path)
            play_obj = wave_obj.play()
            play_obj.wait_done()  # ❌ 问题：这也是阻塞调用，无法中断！
        else:
            self.logger.error("[Voice] 需要 pydub 或 simpleaudio，请安装: pip install pydub simpleaudio")
            return False

        self.logger.debug(f"[Voice] 播放完成: {file_path}")
        return True

    except Exception as e:
        self.logger.error(f"[Voice] 播放失败: {e}")
        import traceback
        self.logger.debug(traceback.format_exc())
        return False

    finally:
        self._set_speaking(False)
```

### 问题代码段 2：缺少停止机制

当前 `Voice` 类**没有实现 `stop()` 方法**，无法主动停止正在播放的音频。

## 🐛 具体问题

1. **`pydub.playback.play()` 是阻塞调用**
   - 它会一直等待音频播放完成才返回
   - 无法中途中断
   - 即使设置了 `_speaking = False`，播放进程仍在运行

2. **`simpleaudio` 的 `wait_done()` 也是阻塞的**
   - 虽然 `simpleaudio` 支持 `play_obj.stop()`，但当前代码没有保存 `play_obj` 的引用
   - 无法在播放中途调用 `stop()`

3. **没有线程管理**
   - 播放可能在主线程中执行，阻塞整个程序
   - 没有独立的播放线程，无法通过线程控制来停止

## ✅ 解决方案

### 方案 1：使用 `simpleaudio` 并实现停止机制（推荐）

**优点**：
- `simpleaudio` 支持 `play_obj.stop()` 方法
- 可以立即停止播放
- 实现简单

**实现要点**：
1. 保存 `play_obj` 的引用到实例变量
2. 在单独的线程中播放
3. 实现 `stop()` 方法，调用 `play_obj.stop()`

### 方案 2：使用 `pydub` 的异步播放

**优点**：
- 支持更多音频格式（mp3, wav, etc.）

**缺点**：
- `pydub.playback.play()` 本身不支持停止
- 需要转换为 `simpleaudio` 或使用其他库

### 方案 3：使用系统命令（macOS `afplay`）

**优点**：
- 可以通过 `killall afplay` 强制停止
- 不依赖 Python 库

**缺点**：
- 平台特定
- 需要进程管理

## 📝 推荐修复代码

需要修改 `modules/voice.py`：
1. 添加 `_play_obj` 实例变量保存播放对象
2. 在单独线程中播放
3. 实现 `stop()` 方法
4. 添加 `_stop_requested` 标志















