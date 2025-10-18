# Luna-2 部署指南

## 🚀 **新电脑快速部署**

### 1. **克隆项目**
```bash
git clone https://github.com/deanluan87/Luna-2.git
cd Luna-2
```

### 2. **自动环境配置**
```bash
# 运行环境配置脚本
./setup_environment.sh

# 设置 API 密钥
export ORS_API_KEY='你的_OpenRouteService_API_密钥'
```

### 3. **快速功能测试**
```bash
# 运行快速测试
python3 quick_test.py
```

### 4. **验证核心功能**
```bash
# 测试语音导航
python3 system_voice_demo.py

# 测试人脸检测
python3 modules/camera.py
```

## 📋 **详细部署步骤**

### 系统要求
- **操作系统**: macOS (推荐) 或 Linux
- **Python**: 3.9 或更高版本
- **硬件**: 摄像头、麦克风、扬声器

### 依赖安装
```bash
# 安装 Python 依赖
pip3 install opencv-python ultralytics edge-tts pyttsx3 openrouteservice requests

# 验证安装
python3 -c "import cv2, pyttsx3, edge_tts, openrouteservice; print('✅ 所有依赖安装成功')"
```

### API 配置
1. **OpenRouteService**:
   - 访问: https://openrouteservice.org/
   - 注册并获取免费 API 密钥
   - 设置环境变量: `export ORS_API_KEY='你的密钥'`

2. **Google Maps** (可选):
   - 访问: https://developers.google.com/maps
   - 获取 API 密钥
   - 设置环境变量: `export GOOGLE_MAPS_API_KEY='你的密钥'`

### 功能验证

#### 语音系统测试
```bash
# 测试系统语音
say "Luna-2 语音系统测试"

# 测试语音导航
python3 system_voice_demo.py
```

#### 视觉系统测试
```bash
# 测试人脸检测
python3 modules/camera.py

# 测试物体识别
python3 test_object_detection.py
```

#### 导航系统测试
```bash
# 测试路径规划
python3 voice_navigation_final.py
```

## 🔄 **日常同步流程**

### 拉取最新代码
```bash
git pull origin main
```

### 提交本地更改
```bash
git add .
git commit -m "更新描述"
git push origin main
```

### 环境同步
```bash
# 更新依赖
pip3 install -r requirements.txt

# 重新配置环境
./setup_environment.sh
```

## 🛠️ **故障排除**

### 常见问题

#### 1. 摄像头无法打开
```bash
# 检查摄像头权限
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('摄像头状态:', cap.isOpened())"
```

#### 2. 语音播报无声音
```bash
# 测试系统音频
say "音频测试"

# 检查音量设置
osascript -e "set volume output volume 50"
```

#### 3. API 调用失败
```bash
# 检查 API 密钥
echo $ORS_API_KEY

# 测试网络连接
curl -I https://api.openrouteservice.org
```

#### 4. 模块导入错误
```bash
# 重新安装依赖
pip3 install --upgrade opencv-python ultralytics edge-tts pyttsx3 openrouteservice

# 检查 Python 路径
python3 -c "import sys; print(sys.path)"
```

## 📱 **开发环境配置**

### VS Code 配置
```json
{
    "python.defaultInterpreterPath": "/usr/bin/python3",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black"
}
```

### 环境变量配置
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export ORS_API_KEY='你的密钥'
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## 🎯 **性能优化**

### 摄像头优化
- 降低分辨率: 640x480
- 降低帧率: 15-20 FPS
- 使用硬件加速

### 语音优化
- 使用系统 say 命令 (更稳定)
- 避免频繁的语音播报
- 异步处理音频

### 内存优化
- 定期释放摄像头资源
- 使用垃圾回收
- 限制并发任务数量

## 📞 **技术支持**

### 日志文件
- 查看日志: `tail -f logs/luna.log`
- 错误日志: `grep ERROR logs/*.log`

### 调试模式
```bash
# 启用调试日志
export LUNA_DEBUG=1
python3 system_voice_demo.py
```

### 联系支持
- GitHub Issues: https://github.com/deanluan87/Luna-2/issues
- 项目文档: README.md
- 状态更新: PROJECT_STATUS.md

---

**部署完成后，运行 `python3 quick_test.py` 验证所有功能！** 🎉
