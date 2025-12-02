#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "============================================"
echo "🚀 Luna Badge 性能测试套件"
echo "============================================"
echo ""

echo "=== 1. YOLO 模型对比 Benchmark ==="
python3 benchmarks/benchmark_yolo_models.py

echo ""
echo "=== 2. 链路压测（60秒，并发4） ==="
python3 benchmarks/stress_realtime_pipeline.py --duration 60 --concurrency 4

echo ""
echo "=== 3. 生成性能 Dashboard ==="
python3 benchmarks/perf_dashboard.py

echo ""
echo "============================================"
echo "✅ 全部完成！"
echo "============================================"
echo ""
echo "📊 查看 Dashboard:"
echo "   打开 perf_logs/perf_dashboard.html"
echo ""
echo "📁 数据文件:"
echo "   - perf_logs/yolo_model_benchmark.json"
echo "   - perf_logs/stress_realtime_result.json"
echo "   - perf_logs/perf_dashboard.html"



