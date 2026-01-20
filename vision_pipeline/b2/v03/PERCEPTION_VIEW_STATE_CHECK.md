# Perception view_state 字段检查结果

**检查日期：** 2025-01-12

---

## 检查结果

### 当前代码状态

在 `b2_v03.py` 的 `tick()` 方法中（第 276-280 行）：

```python
if isinstance(perception, dict):
    view_state = perception.get("view_state", {})
    stability_score = view_state.get("stability_score")
    range_m = view_state.get("range_m")
    visibility_score = view_state.get("visibility_score", 0.75)
```

**代码行为：**
- ✅ 尝试从 `perception.get("view_state", {})` 提取字段
- ✅ 如果 `view_state` 不存在，返回空字典 `{}`
- ✅ 有完整的 fallback 策略（imu_data / 实例变量 / 默认值）

### 实际调用检查

#### 1. `run_b2_video_trace.py`（第 170 行）

```python
perception = extract_perception_from_frame(frame, frame_id, absolute_ts)
result = b2.tick(frame_ts=absolute_ts, perception=perception, frame_id=frame_id)
```

**需要检查：** `extract_perception_from_frame()` 是否包含 `view_state`

#### 2. `vision_pipeline/pipeline_controller.py`（第 461 行）

```python
perception = {
    "factors": {...},
    "events": []
}
world_change = self.b2_v03.tick(frame_ts=frame_ts, perception=perception)
```

**结论：** 当前 `pipeline_controller.py` 构造的 `perception` **不包含 `view_state` 字段**

#### 3. 测试用例 `test_b2_v041_gate_behavior_standalone.py`

测试用例中：
- ✅ 有 `make_view_state()` 函数构造 view_state
- ❌ 但测试用例**不直接调用 `tick()`**，而是直接调用 `_summarize_world_change()`
- ❌ 测试用例中**没有将 view_state 放入 perception**

---

## 结论

### 当前状态

**perception 里还没有 view_state 字段**

### 证据

1. `pipeline_controller.py` 构造的 perception 不包含 view_state
2. `run_b2_video_trace.py` 需要检查 `extract_perception_from_frame()` 的实现
3. 测试用例中 view_state 是单独构造的，没有放入 perception

### 代码兼容性

**好消息：** 当前代码已经兼容这种情况：

- ✅ 代码使用 `perception.get("view_state", {})`，如果不存在返回空字典
- ✅ 有完整的 fallback 策略：
  1. 从 `view_state` 提取（如果存在）
  2. 从 `self.imu_data` 计算（如果存在）
  3. 使用 `self.range_m` 或默认值 10.0
  4. 使用默认 `visibility_score = 0.75`

**结论：** 即使 perception 中没有 view_state，代码也能正常工作（使用 fallback 策略）

---

## 建议

### 选项 1：保持现状（推荐）

- ✅ 代码已经兼容（有 fallback）
- ✅ 不会误输出（fallback 足够保守）
- ⚠️ 需要确保 fallback 策略足够保守（不会误判为 ACTIVE）

### 选项 2：明确 fallback 策略

如果 perception 中没有 view_state，可以：
- 选项 A：降级为 READ_ONLY（更保守）
- 选项 B：使用默认值（当前策略）

**建议：** 如果 perception 中没有 view_state，降级为 READ_ONLY（更保守）

---

**版本：** v0.4.2  
**状态：** ✅ 已检查  
**结论：** perception 里**还没有** view_state 字段，但代码已兼容
