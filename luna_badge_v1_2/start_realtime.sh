#!/usr/bin/env bash
# Luna Badge 真实链路实时推理服务启动脚本

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "========================================"
echo "🌙 Luna Badge 真实链路实时推理服务"
echo "========================================"
echo ""

# 检查依赖
echo "[1/3] 检查依赖..."
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "[WARN] FastAPI 未安装，正在安装..."
    pip3 install fastapi "uvicorn[standard]"
fi

if ! python3 -c "import ultralytics" 2>/dev/null; then
    echo "[WARN] ultralytics 未安装，正在安装..."
    pip3 install ultralytics
fi

echo "[INFO] ✅ 依赖检查完成"
echo ""

# 获取本机 IP
echo "[2/3] 获取本机 IP..."
LOCAL_IP=$(python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
print(s.getsockname()[0])
s.close()
" 2>/dev/null || echo "127.0.0.1")

echo "[INFO] 本机 IP: $LOCAL_IP"
echo ""

# 启动服务
echo "[3/3] 启动服务..."
echo ""
echo "📱 iPhone 访问地址:"
echo "  http://$LOCAL_IP:8899/"
echo ""
echo "📝 查看日志:"
echo "  tail -f realtime_server.log"
echo ""
echo "🛑 停止服务:"
echo "  pkill -f realtime_server.py"
echo ""
echo "========================================"
echo "按 Ctrl+C 停止服务器"
echo "========================================"
echo ""

python3 realtime_server.py --host 0.0.0.0 --port 8899 --model yolo11n.pt


