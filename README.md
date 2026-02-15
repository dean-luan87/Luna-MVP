# Luna-2 智能感知与导航系统

Luna-2 是一个集成了计算机视觉、语音识别、语音合成和智能导航的综合性AI系统。

**技术红线（Technical constraint）**  
Any change to Luna visual navigation must pass `tools/determinism_guard.py` before being considered valid.

### Phase 3.3 Human Annotation

Annotation answers are treated as **immutable assets**. They do not affect runtime behavior, policy, or models. Any learning step must consume answers offline.

（标注答案仅作资产存档，不反写策略、不触碰模型；未来学习阶段须离线消费 answers。）

## 🎯 功能特性

### 🎥 视觉感知系统
- **实时人脸检测**: 使用 OpenCV Haar Cascades 进行高精度人脸识别
- **物体识别**: 基于 YOLOv8 的实时物体检测
- **计算机视觉模块**: 完整的视觉处理框架

### 🎤 语音交互系统
- **语音识别**: whisper.cpp 实时语音识别
- **语音合成**: 支持 edge-tts 和 pyttsx3 多引擎
- **中文语音播报**: 清晰的中文语音输出

### 🗺️ 智能导航系统
- **路径规划**: OpenRouteService API 支持
- **语音导航**: 实时语音导航指导
- **多城市支持**: 支持全球主要城市导航

## 📁 项目结构

```
Luna-2/
├── voice/                    # 语音模块
│   ├── __init__.py
│   ├── tts_engine.py        # 语音合成引擎
│   └── speaker.py           # 语音播报接口
│
├── vision/                   # 视觉模块
│   ├── __init__.py
│   ├── object_detection.py  # 物体检测
│   ├── face_recognition.py  # 人脸识别
│   └── ...                  # 其他视觉功能
│
├── navigation/               # 导航模块
│   ├── __init__.py
│   ├── route_planner.py     # 路径规划器
│   └── voice_navigator.py   # 语音导航器
│
├── modules/                  # 核心模块
│   ├── camera.py            # 摄像头控制
│   ├── state.py             # 状态管理
│   └── ...                  # 其他核心功能
│
├── whisper.cpp/              # 语音识别引擎
├── data/                     # 数据目录
└── logs/                     # 日志目录
```

## 🚀 快速开始

### 环境要求
- Python 3.9+
- OpenCV
- macOS (推荐) 或 Linux

### 安装依赖
```bash
pip3 install opencv-python ultralytics edge-tts pyttsx3 openrouteservice
```

### 配置 API 密钥
1. 注册 OpenRouteService: https://openrouteservice.org/
2. 设置环境变量:
```bash
export ORS_API_KEY='你的_API_密钥'
```

### 运行演示
```bash
# 语音导航演示
python3 system_voice_demo.py

# 视觉识别演示
python3 modules/camera.py

# 完整功能演示
python3 voice_navigation_demo.py
```

## 🎮 使用示例

### 语音导航
```python
from navigation import VoiceNavigator
from navigation.route_planner import TransportMode

navigator = VoiceNavigator()
await navigator.start_navigation(
    start=(121.4737, 31.2304),  # 起点
    end=(121.4997, 31.2397),    # 终点
    mode=TransportMode.WALKING   # 交通方式
)
```

### 语音播报
```python
from voice import Speaker

speaker = Speaker()
await speaker.speak("你好，我是 Luna 语音助手")
```

### 人脸检测
```python
import cv2
from modules.camera import detect_face_live

detect_face_live()  # 启动实时人脸检测
```

## 🔧 技术栈

- **计算机视觉**: OpenCV, YOLOv8
- **语音识别**: whisper.cpp
- **语音合成**: edge-tts, pyttsx3
- **地图服务**: OpenRouteService API
- **编程语言**: Python 3.9+

## 📝 开发说明

### 模块化设计
- 每个功能模块独立开发和测试
- 支持延迟加载，避免依赖冲突
- 统一的配置管理

### 性能优化
- 多线程处理音频和视频
- 智能缓存和资源管理
- 异步编程支持

## 🤝 贡献指南

1. Fork 本项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 📄 许可证

MIT License

## 🎉 致谢

感谢以下开源项目：
- OpenCV
- whisper.cpp
- ultralytics
- OpenRouteService

---

**Luna-2** - 让AI更贴近生活 🚀
