# Luna 实体徽章 MVP

一个基于AI的智能视觉辅助系统，实现"看得见、说得出、记得下"的完整流程。

## 项目概述

Luna 实体徽章 MVP 是一个集成多种AI模型的智能辅助系统，通过摄像头实时识别环境中的物体和文字，生成自然语言描述，并通过语音播报和日志记录为用户提供全方位的环境感知支持。

## 核心功能

### 🔍 视觉识别
- **目标检测**：使用YOLOv8n识别人、车、障碍物、标志牌等
- **文字识别**：使用PaddleOCR识别画面中的文字内容
- **场景理解**：使用Qwen2-VL生成自然语言场景描述

### 🎤 语音交互
- **语音输入**：使用Whisper进行语音识别
- **语音输出**：智能语音播报系统
  - 优先使用pyttsx3（离线TTS，Mac内置语音）
  - 备用edge-tts（在线TTS，支持多种语音）
  - 自动检测系统环境并选择最佳方案
  - 支持中文语音播报（Ting-Ting、Xiaoyi等）

### 📝 数据记录
- **实时日志**：JSON格式记录所有识别结果
- **处理统计**：记录处理时间和性能指标

## 技术架构

```
摄像头帧 → YOLO检测 → OCR识别 → Qwen生成描述 → TTS播报
    ↓           ↓         ↓         ↓         ↓
  图像数据   物体列表   文字列表   AI描述   语音输出
    ↓           ↓         ↓         ↓         ↓
              JSON日志记录 ← 完整结果汇总
```

## 项目结构

```
Luna_Badge_MVP/
├── main.py                 # 主程序入口
├── config.py              # 配置文件
├── requirements.txt       # 依赖包列表
├── README.md             # 项目说明
├── modules/              # 功能模块
│   ├── __init__.py
│   └── voice.py          # 语音播报模块
├── utils/                # 工具模块
│   ├── __init__.py
│   ├── model_interfaces.py  # AI模型接口
│   ├── camera_handler.py    # 摄像头处理
│   ├── logger.py           # 日志处理
│   └── json_logger.py      # JSON日志记录器
├── models/               # 模型文件目录
│   └── (模型文件将存储在这里)
└── logs/                 # 日志文件目录
    ├── luna_recognition.log
    └── luna_recognition.json
```

## 安装和运行

### 1. 环境要求

- Python 3.8+
- 摄像头设备
- 麦克风（可选，用于语音输入）

### 2. 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd Luna_Badge_MVP

# 安装依赖
pip install -r requirements.txt
```

### 3. Mac摄像头权限设置

**重要**：在Mac上首次运行时，需要授予摄像头权限：

1. 运行摄像头诊断工具：
   ```bash
   python3 check_camera.py
   ```

2. 如果提示权限问题：
   - 打开 **系统偏好设置** > **安全性与隐私** > **隐私**
   - 选择 **摄像头** 选项
   - 确保 **Terminal** 或 **Python** 应用有摄像头权限
   - 重启终端后再次运行

3. 如果仍有问题，可以尝试：
   ```bash
   # 更新OpenCV
   pip install --upgrade opencv-python
   
   # 重启电脑
   sudo reboot
   ```

### 4. 模型配置

在运行前，需要下载或配置以下模型：

#### YOLOv8n模型
```bash
# 模型会自动下载到 models/ 目录
# 或手动下载 yolov8n.pt 到 models/ 目录
```

#### PaddleOCR模型
```bash
# PaddleOCR模型会在首次运行时自动下载
```

#### Qwen2-VL API
在 `config.py` 中配置API密钥：
```python
MODEL_PATHS = {
    'qwen2_vl': {
        'api_key': 'your_api_key_here',  # 替换为实际API密钥
        'api_url': 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation',
        'model_name': 'qwen2-vl-plus'
    }
}
```

### 5. 运行程序

```bash
# 方法1: 使用快速启动脚本（推荐）
python3 run.py

# 方法2: 直接运行主程序
python3 main.py

# 方法3: 不显示摄像头画面
python3 main.py --no-camera

# 方法4: 自定义处理间隔（秒）
python3 main.py --interval 3.0

# 方法5: 指定摄像头索引
python3 main.py --camera-index 1
```

## 使用说明

### 操作控制
- **q键**：退出程序
- **s键**：立即处理当前帧

### 语音播报功能
- **启动提示**：程序启动时会语音播报"Luna 已启动"
- **状态播报**：摄像头和系统初始化状态会语音提示
- **识别结果**：每次识别完成后自动播报检测结果
- **智能播报**：自动组合物体检测、文字识别和AI描述信息
- **错误处理**：语音模块出错时不会影响主程序运行

### 输出说明
程序运行时会输出：
1. **控制台信息**：实时显示识别结果
2. **语音播报**：AI生成的场景描述
3. **日志文件**：
   - `logs/luna_recognition.log`：详细日志
   - `logs/luna_recognition.json`：结构化数据

### 配置选项

在 `config.py` 中可以调整：
- 摄像头参数（分辨率、帧率）
- 模型参数（置信度阈值、语言设置）
- 处理间隔和输出选项
- 日志配置

## 示例输出

### 控制台输出
```
==================================================
时间: 2024-01-15T10:30:45.123456
处理时间: 1.23秒

检测到的物体:
  - 人: 0.85
  - 汽车: 0.72

识别的文字:
  - 停车: 0.95
  - 禁止通行: 0.88

AI场景描述: 检测到人和停车标志，请注意安全
==================================================
```

### JSON日志
```json
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "objects": [
    {"class": "person", "confidence": 0.85, "bbox": [100, 100, 200, 300], "label": "人"},
    {"class": "car", "confidence": 0.72, "bbox": [300, 200, 500, 400], "label": "汽车"}
  ],
  "texts": [
    {"text": "停车", "confidence": 0.95, "bbox": [[50, 50], [100, 50], [100, 80], [50, 80]]}
  ],
  "description": "检测到人和停车标志，请注意安全",
  "audio_input": "",
  "processing_time": 1.23,
  "status": "success"
}
```

## 开发说明

### 模型接口
所有AI模型都通过统一的接口调用，便于替换和扩展：

- `YOLODetector`：目标检测
- `OCRProcessor`：文字识别
- `QwenVLProcessor`：场景描述生成
- `WhisperProcessor`：语音识别
- `TTSProcessor`：语音合成

### 扩展开发
1. **添加新模型**：在 `utils/model_interfaces.py` 中添加新的处理器类
2. **修改配置**：在 `config.py` 中调整参数
3. **自定义输出**：修改 `main.py` 中的 `_output_results` 方法

## 故障排除

### 常见问题

1. **摄像头无法打开**
   - 检查摄像头是否被其他程序占用
   - 尝试不同的摄像头索引：`--camera-index 1`

2. **模型加载失败**
   - 检查网络连接（模型需要下载）
   - 确保有足够的磁盘空间
   - 检查Python版本兼容性

3. **语音播报无声音**
   - 检查系统音频设置
   - 尝试不同的TTS引擎（在config.py中修改）

4. **性能问题**
   - 降低摄像头分辨率
   - 增加处理间隔时间
   - 使用GPU加速（如果支持）

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交Issue和Pull Request来改进项目。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 项目Issues
- 邮箱：[your-email@example.com]

---

**注意**：本项目为MVP版本，主要用于演示和测试。在生产环境中使用前，请确保所有模型都已正确配置和测试。
