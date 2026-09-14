# v1.8.3 – System Orchestration Release

**版本**: v1.8.3  
**目标**: 建立 Luna Badge 的「系统级调度与串联层」  
**状态**: ✅ 代码实现完成

---

## 唯一目标（务必聚焦）

建立 Luna Badge 的「系统级调度与串联层」

让所有已有模块从"各自正确"，升级为"协同正确"。

一句话版本名：

**v1.8.3 – System Orchestration Release**

---

## 明确边界：1.8.3 不做什么

1.8.3 明确不做：
- ❌ 不引入新 AI 能力
- ❌ 不换模型
- ❌ 不优化识别精度
- ❌ 不追求"更聪明的文案"

否则会失焦。

---

## 核心问题：补上「中枢神经」

### 修改前的系统结构

```
[Camera] ─┐
[YOLO]   ─┼──► 直接播报
[OCR]    ─┤
[ASR]    ─┘
```

### 修改后的系统结构

```
[Camera / YOLO / OCR / ASR]
            ↓
     【Scene State Builder】
            ↓
     【Decision / Scheduler】
            ↓
        [TTS / Action]
```

---

## 核心新增模块

### 🔹 模块 1：Scene State Builder（场景状态构建器）

**职责**: 把"瞬时识别结果"变成"可判断的状态"

**输出示例**:
```python
{
  "scene_id": "street_static",
  "objects": ["person", "car"],
  "signs": ["no_entry"],
  "risk_level": "low",
  "stability": "stable",
  "last_changed": "5s ago"
}
```

**关键点**:
- 去瞬时
- 引入"稳定度"
- 引入"是否变化"

**实现**: `core/scene_state_builder.py`

---

### 🔹 模块 2：Decision Scheduler（调度与决策层）

**职责**: 唯一有权决定是否触发 TTS 的模块

**回答 3 个问题**:
1. 现在要不要说？
2. 如果要说，说哪一句？
3. 是不是该闭嘴？

**策略示例**:
```python
if scene.stable and already_announced(scene):
    do_nothing()
elif scene.risk_level == "high":
    interrupt_and_speak()
elif user_is_speaking():
    defer_speech()
else:
    speak_once()
```

**实现**: `core/decision_scheduler.py`

---

### 🔹 模块 3：System Memory（系统记忆）

**职责**: 轻量级系统记忆

**记录内容**:
- 最近说过什么
- 最近 10 秒的场景 hash
- 播报历史

**实现**: `core/system_memory.py`

---

## 明确禁止的事情

**❌ 禁止事项（写进 README 都不过分）**:
- ❌ YOLO / OCR 里直接调用 TTS
- ❌ ASR 里直接触发反馈播报
- ❌ "检测到就说"

**✅ 唯一允许的 TTS 调用路径**:
```
DecisionScheduler.should_speak() → tts_callback()
```

---

## 版本拆解

### v1.8.3.a（当前实现）

- ✅ 场景状态构建
- ✅ 场景 hash
- ✅ 相同场景不重复播报
- ✅ 系统记忆
- ✅ 决策调度器

### v1.8.3.b（下一步）

- ⏳ 播报冷却
- ⏳ 危险优先级可打断

### v1.8.3.c（未来）

- ⏳ 用户主动说话时，系统进入"聆听态"（已部分实现）

---

## 关键理解

你现在不是在"优化体验"，
而是在给 Luna 第一次"自我约束能力"。

这是人格系统的起点。

---

## 代码结构

```
core/
├── scene_state_builder.py  # 场景状态构建器
├── system_memory.py        # 系统记忆
└── decision_scheduler.py   # 决策调度器

main.py
└── _handle_speech_decision()  # v1.8.3 唯一 TTS 调用入口
```

---

## 执行流程

```
Frame
 ├─ YOLO
 ├─ OCR
 ├─ SceneStateBuilder.build_state()
 ├─ DecisionScheduler.should_speak()
 │    ├─ 场景稳定且已播报过 → 不播
 │    ├─ 高风险 → 可打断播报
 │    ├─ 用户正在说话 → 延迟播报
 │    ├─ 播报冷却检查
 │    └─ 文本去重检查
 └─ TTS（仅当允许）
```

---

**最后更新**: 2025-12-29  
**状态**: ✅ 代码实现完成，等待测试验证


