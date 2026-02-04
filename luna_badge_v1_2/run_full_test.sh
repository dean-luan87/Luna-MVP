#!/bin/bash
# -*- coding: utf-8 -*-
"""
一键集成测试脚本
启动主程序并监控日志
"""

echo "===== 清理历史进程 ====="
pkill -f "python3 main.py" 2>/dev/null
pkill -f "say" 2>/dev/null
rm -f /tmp/luna_badge_main.lock 2>/dev/null
sleep 1

echo "===== 启动主程序 ====="
cd "$(dirname "$0")"
python3 main.py > logs/full_test_main.log 2>&1 &
MAIN_PID=$!

echo "主程序 PID = $MAIN_PID"
echo "等待系统初始化..."
sleep 3

echo "===== 检查主程序状态 ====="
if ps -p $MAIN_PID > /dev/null 2>&1; then
    echo "✅ 主程序运行中 (PID: $MAIN_PID)"
else
    echo "❌ 主程序启动失败"
    echo "查看日志："
    tail -20 logs/full_test_main.log
    exit 1
fi

echo ""
echo "===== 实时日志跟踪（按 Ctrl+C 停止） ====="
tail -f logs/full_test_main.log
