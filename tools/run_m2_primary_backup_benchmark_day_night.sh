#!/usr/bin/env bash
# M2 分时段抽测：连续跑 day → night 各一轮（默认各 25×4 次 API）。
#
# 前置（与 benchmark 脚本一致）：
#   export DASHSCOPE_API_KEY='...'
#   export LUNA_EXTERNAL_LLM_PROVIDER=qwen
#   unset LUNA_QWEN_REGION   # 北京控制台 Key 时保持默认中国区
#
# 可选：
#   export LUNA_QWEN_USE_PRIMARY_BACKUP=1   # 仅作记录习惯；benchmark 内已用主备 bundle
#   export LUNA_BENCH_ITERS=25              # 每时段迭代轮数（每轮 4 条 case）
#
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -z "${DASHSCOPE_API_KEY:-}" && -z "${LUNA_DASHSCOPE_API_KEY:-}" ]]; then
  echo "错误：请设置 DASHSCOPE_API_KEY 或 LUNA_DASHSCOPE_API_KEY。" >&2
  exit 2
fi

export LUNA_EXTERNAL_LLM_PROVIDER="${LUNA_EXTERNAL_LLM_PROVIDER:-qwen}"
ITERS="${LUNA_BENCH_ITERS:-25}"

echo "=========================================="
echo "M2 分时段 benchmark | iters/slot=${ITERS} | cwd=${ROOT}"
echo "=========================================="

echo ""
echo ">>> 时段 1: day"
LUNA_BENCH_TIME_SLOT=day LUNA_BENCH_ITERS="$ITERS" python3 tools/benchmark_qwen_long_voice_primary_backup_m2.py

echo ""
echo ">>> 时段 2: night"
LUNA_BENCH_TIME_SLOT=night LUNA_BENCH_ITERS="$ITERS" python3 tools/benchmark_qwen_long_voice_primary_backup_m2.py

echo ""
echo "完成。JSON 输出目录: ${ROOT}/logs/"
echo "文件名形如: benchmark_qwen_long_voice_primary_backup_m2_day_*.json"
echo "            benchmark_qwen_long_voice_primary_backup_m2_night_*.json"
ls -1t "${ROOT}/logs"/benchmark_qwen_long_voice_primary_backup_m2_*.json 2>/dev/null | head -4 || true
