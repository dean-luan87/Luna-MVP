#!/bin/bash
# Phase4 跨 seed 稳定性快扫：固定 λ，对多个 seed 各跑一次 tournament（det=1 或 3），输出到 phase4_seed_sweep/lam_X/seed_Y。
# 用法:
#   bash tools/run_d1_phase4_seed_sweep.sh --lam 0.10 --seeds "42 123 777 888 2024 31415 2718 999 1001 4096" --det 1
#   bash tools/run_d1_phase4_seed_sweep.sh --lam 0.40 --seeds "42 123 777" --det 3 --regular-suite high_burst_v1
# 跑完对 sweep 目录跑 monitor 与汇总:
#   bash tools/run_monitor_health_on_runs.sh outputs/d1_runs/phase4_seed_sweep/lam_0.10 outputs/d1_runs/phase4_seed_sweep/lam_0.40
#   python3 tools/summarize_phase4_seed_sweep.py outputs/d1_runs/phase4_seed_sweep

set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SWEEP_ROOT="${SWEEP_ROOT:-$ROOT/outputs/d1_runs/phase4_seed_sweep}"
export PYTHONHASHSEED=0
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

LAM="0.10"
SEEDS="42 123 777 888 2024 31415 2718 999 1001 4096"
DET=1
REGULAR_SUITE="library_store/v1.1/golden_stress_v2"
while [ $# -gt 0 ]; do
  case "$1" in
    --lam)           LAM="$2"; shift 2 ;;
    --seeds)         SEEDS="$2"; shift 2 ;;
    --det)           DET="$2"; shift 2 ;;
    --regular-suite) REGULAR_SUITE="$2"; shift 2 ;;
    *)               echo "Unknown option: $1"; exit 1 ;;
  esac
done

mkdir -p "$SWEEP_ROOT"
LAM_DIR="$SWEEP_ROOT/lam_$LAM"
mkdir -p "$LAM_DIR"

for seed in $SEEDS; do
  RUN_DIR="$LAM_DIR/seed_$seed"
  echo "=== Phase4 lam=$LAM seed=$seed det=$DET -> $RUN_DIR ==="
  python3 "$ROOT/tools/run_d1_tournament.py" \
    --dual-channel --determinism-check "$DET" \
    --modulation-v1 --modulation-lam "$LAM" \
    --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
    --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
    --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
    --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
    --regular-suite "$REGULAR_SUITE" \
    --n-candidates 60 --seed "$seed" \
    --out-dir "$RUN_DIR" --no-ts --mode recompute \
    --phase3-mode convergent \
    --converge-exploit-ratio 0.85 --converge-peak-hold-fixed 3 \
    --converge-alpha-mean 0.696 --converge-alpha-std 0.013 --converge-alpha-min 0.65 --converge-alpha-max 0.73 \
    --converge-decay-mean 0.869 --converge-decay-std 0.004 --converge-decay-min 0.86 --converge-decay-max 0.88 \
    --converge-explore-alpha-min 0.69 --converge-explore-alpha-max 0.72 \
    --converge-explore-decay-min 0.865 --converge-explore-decay-max 0.885
done
echo "=== sweep done: lam=$LAM seeds=$SEEDS -> $LAM_DIR ==="
