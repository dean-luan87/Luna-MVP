#!/bin/bash
# Step 2 (squeeze)：收方差，在 m66 基础上
# alpha_std 0.02→0.015, decay_std 0.01→0.007
# alpha_mean=0.66, decay_mean=0.888 保持

export PYTHONHASHSEED=0
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

SEED="${1:-42}"
if [ "$SEED" = "all" ]; then
  for s in 42 123 777; do
    echo "=== squeeze seed $s ==="
    python3 tools/run_d1_tournament.py \
      --dual-channel --determinism-check 1 \
      --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
      --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
      --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
      --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
      --regular-suite library_store/v1.1/golden_stress_v2 \
      --n-candidates 80 --seed "$s" \
      --out-dir outputs/d1_runs/phase3_convergent_r085_m66_squeezed --mode recompute \
      --phase3-mode convergent \
      --converge-exploit-ratio 0.85 \
      --converge-peak-hold-fixed 3 \
      --converge-alpha-mean 0.66 --converge-alpha-std 0.015 --converge-alpha-min 0.60 --converge-alpha-max 0.68 \
      --converge-decay-mean 0.888 --converge-decay-std 0.007 --converge-decay-min 0.88 --converge-decay-max 0.92 \
      --converge-explore-alpha-min 0.58 --converge-explore-alpha-max 0.72 \
      --converge-explore-decay-min 0.87 --converge-explore-decay-max 0.93
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
    --out-dir outputs/d1_runs/phase3_convergent_r085_m66_squeezed --mode recompute \
    --phase3-mode convergent \
    --converge-exploit-ratio 0.85 \
    --converge-peak-hold-fixed 3 \
    --converge-alpha-mean 0.66 --converge-alpha-std 0.015 --converge-alpha-min 0.60 --converge-alpha-max 0.68 \
    --converge-decay-mean 0.888 --converge-decay-std 0.007 --converge-decay-min 0.88 --converge-decay-max 0.92 \
    --converge-explore-alpha-min 0.58 --converge-explore-alpha-max 0.72 \
    --converge-explore-decay-min 0.87 --converge-explore-decay-max 0.93
fi
