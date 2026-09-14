#!/bin/bash
# Phase4-MVP 最小验收：PHASE3_PRODUCTION_RECIPE_v1.1 + stress pulse/sustain + det=3，唯一新增开启 modulation。
# 跑三 seed 42/123/777，每 seed 跑完立刻 monitor_personality_health，最后汇总 3 行表。
# 可选：bash tools/run_d1_phase4_mvp_seeds.sh 42 --lam 0.25  只跑 seed42、指定 λ，输出到 phase4_lam_sweep/lam_0.25。

set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_ROOT="$ROOT/outputs/d1_runs/phase4_mvp_seeds"
LAM_SWEEP_ROOT="$ROOT/outputs/d1_runs/phase4_lam_sweep"
export PYTHONHASHSEED=0
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

SEED_ARG="${1:-all}"
LAM_ARG=""
if [ "$2" = "--lam" ] && [ -n "${3:-}" ]; then
  LAM_ARG="$3"
fi

if [ -n "$LAM_ARG" ]; then
  # 单点 λ 扫描：只跑一个 seed，固定 run_dir，便于补扫上界
  SEEDS=("${SEED_ARG:-42}")
  RUN_DIR="$LAM_SWEEP_ROOT/lam_$LAM_ARG"
  mkdir -p "$LAM_SWEEP_ROOT"
  echo "=== Phase4 seed=${SEEDS[0]} lam=$LAM_ARG → $RUN_DIR ==="
  python3 "$ROOT/tools/run_d1_tournament.py" \
    --dual-channel --determinism-check 3 \
    --modulation-v1 --modulation-lam "$LAM_ARG" \
    --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
    --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
    --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
    --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
    --regular-suite library_store/v1.1/golden_stress_v2 \
    --n-candidates 60 --seed "${SEEDS[0]}" \
    --out-dir "$RUN_DIR" --no-ts --mode recompute \
    --phase3-mode convergent \
    --converge-exploit-ratio 0.85 --converge-peak-hold-fixed 3 \
    --converge-alpha-mean 0.696 --converge-alpha-std 0.013 --converge-alpha-min 0.65 --converge-alpha-max 0.73 \
    --converge-decay-mean 0.869 --converge-decay-std 0.004 --converge-decay-min 0.86 --converge-decay-max 0.88 \
    --converge-explore-alpha-min 0.69 --converge-explore-alpha-max 0.72 \
    --converge-explore-decay-min 0.865 --converge-explore-decay-max 0.885
  echo "=== health monitor $RUN_DIR ==="
  python3 "$ROOT/tools/monitor_personality_health.py" "$RUN_DIR" || true
  hp="$RUN_DIR/health_report.json"
  echo ""
  echo "=== 单点 λ=$LAM_ARG (seed ${SEEDS[0]}) ==="
  printf "%-6s %-4s %-8s %-14s %-10s %-8s\n" "lam" "det" "eg" "overreact_rate" "alpha_p90" "champion_vol"
  if [ -f "$hp" ]; then
    det=$(python3 -c "import json; d=json.load(open('$hp')); print('PASS' if d.get('determinism_pass') else 'FAIL')" 2>/dev/null || echo "?")
    eg=$(python3 -c "import json; d=json.load(open('$hp')); v=d.get('stress',{}).get('early_gain_mean'); print(round(v,4) if v is not None else '—')" 2>/dev/null || echo "—")
    over=$(python3 -c "import json; d=json.load(open('$hp')); v=d.get('overreact_rate'); print(v if v is not None else '—')" 2>/dev/null || echo "—")
    p90=$(python3 -c "import json; d=json.load(open('$hp')); v=(d.get('alpha_eff_stats') or {}).get('p90'); print(v if v is not None else '—')" 2>/dev/null || echo "—")
    vol=$(python3 -c "import json; d=json.load(open('$hp')); v=d.get('champion_vol'); print(round(v,4) if v is not None else '—')" 2>/dev/null || echo "—")
    printf "%-6s %-4s %-8s %-14s %-10s %-8s\n" "$LAM_ARG" "$det" "$eg" "$over" "$p90" "$vol"
  fi
  exit 0
