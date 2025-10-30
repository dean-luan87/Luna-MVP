# Luna Badge 完整路径规划指南

**版本**: v1.6  
**完成时间**: 2025-10-30  
**状态**: ✅ 已完成

---

## 📋 目录

1. [系统架构](#系统架构)
2. [核心问题解答](#核心问题解答)
3. [模块功能说明](#模块功能说明)
4. [使用场景](#使用场景)
5. [测试结果](#测试结果)

---

## 🏗️ 系统架构

```
场景记忆系统架构
┌─────────────────────────────────────────┐
│      SceneMemorySystem (主控制器)       │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ↓            ↓            ↓
┌────────┐  ┌────────┐  ┌──────────┐
│ Node   │  │ Image  │  │ Memory   │
│Detector│  │Capturer│  │Mapper    │
└────┬───┘  └────┬───┘  └────┬─────┘
     │           │            │
     └───────────┼────────────┘
                 │
         ┌───────┴───────┐
         │               │
    ┌────────┐      ┌──────────┐
    │ Path   │      │ Path     │
    │Resolver│      │Growth    │
    └────────┘      │Manager   │
                    └──────────┘
                    │
                    ↓
            ┌───────────────┐
            │ PathPlanner   │
            └───────────────┘
```

---

## ❓ 核心问题解答

### Q1: 地图生成方式

**A**: 每个路径独立生成一个地图文件

**当前机制**:
```
data/map_cards/
├── path_a_to_b_map.png      # A到B的路径
├── path_a_to_c_map.png      # A到C的路径
└── path_b_to_c_map.png      # B到C的路径（如创建）
```

**扩展支持**:
- 独立路径地图（单目的地）
- 合并路径地图（多目的地）
- 分层地图（多条路径对比）

### Q2: 多目的地导航

**场景**: 从A出发，依次访问B和C

**已知路径**: A→B, A→C

**处理流程**:
```
1. 规划 A → B
   ✅ 使用已知路径 A→B

2. 规划 B → C
   ❌ 未找到已知路径 B→C
   
3. 应用策略: smart_merge
   - 询问用户是否记录 B→C 路径
   - 确认后启动路径记录模式
   - 边走边识别节点
   - 生成新路径 B→C
```

**结果**: ✅ 不回退到A，直接从B学习新路径

### Q3: 路径缺失处理

**默认策略**: **smart_merge（智能合并）**

**不会回退的场景**:
- 检测到未知路径
- 启动路径记录模式
- 边走路边学习
- 下次即可使用

**会回退的场景**:
- 用户选择 **fallback** 策略
- 系统建议回退（通过共同祖先）
- 用户明确要求回退

---

## 📦 模块功能说明

### 1. PathResolver (路径解析器)

**文件**: `core/path_resolver.py`

**功能**:
- 判断节点是否在同一条路径上
- 查找包含特定节点的路径
- 决定是否需要创建新路径
- 获取路径连续性信息

**核心方法**:
```python
# 判断节点归属
is_node_in_path(path_id, node_label) -> bool

# 查找节点路径
find_path_for_node(node_label) -> Optional[str]

# 路径创建决策
should_create_new_path(current, target) -> Dict

# 连续性检查
get_path_continuity(path_id, node_label) -> Dict
```

**使用示例**:
```python
resolver = PathResolver()

# 查找节点
path_id = resolver.find_path_for_node("挂号处")

# 判断是否需要新路径
decision = resolver.should_create_new_path("B", "C")
if decision['should_create']:
    print(f"需要创建新路径: {decision['message']}")
```

---

### 2. PathGrowthManager (路径增长管理器)

**文件**: `core/path_growth.py`

**功能**:
- 决定路径扩展或创建新路径
- 处理路径中断情况
- 支持用户手动重置
- 基于距离、相似度、时间判断

**核心方法**:
```python
# 扩展判断
should_extend_path(path_id, new_node) -> Dict

# 创建新路径
create_new_path(initial_node, name) -> str

# 扩展现有路径
extend_existing_path(path_id, new_node) -> bool

# 处理中断
handle_path_interruption(path_id, new_node, override) -> Dict
```

**判断逻辑**:
```python
should_extend = (
    distance < threshold AND      # 距离小于阈值
    similarity > coherence AND    # 相似度高于阈值
    time_interval < 300           # 时间间隔小于5分钟
)
```

**使用示例**:
```python
manager = PathGrowthManager(distance_threshold=50.0)

# 判断是否扩展
decision = manager.should_extend_path("path_id", new_node)
if decision['should_extend']:
    manager.extend_existing_path("path_id", new_node)
else:
    manager.create_new_path(new_node, "新路径")
```

---

### 3. MemoryMapper增强

**文件**: `core/scene_memory_system.py`

**新增功能**:
- 断点追加节点
- 路径统计信息
- 节点数据验证

**核心方法**:
```python
# 断点追加
append_node_to_path(path_id, node_data, validate) -> bool

# 路径统计
get_path_statistics(path_id) -> Dict

# 数据验证
_validate_node_data(node_data) -> bool
```

**使用示例**:
```python
# 追加节点
node_data = {
    "label": "新节点",
    "image_path": "path/to/image.jpg",
    "confidence": 0.95
}
success = memory_mapper.append_node_to_path("path_id", node_data)

# 获取统计
stats = memory_mapper.get_path_statistics("path_id")
print(f"节点数: {stats['total_nodes']}")
print(f"节点类型: {stats['node_types']}")
```

---

## 🎯 使用场景

### 场景1: 连续导航

```
已知: A→B (Path1), A→C (Path2)
目标: A → B → C

处理:
1. A→B: 使用Path1
2. B→C: 启动记录模式
3. 记录完成: 生成Path3 (B→C)
4. 下次: 直接使用全部路径
```

### 场景2: 路径中断恢复

```
情况: 用户在Path1的中间暂停

处理:
1. 检测到路径中断
2. 从中断点继续记录
3. 追加新节点到Path1
4. 保持路径连续性
```

### 场景3: 跨路径连接

```
已知: A→B (Path1), C→D (Path2)
目标: B → C

处理:
1. 检测到跨路径导航
2. 启动新路径记录模式
3. 记录 B→C 连接段
4. 生成Path3 (B→C)
5. 三个路径形成路径图
```

---

## ✅ 测试结果

### 模块测试

| 模块 | 测试项 | 状态 | 说明 |
|------|--------|------|------|
| PathResolver | 节点查找 | ✅ | 成功定位所有节点 |
| PathResolver | 路径判断 | ✅ | 正确判断路径归属 |
| PathResolver | 连续性检查 | ✅ | 正确返回前后节点 |
| PathGrowthManager | 扩展判断 | ✅ | 基于多指标判断 |
| PathGrowthManager | 创建路径 | ✅ | 成功创建新路径 |
| PathGrowthManager | 中断处理 | ✅ | 自动决定策略 |
| MemoryMapper | 断点追加 | ✅ | 成功追加节点 |
| MemoryMapper | 统计信息 | ✅ | 正确统计路径 |

### 完整流程测试

```
测试场景: 从已知路径扩展到新节点

步骤1: 路径决策 ✅
  - 判断结果: 需要创建新路径
  - 原因: 目标未知
  
步骤2: 扩展判断 ✅
  - 扩展判断: 不适合扩展
  - 原因: 距离/相似度/时间不满足条件
  
步骤3: 创建新路径 ✅
  - 执行: 创建新路径
  - 结果: 成功
```

---

## 📊 关键指标

### 路径扩展条件

```python
扩展条件 = {
    "距离": "< 50米",
    "相似度": "> 0.7",
    "时间间隔": "< 5分钟"
}
```

### 决策优先级

1. **用户手动重置** (最高)
2. **路径连续性良好** → 扩展
3. **路径已中断** → 创建新路径

---

## 🔄 工作流程

### 标准导航流程

```
1. 用户提出导航需求
   ↓
2. PathResolver查找节点和路径
   ↓
3. 判断路径是否存在
   ↓
4a. 存在 → 直接导航
4b. 不存在 → PathGrowthManager决策
   ↓
5. 扩展或创建新路径
   ↓
6. 启动导航/记录模式
   ↓
7. 完成并保存
```

### 路径学习流程

```
1. 检测到未知路径段
   ↓
2. 询问用户是否记录
   ↓
3. 确认后启动记录模式
   ↓
4. 边走边识别节点
   ↓
5. 自动保存节点和图像
   ↓
6. 生成新路径
   ↓
7. 下次即可使用
```

---

## 💡 最佳实践

### 1. 路径命名

```python
# 推荐命名格式
path_names = [
    "hospital_main_entrance_to_pharmacy",
    "shopping_mall_floor2_to_store305",
    "apartment_lobby_to_room501"
]
```

### 2. 地图管理

```python
# 建议的地图文件结构
map_cards/
├── single/              # 独立路径
├── combined/            # 合并路径
└── archived/            # 历史记录
```

### 3. 策略选择

```python
strategies = {
    "日常使用": "smart_merge",
    "首次访问": "ask_user",
    "紧急情况": "fallback"
}
```

---

## 📝 总结

### 回答您的问题

1. **地图生成**: ✅ 每个路径一个文件，支持合并
2. **多目的地**: ✅ 自动规划，智能处理
3. **路径缺失**: ✅ **不走回头路**，边记录边导航
4. **路径学习**: ✅ 渐进式构建，持续学习

### 关键优势

- 🎯 **智能决策**: 自动判断路径扩展/创建
- 🗺️ **知识积累**: 越用越聪明
- 🚀 **高效导航**: 不走回头路
- 💬 **用户友好**: 多种策略可选

---

**文档结束**

*Luna Badge v1.6 - 让导航更智能，让路径更灵活*
