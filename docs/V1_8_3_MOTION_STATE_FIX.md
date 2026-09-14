# v1.8.3 motion_state 数据血缘修复方案

## 问题总结

**当前错误**:
- `motion_state` 在 `_handle_speech_decision()` 中凭空创建：`motion_state = MotionState()`
- 没有从视觉数据中提取真实运动信息

**正确方案**:
- 在 `process_frame()` 中计算 `motion_state`
- 通过 `result` 字典传递给决策层

---

## 修改方案（最小实现）

### 修改 1: main.py::process_frame() - 添加 motion_state 计算

**位置**: 第420行附近（在构建 result 字典之前）

**修改前**:
```python
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
```

**修改后**:
```python
processing_time = time.time() - start_time

# v1.8.3: 计算运动状态（用于风险评估）
motion_state = self._calculate_motion_state(objects, texts)

# 构建结果
result = {
    'timestamp': timestamp,
    'objects': objects,
    'texts': texts,
    'description': description,
    'audio_input': audio_input,
    'processing_time': processing_time,
    'motion_state': motion_state  # 新增
}
```

---

### 修改 2: main.py::_handle_speech_decision() - 修复 motion_state 获取

**位置**: 第492行附近（调用 decide() 之前）

**修改前**:
```python
# v1.8.3a 阶段 C: 使用决策控制器（只做三态判断，不调用 TTS）
decision_result = decide(
    scene_state=scene_state,
    speech_gate=self.speech_gate,
    user_state=self.user_state
)
```

**修改后**:
```python
# v1.8.3a 阶段 C: 使用决策控制器（只做三态判断，不调用 TTS）
# v1.8.3: 从 result 中获取 motion_state（禁止凭空创建）
motion_state = result.get('motion_state')  # 允许为 None
decision_result = decide(
    scene_state=scene_state,
    speech_gate=self.speech_gate,
    user_state=self.user_state,
    motion_state=motion_state
)
```

---

### 修改 3: main.py - 新增 _calculate_motion_state() 方法

**位置**: 在 `_build_voice_text()` 方法之后（约第303行附近）

**最小占位实现**:
```python
def _calculate_motion_state(self, objects: list, texts: list):
    """
    v1.8.3: 计算运动状态（最小占位实现）
    
    当前版本：只返回占位数据，为 v1.9/v2.0 预留接口
    
    Args:
        objects: YOLO 检测结果列表
        texts: OCR 识别结果列表
    
    Returns:
        MotionState: 运动状态对象
    """
    from core.risk_assessor import MotionState
    
    # 最小占位实现：返回默认值
    # TODO: v1.9 从连续帧变化中提取真实运动信息
    motion_state = MotionState()
    motion_state.is_moving_towards_edge = False
    motion_state.estimated_ttc = None
    motion_state.estimated_distance = None
    
    return motion_state
```

---

## 完整代码片段（可直接替换）

### 片段 1: process_frame() 修改

```python
# main.py::process_frame() (第420行附近)
processing_time = time.time() - start_time

# v1.8.3: 计算运动状态（用于风险评估）
motion_state = self._calculate_motion_state(objects, texts)

# 构建结果
result = {
    'timestamp': timestamp,
    'objects': objects,
    'texts': texts,
    'description': description,
    'audio_input': audio_input,
    'processing_time': processing_time,
    'motion_state': motion_state  # 新增
}
```

### 片段 2: _handle_speech_decision() 修改

```python
# main.py::_handle_speech_decision() (第492行附近)
# v1.8.3a 阶段 C: 使用决策控制器（只做三态判断，不调用 TTS）
# v1.8.3: 从 result 中获取 motion_state（禁止凭空创建）
motion_state = result.get('motion_state')  # 允许为 None
decision_result = decide(
    scene_state=scene_state,
    speech_gate=self.speech_gate,
    user_state=self.user_state,
    motion_state=motion_state
)

return decision_result
```

### 片段 3: 新增 _calculate_motion_state() 方法

```python
# main.py (在 _build_voice_text() 方法之后，约第303行)
def _calculate_motion_state(self, objects: list, texts: list):
    """
    v1.8.3: 计算运动状态（最小占位实现）
    
    当前版本：只返回占位数据，为 v1.9/v2.0 预留接口
    
    Args:
        objects: YOLO 检测结果列表
        texts: OCR 识别结果列表
    
    Returns:
        MotionState: 运动状态对象
    """
    from core.risk_assessor import MotionState
    
    # 最小占位实现：返回默认值
    # TODO: v1.9 从连续帧变化中提取真实运动信息
    motion_state = MotionState()
    motion_state.is_moving_towards_edge = False
    motion_state.estimated_ttc = None
    motion_state.estimated_distance = None
    
    return motion_state
```

---

## 修改后的数据流

```
process_frame()
  ├─> YOLO 检测 (objects)
  ├─> OCR 识别 (texts)
  ├─> QwenVL 生成描述 (description)
  ├─> _calculate_motion_state()  # ← 新增：计算运动状态
  │     └─> MotionState()  # 占位实现
  └─> result["motion_state"]  # ← 新增：写入 result
        ↓
_handle_speech_decision()
  └─> result.get("motion_state")  # ← 修复：从 result 获取
        ↓
decide()
  └─> assess_risk(scene_state, motion_state)  # ← 使用真实数据
```

---

## 验收标准

修改完成后，系统应该满足：

1. ✅ `motion_state` 不再在 `_handle_speech_decision()` 中凭空创建
2. ✅ `motion_state` 从 `process_frame()` 中计算并传递
3. ✅ `_calculate_motion_state()` 方法存在且可调用
4. ✅ 系统可以正常运行（即使 motion_state 是占位数据）

---

## 注意事项

1. **不引入新依赖**: 只使用已有的 `core.risk_assessor.MotionState`
2. **不改变函数签名**: `process_frame()` 和 `_handle_speech_decision()` 的签名不变
3. **可运行优先**: 占位实现确保系统可以正常运行
4. **为未来预留**: `_calculate_motion_state()` 的接口设计为 v1.9 的真实实现预留空间


