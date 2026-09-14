#!/usr/bin/env bash
# Model Test Lens — 固定本地服务入口（端口 8765，勿改）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PORT=8765
URL="http://localhost:${PORT}"

if lsof -nP -iTCP:"${PORT}" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Luna Model Test Lens 已在运行"
  echo "  固定地址: ${URL}"
  echo "  目录: ${ROOT}"
  exit 0
fi

echo "Luna Model Test Lens"
echo "  固定地址: ${URL}"
echo "  目录: ${ROOT}"
echo "  按 Ctrl+C 停止"
exec python3 -m http.server "${PORT}" --directory "${ROOT}"
