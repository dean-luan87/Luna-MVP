# 模块 A：亮度检测 + 补光建议

## 📋 模块概述

**模块 A** 是 Luna Badge v1.3.0 的第一个完整实现模块，负责：
- 从摄像头帧估算环境亮度（0.0 ~ 1.0）
- 判断亮度等级（DARK / NORMAL / BRIGHT）
- 根据迟滞阈值，输出是否需要开启补光灯（仅开/关建议）

## 🎯 设计原则

1. **简单实用**：只做开/关建议，不做亮度强弱控制
2. **防抖设计**：使用迟滞阈值（ON_THRESHOLD < OFF_THRESHOLD）避免频繁开关
3. **轻量计算**：每 N 帧计算一次，其他帧复用结果
4. **硬件解耦**：不直接控制硬件，只给出建议

## 📁 文件位置

- **实现文件**：`vision/brightness_detector.py`
- **测试文件**：`tests/test_brightness_detector.py`

## 🔧 使用方法

### 基本用法

```python
from vision.brightness_detector import BrightnessDetector, BrightnessState
import cv2

# 初始化检测器
detector = BrightnessDetector(
    on_threshold=0.35,      # 开灯阈值
    off_threshold=0.45,     # 关灯阈值
    sample_interval_frames=5  # 每5帧计算一次
)

# 在主循环中使用
cap = cv2.VideoCapture(0)
fill_light_on = False  # 当前补光灯状态（由硬件层维护）

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 更新亮度检测（传入当前补光灯状态）
    state = detector.update(frame, fill_light_on=fill_light_on)
    
    # 根据建议控制补光灯
    if state.need_fill_light and not fill_light_on:
        # 开启补光灯
        fill_light_controller.turn_on()
        fill_light_on = True
    elif not state.need_fill_light and fill_light_on:
        # 关闭补光灯
        fill_light_controller.turn_off()
        fill_light_on = False
    
    # 使用亮度信息
    print(f"亮度: {state.value:.3f}, 等级: {state.level}")
```

### 返回数据结构

```python
@dataclass
class BrightnessState:
    value: float          # 0.0 ~ 1.0，当前亮度值
    level: BrightnessLevel  # "DARK" / "NORMAL" / "BRIGHT"
    need_fill_light: bool   # True = 建议开灯，False = 建议关灯
```

## ⚙️ 参数说明

### 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `on_threshold` | float | 0.35 | 开灯阈值，低于此值建议开灯 |
| `off_threshold` | float | 0.45 | 关灯阈值，高于此值建议关灯 |
| `sample_interval_frames` | int | 5 | 采样间隔，每N帧计算一次 |
| `resize_width` | int | 160 | 降采样宽度（降低计算量） |
| `resize_height` | int | 120 | 降采样高度（降低计算量） |

### 亮度等级划分

| 平均亮度 | 等级 | 含义 |
|---------|------|------|
| < 0.30 | DARK | 环境很暗，识别会明显受影响 |
| 0.30 ~ 0.65 | NORMAL | 正常可用 |
| > 0.65 | BRIGHT | 亮度充足 |

### 补光开关逻辑（迟滞防抖）

```
当前未开灯：
  - 亮度 < 0.35 → 建议开灯
  - 亮度 ≥ 0.35 → 保持关闭

当前已开灯：
  - 亮度 > 0.45 → 建议关灯
  - 亮度 ≤ 0.45 → 保持开启

中间区间（0.35 ~ 0.45）：保持现状，不摇摆
```

## 🧪 测试

运行测试：

```bash
cd luna_badge_v1_2
python3 tests/test_brightness_detector.py
```

测试内容包括：
1. **基础功能测试**：不同亮度场景下的检测结果
2. **迟滞逻辑测试**：验证防抖机制是否正常工作

## 🔗 与上层模块的集成

### 1. 与 VisionPipeline 集成

```python
class VisionPipeline:
    def __init__(self):
        self.brightness_detector = BrightnessDetector()
        self.fill_light_controller = FillLightController()
    
    def process(self, frame):
        # 亮度检测
        state = self.brightness_detector.update(
            frame, 
            fill_light_on=self.fill_light_controller.is_on()
        )
        
        # 控制补光灯
        if state.need_fill_light:
            self.fill_light_controller.turn_on()
        else:
            self.fill_light_controller.turn_off()
        
        # 其他视觉处理...
```

### 2. 与 ScenePolicyManager 的未来联动（预留）

未来如果需要场景相关的亮度策略（如"医院里更敏感"），可以在 `ScenePolicyManager` 中动态调整阈值：

```python
# 伪代码示例
if scene_type == "hospital":
    detector.on_threshold = 0.40  # 更宽松
    detector.off_threshold = 0.50
elif scene_type == "night_street":
    detector.on_threshold = 0.30  # 更敏感
    detector.off_threshold = 0.40
```

## 📊 性能特点

- **计算量**：每帧仅做一次灰度转换 + 降采样 + 均值计算
- **内存占用**：极小（仅保存上一次结果）
- **延迟**：< 1ms（在 RV1126 等板子上可实时运行）
- **采样优化**：默认每5帧计算一次，可进一步降低计算量

## ✅ 完成状态

- [x] 亮度计算逻辑
- [x] 亮度等级分类
- [x] 迟滞防抖逻辑
- [x] 采样间隔优化
- [x] 单元测试
- [x] 使用文档

## 🚀 下一步

A 模块已完成，可以开始实现：
- **B 模块**：动态抽帧调度器（FrameScheduler）
- **硬件层**：FillLightController（GPIO 控制）

---

**版本**：v1.3.0  
**状态**：✅ 已完成  
**最后更新**：2024

























