#!/usr/bin/env bash
set -e

APP_MODULE="realtime_server:app"
HOST="0.0.0.0"
PORT="5001"
LOG_DIR="logs"
LOG_FILE="${LOG_DIR}/realtime_server_$(date +%Y%m%d_%H%M%S).log"

mkdir -p "${LOG_DIR}"

echo "========================================"
echo " Luna Badge v1.3.0 Realtime OP 一键启动"
echo "========================================"
echo "[1/4] 启动后端服务: ${APP_MODULE} on ${HOST}:${PORT}"
echo "      日志: ${LOG_FILE}"
echo

# 后台启动 uvicorn（使用 python3 -m 方式）
python3 -m uvicorn "${APP_MODULE}" \
  --host "${HOST}" \
  --port "${PORT}" \
  --reload \
  > "${LOG_FILE}" 2>&1 &

SERVER_PID=$!

sleep 2

if ! ps -p ${SERVER_PID} > /dev/null 2>&1; then
  echo "❌ 后端启动失败，请查看日志: ${LOG_FILE}"
  exit 1
fi

echo "✅ 后端已启动，PID=${SERVER_PID}"
echo

# 简单健康检查
echo "[2/4] 健康检查 /health ..."
HEALTH_URL="http://127.0.0.1:${PORT}/health"
HEALTH_RESP=$(curl -s --max-time 5 "${HEALTH_URL}" || true)

if echo "${HEALTH_RESP}" | grep -q '"status": *"ok"'; then
  echo "✅ 健康检查通过: ${HEALTH_RESP}"
else
  echo "⚠️  健康检查异常，响应: ${HEALTH_RESP}"
fi
echo

# 打印访问地址
LOCAL_URL="http://127.0.0.1:${PORT}/"
LAN_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
if [ -z "$LAN_IP" ]; then
  LAN_IP=$(ipconfig getifaddr en0 2>/dev/null || echo "")
fi

# 检测位置（公司/家庭）
LOCATION=""
if [ "$LAN_IP" = "10.183.232.224" ]; then
  LOCATION="公司"
elif [ "$LAN_IP" = "192.168.3.57" ]; then
  LOCATION="家庭"
fi

LAN_URL=""
if [ -n "${LAN_IP}" ]; then
  LAN_URL="http://${LAN_IP}:${PORT}/"
fi

echo "[3/4] 访问地址："
echo "   本机浏览器: ${LOCAL_URL}"
if [ -n "${LAN_URL}" ]; then
  if [ -n "${LOCATION}" ]; then
    echo "   局域网(iPhone) [${LOCATION}]: ${LAN_URL}"
  else
    echo "   局域网(iPhone): ${LAN_URL}"
  fi
fi
echo

# 是否自动打开浏览器（macOS 支持）
if command -v open >/dev/null 2>&1; then
  echo "[4/4] 尝试在本机打开浏览器..."
  open "${LOCAL_URL}" || true
fi

echo
echo "=== 运行中 ==="
echo "日志: tail -f ${LOG_FILE}"
echo "停止服务: kill ${SERVER_PID}"
echo

