#!/bin/bash
# B1 扩容：Regular 50-ep，3 seed，determinism=1，production recipe v1

export PYTHONHASHSEED=0
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

REGULAR_SUITE="${1:-library_store/v1.1/golden_regular_v3_50eps}"
if [ ! -d "$REGULAR_SUITE" ]; then
  echo "Building 50-ep regular suite..."
  python3 tools/build_regular_suite_50eps.py
fi

for s in 42 123 777; do
  echo "=== B1 Expansion seed $s (det=1) ==="
  python3 tools/run_d1_tournament.py \
    --dual-channel --determinism-check 1 \
    --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
    --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
    --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
    --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
    --regular-suite "$REGULAR_SUITE" \
    --n-candidates 60 --seed "$s" \
    --out-dir outputs/d1_runs/phase3_b1_expansion --mode recompute \
    --phase3-mode convergent \
    --converge-exploit-ratio 0.85 \
    --converge-peak-hold-fixed 3 \
    --converge-alpha-mean 0.696 --converge-alpha-std 0.013 --converge-alpha-min 0.65 --converge-alpha-max 0.73 \
    --converge-decay-mean 0.869 --converge-decay-std 0.004 --converge-decay-min 0.86 --converge-decay-max 0.88 \
    --converge-explore-alpha-min 0.69 --converge-explore-alpha-max 0.72 \
    --converge-explore-decay-min 0.865 --converge-explore-decay-max 0.885
done
