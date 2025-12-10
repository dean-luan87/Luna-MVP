# B1 子进程 TTS 方案补丁应用完成

## ✅ 已完成的修改

### `modules/voice.py`（完全重写）

#### 核心设计
- **主进程**：只负责把文本丢到队列，不直接播放音频
- **子进程**：使用 `pyttsx3` 的 macOS 原生 `nsss` 引擎顺序播报
- **串行播报**：不会叠音
- **进程隔离**：主进程退出时，子进程自动退出，不会留下残留播放

#### 关键特性
1. **子进程 TTS Worker**：
   - 使用 `pyttsx3.init(driverName="nsss")` 在 macOS 上强制使用 nsss 驱动
   - 自动选择中文语音（如果可用）
   - 顺序处理队列中的 SAY / STOP / EXIT 消息

2. **主进程 Voice 接口**：
   - `speak(text, tts_manager=None)` - 提交播报请求（兼容旧接口）
   - `stop()` - 发送 STOP 消息打断当前播报
   - `is_speaking()` - 检查子进程是否存活
   - `close()` / `__del__()` - 发送 EXIT 消息关闭子进程

3. **消息队列**：
   - `SAY` - 播报文本
   - `STOP` - 停止当前播报
   - `EXIT` - 退出子进程

## 🎯 核心改进

### 修复前（B 方案 - sounddevice）
- ❌ 使用 `sounddevice`，可能有残留进程
- ❌ 使用 `pydub` 转码，增加复杂度
- ❌ 可能出现叠音问题

### 修复后（B1 方案 - pyttsx3 子进程）
- ✅ 完全抛弃 `afplay` / `sounddevice` / `pydub.playback`
- ✅ 使用 `pyttsx3` 的 macOS 原生 `nsss` 引擎
- ✅ 进程级隔离，主进程退出时子进程自动退出
- ✅ 串行播报，不会叠音
- ✅ 简单可靠，不依赖复杂的音频库

## 📋 依赖要求

需要安装：
```bash
pip install pyttsx3
```

## 🧪 验证步骤

### 1. 重启电脑（重要）
重启电脑以清除所有 CoreAudio 残留状态。

### 2. 运行测试
```bash
python3 main.py
```

### 3. 观察日志
应该看到：
- `[Voice] 初始化 TTS 子进程...`
- `[Voice] TTS 子进程已启动 pid=...`
- `[Voice] TTS 请求已入队: Luna 已启动`
- `[TTS-WORKER] ... 开始播报: Luna 已启动`
- `[TTS-WORKER] ... 播报完成`

### 4. 观察行为
- ✅ 启动后不应该有杂音（不再使用 sounddevice/afplay）
- ✅ 应该能听到完整的「Luna 已启动」，不会被截断
- ✅ 不会叠音（串行播报）

## 📝 接口兼容性

新的 `Voice` 类接口：
- ✅ `speak(text, tts_manager=None)` - 保持兼容
- ✅ `play_audio(file_path)` - 保留接口但返回 False（B1 不支持文件播放）
- ✅ `stop()` - 保持兼容
- ✅ `is_speaking()` - 保持兼容
- ✅ `is_available` - 保持兼容（属性）
- ✅ `get_status()` - 保持兼容

## ⚠️ 注意事项

1. **macOS 必须使用 spawn 上下文**：
   - 代码中已使用 `mp.get_context("spawn")`
   - 这是 macOS 的要求

2. **子进程日志**：
   - 子进程有独立的日志输出，前缀为 `[TTS-WORKER]`
   - 如果看不到子进程日志，检查子进程是否正常启动

3. **进程退出**：
   - 主进程退出时，子进程会自动退出（daemon=True）
   - 但建议显式调用 `voice.close()` 确保干净退出

## 🚀 下一步

如果这版能正常播报：
- 可以在此基础上添加：
  - 播报队列优先级（导航提示 > 普通提示）
  - 情绪风格（不同语速 / 文案）
  - 与导航任务链的配合（播报完成回调）

如果仍然有问题：
- 检查启动日志（包含 `[TTS-WORKER]` 前缀的部分）
- 检查是否有 `pyttsx3` 报错
- 把完整终端日志贴出来继续调试



