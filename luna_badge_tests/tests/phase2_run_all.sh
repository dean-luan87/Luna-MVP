#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORT_DIR="${ROOT_DIR}/test_reports"

mkdir -p "${REPORT_DIR}"

echo "=== Phase-2: 深度稳定性测试开始 ==="

echo "[1/2] 运行链路延迟测试 (phase2_latency_test.py)..."
python3 "${ROOT_DIR}/tests/phase2_latency_test.py"

echo "[2/2] 运行并发稳定性测试 (phase2_concurrency_test.py)..."
python3 "${ROOT_DIR}/tests/phase2_concurrency_test.py"

echo "=== Phase-2: 完成。结果已写入 test_reports/phase2_*.json / .csv ==="







