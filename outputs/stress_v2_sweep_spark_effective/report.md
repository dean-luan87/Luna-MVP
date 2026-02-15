# Stress_v2 Sweep v2 Report

## PASS 判定
- divergence_rate >= 30%
- avg_volatility_delta < 0.02
- avg_guarded_ratio_delta < 0.15

## Combos
| combo_id | divergence_rate | avg_diff_frames | avg_volatility_delta | avg_guarded_ratio_delta | ema_max | clamp_hit_ratio | PASS |
|----------|-----------------|-----------------|----------------------|--------------------------|---------|-----------------|------|
| hold2_decay0.9_ah0.45 | 1.00 | 3.2 | 0.0000 | 0.0000 | 0.8941789104702185 | 0.1 | PASS |

## Best combo

- **hold2_decay0.9_ah0.45** (PASS=True)
- risk_processing: {"risk_scale_factor": 5.0, "smoothing.peak_hold_frames": 2, "smoothing.peak_decay": 0.9, "smoothing.alpha": 0.25, "smoothing.alpha_high": 0.45, "smoothing.alpha_switch_at": 0.85}