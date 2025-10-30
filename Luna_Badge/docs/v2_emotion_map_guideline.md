# EmotionMap v2 使用指南

**日期**: 2025-10-30  
**版本**: v2.0  
**状态**: 🚧 架构初始化完成

---

## 🧭 架构说明

### 核心设计理念

EmotionMap v2 采用**结构与表现解耦**的架构：

- **v1_core/**: 数据层 - 负责路径结构生成（保留原有逻辑）
- **v2_render/**: 表现层 - 插画式地图渲染 + 情绪注释生成

### 目录结构

```
Luna_Badge/
├── v1_core/                        # 数据层
│   ├── path_struct_generator.py   # 路径结构生成器
│   └── (保留) navigation_scheduler.py 等
│
├── v2_render/                      # 表现层
│   ├── emotion_map_renderer.py    # 插画地图渲染器
│   ├── emotion_story_injector.py  # 节点情绪注释注入器
│   └── config/
│       └── illustration_style.yaml # 视觉风格配置
│
├── assets/
│   ├── illustration_pack/         # 插图资源（SVG/PNG）
│   ├── fonts/                     # 字体文件
│   ├── icons/                     # 图标库
│   └── textures/                  # 纹理资源
│
├── map_cards/                     # 输出目录
│   ├── *.png                      # 情绪地图图卡
│   └── *.meta.json                # 元信息
│
└── docs/
    └── v2_emotion_map_guideline.md # 本文件
```

---

## 🖼️ 使用方式

### 方式1：完整流程

```python
from v2_render.emotion_map_renderer import EmotionMapRenderer
from v2_render.emotion_story_injector import EmotionStoryInjector
from v1_core.path_struct_generator import PathStructGenerator

# 1. 生成路径结构
struct_generator = PathStructGenerator()
path_data = struct_generator.generate_path_structure("path_id")

# 2. 注入情绪叙事
injector = EmotionStoryInjector()
enhanced_data = injector.inject_emotion_story(path_data)

# 3. 渲染插画式地图
renderer = EmotionMapRenderer()
output_path = renderer.render_emotion_map(enhanced_data)

print(f"✅ 地图已生成: {output_path}")
```

### 方式2：快速使用（推荐）

```python
from v2_render import render_emotion_map_quick

# 一行搞定
output_path = render_emotion_map_quick("path_id")
```

---

## 🎨 配置说明

### illustration_style.yaml

视觉风格配置文件，支持以下自定义：

#### 节点样式

```yaml
node_styles:
  elevator:
    icon: elevator.svg           # 图标文件
    color: "#555555"            # 节点颜色
    emotion: "嘈杂"              # 默认情绪
    story: "人流较多，请注意"    # 提示文字
```

#### 路径样式

```yaml
line_style:
  jitter: true                  # 手绘抖动
  stroke: 2.5                   # 线宽
  color: "#606C80"              # 深蓝灰色
```

#### 背景配置

```yaml
background:
  texture: paper_background.png # 纹理文件
  opacity: 0.28                 # 透明度
  color: "#F9F7EE"              # 基础色
```

#### 情绪标签

```yaml
emotion_tags:
  推荐:
    bg: "#FFB6C1"               # 背景色
    text: "#FFFFFF"             # 文字色
    shape: "rounded"            # 形状
    emoji: "❤️"                 # Emoji
```

---

## 📊 输出格式

### PNG地图

- **位置**: `map_cards/<path_id>_emotion.png`
- **分辨率**: 2400x1800
- **格式**: PNG (RGB)

### 元信息JSON

```json
{
  "path_id": "hospital_main",
  "path_name": "医院导航路径",
  "map_direction_reference": "上 = 北",
  "icons_used": true,
  "legend_synced": true,
  "label_font_size": 22,
  "emotions_injected": true,
  "story_hints": true,
  "regions_detected": ["三楼病区", "挂号大厅"],
  "node_count": 6,
  "total_distance": "100米"
}
```

---

## 🔧 开发计划

### Phase 1: 架构初始化 ✅

- [x] 目录结构创建
- [x] 模块骨架搭建
- [x] 配置文件编写
- [x] 文档编写

### Phase 2: 渲染引擎实现 🚧

- [ ] SVG图标加载
- [ ] 路径绘制（贝塞尔曲线+抖动）
- [ ] 区域渲染
- [ ] 情绪标签绘制
- [ ] 背景纹理应用

### Phase 3: 情绪注入 🚧

- [ ] 情绪标签自动生成
- [ ] 叙事文字模板系统
- [ ] 路径级别引导语

### Phase 4: 资源包 🚧

- [ ] 插图打包
- [ ] 字体集成
- [ ] 纹理优化

---

## 🆚 v1 vs v2 对比

| 特性 | v1 | v2 |
|------|----|----|
| 架构 | 单体 | 分层（结构+表现） |
| 配置 | 硬编码 | YAML配置文件 |
| 情绪注入 | 手动 | 自动 |
| 扩展性 | 低 | 高 |
| 定制能力 | 中 | 强 |

---

## 💡 最佳实践

### 1. 自定义情绪标签

编辑 `illustration_style.yaml`：

```yaml
emotion_tags:
  我的自定义情绪:
    bg: "#自定义颜色"
    text: "#FFFFFF"
    shape: "bubble"
    emoji: "⭐"
```

### 2. 添加新节点类型

```yaml
node_styles:
  新类型:
    icon: new_icon.svg
    color: "#HEX颜色"
    emotion: "情绪标签"
    story: "提示文字"
```

### 3. 调整视觉风格

修改配置后重新运行渲染器即可生效。

---

## 📚 相关文档

- [EmotionMap v1 总结](/docs/EMOTIONAL_MAP_SUMMARY.md)
- [Assets使用指南](/docs/ASSETS_USAGE.md)
- [配置系统说明](/docs/CONFIGURATION_GUIDE.md)

---

## 🐛 故障排除

### 问题1: 图标不显示

**解决**: 确保 `assets/icons/tabler/` 下有对应SVG文件

### 问题2: 配置不生效

**解决**: 检查 `illustration_style.yaml` 格式，确保缩进正确

### 问题3: 情绪注入失败

**解决**: 查看日志，检查节点类型是否在预设中

---

## 📝 更新日志

### v2.0 (2025-10-30)

- ✅ 架构切换完成
- ✅ 模块骨架搭建
- ✅ 配置文件创建
- ✅ 文档编写
- 🚧 渲染引擎开发中
- 🚧 资源包准备中

---

**状态**: 🚧 开发中  
**版本**: v2.0  
**最后更新**: 2025-10-30

---

*Luna Badge - EmotionMap v2 插画式情绪地图系统*
