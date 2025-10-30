# Assets资源使用指南

**日期**: 2025-10-30  
**版本**: v1.1  
**状态**: ✅ 完成

---

## 📦 资源包内容

`assets_package.zip` 包含以下内容：

```
assets_package.zip
├── assets/
│   ├── fonts/
│   │   ├── handwriting.ttc          # 中文字体（macOS华文黑体）
│   │   └── README_FONTS.txt         # 字体说明
│   ├── icons/
│   │   └── tabler/
│   │       ├── toilet.svg           # 卫生间图标
│   │       ├── elevator.svg         # 电梯图标
│   │       ├── stairs.svg           # 楼梯图标
│   │       ├── door-enter.svg       # 入口图标
│   │       ├── hospital.svg         # 医院图标
│   │       ├── building.svg         # 建筑图标
│   │       ├── map-pin.svg          # 位置图标
│   │       ├── bus.svg              # 公交图标
│   │       ├── subway.svg           # 地铁图标
│   │       ├── home.svg             # 家图标
│   │       ├── info-square.svg      # 信息图标
│   │       ├── user.svg             # 用户图标
│   │       └── wheelchair.svg       # 无障碍图标
│   └── textures/
│       └── paper_background.png     # 纸张纹理背景
```

---

## 📝 字体使用说明

### 字体文件

**位置**: `assets/fonts/handwriting.ttc`

**来源**: macOS系统字体（STHeiti Light.ttc）

**用途**: 
- 渲染中文节点标签
- 显示路径名称
- 绘制区域标题

### 字体加载

系统会自动按以下顺序尝试加载：

```python
font_paths = [
    "assets/fonts/handwriting.ttf",    # 优先
    "assets/fonts/handwriting.ttc",    # macOS字体
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
]
```

### 自定义字体

如需使用其他字体：

1. **下载字体文件**
   - 推荐：站酷高端黑、站酷快乐体
   - 来源：zcool.com

2. **替换字体文件**
   ```bash
   # 将下载的字体文件重命名
   mv downloaded_font.ttf assets/fonts/handwriting.ttf
   ```

3. **重启系统**
   - 字体会自动加载

### 字体特性

- ✅ 支持中文显示
- ✅ 手写风格友好
- ✅ 商用许可
- ✅ 自动Fallback

---

## 🎨 图标使用说明

### 图标库

**位置**: `assets/icons/tabler/`

**来源**: Tabler Icons (MIT License)

**格式**: SVG

### 图标映射

在 `emotional_map_card_generator.py` 中定义了节点类型到图标名称的映射：

```python
icon_name_map = {
    "destination": "map-pin",
    "waypoint": "map-pin",
    "entrance": "door-enter",
    "toilet": "toilet",
    "elevator": "elevator",
    "stairs": "stairs",
    "building": "building",
    "hospital": "hospital",
    "bus_stop": "bus",
    "subway_station": "subway",
}
```

### 添加新图标

1. **下载SVG文件**
   ```bash
   # 从Tabler Icons下载SVG
   curl -o assets/icons/tabler/new_icon.svg \
     "https://tabler.io/icons/icon/new-icon.svg"
   ```

2. **在代码中引用**
   ```python
   icon_name_map["new_type"] = "new_icon"
   ```

### 图标特性

- ✅ 矢量格式（可缩放）
- ✅ MIT授权（商用免费）
- ✅ 统一风格
- ✅ 支持自定义颜色

---

## 🌁 背景纹理使用说明

### 纹理文件

**位置**: `assets/textures/paper_background.png`

**规格**: 2400x1800px, PNG

**内容**: 米黄色纸张纹理

### 纹理生成

纹理使用PIL生成，包含：

1. **基础颜色**: RGB(249, 247, 238) - 米黄色
2. **噪声效果**: 随机噪声（0-30）
3. **网格线**: 50px间距浅色线
4. **高斯模糊**: radius=2.0

### 自定义纹理

如需使用自定义纹理：

