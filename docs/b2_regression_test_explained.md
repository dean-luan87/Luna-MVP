# B2 回归测试：模拟数据 vs 真实数据

## 一、什么是"真实 perception 数据"？

### 当前状态（模拟数据）

在 `b2_regression_test_all.py` 中，我们使用的是**硬编码的模拟数据**：

```python
perception = {
    "path": {"surface": "concrete", "has_path": True},
    "env": {"scene": "road", "density": "low", "indoor": False},
    "people": {"count": 0, "moving": False},
    "events": [],
}
```

这些数据是**假的、固定的**，不依赖实际视频内容。

### 真实 perception 数据

**真实 perception 数据**应该来自实际的感知系统：

1. **路径信息** (`path`)
   - 来源：`NavigationExecutor` 的输出
   - 字段：`path_type`（concrete/gravel/stairs）、`has_path`（是否有清晰路径）

2. **环境信息** (`env`)
   - 来源：`ModelingExecutor` 的场景识别
   - 字段：`scene_label`（road/plaza/indoor/market）、`density`（人群密度）

3. **人群信息** (`people`)
   - 来源：YOLO 检测结果 + Tracker
   - 字段：`count`（人数）、`moving`（是否移动）

4. **事件信息** (`events`)
   - 来源：事件检测器
   - 字段：`type`（construction/accident/block）、`severity`

## 二、如何获取真实数据？

### 方式 1：通过 PipelineController

在 `vision_pipeline/pipeline_controller.py` 的 `process_frame` 方法中（第 432-458 行），已经实现了从真实模块提取 perception 的逻辑：

```python
# 构建 perception 字典（B2 v0.3 需要）
perception = {}

# path 信息（从 navigation_result）
if navigation_result:
    if hasattr(navigation_result, "path_type"):
        perception["path"]["surface"] = navigation_result.path_type
    if hasattr(navigation_result, "has_path"):
        perception["path"]["has_path"] = navigation_result.has_path

# env 信息（从 modeling_result）
if modeling_result:
    scene = getattr(modeling_result, "scene_label", None)
    if scene:
        perception["env"]["scene"] = scene

# people 信息（从 objects 中统计）
person_count = sum(1 for obj in objects if obj.get("class", "").lower() in ("person", "people", "human"))
perception["people"] = {"count": person_count, "moving": False}

# events
perception["events"] = []
```

### 方式 2：在回归测试中直接调用 PipelineController

```python
from vision_pipeline.pipeline_controller import PipelineController

# 初始化
controller = PipelineController(config)

# 对每一帧处理
result = controller.process_frame(
    frame=frame,
    frame_idx=frame_idx,
    timestamp=t_video
)

# 从 result 中提取 perception
perception = result.get("perception", {})
# 或者从各个模块结果中手动构建（如上面的代码）
```

## 三、使用方式

### 当前（模拟数据）

```bash
python3 -m examples.b2_regression_test_all
```

### 使用真实数据

```bash
python3 -m examples.b2_regression_test_all --real
```

## 四、两种方式的对比

| 维度 | 模拟数据 | 真实数据 |
|------|---------|---------|
| **数据来源** | 硬编码、固定值 | 实际感知系统输出 |
| **可控性** | ✅ 完全可控 | ❌ 依赖实际检测结果 |
| **可重复性** | ✅ 完全可重复 | ⚠️ 可能因检测波动而变化 |
| **运行速度** | ✅ 快速 | ❌ 需要完整 pipeline，较慢 |
| **测试目的** | 验证 B2 逻辑正确性 | 验证 B2 在实际环境中的表现 |
| **适用场景** | 单元测试、逻辑验证 | 集成测试、真实场景验证 |

## 五、建议

1. **开发阶段**：使用模拟数据，快速验证逻辑
2. **集成测试**：使用真实数据，验证实际表现
3. **回归测试**：两种方式都跑，对比结果

## 六、下一步

如果你想要使用真实数据，需要：

1. ✅ 确保 `PipelineController` 已正确初始化
2. ✅ 确保各个感知模块（Navigation、Modeling、YOLO）已加载
3. ✅ 在回归测试中调用 `controller.process_frame()` 获取真实 perception
4. ✅ 对比模拟数据和真实数据的差异，分析 B2 的表现

