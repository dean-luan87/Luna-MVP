#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "============================================"
echo "🚀 Luna Badge 真实链路性能测试"
echo "============================================"
echo ""

echo "=== [1] 单次链路 Benchmark（真实链路，带 A-G 分段）==="
python3 benchmarks/benchmark_full_realtime.py --runs 10 --target 250.0

echo ""
echo "=== [2] 并发压测（真实链路，60s / 4 并发）==="
python3 benchmarks/stress_full_realtime.py --duration 60 --concurrency 4 --target 250.0

echo ""
echo "============================================"
echo "✅ 完成"
echo "============================================"
echo ""
echo "📊 详细报告:"
echo "  - test_reports/benchmark_full_realtime_report.json"
echo "  - test_reports/stress_full_realtime_report.json"
echo "  - test_reports/benchmark_full_realtime_log.json (历史记录)"







