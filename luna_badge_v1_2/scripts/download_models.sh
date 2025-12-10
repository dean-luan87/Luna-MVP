#!/bin/bash
# 下载 YOLO 模型文件

set -e

MODELS_DIR="models"
mkdir -p "$MODELS_DIR"

echo "==========================================="
echo "  YOLO 模型下载工具"
echo "==========================================="
echo ""

# YOLO11-nano ONNX 模型
echo "[1/2] 下载 YOLO11-nano 模型..."
echo "  目标: $MODELS_DIR/yolo11_nav_nano_v1.onnx"
echo ""
echo "  ⚠️  请提供 YOLO11-nano ONNX 模型的下载 URL"
echo "  或者手动将模型文件放置到: $MODELS_DIR/yolo11_nav_nano_v1.onnx"
echo ""

# YOLO11-tiny ONNX 模型
echo "[2/2] 下载 YOLO11-tiny 模型..."
echo "  目标: $MODELS_DIR/yolo11_nav_tiny_v1.onnx"
echo ""
echo "  ⚠️  请提供 YOLO11-tiny ONNX 模型的下载 URL"
echo "  或者手动将模型文件放置到: $MODELS_DIR/yolo11_nav_tiny_v1.onnx"
echo ""

echo "==========================================="
echo "  使用说明："
echo "==========================================="
echo ""
echo "1. 编辑此脚本，填入模型下载 URL："
echo "   curl -L \"<YOUR_NANO_URL>\" -o $MODELS_DIR/yolo11_nav_nano_v1.onnx"
echo "   curl -L \"<YOUR_TINY_URL>\" -o $MODELS_DIR/yolo11_nav_tiny_v1.onnx"
echo ""
echo "2. 或者手动下载模型文件到 $MODELS_DIR/ 目录"
echo ""
echo "3. 验证模型文件："
echo "   ls -lh $MODELS_DIR/*.onnx"
echo ""





