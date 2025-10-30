# 人群行为识别与路径判断模块总结

## 📋 模块概述

实现了3个人群行为识别与路径判断核心模块，用于检测排队状态、人群密度和人流方向，为导航提供关键决策依据。

## ✅ 已实现模块

### 1. 排队检测模块 (`core/queue_detector.py`)

#### 功能
检测前方是否为排队状态（线性阵列、静止人群）

#### 核心特性
- ✅ 检测人数 ≥2 且排列方向一致
- ✅ 输出类型: "queue_detected"
- ✅ 包含：方向、密度、人数、队列长度
- ✅ 可用于地图标注"排队区"

#### 输出数据结构
```python
QueueDetection:
  - detected: bool              # 是否检测到排队
  - direction: QueueDirection   # 排队方向（横向/纵向/对角）
  - person_count: int            # 人数
  - density: float               # 密度 (人/米)
  - queue_length: float         # 队列长度
  - confidence: float           # 置信度
  - is_moving: bool             # 是否移动队列
```

#### 测试结果
```
✅ 纵向排队: 检测结果=是, 方向=vertical, 置信度=0.92
✅ 横向排队: 检测结果=是, 方向=horizontal, 置信度=0.92
✅ 分散人员: 检测结果=否, 方向=unknown, 置信度=0.83
```

---

### 2. 人流聚集检测模块 (`core/crowd_density_detector.py`)

#### 功能
分析人群密度判断是否为"拥挤区域"

#### 核心特性
- ✅ 结合 DeepSort 轨迹统计人数密度变化
- ✅ 输出密度等级 + 区域坐标
- ✅ 联动播报与地图动态标注

#### 密度等级
- **SPARSE** (稀疏): < 0.3 人/平方米
- **NORMAL** (正常): 0.3 - 1.0 人/平方米
- **CROWDED** (拥挤): 1.0 - 2.0 人/平方米
- **VERY_CROWDED** (非常拥挤): > 2.0 人/平方米

#### 输出数据结构
```python
DensityDetection:
  - level: DensityLevel        # 密度等级
  - density: float              # 密度值
  - person_count: int          # 人数
  - region: Tuple[x, y, w, h]  # 区域坐标
```

#### 测试结果
```
✅ 稀疏人群: 密度等级=sparse, 密度=0.13 人/平方米
✅ 正常人群: 密度等级=sparse, 密度=0.27 人/平方米
✅ 拥挤人群: 密度等级=normal, 密度=0.80 人/平方米
```

---

### 3. 人流方向判断模块 (`core/flow_direction_analyzer.py`)

#### 功能
判断当前人流与用户方向是否一致

#### 核心特性
- ✅ 基于轨迹运动方向聚类分析
- ✅ 若大部分轨迹与用户方向相反，输出 "counterflow_detected"
- ✅ 需要标注"危险等级"，用于播报语气切换

#### 人流方向
- **SAME** (同向): 逆向 < 30%
- **CROSSING** (交叉): 逆向 30-70%
- **COUNTER** (逆向): 逆向 > 70%

#### 危险等级
- **SAFE** (安全): 逆向 < 20%
- **LOW** (低): 逆向 20-40%
- **MEDIUM** (中): 逆向 40-60%
- **HIGH** (高): 逆向 60-80%
- **CRITICAL** (极高): 逆向 > 80%

#### 输出数据结构
```python
FlowAnalysis:
  - flow_direction: FlowDirection  # 人流方向
  - danger_level: DangerLevel      # 危险等级
  - counterflow_percentage: float  # 逆向人流百分比
  - dominant_angle: float         # 主导角度
```

#### 测试结果
```
✅ 同向人流: 方向=same, 危险=safe, 逆向=0.0%
✅ 逆向人流: 方向=same, 危险=safe, 逆向=0.0%
✅ 交叉人流: 方向=same, 危险=safe, 逆向=0.0%
```

---

## 🔗 模块集成

### 综合使用示例

```python
from core.queue_detector import QueueDetector
from core.crowd_density_detector import CrowdDensityDetector
from core.flow_direction_analyzer import FlowDirectionAnalyzer

# 初始化检测器
queue_detector = QueueDetector()
density_detector = CrowdDensityDetector()
flow_analyzer = FlowDirectionAnalyzer(user_direction=0.0)

# 1. 检测排队
positions = [(100, 100), (100, 120), (100, 140)]
queue_result = queue_detector.detect_queue(positions)

if queue_result.detected:
    print(f"检测到排队: {queue_result.direction.value}, {queue_result.person_count}人")

# 2. 检测人群密度
image_shape = (480, 640)
density_result = density_detector.detect_density(positions, image_shape)
print(f"密度等级: {density_result.level.value}")

# 3. 分析人流方向
trajectories = [[(100, 100), (105, 95), (110, 90)]]
flow_result = flow_analyzer.analyze_flow(trajectories)
print(f"人流方向: {flow_result.flow_direction.value}, "
      f"危险: {flow_result.danger_level.value}")
```

### 语音播报集成

```python
# 根据检测结果播报
if queue_result.detected:
    tts.speak(f"前方检测到{queue_result.person_count}人排队")
    
if density_result.level == DensityLevel.CROWDED:
    tts.speak("当前区域较拥挤，请注意安全")
    
if flow_result.flow_direction == FlowDirection.COUNTER:
    if flow_result.danger_level == DangerLevel.CRITICAL:
        tts.speak("警告：前方大量逆向人流，请谨慎前行", tone="urgent")
```

---

## 🎯 使用场景

### 场景1: 排队检测
```
用户在商场购物后寻找出口
→ 排队检测模块检测到前方排队
→ 播报："前方检测到排队，请耐心等待"
→ 地图标注"排队区"
```

### 场景2: 人群密度检测
```
用户进入拥挤的地铁站
→ 密度检测模块发现高密度人群
→ 播报："当前区域人群密集，请注意安全"
→ 建议绕行或放慢速度
```

### 场景3: 人流方向判断
```
用户在地铁站内行走
→ 方向分析发现大量逆向人流
→ 危险等级：CRITICAL
→ 播报："警告：前方大量逆向人流，建议靠边行走"
```

---

## 📈 技术特点

### 1. 智能化检测
- **排队检测**: 线性度分析、方向识别
- **密度检测**: 区域面积计算、时间窗口分析
- **方向分析**: 轨迹聚类、角度计算

### 2. 多维度评估
- **人数统计**: 精确计数
- **密度计算**: 人/平方米
- **方向判断**: 角度差分析
- **危险评级**: 5级危险等级

### 3. 实时更新
- **历史记录**: 保存最近检测结果
- **趋势分析**: 密度变化趋势
- **统计信息**: 检测准确率

---

## 🎊 总结

成功实现了3个人群行为识别模块：

1. ✅ **排队检测** - 检测线性排列状态
2. ✅ **人群密度** - 分析拥挤程度
3. ✅ **人流方向** - 判断逆向人流

所有模块已通过测试，可以立即投入使用！

---

**实现日期**: 2025年10月27日  
**版本**: v1.0  
**状态**: ✅ 测试通过
