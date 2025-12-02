# 模块 B：动态抽帧调度器

## 📋 模块概述

**模块 B** 是 Luna Badge v1.3.0 的第二个完整实现模块，负责：
- 根据场景复杂度、用户移动速度、亮度等因素，动态决定摄像头处理帧率
- 在保证安全的前提下，尽可能节省计算资源
- 通过平滑机制避免频繁跳变，提供稳定的用户体验

## 🎯 设计原则

1. **多因子综合决策**：综合考虑复杂度、速度、亮度等多个因素
2. **平滑过渡**：使用指数平滑避免 FPS 频繁跳变
3. **安全优先**：复杂/快速/暗环境自动提高 FPS，确保安全
4. **资源优化**：静态稳定环境可降频，节省算力

## 📁 文件位置

- **实现文件**：`vision/frame_scheduler.py`
- **测试文件**：`tests/test_frame_scheduler.py`

## 🔧 使用方法

### 基本用法

```python
from vision.frame_scheduler import FrameScheduler
from vision.brightness_detector import BrightnessDetector

# 初始化
frame_scheduler = FrameScheduler()
brightness_detector = BrightnessDetector()

# 在主循环中使用
while True:
    frame = camera.read()
    
    # 获取各因子（来自其他模块）
    scene_complexity = scene_complexity_estimator.evaluate(frame)  # 0~1
    motion_speed = speed_estimator.estimate()                       # 0~1
    brightness_state = brightness_detector.update(frame)
    brightness = brightness_state.value                            # 0~1
    
    # 可选参数（未来接入）
    is_turning = False          # 是否转头（由 OrientationFilter 提供）
    static_stable = False       # 是否静态稳定（由 StaticMapMemory 提供）
    
    # 获取建议 FPS
    fps = frame_scheduler.suggest_fps(
        scene_complexity,
        motion_speed,
        brightness,
        is_turning=is_turning,
        static_stable=static_stable
    )
    
    # 计算采集间隔
    interval_ms = int(1000 / max(fps, 1))
    # 控制摄像头采集间隔...
```

### 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `min_fps` | int | 2 | 最小 FPS（安全下限） |
| `max_fps` | int | 15 | 最大 FPS（性能上限） |
| `base_fps` | int | 6 | 基准 FPS（中等环境） |
| `complexity_weight` | float | 6.0 | 复杂度权重（影响范围 0~6 FPS） |
| `speed_weight` | float | 4.0 | 速度权重（影响范围 0~4 FPS） |
| `smoothing_alpha` | float | 0.5 | 平滑系数（0~1，越大越敏感） |

## 📊 调度策略详解

### 1. 场景复杂度影响

- **公式**：`complexity_factor = complexity_weight * scene_complexity`
- **效果**：复杂度 0 → +0 FPS，复杂度 1 → +6 FPS
- **逻辑**：越复杂的环境，需要更高的识别频率

### 2. 用户移动速度影响

- **公式**：`speed_factor = speed_weight * motion_speed`
- **效果**：速度 0 → +0 FPS，速度 1 → +4 FPS
- **逻辑**：移动越快，需要更频繁的识别

### 3. 亮度影响

- **规则**：
  - `brightness < 0.25` → +2 FPS（极暗环境）
  - `0.25 ≤ brightness < 0.40` → +1 FPS（较暗环境）
  - `brightness ≥ 0.40` → +0 FPS（正常/明亮）
- **逻辑**：暗环境下识别质量下降，提高频率补偿

### 4. 静态稳定降频

- **条件**：
  - `static_stable == True`（静态环境 + 记忆可复用）
  - `scene_complexity < 0.3`（环境简单）
  - `motion_speed < 0.3`（移动缓慢）
- **效果**：满足条件时 -2 FPS（但不低于 min_fps）
- **逻辑**：熟悉环境可复用记忆，降低识别频率

### 5. 转头阶段（预留）

- 当前不做额外处理，主要靠 `OrientationFilter` 过滤无效识别
- 未来可扩展：转头时保持当前 FPS，不做大幅调整

### 6. 最终计算

```python
target_fps = base_fps
         + complexity_factor
         + speed_factor
         + brightness_boost
         + static_adjust

# 限制在 [min_fps, max_fps]
target_fps = clamp(target_fps, min_fps, max_fps)

# 平滑处理（避免跳变）
new_fps = α * target_fps + (1-α) * current_fps
```

## 🧪 测试

运行测试：

```bash
cd luna_badge_v1_2
python3 tests/test_frame_scheduler.py
```

