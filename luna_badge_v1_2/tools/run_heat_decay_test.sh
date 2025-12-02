#!/bin/bash
# -*- coding: utf-8 -*-
#
# 热衰减测试启动脚本
#
# 功能：
# - 运行 10 分钟持续压测
# - 监控 CPU/GPU/内存使用率
# - 叠加实时性能延迟数据
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

DURATION=${DURATION:-600}      # 默认 10 分钟
INTERVAL=${INTERVAL:-10}
JSONL_LATEST=$(ls -t perf_logs/run_*.jsonl 2>/dev/null | head -n 1 || true)

# 压测命令（默认启动服务器，实际使用时可以改为其他压测命令）
STRESS_CMD=${STRESS_CMD:-""}

echo "============================================"
echo "  Luna Badge 热衰减测试"
echo "============================================"
echo "时长: ${DURATION}s（$(($DURATION / 60)) 分钟），采样间隔: ${INTERVAL}s"
if [ -n "$STRESS_CMD" ]; then
    echo "压测命令: ${STRESS_CMD}"
else
    echo "压测命令: 无（仅监控系统资源）"
fi
if [ -n "$JSONL_LATEST" ]; then
    echo "叠加延迟数据来源: $JSONL_LATEST"
else
    echo "未找到 run_*.jsonl，将只记录系统资源，不记录延迟。"
fi
echo "============================================"
echo ""

CMD="python3 scripts/heat_decay_test.py --duration ${DURATION} --interval ${INTERVAL}"
if [ -n "$STRESS_CMD" ]; then
    CMD="${CMD} --stress-cmd \"${STRESS_CMD}\""
fi
if [ -n "$JSONL_LATEST" ]; then
    CMD="${CMD} --jsonl ${JSONL_LATEST}"
fi

echo "执行: $CMD"
echo ""
eval $CMD


