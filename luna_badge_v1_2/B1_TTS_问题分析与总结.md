# B1 子进程 TTS 方案 - 问题分析与总结

## 📋 用户反馈的问题

1. **只听到了"已到达示例地点"** - 启动语音（"Luna 已启动"）可能没有播放
2. **声音变成了男声** - 原来是女声，现在变成了男声
3. **声音很小，听不清楚** - 音量设置可能不够
4. **测试一直在运行** - 需要手动停止（这是正常的，但需要改进）
5. **语音播报次数不清楚** - 只听到了2次，但实际可能播报了更多次

---

## 🔍 问题分析

### 问题 1: 启动语音未播放

**可能原因：**
- `VOICE_READY` 标志在启动后 2 秒才设置为 `True`，但启动语音可能在 2 秒内就尝试播放了
- `INIT_READY` 标志可能还未设置
- TTSGuard 可能阻止了重复的启动语音

**检查点：**
- `main.py` 中的 `boot_sequence()` 函数
- `VOICE_READY` 和 `INIT_READY` 的设置时机
- TTSGuard 的防抖逻辑

### 问题 2: 声音变成了男声（关键问题）

**根本原因：**
当前 `modules/voice.py` 中的语音选择逻辑（第 72-84 行）只检查了是否包含中文关键词，**没有优先选择女声**。

```python
# 当前代码（有问题）
voices = engine.getProperty("voices")
selected = None
for v in voices:
    name = (v.name or "").lower()
    if any(k in name for k in ("zh", "chinese", "ting-ting", "mandarin")):
        selected = v
        break  # 找到第一个中文语音就停止，可能是男声
```

**macOS nsss 驱动的语音特点：**
- macOS 的 nsss 驱动通常提供多个语音，包括：
  - `Ting-Ting` (中文女声) - 这是用户原来使用的
  - `Sin-Ji` (中文女声)
  - `Yu-shu` (中文男声)
  - 其他英文语音

**解决方案：**
需要修改语音选择逻辑，优先选择：
1. 中文 + 女声
2. 中文（任何性别）
3. 默认语音

### 问题 3: 声音很小

**当前设置：**
```python
engine.setProperty("volume", 0.9)  # 90% 音量
```

**可能原因：**
- macOS 系统音量可能较低
- pyttsx3 的 volume 属性范围是 0.0-1.0，0.9 应该是足够的
- 可能需要检查系统音量设置

**解决方案：**
- 将 volume 设置为 1.0（最大）
- 添加系统音量检查/设置功能（可选）

### 问题 4: 测试一直在运行

**这是正常行为**，但可以改进：
- 添加优雅的退出机制（Ctrl+C 处理）
- 添加 `--timeout` 参数用于测试
- 确保子进程能正确清理

### 问题 5: 语音播报次数不清楚

**可能原因：**
- TTSGuard 的防抖机制可能阻止了一些播报
- 日志不够详细，无法追踪每次播报请求
- 子进程日志（TTS-WORKER）可能没有完整输出

**解决方案：**
- 增强日志记录，记录每次 `speak()` 调用
- 记录 TTSGuard 的过滤情况
- 确保子进程日志完整输出

---

## 📝 前面做的事情总结

### 1. 应用 B1 子进程 TTS 方案

**目标：** 彻底抛弃 `afplay` / `sounddevice` / `pydub.playback`，使用 `pyttsx3` 子进程模型

**完成的工作：**

#### a) 重写 `modules/voice.py`
- 实现了基于 `multiprocessing` 的子进程 TTS 架构
- 主进程只负责将文本放入队列
- 子进程使用 `pyttsx3` 的 `nsss` 驱动顺序播报
- 实现了 `SAY` / `STOP` / `EXIT` 消息机制

#### b) 修复导入路径问题
- 删除了项目根目录的旧版 `modules/voice.py`
- 删除了项目根目录的 `modules/__init__.py`（避免导入冲突）
- 创建了 `luna_badge_v1_2/modules/__init__.py`
- 修复了 `main.py` 的路径设置

#### c) 验证方案运行
- 程序成功启动
- TTS 子进程成功启动（看到 `[TTS-WORKER] TTS 子进程启动中...` 日志）
- 系统正常运行

### 2. 保留的现有功能

- **TTSGuard** - 文本级防抖（防止重复播报）
- **状态防抖** - TaskTransitionManager 中的 ASK_END 防抖
- **启动静音保护** - `INIT_READY` 和 `VOICE_READY` 标志
- **统一 TTS 入口** - `tts_say()` 函数

### 3. 架构优势

✅ **进程隔离** - 主进程崩溃不会留下残留播放进程  
✅ **串行播报** - 不会叠音  
✅ **可控停止** - 支持 `stop()` 方法  
✅ **简单可靠** - 不依赖复杂的音频库  

---

## 🔧 需要修复的问题

### 优先级 1: 修复语音选择（女声）

**修改 `modules/voice.py` 的语音选择逻辑：**

