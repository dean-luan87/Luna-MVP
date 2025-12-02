#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

VENV_DIR="$ROOT_DIR/.venv_realtime"

echo "[1/4] 创建 / 激活虚拟环境 ..."
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

echo "[2/4] 安装依赖 ..."
pip install --upgrade pip >/dev/null
pip install -r backend/requirements.txt >/dev/null

echo "[2.5/4] 检查 SSL 证书 ..."
if [ ! -f "$ROOT_DIR/ssl_certs/cert.pem" ] || [ ! -f "$ROOT_DIR/ssl_certs/key.pem" ]; then
  echo "   未找到 SSL 证书，生成中..."
  bash "$ROOT_DIR/scripts/generate_ssl_cert.sh"
fi

echo "[3/4] 启动后端（YOLO WebSocket 服务） ..."
python3 backend/server.py 5001 &
SERVER_PID=$!
sleep 2

echo "[4/4] 启动前端静态服务器（H5 页面，HTTPS） ..."
python3 scripts/https_server.py 8081 &
FRONT_PID=$!
sleep 2

cd "$ROOT_DIR"

IP_ADDR=$(hostname -I 2>/dev/null | awk '{print $1}')
if [ -z "$IP_ADDR" ]; then
  IP_ADDR=$(ipconfig getifaddr en0 2>/dev/null || echo "你的电脑IP")
fi

# 检查是否使用 HTTPS
if [ -f "$ROOT_DIR/ssl_certs/cert.pem" ] && [ -f "$ROOT_DIR/ssl_certs/key.pem" ]; then
  PROTOCOL="https"
  WS_PROTOCOL="wss"
  HTTPS_NOTE="✅ 使用 HTTPS（支持摄像头访问）"
else
  PROTOCOL="http"
  WS_PROTOCOL="ws"
  HTTPS_NOTE="⚠️  使用 HTTP（iOS Safari 无法访问摄像头，请生成 SSL 证书）"
fi

echo ""
echo "==========================================="
echo " Luna Realtime H5 Lab 已启动"
echo " $HTTPS_NOTE"
echo ""
echo " 前端访问地址 (iPhone Safari)："
echo "   $PROTOCOL://$IP_ADDR:8081"
echo ""
echo " WebSocket 推理地址："
echo "   $WS_PROTOCOL://$IP_ADDR:5001/ws"
echo ""
if [ "$PROTOCOL" = "http" ]; then
  echo " ⚠️  摄像头访问提示："
  echo "    iOS Safari 需要 HTTPS 才能访问摄像头"
  echo "    运行以下命令生成 SSL 证书："
  echo "    bash scripts/generate_ssl_cert.sh"
  echo ""
fi
echo "==========================================="
echo " 按 Ctrl+C 停止全部进程。"

trap "echo '停止中...'; kill $SERVER_PID $FRONT_PID 2>/dev/null || true; exit 0" SIGINT SIGTERM

wait

