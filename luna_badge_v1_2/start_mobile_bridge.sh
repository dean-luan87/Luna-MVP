#!/usr/bin/env bash
# Luna Badge 手机桥接服务启动脚本

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "========================================"
echo "🌙 Luna Badge Mobile Bridge Server"
echo "========================================"
echo ""

# 检查依赖
echo "[1/3] 检查依赖..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "[WARN] Flask 未安装，正在安装..."
    pip3 install flask flask-cors
fi

if ! python3 -c "import PIL" 2>/dev/null; then
    echo "[WARN] Pillow 未安装，正在安装..."
    pip3 install pillow
fi

echo "[INFO] ✅ 依赖检查完成"
echo ""

# 启动服务器
echo "[2/3] 启动服务器..."
echo ""
python3 mobile_bridge_server.py






