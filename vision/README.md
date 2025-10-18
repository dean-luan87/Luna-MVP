# Luna Vision 模块

这是一个完整的计算机视觉功能集合，专为Luna项目设计。

## 功能模块

### 1. 摄像头初始化 (`init_camera.py`)
- 支持多种分辨率和帧率设置
- 摄像头测试功能
- 资源管理

**使用方法:**
```bash
python init_camera.py --source=0 --resolution=1280x720 --fps=30 --test
```

### 2. 物体检测 (`object_detection.py`)
- 基于YOLO的实时物体检测
- 距离估算和过滤
- 检测框绘制

**使用方法:**
```bash
python object_detection.py --model=yolov8n.pt --distance_filter=5 --draw_box=True
```

### 3. OCR文本识别 (`ocr_readout.py`)
- 多语言文本识别
- TTS语音朗读
- 实时文本提取

**使用方法:**
```bash
python ocr_readout.py --lang=zh --speak=True --trigger_button="space"
```

### 4. 动态物体追踪 (`dynamic_tracking.py`)
- 追踪行人、车辆等动态物体
- 距离过滤
- 实时追踪显示

**使用方法:**
```bash
python dynamic_tracking.py --classes="person,car,bicycle" --max_distance=15
```

### 5. 夜间增强 (`night_mode.py`)
- 亮度增强
- 降噪处理
- 夜视模式

**使用方法:**
```bash
python night_mode.py --brightness_boost=2.0 --denoise=True
```

### 6. 视频稳定 (`video_stabilization.py`)
- 防抖处理
- 特征点匹配
- 画面稳定

**使用方法:**
```bash
python video_stabilization.py --input=live --output=stabilized --mode=light
```

### 7. 人脸识别 (`face_recognition.py`)
- 人脸检测和识别
- 身份提示
- 数据库管理

**使用方法:**
```bash
python face_recognition.py --db=faces_db/ --notify="yes" --speech_notify="yes"
```

### 8. 风险碰撞提醒 (`risk_alert.py`)
- 路径遮挡检测
- 行人车辆接近警告
- 多级风险警报

**使用方法:**
```bash
python risk_alert.py --alert_level="medium" --voice_alert=True
```

### 9. 调试覆盖 (`debug_overlay.py`)
- FPS显示
- 物体计数
- 风险等级显示

**使用方法:**
```bash
python debug_overlay.py --fps --object_count --risk_level
```

## 依赖安装

```bash
pip3 install opencv-python ultralytics pytesseract pyttsx3
```

## 目录结构

```
vision/
├── __init__.py              # 模块初始化
├── init_camera.py           # 摄像头初始化
├── object_detection.py      # 物体检测
├── ocr_readout.py          # OCR文本识别
├── dynamic_tracking.py     # 动态物体追踪
├── night_mode.py           # 夜间增强
├── video_stabilization.py  # 视频稳定
├── face_recognition.py     # 人脸识别
├── risk_alert.py           # 风险碰撞提醒
├── debug_overlay.py        # 调试覆盖
├── faces_db/               # 人脸数据库
├── models/                 # 模型文件
└── data/                   # 数据文件
```

## 注意事项

1. 确保摄像头权限已开启
2. 某些功能需要额外的依赖包
3. 建议在虚拟环境中运行
4. 首次运行会下载YOLO模型文件

## 快捷键

- `q`: 退出程序
- `space`: 触发OCR识别
- 其他按键根据具体模块而定
