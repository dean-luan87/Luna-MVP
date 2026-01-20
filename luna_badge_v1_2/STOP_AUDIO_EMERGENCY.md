# 紧急停止音频播放指南

## 🚨 如果音频无法停止

### 方法 1：使用代码停止（推荐）

```python
from modules.voice import Voice

voice = Voice()
voice.stop()  # 强制停止
```

### 方法 2：命令行强制停止

```bash
# 停止所有 Python 进程
pkill -9 -f "python.*main"

# 停止系统音频播放进程
killall -9 afplay
killall -9 say

# 重置系统音量（可能中断播放）
osascript -e 'tell application "System Events" to set volume output volume 0'
sleep 1
osascript -e 'tell application "System Events" to set volume output volume 50'
```

### 方法 3：系统级停止

如果以上方法都不行，可能是系统音频缓冲区的问题：

1. **等待播放完成**：音频已经在系统缓冲区中，只能等待播放完（通常几秒内）

2. **重启音频服务**（需要管理员权限）：
   ```bash
   sudo killall coreaudiod
   # 系统会自动重启 coreaudiod
   ```

3. **静音系统音量**：
   - 按 `F10` 或 `F11` 静音
   - 或使用菜单栏音量控制

## ⚠️ 已知问题

1. **pydub 播放无法中断**
   - `pydub.playback.play()` 是阻塞调用
   - 一旦开始播放，无法中途停止
   - **解决方案**：优先使用 `simpleaudio`（已实现）

2. **系统音频缓冲区**
   - macOS 的音频系统有缓冲区
   - 即使进程停止，已缓冲的音频仍会播放完
   - 通常只有几秒的延迟

3. **线程无法强制终止**
   - Python 的线程无法真正强制终止
   - 只能通过标志位让线程自然结束
   - 如果线程卡在阻塞调用中，可能需要等待

## 🔧 已实现的改进

1. ✅ 添加了 `stop()` 方法
2. ✅ 使用 `simpleaudio` 优先（支持停止）
3. ✅ 在单独线程中播放（不阻塞主线程）
4. ✅ 自动停止系统音频进程（macOS）
5. ✅ 立即清理状态标志

## 📝 使用建议

1. **安装 simpleaudio**（推荐）：
   ```bash
   pip install simpleaudio
   ```
   这样可以获得最好的停止支持。

2. **及时调用 stop()**：
   ```python
   voice.speak("长文本...", tts_manager)
   # 需要停止时
   voice.stop()
   ```

3. **检查状态**：
   ```python
   if voice.is_speaking():
       voice.stop()
   ```















