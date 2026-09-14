#!/bin/bash
# Phase3 Step3 GradualShift：把 exploit 分布向 0.70/0.87 赢家带渐进迁移
# exploit_ratio 0.80, alpha_mean 0.685, decay_mean 0.878
# explore 收窄到 [0.68,0.72]×[0.865,0.885] 巡航带

export PYTHONHASHSEED=0
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

SEED="${1:-42}"
if [ "$SEED" = "all" ]; then
  for s in 42 123 777 888 2024; do
    echo "=== Step3 GradualShift seed $s ==="
    python3 tools/run_d1_tournament.py \
      --dual-channel --determinism-check 1 \
      --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
      --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
      --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
      --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
      --regular-suite library_store/v1.1/golden_stress_v2 \
      --n-candidates 80 --seed "$s" \
      --out-dir outputs/d1_runs/phase3_step3_gradualshift --mode recompute \
      --phase3-mode convergent \
      --converge-exploit-ratio 0.80 \
      --converge-peak-hold-fixed 3 \
      --converge-alpha-mean 0.685 --converge-alpha-std 0.015 --converge-alpha-min 0.64 --converge-alpha-max 0.72 \
      --converge-decay-mean 0.878 --converge-decay-std 0.007 --converge-decay-min 0.86 --converge-decay-max 0.90 \
      --converge-explore-alpha-min 0.68 --converge-explore-alpha-max 0.72 \
      --converge-explore-decay-min 0.865 --converge-explore-decay-max 0.885
  done
else
  python3 tools/run_d1_tournament.py \
    --dual-channel --determinism-check 1 \
    --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
    --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
    --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
    --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
    --regular-suite library_store/v1.1/golden_stress_v2 \
    --n-candidates 80 --seed "$SEED" \
    --out-dir outputs/d1_runs/phase3_step3_gradualshift --mode recompute \
    --phase3-mode convergent \
    --converge-exploit-ratio 0.80 \
    --converge-peak-hold-fixed 3 \
    --converge-alpha-mean 0.685 --converge-alpha-std 0.015 --converge-alpha-min 0.64 --converge-alpha-max 0.72 \
    --converge-decay-mean 0.878 --converge-decay-std 0.007 --converge-decay-min 0.86 --converge-decay-max 0.90 \
    --converge-explore-alpha-min 0.68 --converge-explore-alpha-max 0.72 \
    --converge-explore-decay-min 0.865 --converge-explore-decay-max 0.885
fi
