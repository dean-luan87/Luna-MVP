# Luna Badge 路径规划策略详解

**版本**: v1.6  
**文档日期**: 2025-10-30  
**主题**: 多目的地导航和路径合并策略

---

## 📋 目录

1. [问题分析](#问题分析)
2. [解决方案设计](#解决方案设计)
3. [地图生成策略](#地图生成策略)
4. [路径规划场景](#路径规划场景)
5. [使用示例](#使用示例)

---

## 🎯 问题分析

### 问题1: 地图生成方式
**Q**: 现在生成的地图是集合在一起的，还是一个目的地生成一个文件？

**A**: 当前每个路径独立生成一个地图文件。

**当前行为**:
- 每个 `path_id` 对应一个独立的地图文件
- 例如：`path_a_to_b_map.png` 和 `path_a_to_c_map.png`
- 地图之间没有关联

**建议改进**:
- 支持单一路径地图（当前方式）
- 支持合并路径地图（新增功能）

### 问题2: 多目的地导航
**Q**: 当出现多个目的地（从A到B再到C）时，会怎么处理？

**A**: 使用智能路径规划算法处理。

**场景分析**:
- **已知路径**: A→B, A→C 都存在
- **目标**: 从A出发，依次访问B和C
- **处理方式**: 自动规划 A→B→C 的连续路径

### 问题3: 路径缺失处理
**Q**: 如果有A到B的路径，A到C的路径，但缺少B到C的路径，会出现让用户回退到A点，再前往C点的情况吗？

**A**: 默认情况下会，但提供多种策略选择。

---

## 🏗️ 解决方案设计

### 策略1: 智能合并 (smart_merge) ⭐推荐

**行为**:
1. 尝试通过共同祖先节点连接
2. 如果找不到共同路径，启动实时路径记录模式
3. 边记录边导航，逐步构建完整路径图

**优点**:
- 不会强制用户回退
- 自动学习新路径
- 逐步积累知识

**示例**:
```
用户需求: B -> C (未知路径)

策略执行:
1. 检测到B->C路径未知
2. 询问用户: "需要记录从B到C的新路径吗？"
3. 如果确认: 启动路径记录模式
4. 边走路边识别节点，生成新路径
5. 保存后下次即可直接使用
```

### 策略2: 回退策略 (fallback)

**行为**:
1. 遇到未知路径，建议回退到最近的已知节点
2. 通过已知路径到达目标

**优点**:
- 确保路径可靠性
- 避免迷路

**缺点**:
- 可能需要走回头路
- 效率较低

**示例**:
```
用户需求: B -> C (未知路径)

策略执行:
1. 检测到B->C路径未知
2. 分析: B可以通过B->Start连接，C可以通过Start->C连接
3. 建议: "请回退到Start，然后前往C"
```

### 策略3: 询问用户 (ask_user)

**行为**:
1. 遇到未知路径，直接询问用户
2. 根据用户选择决定策略

**优点**:
- 灵活性高
- 尊重用户意愿

**缺点**:
- 需要用户交互
- 可能打断导航流程

---

## 🗺️ 地图生成策略

### 方式1: 独立路径地图（当前）

**适用场景**: 独立的目的地导航

**生成方式**:
```python
generator = MapCardGenerator()
map_path = generator.generate_map_card(path_memory, "hospital_visit_map.png")
```

**文件结构**:
```
data/map_cards/
├── path_a_to_b_map.png
├── path_a_to_c_map.png
└── path_b_to_c_map.png
```

### 方式2: 合并路径地图（新增）

**适用场景**: 连续多目的地导航

**生成方式**:
```python
from core.path_planner import PathPlanner

planner = PathPlanner(system)

# 合并多条路径
merged = planner.merge_paths_to_continuous(["path_a_to_b", "path_a_to_c"])

# 生成合并地图
generator = MapCardGenerator()
map_path = generator.generate_map_card_from_nodes(merged['merged_nodes'], "combined_map.png")
```

**文件结构**:
```
data/map_cards/
├── combined_route.png  # 合并后的连续路径
└── path_details/
    ├── path_a_to_b_map.png
    └── path_a_to_c_map.png
```

---

## 📊 路径规划场景

### 场景1: 完整已知路径

```
已知路径:
  - A -> B (Path1)
  - A -> C (Path2)

用户需求: A -> B -> C

处理流程:
  1. 查找 A -> B: ✅ 找到 (使用Path1)
  2. 查找 B -> C: ❌ 未找到
  3. 应用策略: smart_merge
  4. 执行: 启动B->C路径记录模式
  5. 结果: 边记录边导航
```

### 场景2: 通过回退连接

```
已知路径:
  - A -> B (Path1)
  - A -> C (Path2)
  - 共同节点: A

用户需求: B -> C

处理流程:
  1. 查找 B -> C: ❌ 未找到
  2. 查找共同祖先: ✅ 找到 A
  3. 应用策略: fallback
  4. 建议: "回退到A，再从A前往C"
  5. 结果: B -> A -> C
```

### 场景3: 智能学习路径

```
已知路径:
  - A -> B (Path1)
  
用户需求: A -> B -> C (第一次访问C)

处理流程:
  1. A -> B: ✅ 已知路径
  2. B -> C: ❌ 未知路径
  3. 应用策略: smart_merge
  4. 询问: "开始记录B到C的新路径？"
  5. 确认后: 启动路径记录
  6. 行走过程中识别节点并保存
  7. 完成记录，生成新路径
  8. 下次即可直接使用B->C路径
```

---

## 🚀 使用示例

### 示例1: 多目的地规划

```python
from core.scene_memory_system import get_scene_memory_system
from core.path_planner import PathPlanner

# 初始化
system = get_scene_memory_system()
planner = PathPlanner(system)

# 设置策略
planner.preferred_strategy = "smart_merge"

# 规划路径
result = planner.plan_route(
    start="挂号处",
    destinations=["检查室", "药房", "出口"]
)

# 处理结果
if result['can_navigate']:
    if result['strategy'] == "direct":
        # 完整路径已知，直接导航
        speak("开始导航")
        navigate(result['segments'])
    else:
        # 需要学习新路径
        speak(result['message'])
        # 启动路径记录模式
        record_new_segments(result['unknown_segments'])
```

### 示例2: 路径合并

```python
# 合并多条路径
merged = planner.merge_paths_to_continuous([
    "hospital_path_morning",
    "hospital_path_afternoon"
])

# 生成合并地图
generator = MapCardGenerator()
map_path = generator.generate_map_card_from_merged(merged)
```

### 示例3: 策略选择

```python
# 根据场景选择策略
situations = {
    "熟悉环境": "smart_merge",      # 智能学习
    "首次访问": "ask_user",         # 询问用户
    "紧急情况": "fallback",         # 可靠优先
}

planner.preferred_strategy = situations["熟悉环境"]
```

---

## 🎨 地图生成机制

### 单路径地图

```python
# 生成单个路径的地图
path_memory = system.get_path_memory("hospital_visit")
generator.generate_map_card(path_memory, "hospital_visit_map.png")
```

**特点**:
- 专注于单一路径
- 清晰简洁
- 适合单次导航

### 合并路径地图

```python
# 生成合并路径的地图
merged = planner.merge_paths_to_continuous(["path1", "path2", "path3"])
generator.generate_combined_map_card(merged, "combined_route_map.png")
```

**特点**:
- 展示完整路线
- 包含所有关键节点
- 适合多目的地规划

### 分层地图

```python
# 生成多层地图（不同路径用不同颜色）
paths = {
    "主路径": "path_main",
    "备用路径": "path_backup"
}
generator.generate_layered_map(paths, "layered_map.png")
```

**特点**:
- 同时展示多条路径
- 用颜色区分
- 适合路径对比

---

## 🔄 路径学习机制

### 实时学习模式

```
1. 检测到未知路径
   ↓
2. 询问用户是否记录
   ↓
3. 用户确认后启动记录
   ↓
4. 摄像头连续识别节点
   ↓
5. 自动保存节点和图像
   ↓
6. 生成完整路径
   ↓
7. 下次即可使用新路径
```

### 渐近式构建

```
第一次: A -> B
第二次: A -> C
第三次: B -> C (智能学习)

结果: 完整的路径图
```

---

## 📊 策略对比表

| 策略 | 可靠性 | 效率 | 用户体验 | 适用场景 |
|------|--------|------|----------|----------|
| **smart_merge** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 日常使用 |
| **fallback** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | 紧急情况 |
| **ask_user** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 首次访问 |

---

## 💡 最佳实践建议

### 1. 地图存储建议

```
data/map_cards/
├── single_paths/          # 独立路径
│   ├── hospital_visit.png
│   └── shopping_route.png
├── combined/              # 合并路径
│   ├── multi_dest_route.png
│   └── complex_nav.png
└── archived/              # 历史记录
    └── old_paths/
```

### 2. 路径命名规范

```python
# 建议使用描述性命名
path_names = [
    "hospital_path_main_entrance_to_pharmacy",
    "shopping_mall_parking_to_store_305",
    "apartment_building_lobby_to_room_501"
]
```

### 3. 路径合并条件

```python
# 自动合并条件
auto_merge_conditions = {
    "same_building": True,      # 同一建筑内
    "time_proximity": True,     # 时间相近
    "user_tagged": True         # 用户标记的
}
```

---

## 📝 总结

### 回答您的核心问题

1. **地图生成**: 当前每个路径一个文件，支持合并地图
2. **多目的地**: 自动规划连续路径，智能处理
3. **路径缺失**: 默认不回退（smart_merge），可选择回退策略
4. **路径学习**: 边走边生成，渐进式构建知识图谱

### 推荐配置

```python
# 推荐的默认配置
recommended_config = {
    "strategy": "smart_merge",           # 智能学习
    "map_generation": "both",            # 生成独立和合并地图
    "auto_record": True,                 # 自动记录新路径
    "user_confirmation": True            # 需要用户确认
}
```

---

**文档结束**

*Luna Badge v1.6 - 让导航更智能，让路径更灵活*
