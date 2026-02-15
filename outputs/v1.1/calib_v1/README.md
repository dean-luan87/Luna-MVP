# calib_v1 校准产物

- **calib_three_tiers.json**：三档阈值(0.21/0.195/0.19)在 stress suite 上的四指标：near_threshold_ratio, max_consecutive_near_frames, volatility_delta_vs_baseline。
- **calib_three_candidates.json**：选定档(如 0.195)下三候选(baseline/aggressive/conservative)的 volatility_mean, early_gain_mean, guarded_ratio_delta_mean。

选择规则（三档）：先挑 near_threshold_ratio 在 0.5%~5% 的档；若有多个取 max_consecutive_near_frames 更高、volatility 增幅更小的。

三候选验收：diff_frames > 0，aggressive early_gain > baseline，volatility ≤ 0.2，guarded_ratio_delta ≤ 0.30。
