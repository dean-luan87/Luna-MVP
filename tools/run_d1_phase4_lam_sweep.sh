#!/bin/bash
# Phase4 λ 敏感性扫描：单变量 lam ∈ {0.00, 0.05, 0.10, 0.15, 0.20}，单 seed 42。
# 目标：量化调制强度对系统形态的影响，找到稳定带宽。
# 输出表：lam  early_gain  overreact_rate  alpha_p90  det

set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SWEEP_ROOT="$ROOT/outputs/d1_runs/phase4_lam_sweep"
export PYTHONHASHSEED=0
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

LAMS="0.00 0.05 0.10 0.15 0.20"
SEED=42

mkdir -p "$SWEEP_ROOT"

for lam in $LAMS; do
  run_dir="$SWEEP_ROOT/lam_$lam"
  echo "=== Phase4 lam=$lam seed=$SEED → $run_dir ==="
  python3 "$ROOT/tools/run_d1_tournament.py" \
    --dual-channel --determinism-check 3 \
    --modulation-v1 --modulation-lam "$lam" \
    --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
    --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
    --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
    --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
    --regular-suite library_store/v1.1/golden_stress_v2 \
    --n-candidates 60 --seed "$SEED" \
    --out-dir "$run_dir" --no-ts --mode recompute \
    --phase3-mode convergent \
    --converge-exploit-ratio 0.85 --converge-peak-hold-fixed 3 \
    --converge-alpha-mean 0.696 --converge-alpha-std 0.013 --converge-alpha-min 0.65 --converge-alpha-max 0.73 \
    --converge-decay-mean 0.869 --converge-decay-std 0.004 --converge-decay-min 0.86 --converge-decay-max 0.88 \
    --converge-explore-alpha-min 0.69 --converge-explore-alpha-max 0.72 \
    --converge-explore-decay-min 0.865 --converge-explore-decay-max 0.885
  echo "=== health monitor $run_dir ==="
  python3 "$ROOT/tools/monitor_personality_health.py" "$run_dir" --json-only >/dev/null || true
done

echo ""
echo "=== Phase4 λ 敏感性表 (lam / early_gain / overreact_rate / alpha_p90 / det) ==="
printf "%-6s %-12s %-14s %-10s %-6s\n" "lam" "early_gain" "overreact_rate" "alpha_p90" "det"
echo "------ ------------ -------------- ---------- ------"
for lam in $LAMS; do
  hp="$SWEEP_ROOT/lam_$lam/health_report.json"
  if [ -f "$hp" ]; then
    eg=$(python3 -c "import json; d=json.load(open('$hp')); v=d.get('stress',{}).get('early_gain_mean'); print(round(v,4) if v is not None else '—')" 2>/dev/null || echo "—")
    over=$(python3 -c "import json; d=json.load(open('$hp')); v=d.get('overreact_rate'); print(v if v is not None else '—')" 2>/dev/null || echo "—")
    p90=$(python3 -c "import json; d=json.load(open('$hp')); v=(d.get('alpha_eff_stats') or {}).get('p90'); print(v if v is not None else '—')" 2>/dev/null || echo "—")
    det=$(python3 -c "import json; d=json.load(open('$hp')); print('PASS' if d.get('determinism_pass') else 'FAIL')" 2>/dev/null || echo "?")
  else
    eg="—"; over="—"; p90="—"; det="—"
  fi
  printf "%-6s %-12s %-14s %-10s %-6s\n" "$lam" "$eg" "$over" "$p90" "$det"
done
