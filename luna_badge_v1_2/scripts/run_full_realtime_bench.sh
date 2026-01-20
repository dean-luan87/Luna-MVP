#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p perf_logs

echo "========================================"
echo "🚀 Luna Badge 真实链路性能测试"
echo "========================================"
echo ""

echo "========================================"
echo " 1) 单次全链路实时 Benchmark"
echo "========================================"
python3 tests/benchmark_full_realtime.py || {
  echo "[ERROR] benchmark_full_realtime 失败"
  exit 1
}

echo ""
echo "========================================"
echo " 2) 压力测试 (60s, 4 线程)"
echo "========================================"

export LUNA_STRESS_DURATION=60
export LUNA_STRESS_THREADS=4

python3 tests/stress_full_realtime.py || {
  echo "[ERROR] stress_full_realtime 失败"
  exit 1
}

echo ""
echo "========================================"
echo "✅ 完成。报告路径：perf_logs/"
echo "  - full_realtime_benchmark.json"
echo "  - full_realtime_stress_report.json"
echo "  - full_realtime_stress_samples.csv"
echo "========================================"

















