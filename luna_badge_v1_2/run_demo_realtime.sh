#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "============================================"
echo "🚀 Luna Badge v1.3.0 真实链路 Demo"
echo "============================================"
echo ""
echo ">>> 启动实时导航 Demo (YOLO11-tiny)..."
echo ""

# 检查摄像头是否可用
if command -v ffmpeg &> /dev/null; then
    echo "[INFO] 检测到 ffmpeg，摄像头应该可用"
else
    echo "[WARN] 未检测到 ffmpeg，摄像头可能不可用"
fi

echo ""
echo "提示："
echo "  - 按 Ctrl+C 退出"
echo "  - 使用 --show 参数可以显示调试画面"
echo "  - 使用 --camera N 指定摄像头设备索引"
echo ""

python3 demo_realtime_navigation.py "$@"

