fi

if [ "$SEED_ARG" = "all" ]; then
  SEEDS=(42 123 777)
else
  SEEDS=("$SEED_ARG")
fi

mkdir -p "$OUT_ROOT"
RUN_DIRS=()

for seed in "${SEEDS[@]}"; do
  echo "=== Phase4-MVP (modulation-v1) seed $seed ==="
  python3 "$ROOT/tools/run_d1_tournament.py" \
    --dual-channel --determinism-check 3 \
    --modulation-v1 --modulation-lam 0.10 \
    --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
    --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
    --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
    --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
    --regular-suite library_store/v1.1/golden_stress_v2 \
    --n-candidates 60 --seed "$seed" \
    --out-dir "$OUT_ROOT" --mode recompute \
    --phase3-mode convergent \
    --converge-exploit-ratio 0.85 --converge-peak-hold-fixed 3 \
    --converge-alpha-mean 0.696 --converge-alpha-std 0.013 --converge-alpha-min 0.65 --converge-alpha-max 0.73 \
    --converge-decay-mean 0.869 --converge-decay-std 0.004 --converge-decay-min 0.86 --converge-decay-max 0.88 \
    --converge-explore-alpha-min 0.69 --converge-explore-alpha-max 0.72 \
    --converge-explore-decay-min 0.865 --converge-explore-decay-max 0.885
  LATEST=$(ls -t "$OUT_ROOT" | head -1)
  RUN_DIR="$OUT_ROOT/$LATEST"
  RUN_DIRS+=("$RUN_DIR")
  echo "=== health monitor $RUN_DIR ==="
  python3 "$ROOT/tools/monitor_personality_health.py" "$RUN_DIR" || true
done

# 汇总 3 行表：seed / det / eg / overreact_rate / alpha_p90 / champion_id
echo ""
echo "=== Phase4-MVP 汇总表 (seed / det / eg / overreact_rate / alpha_p90 / champion_id) ==="
printf "| %-6s | %-4s | %-8s | %-14s | %-8s | %-20s |\n" "seed" "det" "eg" "overreact_rate" "alpha_p90" "champion_id"
echo "|--------|------|----------|----------------|----------|----------------------|"
for i in "${!SEEDS[@]}"; do
  seed="${SEEDS[$i]}"
  run_dir="${RUN_DIRS[$i]}"
  hp="$run_dir/health_report.json"
  if [ -f "$hp" ]; then
    det=$(python3 -c "import json; d=json.load(open('$hp')); print('PASS' if d.get('determinism_pass') else 'FAIL')" 2>/dev/null || echo "?")
    eg=$(python3 -c "import json; d=json.load(open('$hp')); v=d.get('stress',{}).get('early_gain_mean'); print(round(v,4) if v is not None else '—')" 2>/dev/null || echo "—")
    over=$(python3 -c "import json; d=json.load(open('$hp')); v=d.get('overreact_rate'); print(v if v is not None else '—')" 2>/dev/null || echo "—")
    p90=$(python3 -c "import json; d=json.load(open('$hp')); v=(d.get('alpha_eff_stats') or {}).get('p90'); print(v if v is not None else '—')" 2>/dev/null || echo "—")
    cid=$(python3 -c "import json; d=json.load(open('$hp')); v=d.get('champion_id'); print((v or '—')[:20])" 2>/dev/null || echo "—")
  else
    det="—"; eg="—"; over="—"; p90="—"; cid="—"
  fi
  printf "| %-6s | %-4s | %-8s | %-14s | %-8s | %-20s |\n" "$seed" "$det" "$eg" "$over" "$p90" "$cid"
done
