# 双层防抖补丁应用完成

## ✅ 已完成的修改

### 补丁 1：main.py - TTSGuard 文本级防抖

#### 1. 添加 TTSGuard 类
- ✅ 位置：`main.py` 第 39-77 行
- ✅ 功能：
  - 同一句话 8 秒内只说一次
  - 全局调用最小间隔 300ms
  - 防止重复播报

#### 2. 在 App.__init__ 中实例化
- ✅ 位置：`main.py` 第 89 行
- ✅ `self._tts_guard = TTSGuard()`

#### 3. 修改统一 TTS 入口 tts_say
- ✅ 位置：`main.py` 第 91-108 行
- ✅ 添加了文本级防抖检查
- ✅ 统一了所有 tts_say 函数（之前有 3 个重复定义，现在只有 1 个）

### 补丁 2：task_transition_manager.py - ASK_END 状态防抖

#### 1. 添加状态变量
- ✅ 位置：`task_transition_manager.py` 第 37-40 行
- ✅ `_ask_end_pending`: 是否已有待处理的 ASK_END
- ✅ `_last_ask_end_ts`: 上次触发时间
- ✅ `_ask_end_cooldown_sec`: 冷却时间 10 秒

#### 2. 修改 decide() 方法
- ✅ 位置：`task_transition_manager.py` 第 53-69 行
- ✅ 接近目标判断：只有在状态变化或超过冷却时间时才触发
- ✅ 离开接近区域时重置状态

#### 3. 添加 clear_ask_end_pending() 方法
- ✅ 位置：`task_transition_manager.py` 第 42-46 行
- ✅ 用户做出选择后清除待处理状态

#### 4. 在 main.py 中调用清除方法
- ✅ 位置：`main.py` 第 151 行
- ✅ 在 `_handle_end_task_answer()` 中调用 `clear_ask_end_pending()`

## 🎯 预期效果

### 修复前
- ❌ 每帧都触发 ASK_END → 重复播报
- ❌ 同一句话被多次排队 → 语音叠加
- ❌ 无法停止播报

### 修复后
- ✅ 只在状态变化时触发一次 ASK_END
- ✅ 同一句话 8 秒内只播一次
- ✅ 全局调用最小间隔 300ms
- ✅ 用户做出选择后可以再次触发

## 📝 测试建议

1. **测试状态防抖**：
   - 接近目标时，应该只看到一次 `[TASK] near target, ASK_END (emit)`
   - 后续应该看到 `[TASK] near target, ASK_END already pending, skip`

2. **测试文本防抖**：
   - 连续调用相同文本，应该看到 `[TTS] guard drop: ...`
   - 8 秒后可以再次播报

3. **测试离开区域**：
   - 离开接近区域后，应该看到 `[TASK] leave target area, reset ASK_END pending`
   - 再次接近时可以重新触发

## 📋 相关文件

- `luna_badge_v1_2/main.py` - 添加了 TTSGuard
- `luna_badge_v1_2/core/task/task_transition_manager.py` - 添加了状态防抖















