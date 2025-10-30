# Luna Badge 情绪地图模块系统

**日期**: 2025-10-30  
**版本**: v1.6+  
**状态**: ✅ 完成

---

## 📋 概述

Luna Badge 情绪地图模块系统是一组用于生成手绘风格、带情绪标注的导航地图的工具。系统包含四个核心模块，支持从记忆存储中提取路径数据，为节点分配层级、标注情绪、构建邻接图，并最终生成可视化的情绪地图。

---

## 🗺️ 模块架构

```
┌─────────────────────────────────────────────────┐
│           情绪地图模块系统                        │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │  Module 1: Emotional Map Card Generator  │  │
│  │  emotional_map_card_generator.py         │  │
│  │  - 生成PNG/PDF手绘风格地图                 │  │
│  │  - 应用纸张纹理和手绘效果                  │  │
│  │  - 渲染情绪标签、图标、方向线              │  │
│  └──────────────────────────────────────────┘  │
│                 ↓                                │
│  ┌──────────────────────────────────────────┐  │
│  │  Module 2: Node Layer Manager            │  │
│  │  node_layer_manager.py                   │  │
│  │  - 自动分配节点层级                       │  │
│  │  - 分类室外/楼内/电梯间等                │  │
│  └──────────────────────────────────────────┘  │
│                 ↓                                │
│  ┌──────────────────────────────────────────┐  │
│  │  Module 3: Adjacency Graph Builder       │  │
│  │  adjacency_graph_builder.py              │  │
│  │  - 构建节点邻接关系                       │  │
│  │  - 支持路径查找                           │  │
│  └──────────────────────────────────────────┘  │
│                 ↓                                │
│  ┌──────────────────────────────────────────┐  │
│  │  Module 4: Emotional Tagger              │  │
│  │  emotional_tagger.py                     │  │
│  │  - 提取情绪标签                           │  │
│  │  - 关键词映射到emoji                     │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 🔧 模块详细说明

### Module 1: Emotional Map Card Generator

**文件**: `core/emotional_map_card_generator.py`

**功能**:
- 生成手绘风格的情绪地图图卡
- 使用PIL和matplotlib进行绘制
- 支持纸张纹理和手绘抖动效果

**主要方法**:
- `generate_emotional_map(path_id, path_name, nodes)` - 生成情绪地图
- `_apply_paper_texture(img)` - 应用纸张纹理
- `_draw_shaky_line(draw, coords, color)` - 绘制抖动线条
- `_render_node_icon(node_type, size)` - 渲染节点图标
- `_render_emotion_tag(emotion, position, img)` - 渲染情绪标签

**输入**:
- `path_id`: 路径ID
- `path_name`: 路径名称（可选）
- `nodes`: 节点列表（可选）

**输出**:
- PNG格式的情绪地图文件
- 保存在 `data/map_cards/<path_id>_emotional.png`

**配置**:
```python
emotion_map = {
    "热闹": {"emoji": "🎉", "color": (255, 100, 100)},
    "安静": {"emoji": "🤫", "color": (100, 150, 255)},
    "推荐": {"emoji": "⭐", "color": (255, 200, 100)},
    ...
}