```python
# 修改前（第 72-84 行）
voices = engine.getProperty("voices")
selected = None
for v in voices:
    name = (v.name or "").lower()
    if any(k in name for k in ("zh", "chinese", "ting-ting", "mandarin")):
        selected = v
        break

# 修改后（优先选择女声）
voices = engine.getProperty("voices")
selected = None

# 第一优先级：中文 + 女声
for v in voices:
    name = (v.name or "").lower()
    if any(k in name for k in ("zh", "chinese", "ting-ting", "mandarin")):
        if any(k in name for k in ("female", "女", "ting-ting", "sin-ji")):
            selected = v
            worker_logger.info(f"找到中文女声: {v.name}")
            break

# 第二优先级：任何中文语音
if selected is None:
    for v in voices:
        name = (v.name or "").lower()
        if any(k in name for k in ("zh", "chinese", "ting-ting", "mandarin")):
            selected = v
            worker_logger.info(f"找到中文语音: {v.name}")
            break

# 第三优先级：默认语音
if selected is None:
    selected = voices[0] if voices else None
    worker_logger.info(f"使用默认语音: {selected.name if selected else 'N/A'}")
```

### 优先级 2: 提高音量

```python
# 修改第 70 行
engine.setProperty("volume", 1.0)  # 改为最大音量
```

### 优先级 3: 增强日志

在 `Voice.speak()` 方法中添加详细日志：
```python
def speak(self, text: str, tts_manager: Optional[object] = None) -> bool:
    # ... 现有代码 ...
    self.logger.info(f"[Voice] TTS 请求已入队: {text[:50]}... (队列大小: {self._queue.qsize()})")
```

在子进程的播报逻辑中添加日志：
```python
if msg.type == "SAY":
    text = msg.text.strip()
    if not text:
        continue
    worker_logger.info(f"[TTS-WORKER] 开始播报 ({len(text)} 字符): {text[:50]}...")
    # ... 播报代码 ...
    worker_logger.info(f"[TTS-WORKER] 播报完成: {text[:50]}...")
```

### 优先级 4: 检查启动语音

检查 `main.py` 中的 `boot_sequence()` 函数，确保：
- `VOICE_READY` 在播报启动语音之前已设置为 `True`
- `INIT_READY` 在播报启动语音之前已设置为 `True`
- TTSGuard 不会阻止启动语音

---

## 📊 日志收集

### 需要收集的日志信息

1. **启动日志** - 包含 Voice 初始化和 TTS-WORKER 启动
2. **播报日志** - 每次 `speak()` 调用和 TTS-WORKER 的播报记录
3. **TTSGuard 日志** - 被过滤的播报请求
4. **错误日志** - 任何异常或错误

### 日志位置

- `logs/runtime.log` - 主进程日志
- `logs/*.log` - 其他日志文件
- 终端输出 - TTS-WORKER 子进程日志（前缀 `[TTS-WORKER]`）

### macOS nsss 可用中文语音

从测试结果看，系统中有以下中文语音：

**女声（优先选择）：**
- `Tingting (Chinese (China mainland))` - **这是用户原来使用的女声**
- `Sinji` (香港)
- `Meijia` (台湾)

**其他中文语音：**
- `Eddy (Chinese (China mainland))` - 可能是男声
- `Flo (Chinese (China mainland))` - 可能是女声
- `Grandma/Grandpa (Chinese (China mainland))` - 老人声音
- `Reed/Rocko/Sandy/Shelley (Chinese (China mainland))` - 各种声音

**修复后的选择逻辑：**
1. 第一优先级：`Tingting`（用户原来使用的）
2. 第二优先级：其他中文女声（Sinji, Meijia）
3. 第三优先级：任何中文语音
4. 第四优先级：默认语音

---

## 🎯 下一步行动

1. **立即修复语音选择** - 优先选择女声（Ting-Ting）
2. **提高音量** - 设置为 1.0
3. **增强日志** - 便于追踪播报情况
4. **检查启动语音** - 确保启动语音能正常播放
5. **测试验证** - 重新运行并验证所有问题是否解决

---

## 📌 技术细节

### B1 方案架构

```
主进程 (main.py)
  └─ Voice.speak(text)
       └─ 消息队列 (mp.Queue)
            └─ 子进程 (TTS-WORKER)
                 └─ pyttsx3 (nsss 驱动)
                      └─ macOS 系统 TTS
```

### 消息类型

- `SAY` - 播报文本
- `STOP` - 停止当前播报
- `EXIT` - 退出子进程

### 关键文件

- `luna_badge_v1_2/modules/voice.py` - B1 子进程 TTS 实现
- `luna_badge_v1_2/main.py` - 主程序，包含 TTSGuard 和统一入口
- `luna_badge_v1_2/core/task/task_transition_manager.py` - 状态防抖

---

生成时间: 2025-12-05
版本: B1 子进程 TTS 方案 v1.0

