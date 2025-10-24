# Luna Badge MVP

## 🎯 项目概述

Luna Badge MVP是一个轻量级的实时视觉导航系统，集成了目标检测、目标跟踪、路径预测和语音播报功能。

## 📁 项目结构

```
Luna_Badge_MVP/
├── main.py                      # 主程序入口
├── config/
│   └── system_config.yaml      # 系统配置文件
├── vision/
│   ├── yolov5_detector.py      # YOLOv5目标检测器
│   ├── deepsort_tracker.py     # DeepSort目标跟踪器
│   └── path_predict.py         # 路径预测器
├── speech/
│   ├── tts_config.yaml         # TTS语音配置文件
│   └── speech_engine.py        # 语音引擎
├── core/
│   ├── cooldown_manager.py     # 冷却管理器
│   ├── state_tracker.py        # 状态跟踪器
│   └── logger.py               # 日志管理器
├── test_system.py              # 系统测试脚本
└── README.md                   # 项目说明文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install torch torchvision ultralytics opencv-python numpy pyyaml
```

### 2. 运行测试

```bash
python test_system.py
```

### 3. 运行主程序

```bash
python main.py
```

## 🔧 功能特性

### 视觉模块
- **YOLOv5检测器**: 实时目标检测
- **DeepSort跟踪器**: 目标跟踪和ID分配
- **路径预测器**: 路径状态分析和预测

### 语音模块
- **语音引擎**: 异步语音播报
- **TTS配置**: 支持多种语音风格和优先级

### 核心模块
- **冷却管理器**: 防止重复播报
- **状态跟踪器**: 系统状态管理
- **日志管理器**: 统一的日志记录

## 📊 配置说明

### 系统配置 (config/system_config.yaml)
- 摄像头参数设置
- 检测和跟踪参数
- 语音播报配置
- 冷却时间设置

### 语音配置 (speech/tts_config.yaml)
- 语音事件定义
- 语音风格配置
- 播报优先级设置

## 🎮 使用方法

### 基本使用

```python
from main import LunaBadgeMVP

# 创建系统实例
luna_system = LunaBadgeMVP()

# 运行系统
luna_system.run()
```

### 模块使用

```python
# 使用YOLOv5检测器
detector = YOLOv5Detector()
detector.initialize()
detections = detector.detect(frame)

# 使用DeepSort跟踪器
tracker = DeepSortTracker()
tracker.initialize()
tracks = tracker.update(detections)

# 使用路径预测器
predictor = PathPredictor()
predictor.initialize()
prediction = predictor.predict(tracks)

# 使用语音引擎
speech_engine = SpeechEngine()
speech_engine.initialize()
speech_engine.speak("前方路径畅通", priority=1)
```

## 🔍 测试

### 运行测试

```bash
python test_system.py
```

### 测试内容
- 核心模块功能测试
- 视觉模块集成测试
- 语音模块功能测试
- 配置文件验证测试

## 📝 日志

系统会自动生成日志文件 `luna_mvp.log`，记录系统运行状态和错误信息。

## 🛠️ 开发说明

### 添加新功能
1. 在相应模块中添加功能代码
2. 更新配置文件
3. 添加测试用例
4. 更新文档

### 调试模式
在配置文件中设置 `debug_mode: true` 启用调试模式。

## 📄 许可证

本项目采用MIT许可证。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目。

## 📞 联系方式

如有问题，请通过Issue联系。
