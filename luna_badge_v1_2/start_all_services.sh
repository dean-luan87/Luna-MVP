#!/usr/bin/env bash
# Luna Badge 手机桥接服务完整启动脚本（HTTP + WebSocket）

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "========================================"
echo "🌙 Luna Badge Mobile Bridge Services"
echo "========================================"
echo ""

# 检查依赖
echo "[1/4] 检查依赖..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "[WARN] Flask 未安装，正在安装..."
    pip3 install flask flask-cors
fi

if ! python3 -c "import websockets" 2>/dev/null; then
    echo "[WARN] websockets 未安装，正在安装..."
    pip3 install websockets
fi

if ! python3 -c "import PIL" 2>/dev/null; then
    echo "[WARN] Pillow 未安装，正在安装..."
    pip3 install pillow
fi

echo "[INFO] ✅ 依赖检查完成"
echo ""

# 获取本机 IP
echo "[2/4] 获取本机 IP..."
LOCAL_IP=$(python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
print(s.getsockname()[0])
s.close()
" 2>/dev/null || echo "127.0.0.1")

echo "[INFO] 本机 IP: $LOCAL_IP"
echo ""

# 提示信息
echo "[3/4] 服务信息:"
echo "  HTTP 服务: http://$LOCAL_IP:8899"
echo "  WebSocket: ws://$LOCAL_IP:8898/ws"
echo "  手机端页面: http://$LOCAL_IP:8899/static/mobile_client.html"
echo ""

echo "[4/4] 启动服务..."
echo ""
echo "⚠️  注意：需要同时运行两个服务"
echo ""
echo "方式一：使用两个终端"
echo "  终端1: python3 mobile_bridge_server.py"
echo "  终端2: python3 ws_server.py"
echo ""
echo "方式二：后台运行"
echo "  python3 mobile_bridge_server.py > http.log 2>&1 &"
echo "  python3 ws_server.py > ws.log 2>&1 &"
echo ""
echo "========================================"
echo "按 Enter 启动 HTTP 服务（Ctrl+C 停止）..."
echo "========================================"
read

python3 mobile_bridge_server.py

















