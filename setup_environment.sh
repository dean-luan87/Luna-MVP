#!/bin/bash
# Luna-2 环境配置脚本

echo "🚀 Luna-2 环境配置开始..."

# 检查 Python 版本
echo "📋 检查 Python 版本..."
python3 --version

# 安装 Python 依赖
echo "📦 安装 Python 依赖..."
pip3 install opencv-python ultralytics edge-tts pyttsx3 openrouteservice requests

# 检查 OpenCV 安装
echo "🎥 检查 OpenCV..."
python3 -c "import cv2; print(f'OpenCV 版本: {cv2.__version__}')"

# 检查其他依赖
echo "🔍 检查依赖..."
python3 -c "
import sys
packages = ['ultralytics', 'edge_tts', 'pyttsx3', 'openrouteservice']
for pkg in packages:
    try:
        __import__(pkg)
        print(f'✅ {pkg} 已安装')
    except ImportError:
        print(f'❌ {pkg} 未安装')
"

# 设置环境变量提示
echo "🔧 环境变量配置提示:"
echo "export ORS_API_KEY='你的_OpenRouteService_API_密钥'"
echo "export GOOGLE_MAPS_API_KEY='你的_Google_Maps_API_密钥'"

echo "✅ 环境配置完成！"
echo "📝 请记得设置 API 密钥环境变量"
