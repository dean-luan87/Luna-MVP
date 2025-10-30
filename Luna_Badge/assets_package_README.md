# Luna Badge Assets资源包说明

**版本**: v1.1  
**日期**: 2025-10-30  
**大小**: 28MB

---

## 📦 资源包内容

本资源包包含Luna Badge情绪地图生成系统所需的所有资源文件：

```
assets_package.zip
└── assets/
    ├── fonts/                           # 字体文件
    │   ├── handwriting.ttc             # 中文字体（53MB）
    │   └── README_FONTS.txt            # 字体说明
    │
    ├── icons/
    │   └── tabler/                     # Tabler Icons SVG图标库
    │       ├── toilet.svg              # 卫生间
    │       ├── elevator.svg            # 电梯
    │       ├── stairs.svg              # 楼梯
    │       ├── door-enter.svg          # 入口
    │       ├── hospital.svg            # 医院
    │       ├── building.svg            # 建筑
    │       ├── map-pin.svg             # 位置标记
    │       ├── bus.svg                 # 公交
    │       ├── subway.svg              # 地铁
    │       ├── home.svg                # 家
    │       ├── info-square.svg         # 信息
    │       ├── user.svg                # 用户
    │       └── wheelchair.svg          # 无障碍
    │
    └── textures/
        └── paper_background.png        # 纸张纹理背景（19KB）
```

---

## 🚀 安装步骤

### 1. 解压资源包

```bash
cd Luna_Badge
unzip assets_package.zip
```

### 2. 验证安装

```bash
# 检查字体文件
ls -lh assets/fonts/

# 检查图标文件
ls assets/icons/tabler/*.svg

# 检查纹理文件
ls -lh assets/textures/
```

### 3. 测试地图生成

```bash
python3 test_emotional_map_enhanced.py
```

---

## 📝 资源说明

### 字体 (fonts/)

**文件**: `handwriting.ttc`  
**大小**: 53MB（压缩后约12MB）  
**格式**: TrueType Collection  
**来源**: macOS STHeiti Light  

**用途**:
- 渲染中文节点标签
- 显示地图标题
- 绘制区域名称

**替换说明**:
如需使用其他字体，请：
1. 下载站酷字体（zcool.com）
2. 重命名为 `handwriting.ttf`
3. 替换原文件

### 图标 (icons/tabler/)

**数量**: 13个SVG图标  
**总大小**: ~5KB  
**来源**: Tabler Icons（MIT License）  
**格式**: SVG矢量图标

**特点**:
- ✅ 矢量格式（可无限缩放）
- ✅ MIT授权（商用免费）
- ✅ 统一风格（简洁线性）
- ✅ 支持自定义颜色

**使用**:
图标会根据节点类型自动加载，映射关系在代码中定义。

### 纹理 (textures/)

**文件**: `paper_background.png`  
**大小**: 19KB  
**分辨率**: 2400x1800px  
**内容**: 米黄色纸张纹理

**特点**:
- 真实纸张质感
- 低对比度设计
- 网格线纹理
- 高斯噪声效果

**自定义**:
可以将自定义纹理替换此文件，建议尺寸为2400x1800或更大。

---

## 🔧 技术细节

### 字体加载机制

系统按以下顺序尝试加载字体：

1. `assets/fonts/handwriting.ttf`
2. `assets/fonts/handwriting.ttc`
3. `/System/Library/Fonts/PingFang.ttc` (macOS)
4. `/System/Library/Fonts/STHeiti Light.ttc` (macOS)
5. 系统默认字体

### 图标加载机制

```python
# 图标映射
icon_name_map = {
    "destination": "map-pin",
    "entrance": "door-enter",
    "toilet": "toilet",
    "elevator": "elevator",
    ...
}

# 加载SVG
icon_img = SVGIconLoader.load_svg_icon(
    "assets/icons/tabler/toilet.svg",
    size=48
)
```

### 纹理应用

```python
# 加载背景纹理
texture = Image.open("assets/textures/paper_background.png")
texture.putalpha(30)  # 半透明
img = Image.alpha_composite(img, texture)
```

---

## 📄 详细文档

完整使用说明请参考：

**`docs/ASSETS_USAGE.md`**

包含：
- 字体使用指南
- 图标添加方法
- 纹理自定义
- 故障排除
- 代码示例

---

## ✅ 授权信息

### 字体

**STHeiti Light.ttc**: macOS系统字体  
**PingFang.ttc**: macOS系统字体

**自定义字体**: 请确保下载商用许可字体

### 图标

**Tabler Icons**: MIT License

```
MIT License

Copyright (c) 2020-2024 Tabler

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the 
"Software"), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish, 
distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to 
the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.
```

参考: https://tabler.io/icons

### 纹理

**自生成**: 无版权限制，可自由使用

---

## 🔄 更新日志

### v1.1 (2025-10-30)

- ✅ 集成13个Tabler Icons
- ✅ 添加中文字体支持
- ✅ 生成纸张纹理背景
- ✅ 创建资源包ZIP
- ✅ 编写完整文档

---

## 💬 技术支持

如遇问题，请：

1. 查阅 `docs/ASSETS_USAGE.md`
2. 检查文件路径是否正确
3. 验证文件格式是否有效
4. 查看系统日志

---

**版本**: v1.1  
**日期**: 2025-10-30  
**大小**: 28MB (压缩后)

---

*Luna Badge - 让地图更有体感*


