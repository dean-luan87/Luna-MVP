# v1.8.3a · 阶段 C：决策闭环（SPEAK / WAIT / YIELD）

**版本**: v1.8.3a  
**阶段**: C  
**目标**: 当系统"不说话"时，它必须是一个明确的决策结果，而不是悬空状态  
**状态**: ✅ 代码实现完成

---

## 阶段 C 的目标

当系统"不说话"时，它必须是一个明确的决策结果，而不是悬空状态。

---

## 决策闭环定义

### 决策只有三种状态

| 状态 | 含义 | 行为 |
|------|------|------|
| SPEAK | 可以且应该说 | 调用 TTS |
| WAIT | 不能说，但系统继续运行 | 不播报 |
| YIELD | 用户优先 | 主动让位 |

**注意**: 这是决策状态，不是 TTS 状态

---

## 最小结构定义

```python
DecisionResult = {
    "action": "SPEAK" | "WAIT" | "YIELD",
    "reason": str
}
```

---

## 决策逻辑（核心）

```python
def decide(scene_state, speech_gate, user_state):
    # 决策 1: 用户正在说话 → YIELD
    if user_state.is_speaking:
        return {"action": "YIELD", "reason": "user_speaking"}

    # 决策 2: 语音总闸检查 → WAIT 或 SPEAK
    if not speech_gate.can_speak(scene_state.scene_hash):
        return {"action": "WAIT", "reason": "speech_gate_blocked"}

    # 决策 3: 可以说话 → SPEAK
    return {"action": "SPEAK", "reason": "normal_scene"}
```

**只有这三条判断，不要多。**

---

## 主循环必须明确消费这个结果

```python
decision = decide(...)

if decision["action"] == "SPEAK":
    _speak_safely(text, scene_hash)

elif decision["action"] == "WAIT":
    pass  # 明确：系统在运行，只是不说话

elif decision["action"] == "YIELD":
    pass  # 明确：用户优先，系统让位
```

**关键点**:
- 没有 default
- 没有 else
- 没有"兜底说一句"

---

## 这一步完成后，会立刻解决什么问题

### 1. "卡住感"消失

系统沉默 ≠ 系统挂了

### 2. 调试可读性暴涨

日志能明确告诉你：
- 现在是在 WAIT，原因是 `speech_gate_blocked_cooldown`
- 现在是在 YIELD，原因是 `user_speaking`

### 3. 为阶段 A（调度器）打基础

没有 C，A 一定乱

---

## 工程级判断

**B 控制"能不能说"，C 定义"现在在干嘛"。**

你刚才遇到的所有"卡住""怪""不像活的"，
100% 是因为 C 不存在，不是你写错代码。

---

## 实现位置

- `main.py` `_handle_speech_decision()`: 返回决策结果
- `main.py` `_execute_speech_decision()`: 执行决策结果
- `main.py` `process_frame()`: 明确消费决策结果

---

## 决策原因列表

### YIELD
- `user_speaking`: 用户正在说话

### WAIT
- `speech_gate_blocked_user_speaking`: 用户正在说话（总闸检查）
- `speech_gate_blocked_tts_busy`: TTS 正在占用
- `speech_gate_blocked_cooldown`: 播报冷却中
- `speech_gate_blocked_duplicate_scene`: 重复场景
- `no_result`: 没有处理结果
- `audio_disabled_or_no_text`: 音频禁用或没有文本

### SPEAK
- `normal_scene`: 正常场景

---

**最后更新**: 2025-12-29  
**状态**: ✅ 代码实现完成，等待测试验证


