#!/bin/bash
# 对指定目录下所有含 rank_report.json 的子目录执行 monitor_personality_health.py（不重跑 tournament）。
# 用法: bash tools/run_monitor_health_on_runs.sh [--grade smoke|release] [目录1 目录2 ...]
# 无参时默认: grade=smoke, 目录=outputs/d1_runs/phase4_mvp_seeds
# 例: bash tools/run_monitor_health_on_runs.sh outputs/d1_runs/phase4_seed_sweep/lam_0.10 outputs/d1_runs/phase4_seed_sweep/lam_0.40
# 例: bash tools/run_monitor_health_on_runs.sh --grade release outputs/d1_runs/phase4_seed_sweep/lam_0.10 outputs/d1_runs/phase4_seed_sweep/lam_0.40

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GRADE="smoke"
while [ $# -gt 0 ]; do
  case "$1" in
    --grade) GRADE="$2"; shift 2 ;;
    *)       break ;;
  esac
done
if [ $# -eq 0 ]; then
  set -- "$ROOT/outputs/d1_runs/phase4_mvp_seeds"
fi
for BASE in "$@"; do
  if [ ! -d "$BASE" ]; then
    echo "目录不存在: $BASE"
    continue
  fi
  for d in "$BASE"/*/; do
    [ -f "${d}rank_report.json" ] || continue
    echo "=== health monitor (grade=$GRADE) $d ==="
    python3 "$ROOT/tools/monitor_personality_health.py" --grade "$GRADE" "$d"
  done
done