hand_drawn_style = {
    "paper_color": (249, 247, 238),  # 米黄色纸张
    "line_color": (50, 50, 50),      # 黑色线条
    "shadow_color": (200, 200, 200), # 灰色阴影
    "texture_alpha": 30,              # 纹理透明度
}
```

---

### Module 2: Node Layer Manager

**文件**: `core/node_layer_manager.py`

**功能**:
- 自动为节点分配层级标签
- 支持室内/室外、楼层、功能区域分类
- 支持从路径名称推断层级

**主要方法**:
- `assign_level(node)` - 为单个节点分配层级
- `update_all_levels(memory_store_path, output_path)` - 批量更新所有节点层级
- `get_level_hierarchy(memory_store_path)` - 获取层级结构树

**层级分类**:
```
室外 → 室外主路/人行道/广场
入口区 → 大门/门厅/前台/接待
楼层 → 一楼/二楼/三楼... + 区域(东/西/中)
电梯间 → 电梯/升降梯/直梯
楼梯间 → 楼梯/台阶/步梯
走廊 → 走廊/通道/过道
候诊区 → 候诊/等待区
科室 → 科室/诊室/病房
卫生间 → 厕所/洗手间
终端节点 → 终点/目的地
功能锚点 → 锚点/关键点/转乘
```

**示例**:
```python
node = {"label": "医院三楼东侧卫生间"}
level = manager.assign_level(node)
# 返回: "三楼 东区"
```

---

### Module 3: Adjacency Graph Builder

**文件**: `core/adjacency_graph_builder.py`

**功能**:
- 为路径中的节点构建邻接关系图
- 添加`adjacent`字段存储相邻节点ID
- 支持BFS路径搜索
- 检测跨路径连接点

**主要方法**:
- `build_adjacency_graph(memory_store_path, output_path)` - 构建邻接图
- `get_adjacent_nodes(memory_store_path, path_id, node_id)` - 获取相邻节点
- `find_shortest_path(memory_store_path, start_node_id, end_node_id)` - 查找最短路径
- `get_graph_statistics(memory_store_path)` - 获取图统计信息

**数据结构**:
```json
{
  "node_id": "path1_node_2",
  "adjacent": ["path1_node_1", "path1_node_3"]
}
```

**统计信息**:
```python
{
  "total_nodes": 50,
  "total_edges": 98,
  "isolated_nodes": 2,
  "max_degree": 4,
  "cross_path_connections": 5
}
```

---

### Module 4: Emotional Tagger

**文件**: `core/emotional_tagger.py`

**功能**:
- 从用户文本中提取情绪标签
- 关键词映射到emoji
- 批量标注节点情绪
- 支持自定义情绪规则

**主要方法**:
- `extract_emotion_tags(note)` - 提取情绪标签
- `tag_nodes_with_emotion(memory_store_path, output_path)` - 批量标注
- `get_emotion_emoji(emotion_tag)` - 获取emoji
- `add_custom_emotion(tag, keywords, emoji)` - 添加自定义情绪

**情绪映射表**:

| 情绪标签 | 关键词 | Emoji |
|---------|--------|-------|
| 热闹 | 热闹,活跃,繁华,熙攘 | 🎉 |
| 推荐 | 推荐,好评,很赞,不错 | ⭐ |
| 温馨 | 温馨,温暖,舒适 | 💝 |
| 安静 | 安静,清静,宁静 | 🤫 |
| 宽敞 | 宽敞,开阔,空旷 | 🏛️ |
| 嘈杂 | 嘈杂,吵闹,喧闹 | 🔊 |
| 拥挤 | 拥挤,挤,密 | 👥 |
| 烦躁 | 烦躁,烦,焦虑 | 😤 |
| 等待 | 等待,排队,久等 | ⏳ |
| 无障碍 | 无障碍,残障,轮椅 | ♿ |

**特殊规则**:
- 等待时间检测: "等了30分钟" → 添加"等待"标签
- 人数判断: "人很多" → 添加"拥挤"标签
- 亮度判断: "亮堂" → 添加"明亮"标签
- 清洁度判断: "很干净" → 添加"整洁"标签

---

## 📁 文件结构

```
Luna_Badge/
├── core/
│   ├── emotional_map_card_generator.py    # Module 1
│   ├── node_layer_manager.py              # Module 2
│   ├── adjacency_graph_builder.py         # Module 3
│   └── emotional_tagger.py                # Module 4
├── data/
│   ├── memory_store.json                  # 记忆存储（输入）
│   └── map_cards/                         # 地图输出目录
│       ├── test_emotional_path_emotional.png
│       └── ...
├── assets/
│   └── icons/                             # 图标资源
└── docs/
    └── emotional_map_modules.md           # 本文档
