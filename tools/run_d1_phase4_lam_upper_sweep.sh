#!/bin/bash
# Phase4 λ 上界扫描：seed42 下 lam ∈ {0.25, 0.30, 0.40}，找到第一次红灯（det FAIL / overreact>0.60 / miss_rate>0 / champion_vol>0.01）。
# 跑完输出表：lam  det  early_gain  overreact_rate  alpha_p90  champion_vol

set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LAMS="0.25 0.30 0.40"
SEED=42

for lam in $LAMS; do
  bash "$ROOT/tools/run_d1_phase4_mvp_seeds.sh" "$SEED" --lam "$lam"
done

echo ""
echo "=== Phase4 λ 上界汇总 (lam / det / eg / overreact_rate / alpha_p90 / champion_vol) ==="
printf "%-6s %-4s %-8s %-14s %-10s %-10s\n" "lam" "det" "eg" "overreact_rate" "alpha_p90" "champion_vol"
echo "------ ---- -------- -------------- ---------- ----------"
for lam in $LAMS; do
  hp="$ROOT/outputs/d1_runs/phase4_lam_sweep/lam_$lam/health_report.json"
  if [ -f "$hp" ]; then
    det=$(python3 -c "import json; d=json.load(open('$hp')); print('PASS' if d.get('determinism_pass') else 'FAIL')" 2>/dev/null || echo "?")
    eg=$(python3 -c "import json; d=json.load(open('$hp')); v=d.get('stress',{}).get('early_gain_mean'); print(round(v,4) if v is not None else '—')" 2>/dev/null || echo "—")
    over=$(python3 -c "import json; d=json.load(open('$hp')); v=d.get('overreact_rate'); print(v if v is not None else '—')" 2>/dev/null || echo "—")
    p90=$(python3 -c "import json; d=json.load(open('$hp')); v=(d.get('alpha_eff_stats') or {}).get('p90'); print(v if v is not None else '—')" 2>/dev/null || echo "—")
    vol=$(python3 -c "import json; d=json.load(open('$hp')); v=d.get('champion_vol'); print(round(v,4) if v is not None else '—')" 2>/dev/null || echo "—")
  else
    det="—"; eg="—"; over="—"; p90="—"; vol="—"
  fi
  printf "%-6s %-4s %-8s %-14s %-10s %-10s\n" "$lam" "$det" "$eg" "$over" "$p90" "$vol"
done
