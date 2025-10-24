# Luna Badge - AI控制系统

## 项目简介

Luna Badge是一个可在Mac与嵌入式设备(RV1126)上通用的AI控制系统，专为Luna徽章项目设计。系统支持双运行环境，通过硬件抽象层实现跨平台兼容。

## 项目架构

```
Luna_Badge/
│
├─ core/                        # 系统核心逻辑层（通用）
│   ├─ config.py                # 配置管理与加载
│   ├─ system_control.py        # 状态机、自检、错误日志、状态循环
│   ├─ ai_navigation.py         # AI识别模块统一调度
│   ├─ hal_interface.py         # 硬件抽象层接口定义
│
├─ hal_mac/                     # Mac 版本硬件驱动层
│   ├─ hardware_mac.py          # 摄像头、麦克风、TTS播报
│
├─ hal_embedded/                # 嵌入式硬件驱动层（RV1126）
│   ├─ hardware_embedded.py     # 摄像头GPIO、电源控制、语音输出
│
├─ config.json                  # 模式与参数配置文件
├─ main_mac.py                  # Mac 运行入口
├─ main_embedded.py             # 嵌入式运行入口
└─ requirements.txt             # 依赖清单
```

## 核心功能

### 1. 双平台支持
- **Mac平台**: 使用YOLO + Whisper + Edge-TTS
- **嵌入式平台**: 使用RKNN + PicoVoice + Coqui-TTS

### 2. 状态机管理
- `ACTIVE`: 活跃状态，执行AI导航
- `IDLE`: 空闲状态，等待用户指令
- `SLEEP`: 睡眠状态，低功耗模式
- `OFF`: 关闭状态

### 3. AI导航模块
- **环境检测**: 识别环境类型（道路、人行道、室内等）
- **天气故障保护**: 检测极端天气和摄像头故障
- **指示牌导航**: 识别指示牌并生成导航路径
- **语音路径理解**: 理解人类语音中的路径描述

### 4. 硬件抽象层
- 统一的硬件接口定义
- 平台特定的硬件实现
- 自动硬件检测和初始化

## 安装和使用

### 环境要求

#### Mac平台
- Python 3.10+
- macOS 10.15+
- 摄像头和麦克风

#### 嵌入式平台
- Python 3.8+
- Linux系统
- RV1126开发板
- 摄像头模块

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置系统

编辑 `config.json` 文件：

```json
{
  "platform": "mac",  # 或 "embedded"
  "system": {
    "mode": "OFF",
    "auto_start": false,
    "debug_mode": true
  },
  "hardware": {
    "camera": {
      "enabled": true,
      "resolution": "640x480",
      "fps": 30
    }
  }
}
```

### 运行系统

#### Mac平台
```bash
python main_mac.py
```

#### 嵌入式平台
```bash
python main_embedded.py
```

## 系统特性

### 1. 自动平台检测
系统会自动检测运行平台并加载相应的硬件驱动。

### 2. 配置管理
支持动态配置加载和保存，无需重启系统。

### 3. 错误处理
完善的错误日志记录和自动修复机制。

### 4. 状态监控
实时监控系统状态和硬件状态。

### 5. 语音交互
支持语音唤醒和语音播报功能。

## 开发指南

### 添加新的AI模块

1. 在 `core/ai_navigation.py` 中添加新的模块枚举
2. 实现平台特定的模块类
3. 在 `AI导航统一调度器` 中添加调度逻辑

### 添加新的硬件接口

1. 在 `core/hal_interface.py` 中定义接口
2. 在平台特定的硬件层中实现接口
3. 在硬件抽象层中注册接口

### 配置管理

使用 `ConfigManager` 类进行配置管理：

```python
from core import config_manager

# 获取配置
value = config_manager.get_config("hardware.camera.resolution")

# 设置配置
config_manager.set_config("hardware.camera.fps", 30)
```

## 故障排除

### 常见问题

1. **摄像头初始化失败**
   - 检查摄像头是否被其他程序占用
   - 确认摄像头权限设置

2. **语音引擎初始化失败**
   - 检查TTS引擎是否已安装
   - 确认音频设备是否可用

3. **网络连接失败**
   - 检查网络连接状态
   - 确认防火墙设置

### 调试模式

启用调试模式以获取详细的日志信息：

```json
{
  "system": {
    "debug_mode": true
  }
}
```

## 许可证

本项目采用MIT许可证。

## 贡献

欢迎提交Issue和Pull Request。

## 联系方式

如有问题，请联系项目维护者。