```bash
# 1. 准备纹理图片（2400x1800或更大）
cp your_texture.png assets/textures/paper_background.png

# 2. 系统会自动加载
```

### 纹理特性

- ✅ 真实纸张质感
- ✅ 低对比度（不干扰内容）
- ✅ 半透明叠加
- ✅ 自动适配尺寸

---

## 🔧 代码集成

### 字体加载

```python
from core.emotional_map_card_generator import EmotionalMapCardGenerator

# 自动加载字体
generator = EmotionalMapCardGenerator()
# 字体路径: assets/fonts/handwriting.ttc
```

### 图标加载

```python
# 自动加载SVG图标
icon_img = generator._load_svg_icon("toilet", size=48)
# 图标路径: assets/icons/tabler/toilet.svg
```

### 纹理加载

```python
# 自动加载背景纹理
img = generator._apply_paper_texture(img)
# 纹理路径: assets/textures/paper_background.png
```

---

## 📊 资源统计

### 文件大小

| 资源 | 大小 | 说明 |
|------|------|------|
| fonts/handwriting.ttc | ~24MB | macOS字体（压缩后约12MB） |
| icons/tabler/*.svg | ~5KB | 13个SVG图标 |
| textures/paper_background.png | ~2MB | 2400x1800 PNG（压缩后约200KB） |
| **总计** | **~28MB** | **压缩ZIP包** |

### 资源数量

- 字体文件: 1个
- SVG图标: 13个
- 纹理文件: 1个

---

## 🚀 部署说明

### 部署步骤

1. **解压资源包**
   ```bash
   cd Luna_Badge
   unzip assets_package.zip
   ```

2. **验证资源**
   ```bash
   ls -lh assets/fonts/
   ls -lh assets/icons/tabler/
   ls -lh assets/textures/
   ```

3. **测试地图生成**
   ```bash
   python3 test_emotional_map_enhanced.py
   ```

### 环境要求

- PIL/Pillow
- numpy
- matplotlib
- cairosvg (可选，用于SVG渲染)

### 安装依赖

```bash
pip install pillow numpy matplotlib cairosvg
```

---

## 🐛 故障排除

### 问题1: 中文字体无法显示

**症状**: 中文显示为方块

**解决**:
1. 检查字体文件是否存在
2. 尝试使用系统字体fallback
3. 下载站酷字体手动替换

### 问题2: SVG图标不显示

**症状**: 节点没有图标

**解决**:
1. 检查图标文件是否在正确路径
2. 安装cairosvg: `pip install cairosvg`
3. 检查图标名称映射是否正确

### 问题3: 背景纹理不显示

**症状**: 背景纯色无纹理

**解决**:
1. 检查PNG文件是否存在
2. 确认文件格式正确
3. 检查纹理透明度设置

---

## ✅ 验证清单

### 字体验证

- [ ] 中文字符正常显示
- [ ] 标题使用指定字体
- [ ] 标签清晰可读

### 图标验证

- [ ] 所有图标类型都有对应SVG
- [ ] 图标大小正确（48x48）
- [ ] 图标透明背景正常

### 纹理验证

- [ ] 背景纸张质感可见
- [ ] 纹理不干扰地图内容
- [ ] 整体视觉协调

---

## 📄 授权信息

### 字体授权

**STHeiti Light.ttc**: macOS系统字体
**PingFang.ttc**: macOS系统字体
**handwriting.ttf**: 需自行下载商用许可字体

### 图标授权

**Tabler Icons**: MIT License
- 可商用
- 可修改
- 需保留版权声明

参考: https://tabler.io/icons

---

## 🔄 更新日志

### v1.1 (2025-10-30)

- ✅ 集成Tabler Icons
- ✅ 添加中文字体支持
- ✅ 生成纸张纹理
- ✅ 创建资源包ZIP
- ✅ 编写使用文档

---

**更新日期**: 2025-10-30  
**版本**: v1.1  
**状态**: ✅ 完成

---

*Luna Badge - Assets资源使用指南*