测试内容包括：
1. **基本功能测试**：不同场景下的 FPS 建议
2. **平滑机制测试**：验证场景变化时的平滑过渡
3. **静态稳定测试**：验证降频机制
4. **亮度影响测试**：验证暗环境提频
5. **边界情况测试**：输入越界处理
6. **集成测试**：与 A 模块（BrightnessDetector）的集成

## 📈 典型场景示例

### 场景 1：简单环境 + 静止 + 明亮
- 输入：`complexity=0.1, speed=0.1, brightness=0.8`
- 输出：FPS ≈ 6-8（接近基准值）

### 场景 2：复杂环境 + 快速移动 + 黑暗
- 输入：`complexity=0.9, speed=0.9, brightness=0.2`
- 输出：FPS ≈ 14-15（接近最大值）

### 场景 3：静态稳定 + 有记忆
- 输入：`complexity=0.2, speed=0.1, brightness=0.7, static_stable=True`
- 输出：FPS ≈ 4-6（降频 2 FPS）

### 场景 4：中等环境
- 输入：`complexity=0.5, speed=0.5, brightness=0.5`
- 输出：FPS ≈ 9-11（中等值）

## 🔗 与上层模块的集成

### 1. 与 VisionPipeline 集成

```python
class VisionPipeline:
    def __init__(self):
        self.brightness_detector = BrightnessDetector()
        self.frame_scheduler = FrameScheduler()
        self.scene_complexity_estimator = SceneComplexityEstimator()
        self.speed_estimator = SpeedEstimator()
    
    def process(self, frame):
        # 获取各因子
        brightness_state = self.brightness_detector.update(frame)
        scene_complexity = self.scene_complexity_estimator.evaluate(frame)
        motion_speed = self.speed_estimator.estimate()
        
        # 获取建议 FPS
        fps = self.frame_scheduler.suggest_fps(
            scene_complexity,
            motion_speed,
            brightness_state.value
        )
        
        # 控制采集间隔
        interval_ms = int(1000 / max(fps, 1))
        # ...
```

### 2. 与摄像头采集集成

```python
# 伪代码示例
last_capture_time = 0
target_interval_ms = 1000 / base_fps

while True:
    current_time = time.time()
    
    # 更新 FPS 建议
    fps = frame_scheduler.suggest_fps(...)
    target_interval_ms = 1000 / max(fps, 1)
    
    # 控制采集间隔
    if current_time - last_capture_time >= target_interval_ms / 1000.0:
        frame = camera.read()
        process_frame(frame)
        last_capture_time = current_time
```

## ⚙️ 参数调优建议

### 性能优化场景

如果设备性能有限，可以降低上限：
```python
scheduler = FrameScheduler(
    min_fps=2,
    max_fps=10,  # 降低上限
    base_fps=5   # 降低基准
)
```

### 安全优先场景

如果需要更高安全性，可以提高上限和权重：
```python
scheduler = FrameScheduler(
    min_fps=3,
    max_fps=20,              # 提高上限
    base_fps=8,             # 提高基准
    complexity_weight=8.0,   # 提高复杂度权重
    speed_weight=6.0        # 提高速度权重
)
```

### 平滑度调整

如果需要更平滑的变化：
```python
scheduler = FrameScheduler(
    smoothing_alpha=0.3  # 降低平滑系数（更平滑）
)
```

如果需要更快速响应：
```python
scheduler = FrameScheduler(
    smoothing_alpha=0.7  # 提高平滑系数（更敏感）
)
```

## 📊 性能特点

- **计算量**：极小（仅做简单数学运算）
- **内存占用**：极小（仅保存当前 FPS 状态）
- **延迟**：< 0.1ms（可忽略）
- **平滑性**：通过指数平滑避免跳变

## ✅ 完成状态

- [x] 多因子综合决策逻辑
- [x] 平滑机制
- [x] 静态稳定降频
- [x] 亮度影响
- [x] 边界情况处理
- [x] 单元测试
- [x] 集成测试
- [x] 使用文档

## 🚀 下一步

B 模块已完成，可以开始实现：
- **C 模块**：SceneComplexityEstimator（环境复杂度评分）
- **D 模块**：StaticMapMemory（静态地图记忆）
- **F 模块**：SpeedEstimator（速度估计）

或者先整理一个简单的 **VisionPipeline 雏形**，将 A + B 模块整合起来。

---

**版本**：v1.3.0  
**状态**：✅ 已完成  
**最后更新**：2024










