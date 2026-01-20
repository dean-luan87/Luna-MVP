# v1.8.5 C1 → PipelineController 接入文档

## 一、接入概述

**接入原则**：
- 不破坏现有结构
- 最小侵入
- 可回滚

**接入位置**：
C1 必须放在 `PipelineController.process_frame()` 的最前面

**原因**：
- C1 决定 "要不要看 / 看多少 / 看哪里"
- Pipeline 决定 "怎么看 / 调哪些 executor"
- 世界模型、任务链一律不能反向影响 C1

**数据流**：
```
Camera → C1 → PipelineController → LV2/LV3/LV4…
```

---

## 二、代码修改

### 2.1 文件修改

**文件**：`vision_pipeline/pipeline_controller.py`

**修改点**：
1. 引入 C1Controller 和 C1Input
2. 在 `__init__` 中初始化 C1Controller
3. 在 `process_frame()` 最前面插入 C1 决策逻辑

### 2.2 具体修改

#### Step 1: 引入 C1Controller

```python
# C1: Continuous Vision Controller（连续视觉调度中台）
from c1_controller.c1_controller import C1Controller
from c1_controller.c1_types import C1Input
```

#### Step 2: 在 `__init__` 中初始化 C1Controller

```python
# ✅ C1 控制器（新增）
# C1 是有状态的（state machine），不能每帧 new
# 生命周期和 PipelineController 绑定是对的
self.c1_controller = C1Controller()
```

#### Step 3: 在 `process_frame()` 最前面插入 C1 决策

```python
# ===============================
# C1：是否观察 / 如何观察
# ===============================
# 从 context 中提取 C1 需要的信号（如果 context 为 None 则使用默认值）
c1_input = C1Input(
    timestamp=time.time(),
    motion_score=context.get("motion_score", 0.0) if context else 0.0,
    frame_diff_score=context.get("frame_diff_score", 0.0) if context else 0.0,
    next_scene_hint=context.get("next_scene") if context else None,
    risk_hint=context.get("risk_hint") if context else None,
    privacy_zone=context.get("privacy_zone") if context else None,
    user_camera_override=context.get("user_camera_override", False) if context else False,
)

c1_decision = self.c1_controller.decide(c1_input)
result["c1_decision"] = c1_decision

# 🚨 C1 硬暂停：直接返回空 pipeline 结果
if not c1_decision.allow_frame:
    result["navigation_result"] = None
    result["modeling_result"] = None
    result["quality_result"] = None
    result["route_result"] = None
    return result

# 可选：把 fps / observation_mode 写入 context（供后续使用）
if context:
    context["target_fps"] = c1_decision.target_fps
    context["observation_mode"] = c1_decision.observation_mode
    context["observation_priority"] = c1_decision.priority
```

**注意**：
- C1 只负责"开关 + 策略提示"
- 不做任何 executor 调用
- 如果 C1 禁止抽帧，直接返回空结果

---

## 三、接入后获得的能力

不写一行模型代码，你已经得到：

### ✅ 1. 动态抽帧入口已经存在
- `target_fps` 已经计算出来
- 后面只需要在 CameraHandler 或 Scheduler 里用

### ✅ 2. 视觉熔断能力
- 摔倒 / 甩飞 / 剧烈晃动 → 自动停看
- 稳定后自动恢复

### ✅ 3. 隐私不可协商
- 洗手间 / 医疗 / 用户声明 → 镜头永远关

### ✅ 4. 防恶意输入
- 静态遮挡 / 频闪 → 自动降级或转场景态

### ✅ 5. C1 → C2 的天然接口
- `c1_decision.reason`
- `observation_mode`
- `priority`

---

## 四、测试验证

### 4.1 测试脚本

**文件**：`examples/c1_pipeline_integration_test.py`

**测试场景**：
1. C1Controller 已正确初始化
2. C1 禁止抽帧（严重晃动）
3. C1 允许抽帧（正常环境）
4. `process_frame` 中的 C1 决策（严重晃动）
5. `process_frame` 中的 C1 决策（正常环境）

### 4.2 快速测试（5 分钟）

**Mock 测试**：

```python
# 测试 1: 严重晃动（应该禁止抽帧）
context = {
    "motion_score": 0.9,  # 超过阈值
    "frame_diff_score": 0.1,
}
result = pipeline.process_frame(frame, context=context)
assert result["c1_decision"].allow_frame == False
assert result["c1_decision"].reason == "suspended"

# 测试 2: 正常环境（应该允许抽帧）
context = {
    "motion_score": 0.1,
    "frame_diff_score": 0.5,
}
result = pipeline.process_frame(frame, context=context)
assert result["c1_decision"].allow_frame == True
assert result["c1_decision"].observation_mode == "forward"
```

---

## 五、Context 字段说明

### 5.1 C1 需要的 Context 字段

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `motion_score` | float | 镜头晃动强度（0~1） | 0.0 |
| `frame_diff_score` | float | 帧变化幅度（0~1） | 0.0 |
| `next_scene` | str | 未来场景提示 | None |
| `risk_hint` | str | 潜在风险提示 | None |
| `privacy_zone` | str | 隐私区域（A/B/C） | None |
| `user_camera_override` | bool | 用户是否强制要求开启 | False |

### 5.2 C1 写入的 Context 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `target_fps` | int | 目标 fps（供后续使用） |
| `observation_mode` | str | 观察模式（forward/surround/local） |
| `observation_priority` | str | 优先级（safety/navigation/environment） |

---

## 六、下一步建议

不要一口气吃掉，按这个来：

1. ✅ **C1 接入**（已完成）
2. 🔜 **用 C1.target_fps 控制 CameraHandler 抽帧**
3. 🔜 **用 C1.priority 决定是否执行 ModelingExecutor**
4. 🔜 **C1 → C2（时间连续性）**

---

## 七、回滚方案

如果需要回滚，只需要：

1. 删除 `vision_pipeline/pipeline_controller.py` 中的 C1 相关代码
2. 恢复 `process_frame()` 的原始逻辑

**修改点**：
- 删除 C1 的 import
- 删除 `__init__` 中的 `self.c1_controller = C1Controller()`
- 删除 `process_frame()` 开头的 C1 决策逻辑

---

## 八、总结

**接入状态**：✅ 完成

**修改文件**：1 个（`vision_pipeline/pipeline_controller.py`）

**新增代码**：约 30 行

**影响范围**：
- ✅ 不破坏现有结构
- ✅ 最小侵入
- ✅ 可回滚

**测试状态**：
- ✅ 代码修改完成
- ✅ 测试脚本已准备
- ⏳ 需要在实际环境中运行测试

---

**文档版本**：v1.0  
**最后更新**：2024-12-19


