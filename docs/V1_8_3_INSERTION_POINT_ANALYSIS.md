# v1.8.3 风险评估插入点分析报告

## Prompt 2 结果：精确插入点定位

### 当前实现状态检查

**发现**: `assess_risk()` 已经在 `core/decision_controller.py::decide()` 中被调用

**当前代码位置**: `core/decision_controller.py` 第57-84行

```python
# 决策 0: 风险评估（最高优先级，但用户说话时仍让位）
risk = assess_risk(scene_state, motion_state)

if risk.level == RiskLevel.IMMEDIATE:
    # LV1: 强制插队，但用户说话时仍让位
    if user_state.is_speaking:
        # 用户正在说话，等用户说完再警报
        return {
            "action": "YIELD",
            "reason": "user_speaking_risk_pending",
            "risk_result": risk
        }
    else:
        # LV1 强制发声
        return {
            "action": "RISK_LV1",
            "reason": f"immediate_risk_{risk.reason}",
            "risk_result": risk
        }
elif risk.level == RiskLevel.POTENTIAL:
    # LV2: 只算不说，不触发语音
    return {
        "action": "WAIT",
        "reason": f"lv2_risk_{risk.reason}",
        "risk_result": risk
    }
# SAFE: 继续正常流程
```

---

## 最优插入点分析

### ✅ 当前插入点评估

**位置**: `core/decision_controller.py::decide()` 函数内部（第57行）

**优点**:
1. ✅ **不改变业务逻辑顺序**: 风险评估在决策流程的最开始，优先级最高
2. ✅ **不破坏 scene description**: `scene_state` 已经在 `_handle_speech_decision()` 中构建完成
3. ✅ **不直接调用 TTS**: 只返回决策结果，由 `_execute_speech_decision()` 处理
4. ✅ **符合决策层职责**: 风险评估是决策的一部分，放在决策控制器中合理

**调用链**:
```
main.py::process_frame()
  → _handle_speech_decision()
    → scene_state_builder.build_state()  # 构建场景状态
    → decide()  # ← assess_risk() 在这里调用
      → assess_risk(scene_state, motion_state)
```

---

### ⚠️ 当前问题：motion_state 传递

**问题**: `motion_state` 目前是占位实现，需要从视觉数据中提取

**当前调用位置**: `main.py::_handle_speech_decision()` 第490行

```python
# v1.8.3: 集成风险评估（LV2 → LV1）
from core.risk_assessor import MotionState
motion_state = MotionState()  # TODO: 从视觉数据中提取真实运动状态
decision_result = decide(
    scene_state=scene_state,
    speech_gate=self.speech_gate,
    user_state=self.user_state,
    motion_state=motion_state
)
```

**问题分析**:
- `motion_state` 应该在 `process_frame()` 中计算，而不是在 `_handle_speech_decision()` 中创建空对象
- 需要从连续帧的 YOLO/OCR 结果中提取运动信息

---

## 推荐的完整插入方案

### 方案 A：保持当前结构（推荐）

**插入点 1**: `main.py::process_frame()` (第420行附近)
- **目的**: 计算 `motion_state`
- **位置**: 在生成 `result` 字典之后，调用 `_handle_speech_decision()` 之前

```python
# 当前代码（第420-430行）
processing_time = time.time() - start_time

# 构建结果
result = {
    'timestamp': timestamp,
    'objects': objects,
    'texts': texts,
    'description': description,
    'audio_input': audio_input,
    'processing_time': processing_time
}

# ⬇️ 建议插入位置：在这里计算 motion_state
# v1.8.3: 计算运动状态（用于风险评估）
from core.risk_assessor import MotionState
motion_state = self._calculate_motion_state(objects, texts)  # 需要实现

# 然后传递给决策层
result['motion_state'] = motion_state
```

**插入点 2**: `main.py::_handle_speech_decision()` (第490行)
- **目的**: 传递 `motion_state` 给 `decide()`
- **当前状态**: ✅ 已实现，但 `motion_state` 是空对象

**需要修改**:
```python
# 当前代码（第490行）
motion_state = MotionState()  # ❌ 空对象

# 应该改为
motion_state = result.get('motion_state')  # ✅ 从 result 中获取
```

**插入点 3**: `core/decision_controller.py::decide()` (第57行)
- **目的**: 调用 `assess_risk()`
- **当前状态**: ✅ 已实现，位置合理

---

### 方案 B：在 process_frame 中直接调用（不推荐）

**原因**: 
- 会破坏决策层的封装
- 风险评估结果需要在决策流程中使用
- 不符合"决策层统一管理"的原则

---

## 最终推荐：方案 A

### 需要修改的文件和位置

1. **`main.py::process_frame()`** (第420行附近)
   - 添加 `motion_state` 计算逻辑
   - 将 `motion_state` 添加到 `result` 字典

2. **`main.py::_handle_speech_decision()`** (第490行)
   - 从 `result` 中获取 `motion_state`，而不是创建空对象

3. **`main.py`** (新增方法)
   - 实现 `_calculate_motion_state()` 方法
   - 从连续帧的 YOLO/OCR 结果中提取运动信息

4. **`core/decision_controller.py::decide()`** (第57行)
   - ✅ 已正确实现，无需修改

---

## 代码片段（前后对比）

### 修改前

```python
# main.py::process_frame() (第420-433行)
processing_time = time.time() - start_time

result = {
    'timestamp': timestamp,
    'objects': objects,
    'texts': texts,
    'description': description,
    'audio_input': audio_input,
    'processing_time': processing_time
}

# 5. v1.8.3a 阶段 C: 决策闭环（SPEAK / WAIT / YIELD）
decision = self._handle_speech_decision(result)
```

```python
# main.py::_handle_speech_decision() (第490行)
motion_state = MotionState()  # TODO: 从视觉数据中提取真实运动状态
decision_result = decide(
    scene_state=scene_state,
    speech_gate=self.speech_gate,
    user_state=self.user_state,
    motion_state=motion_state
)
```

### 修改后（推荐）

```python
# main.py::process_frame() (第420-433行)
processing_time = time.time() - start_time

# v1.8.3: 计算运动状态（用于风险评估）
motion_state = self._calculate_motion_state(objects, texts)

result = {
    'timestamp': timestamp,
    'objects': objects,
    'texts': texts,
    'description': description,
    'audio_input': audio_input,
    'processing_time': processing_time,
    'motion_state': motion_state  # 新增
}

# 5. v1.8.3a 阶段 C: 决策闭环（SPEAK / WAIT / YIELD）
decision = self._handle_speech_decision(result)
```

```python
# main.py::_handle_speech_decision() (第490行)
motion_state = result.get('motion_state')  # 从 result 中获取
decision_result = decide(
    scene_state=scene_state,
    speech_gate=self.speech_gate,
    user_state=self.user_state,
    motion_state=motion_state
)
```

---

## 结论

**最优插入点**: 
- ✅ `assess_risk()` 的调用位置（`core/decision_controller.py::decide()` 第57行）**已正确**
- ⚠️ 需要补充：`motion_state` 的计算和传递逻辑

**需要实现**:
1. `main.py::_calculate_motion_state()` 方法（从视觉数据提取运动信息）
2. 在 `process_frame()` 中计算 `motion_state` 并传递给决策层

**不改变**:
- ✅ 决策流程顺序
- ✅ scene description 生成
- ✅ TTS 调用路径


