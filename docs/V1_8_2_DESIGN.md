# v1.8.2「场景稳定 × 播报抑制」设计文档

**版本**: v1.8.2  
**目标**: 让 Luna 学会"什么时候该说、什么时候不该说、什么时候只说一次"  
**状态**: ✅ 代码实现完成

---

## 目标定义

### 一句话目标

让 Luna 学会"什么时候该说、什么时候不该说、什么时候只说一次"。

### 明确不做的事

- ❌ 不引入复杂情绪模型
- ❌ 不改 YOLO / OCR / ASR
- ❌ 不碰 Observer Mode 主逻辑
- ❌ 不做学习型记忆（那是 v2）

---

## 架构设计

### 新增能力总览

引入一个轻量级「播报决策层」，放在：

```
【场景生成】 → 【播报决策层 v1.8.2】 → 【TTS 队列】
```

它只做三件事：
1. 语义去重
2. 场景稳定判断
3. 播报优先级裁决

---

## 模块拆解

### 🧩 新增模块 1：SpeechDeduplicator（语义去重）

**职责**: 同一句话，在短时间内最多播一次

**接口定义**:
```python
class SpeechDeduplicator:
    def should_speak(self, text: str) -> bool
```

**规则（v1.8.2 固定值）**:
- TTL = 8 秒
- 精确字符串匹配（不做 embedding）

**实现**: `core/speech_deduplicator.py`

---

### 🧩 新增模块 2：SceneStabilityTracker（场景稳定器）

**职责**: 判断"这是新场景，还是同一个场景在抖动"

**核心思想**: 用 hash，不用复杂结构

**输入**:
```python
scene = {
  "objects": ["person", "car"],
  "signs": ["停车", "禁止通行"]
}
```

**处理**:
```python
scene_hash = hash(sorted(objects) + sorted(signs))
```

**状态字段**:
- `last_scene_hash`
- `stable_count`

**规则**:

| 条件 | 行为 |
|------|------|
| hash 变化 | stable_count = 0 |
| hash 相同 | stable_count += 1 |
| stable_count ≥ 2 | 认为"稳定场景" |

**实现**: `core/scene_stability_tracker.py`

---

### 🧩 新增模块 3：SpeechPolicyEngine（播报策略引擎）

**职责**: 最终裁决：播 or 不播

**输入**:
```python
speech_candidate = {
  "text": "...",
  "priority": 1 | 2 | 3,
  "scene_hash": ...
}
```

**优先级定义（v1.8.2 固定）**:

| priority | 含义 | 示例 |
|----------|------|------|
| 3 | 危险 | 前方有人靠近 |
| 2 | 提醒 | 前方有停车标志 |
| 1 | 描述 | 当前环境描述 |

**决策规则（顺序不可变）**:
1. 危险永远可播（优先级穿透）
2. 非危险：
   - 场景稳定 + 已播过 → 不播
   - TTL 内重复 → 不播
3. 新场景 → 可播

**实现**: `core/speech_policy_engine.py`

---

### 🔧 修改模块 1：TTS 调用入口（唯一改点）

**修改前**:
```
generate_text → tts_engine.speak()
```

**修改后**:
```
generate_text
   ↓
SpeechPolicyEngine.should_speak()
   ↓
tts_queue.submit()
```

**⚠️ 禁止任何模块绕过 PolicyEngine 直呼 TTS**

**修改位置**: `main.py` `_handle_speech_decision()` 方法

---

## 完整执行链

```
Frame
 ├─ YOLO
 ├─ OCR
 ├─ SceneBuilder
 ├─ SceneStabilityTracker
 ├─ LLM 文本生成
 ├─ SpeechPolicyEngine
 │    ├─ 去重
 │    ├─ 稳定判断
 │    ├─ 优先级裁决
 └─ TTS（仅当允许）
```

---

## 测试用例（v1.8.2 必须通过）

### ✅ TC-08：静态场景抑制

**前置**:
- 人 + 停车牌静止 10 秒

**期望**:
- 第 1 次播
- 后续不再播

---

### ✅ TC-09：新物体进入

**前置**:
- 原场景稳定
- 新增 "自行车"

**期望**:
- 立即播一次

---

### ✅ TC-10：危险优先级穿透

**前置**:
- 场景稳定
- 连续检测到"人靠近"

**期望**:
- 可重复播（受单独 TTL 控制）

---

## 代码结构

```
core/
├── speech_deduplicator.py      # 语义去重器
├── scene_stability_tracker.py  # 场景稳定器
└── speech_policy_engine.py     # 播报策略引擎

main.py
└── _handle_speech_decision()   # v1.8.2 唯一 TTS 调用入口
```

---

## 关键原则

1. **禁止绕过 PolicyEngine**: 所有 TTS 调用必须通过 `SpeechPolicyEngine.should_speak()`
2. **轻量级设计**: 不做 embedding，不做复杂模型
3. **固定规则**: v1.8.2 使用固定规则，不做学习
4. **可调试**: 所有决策都有明确的 reason 和 metadata

---

## 下一步

1. ✅ 代码实现完成
2. ⏳ 运行测试用例（TC-08, TC-09, TC-10）
3. ⏳ 验证播报抑制效果
4. ⏳ 性能测试（确保不增加延迟）

---

**最后更新**: 2025-12-29  
**状态**: ✅ 代码实现完成，等待测试验证


