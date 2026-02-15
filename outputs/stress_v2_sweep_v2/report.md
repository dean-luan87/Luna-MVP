# Stress_v2 Sweep v2 Report

## PASS 判定
- divergence_rate >= 30%
- avg_volatility_delta < 0.02
- avg_guarded_ratio_delta < 0.15

## Combos
| combo_id | divergence_rate | avg_diff_frames | avg_volatility_delta | avg_guarded_ratio_delta | ema_max | clamp_hit_ratio | PASS |
|----------|-----------------|-----------------|----------------------|--------------------------|---------|-----------------|------|
| hold0_decay0.85 | 0.00 | 0.0 | 0.0000 | 0.0000 | 0.26982824221613555 | 0.1 | FAIL: 分叉不足(divergence_rate<30%) |
| hold0_decay0.9 | 0.00 | 0.0 | 0.0000 | 0.0000 | 0.26982824221613555 | 0.1 | FAIL: 分叉不足(divergence_rate<30%) |
| hold0_decay0.92 | 0.00 | 0.0 | 0.0000 | 0.0000 | 0.26982824221613555 | 0.1 | FAIL: 分叉不足(divergence_rate<30%) |
| hold1_decay0.85 | 0.89 | 1.1 | 0.0000 | 0.0000 | 0.6568487585248126 | 0.1 | PASS |
| hold1_decay0.9 | 0.33 | 0.2 | 0.0000 | 0.0000 | 0.7469212017816006 | 0.1 | PASS |
| hold1_decay0.92 | 1.00 | 2.7 | 0.0000 | 0.0000 | 0.7886849382176035 | 0.1 | PASS |
| hold2_decay0.85 | 0.44 | 0.3 | 0.0000 | 0.0000 | 0.7459788242209721 | 0.1 | PASS |
| hold2_decay0.9 | 1.00 | 2.4 | 0.0000 | 0.0000 | 0.8130481812854923 | 0.1 | PASS |
| hold2_decay0.92 | 1.00 | 3.0 | 0.0000 | 0.0000 | 0.8446510874874001 | 0.1 | PASS |
| hold3_decay0.85 | 1.00 | 2.4 | 0.0000 | 0.0000 | 0.8238438726776502 | 0.1 | PASS |
| hold3_decay0.9 | 1.00 | 2.8 | 0.0000 | 0.0000 | 0.8730276870788537 | 0.1 | PASS |
| hold3_decay0.92 | 1.00 | 2.2 | 0.0000 | 0.0000 | 0.8950022971879124 | 0.1 | PASS |

## Best combo

- **hold1_decay0.92** (PASS=True)
- risk_processing: {"risk_scale_factor": 5.0, "smoothing.peak_hold_frames": 1, "smoothing.peak_decay": 0.92, "smoothing.alpha": 0.25}