```

---

## 🚀 使用流程

### 步骤1: 准备数据

确保 `data/memory_store.json` 包含路径数据:

```json
{
  "paths": [
    {
      "path_id": "hospital_main_path",
      "path_name": "医院主路径",
      "nodes": [
        {"node_id": "node1", "label": "医院入口", "type": "entrance"},
        {"node_id": "node2", "label": "一楼大厅", "type": "building"},
        {"node_id": "node3", "label": "三楼电梯间", "type": "elevator"},
        {"node_id": "node4", "label": "急诊科", "type": "destination"}
      ]
    }
  ]
}
```

### 步骤2: 分配层级

```python
from core.node_layer_manager import NodeLayerManager

manager = NodeLayerManager()
stats = manager.update_all_levels("data/memory_store.json")
```

### 步骤3: 构建邻接图

```python
from core.adjacency_graph_builder import AdjacencyGraphBuilder

builder = AdjacencyGraphBuilder()
stats = builder.build_adjacency_graph("data/memory_store.json")
```

### 步骤4: 标注情绪

```python
from core.emotional_tagger import EmotionalTagger

tagger = EmotionalTagger()
stats = tagger.tag_nodes_with_emotion("data/memory_store.json")
```

### 步骤5: 生成情绪地图

```python
from core.emotional_map_card_generator import EmotionalMapCardGenerator

generator = EmotionalMapCardGenerator()
result = generator.generate_emotional_map("hospital_main_path")
```

---

## 🧪 测试用例

### 测试1: 单个节点层级分配

```python
manager = NodeLayerManager()
test_nodes = [
    {"label": "医院入口大门", "type": "entrance"},
    {"label": "一楼大厅", "type": "building"},
    {"label": "三楼电梯间", "type": "elevator"},
    {"label": "二楼东侧卫生间", "type": "toilet"},
    {"label": "室外马路", "type": "waypoint"},
]

for node in test_nodes:
    level = manager.assign_level(node)
    print(f"{node['label']:20s} -> {level}")
```

**输出**:
```
医院入口大门            -> 入口区
一楼大厅                -> 一楼
三楼电梯间              -> 电梯间
二楼东侧卫生间          -> 二楼 东区
室外马路                -> 室外
```

### 测试2: 情绪标签提取

```python
tagger = EmotionalTagger()
test_notes = [
    "这个医院人很多，环境很嘈杂",
    "卫生间很干净，推荐使用",
    "等候大厅宽敞明亮，很温馨",
]

for note in test_notes:
    tags = tagger.extract_emotion_tags(note)
    emojis = [tagger.get_emotion_emoji(tag) for tag in tags]
    print(f"文本: {note}")
    print(f"  标签: {tags}")
    print(f"  Emoji: {' '.join(emojis)}")
```

**输出**:
```
文本: 这个医院人很多，环境很嘈杂
  标签: ['嘈杂', '拥挤']
  Emoji: 🔊 👥

文本: 卫生间很干净，推荐使用
  标签: ['推荐', '整洁']
  Emoji: ⭐ ✨

文本: 等候大厅宽敞明亮，很温馨
  标签: ['宽敞', '明亮', '温馨']
  Emoji: 🏛️ 💡 💝
