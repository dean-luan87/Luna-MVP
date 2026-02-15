# D1 Rank Report (Dual Channel)

**Champion**: baseline

**排序说明**: 先过 Stress 安全门禁（high_risk_frames>0 且 gate pass），再按 L1 Stress early_gain↑ → L2 Regular guarded_ratio_delta↓ → L3 Regular volatility↓ 词典序排序。

## Stress Channel (门禁 + L1 early_gain)

| Rank | patch_id | stress_early_gain_mean | stress_high_risk_frames |
|------|----------|-------------------------|-------------------------|
| 1 | baseline | 0.0 | 396 |
| 2 | conservative | 0.0 | 396 |
| 3 | d1_candidate_001 | 0.0 | 396 |
| 4 | d1_candidate_000 | 0.0 | 396 |
| 5 | aggressive | 0.0 | 396 |

## Regular Channel (L2/L3)

| Rank | patch_id | regular_guarded_ratio_delta_mean | regular_volatility_mean |
|------|----------|-----------------------------------|------------------------|
| 1 | baseline | 0.0 | 0.0 |
| 2 | conservative | 0.0 | 0.0 |
| 3 | d1_candidate_001 | 0.0 | 0.0 |
| 4 | d1_candidate_000 | 0.0 | 0.0022 |
| 5 | aggressive | 0.0 | 0.0216 |

## Eliminated (L0)
