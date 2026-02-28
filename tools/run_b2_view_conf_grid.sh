#!/bin/bash
# B2 view_conf gate 网格：6 组 (floor,k) × 3 seed = 18 runs
# floor ∈ {0.5,0.6}  k ∈ {1.0,0.7,0.5}

export PYTHONHASHSEED=0
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PATCH_BASE="$ROOT/patches/physics/stress_channel_phys_v1_responsive.json"
OUT_BASE="$ROOT/outputs/d1_runs/phase3_b2_view_conf"
mkdir -p "$OUT_BASE/patches"

create_patch() {
  local floor="$1"
  local k="$2"
  local out="$OUT_BASE/patches/responsive_floor${floor}_k${k}.json"
  python3 -c "
import json
d = json.load(open('$PATCH_BASE'))
d['view_conf_gate_floor'] = $floor
d['view_conf_gate_k'] = $k
json.dump(d, open('$out', 'w'), ensure_ascii=False, indent=2)
"
  echo "[B2] created $out"
}

run_group() {
  local floor="$1"
  local k="$2"
  local patch="$OUT_BASE/patches/responsive_floor${floor}_k${k}.json"
  local out_dir="$OUT_BASE/floor${floor}_k${k}"
  for seed in 42 123 777; do
    echo "=== B2 floor=$floor k=$k seed=$seed ==="
    python3 "$ROOT/tools/run_d1_tournament.py" \
      --dual-channel --determinism-check 1 \
      --stress-base-patch "$ROOT/patches/physics/stress_channel_phys_v1_conservative.json" \
      --stress-base-patch-responsive "$patch" \
      --stress-suite-sustain library_store/v1.1/golden_stress_v2_powerclips_sustain \
      --stress-suite-pulse library_store/v1.1/golden_stress_v2_powerclips_pulse \
      --regular-suite library_store/v1.1/golden_regular_v3_50eps \
      --n-candidates 60 --seed "$seed" \
      --out-dir "$out_dir" --mode recompute \
      --phase3-mode convergent \
      --converge-exploit-ratio 0.85 --converge-peak-hold-fixed 3 \
      --converge-alpha-mean 0.696 --converge-alpha-std 0.013 --converge-alpha-min 0.65 --converge-alpha-max 0.73 \
      --converge-decay-mean 0.869 --converge-decay-std 0.004 --converge-decay-min 0.86 --converge-decay-max 0.88 \
      --converge-explore-alpha-min 0.69 --converge-explore-alpha-max 0.72 \
      --converge-explore-decay-min 0.865 --converge-explore-decay-max 0.885
  done
}

# 6 组：(0.5,1.0) 回归点；(0.5,0.7)/(0.5,0.5)；(0.6,1.0)/(0.6,0.7)/(0.6,0.5)
for floor in 0.5 0.6; do
  for k in 1.0 0.7 0.5; do
    create_patch "$floor" "$k"
  done
done

for floor in 0.5 0.6; do
  for k in 1.0 0.7 0.5; do
    run_group "$floor" "$k"
  done
done

echo "[B2] grid done. Run: python3 tools/summarize_b2_view_conf_grid.py"