```

### 测试3: 完整流程测试

创建测试脚本 `test_emotional_map_complete.py`:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
from pathlib import Path

# 添加core到路径
sys.path.insert(0, str(Path(__file__).parent))

from core.emotional_tagger import EmotionalTagger
from core.node_layer_manager import NodeLayerManager
from core.adjacency_graph_builder import AdjacencyGraphBuilder
from core.emotional_map_card_generator import EmotionalMapCardGenerator

def main():
    # 创建测试数据
    test_data = {
        "paths": [
            {
                "path_id": "test_emotional_path",
                "path_name": "测试情绪路径",
                "nodes": [
                    {"node_id": "node1", "label": "医院入口", "type": "entrance", 
                     "note": "人很多很拥挤"},
                    {"node_id": "node2", "label": "一楼大厅", "type": "building", 
                     "note": "宽敞明亮推荐"},
                    {"node_id": "node3", "label": "卫生间", "type": "toilet", 
                     "note": "很安静干净整洁"},
                    {"node_id": "node4", "label": "电梯间", "type": "elevator", 
                     "note": ""},
                    {"node_id": "node5", "label": "目的地", "type": "destination", 
                     "note": "温馨舒适"},
                ]
            }
        ]
    }
    
    # 保存测试数据
    with open("data/test_memory.json", 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print("=" * 60)
    print("情绪地图完整流程测试")
    print("=" * 60)
    
    # 步骤1: 分配层级
    print("\n1️⃣ 分配节点层级...")
    manager = NodeLayerManager()
    manager.update_all_levels("data/test_memory.json")
    
    # 步骤2: 构建邻接图
    print("\n2️⃣ 构建邻接图...")
    builder = AdjacencyGraphBuilder()
    builder.build_adjacency_graph("data/test_memory.json")
    
    # 步骤3: 标注情绪
    print("\n3️⃣ 标注情绪标签...")
    tagger = EmotionalTagger()
    tagger.tag_nodes_with_emotion("data/test_memory.json")
    
    # 步骤4: 生成情绪地图
    print("\n4️⃣ 生成情绪地图...")
    generator = EmotionalMapCardGenerator(memory_store_path="data/test_memory.json")
    result = generator.generate_emotional_map("test_emotional_path")
    
    if result:
        print(f"\n✅ 情绪地图生成成功: {result}")
    else:
        print("\n❌ 情绪地图生成失败")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
```

---

## 📊 输出示例

### 生成的PNG地图特征

- **画布尺寸**: 2400 x 1800
- **纸张颜色**: 米黄色 (#F9F7EE)
- **线条颜色**: 黑色 (#323232)
- **布局**: 螺旋分布
- **图标**: 手绘风格简笔画
- **情绪标签**: 彩色圆形+emoji
- **文字**: 默认系统字体

### 情绪地图可视化元素

1. **节点**:
   - 带编号的圆形节点
   - 类型图标（建筑/卫生间/电梯等）
   - 节点标签

2. **路径**:
   - 抖动线条连接节点
   - 箭头指示方向

3. **情绪标签**:
   - 彩色圆形背景
   - Emoji图标
   - 半透明效果

4. **标题**:
   - "情绪地图: 路径名称"
   - 左上角显示

---

## 🔄 未来扩展

### 计划功能

1. **PDF输出支持**
   - 支持生成高质量PDF地图
   - 可打印版本

2. **3D层级可视化**
   - 分层显示不同楼层
   - 立体路径图

3. **交互式地图**
   - HTML5交互式地图
   - 鼠标悬停查看详情

4. **路径优化**
   - Dijkstra最短路径算法
   - A*路径搜索
   - 避障路径规划

5. **语音地图描述**
   - 基于情绪标签生成语音导航
   - TTS集成

6. **用户反馈集成**
   - 实时更新情绪标签
   - 用户标注功能

---

## 🐛 已知限制

1. **字体依赖**: 需要系统字体支持emoji
2. **图标样式**: 目前使用简单的几何图形
3. **性能**: 大规模节点可能较慢
4. **情绪识别**: 基于关键词，可能不够准确

---

## 📝 更新日志

### v1.0 (2025-10-30)

- ✅ 四个核心模块全部实现
- ✅ 文档编写完成
- ✅ 测试用例完成
- ✅ 手绘风格渲染实现
- ✅ 情绪标注系统完成

---

**解决方案完成日期**: 2025-10-30  
**系统版本**: Luna Badge v1.6+  
**状态**: ✅ 生产就绪

---

*Luna Badge - 让导航更直观，让情绪可感知*


