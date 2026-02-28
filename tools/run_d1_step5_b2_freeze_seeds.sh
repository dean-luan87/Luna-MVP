#!/bin/bash
# B2 准冻结：回归点 (floor=0.5, k=1.0)，det=3，3-seed 验收。
# 验收口径同 Step5：champion_eg、champion_vol、high_risk_frames_total、guarded_frames_total + 3-pass hash 一致。

export PYTHONHASHSEED=0
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

SEED="${1:-42}"
if [ "$SEED" = "all" ]; then
  for s in 42 123 777; do
    echo "=== Step5 B2 Freeze (determinism=3) seed $s ==="
    python3 tools/run_d1_tournament.py \
      --dual-channel --determinism-check 3 \
      --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
      --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
      --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
      --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
      --regular-suite library_store/v1.1/golden_stress_v2 \
      --n-candidates 60 --seed "$s" \
      --out-dir outputs/d1_runs/step5_b2_freeze --mode recompute \
      --phase3-mode convergent \
      --converge-exploit-ratio 0.85 \
      --converge-peak-hold-fixed 3 \
      --converge-alpha-mean 0.696 --converge-alpha-std 0.013 --converge-alpha-min 0.65 --converge-alpha-max 0.73 \
      --converge-decay-mean 0.869 --converge-decay-std 0.004 --converge-decay-min 0.86 --converge-decay-max 0.88 \
      --converge-explore-alpha-min 0.69 --converge-explore-alpha-max 0.72 \
      --converge-explore-decay-min 0.865 --converge-explore-decay-max 0.885
  done
else
  python3 tools/run_d1_tournament.py \
    --dual-channel --determinism-check 3 \
    --stress-base-patch patches/physics/stress_channel_phys_v1_conservative.json \
    --stress-base-patch-responsive patches/physics/stress_channel_phys_v1_responsive.json \
    --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
    --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
    --regular-suite library_store/v1.1/golden_stress_v2 \
    --n-candidates 60 --seed "$SEED" \
    --out-dir outputs/d1_runs/step5_b2_freeze --mode recompute \
    --phase3-mode convergent \
    --converge-exploit-ratio 0.85 \
    --converge-peak-hold-fixed 3 \
    --converge-alpha-mean 0.696 --converge-alpha-std 0.013 --converge-alpha-min 0.65 --converge-alpha-max 0.73 \
    --converge-decay-mean 0.869 --converge-decay-std 0.004 --converge-decay-min 0.86 --converge-decay-max 0.88 \
    --converge-explore-alpha-min 0.69 --converge-explore-alpha-max 0.72 \
    --converge-explore-decay-min 0.865 --converge-explore-decay-max 0.885
fi
