# 双层防抖补丁应用总结

## ✅ 已完成的修改

### 补丁 1：main.py - TTSGuard 文本级防抖 ✅

#### 修改内容
1. **添加 TTSGuard 类**（第 39-77 行）
   - `same_text_interval`: 8.0 秒（同一句话 8 秒内只说一次）
   - `min_interval_any`: 0.3 秒（全局调用最小间隔 300ms）

2. **在 App.__init__ 中实例化**（第 91 行）
   ```python
   self._tts_guard = TTSGuard()
   ```

3. **修改统一 TTS 入口 tts_say**（第 94-110 行）
   - 添加了文本级防抖检查
   - 统一了所有 tts_say 函数（之前有 3 个重复定义，现在只有 1 个）
   - 所有模块（QueryBus、SafeMode、Navigation）都使用同一个 tts_say

#### 关键代码
```python
def tts_say(text: str) -> None:
    """统一 TTS 播报入口（带防抖）"""
    global VOICE_READY, INIT_READY
    if not INIT_READY or not VOICE_READY:
        logger.debug(f"[TTS] 初始化保护中，跳过播报: {text[:30]}...")
        return

    if not text or not text.strip():
        return

    # 文本级防抖（兜底保护）
    if not self._tts_guard.allow(text):
        logger.debug(f"[TTS] guard drop: {text[:30]}...")
        return

    self.voice.speak(text, self.tts_manager)
```

### 补丁 2：task_transition_manager.py - ASK_END 状态防抖 ✅

#### 修改内容
1. **添加状态变量**（第 37-40 行）
   ```python
   self._ask_end_pending: bool = False
   self._last_ask_end_ts: float = 0.0
   self._ask_end_cooldown_sec: float = 10.0  # 10 秒不重复问
   ```

2. **修改 decide() 方法**（第 53-69 行）
   - 接近目标判断：只有在状态变化或超过冷却时间时才触发
   - 离开接近区域时重置状态

3. **添加 clear_ask_end_pending() 方法**（第 42-46 行）
   - 用户做出选择后清除待处理状态

4. **在 main.py 中调用清除方法**（第 151 行）
   ```python
   def _handle_end_task_answer(self, result: dict) -> None:
       answer = result.get("answer")
       # 清除 ASK_END 待处理状态
       self.task_transition_manager.clear_ask_end_pending()
       ...
   ```

#### 关键代码
```python
# 接近目标判断（带状态+时间防抖）
if ctx.position.at_target or ctx.position.distance_to_target < 1.5:
    now = time.time()
    if (not self._ask_end_pending) or (now - self._last_ask_end_ts > self._ask_end_cooldown_sec):
        self._ask_end_pending = True
        self._last_ask_end_ts = now
        logger.info("[TASK] near target, ASK_END (emit)")
        self._ask_end_callback()
        return TaskDecision.ASK_END
    else:
        logger.debug("[TASK] near target, ASK_END already pending, skip")
        return TaskDecision.ASK_END
else:
    # 一旦离开"接近区域"，就允许未来再次触发
    if self._ask_end_pending:
        logger.debug("[TASK] leave target area, reset ASK_END pending")
    self._ask_end_pending = False
```

## 🎯 预期效果

### 修复前的问题
- ❌ 每帧都触发 ASK_END → 重复播报
- ❌ 同一句话被多次排队 → 语音叠加
- ❌ 无法停止播报

### 修复后的效果
- ✅ **状态防抖**：只在状态变化时触发一次 ASK_END
- ✅ **文本防抖**：同一句话 8 秒内只播一次
- ✅ **全局频率限制**：最小间隔 300ms
- ✅ **状态重置**：用户做出选择后可以再次触发

## 📝 测试验证

### 1. 状态防抖测试
**预期日志**：
```
[TASK] near target, ASK_END (emit)  # 第一次触发
[TASK] near target, ASK_END already pending, skip  # 后续跳过
[TASK] leave target area, reset ASK_END pending  # 离开时重置
```

### 2. 文本防抖测试
**预期日志**：
```
[TTS] guard drop: 您已经接近目的地，需要结束当前任务吗？...  # 重复文本被拦截
```

### 3. 用户选择后重置
**预期行为**：
- 用户选择"结束"或"继续"后，状态被清除
- 再次接近目标时可以重新触发

## 📋 相关文件

- `luna_badge_v1_2/main.py` - 添加了 TTSGuard 和防抖逻辑
- `luna_badge_v1_2/core/task/task_transition_manager.py` - 添加了状态防抖

## ✅ 语法检查

- ✅ 所有文件语法检查通过
- ✅ 无 linter 错误

## 🚀 下一步

运行实际测试，验证：
1. 日志中 `[TASK] near target, ASK_END` 不再刷屏
2. 语音播报不再重复
3. 用户选择后可以重新触发















