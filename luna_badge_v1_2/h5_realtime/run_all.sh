#!/bin/bash
# Luna Badge H5 实时测试 - 一键启动脚本

set -e

echo "============================================"
echo "  Luna Badge H5 实时测试系统"
echo "============================================"
echo ""

# 获取本机 IP
LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}' | head -n 1)
if [ -z "$LOCAL_IP" ]; then
    LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || echo "127.0.0.1")
fi

echo "📦 步骤 1: 检查依赖..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

echo "📦 激活虚拟环境..."
source venv/bin/activate

echo "📦 安装依赖..."
pip install -q flask flask-sock ultralytics pillow

echo ""
echo "============================================"
echo "📦 步骤 2: 启动服务器..."
echo "============================================"
echo ""

# 启动后端服务器
echo "🚀 启动推理服务器 (端口 5000)..."
python3 server.py > server.log 2>&1 &
SERVER_PID=$!
echo "   后端 PID: $SERVER_PID"
echo "   日志文件: server.log"

# 等待服务器启动
sleep 3

# 检查服务器是否启动成功
if ! ps -p $SERVER_PID > /dev/null; then
    echo "❌ 服务器启动失败，请查看 server.log"
    exit 1
fi

echo ""
echo "============================================"
echo "✅ 服务器启动成功！"
echo "============================================"
echo ""
echo "📱 iPhone 访问地址:"
echo "   http://${LOCAL_IP}:5000"
echo ""
echo "🔌 WebSocket 地址:"
echo "   ws://${LOCAL_IP}:5000/ws"
echo ""
echo "📊 查看日志:"
echo "   tail -f server.log"
echo ""
echo "🛑 停止服务器:"
echo "   kill $SERVER_PID"
echo ""
echo "============================================"
echo ""

# 保持脚本运行
wait $SERVER_PID
















