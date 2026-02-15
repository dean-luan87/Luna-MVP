# Scale Sweep 结果 (6.0 / 8.0)

## 运行命令

```bash
python3 tools/run_stress_v2_divergence_test.py --risk-scale 6.0
python3 tools/run_stress_v2_divergence_test.py --risk-scale 8.0
```

## 结果

| scale | diff_frames | first_diff_seq | guarded_ratio_delta | volatility_delta |
|-------|-------------|----------------|---------------------|------------------|
| 6.0   | 全 0        | null           | 0.0                 | 0.0              |
| 8.0   | 全 0        | null           | 0.0                 | 0.0              |

**结论**：6x、8x 均未出现分叉；`summary.json` 为最后一次运行（8.0）的 18 条记录。

## 物理原因（STEP 1 验证）

- scale=5 时：effective_risk 已 clamp 到 max=1.0（raw 0.36×5=1.8→1.0），EMA 输入封顶。
- scale=8 时：ema_max 仍为 **0.2698**，与 scale=5 相同——再提高 scale 无法再抬升 EMA，因为 **clamp 在 scale 之后、EMA 之前**，单帧峰值 ema_peak ≈ alpha × 1.0 = 0.25。
- 因此：**仅靠 scale 无法让 ema 跨过 0.38**，除非有连续多帧高 effective 让 EMA 累积，或动 alpha/hold。

## 建议下一步（按你之前约定）

- scale=8 仍无分叉 → 视为「stress_v2 仍是瞬时 spike，非连续风险」。
- 可选：
  1. **提高 alpha** 到 0.4（单帧峰值 ema ≈ 0.4，可触边）；
  2. **或增加 hold_time**（2 帧触发）；
  3. 或保留 scale 甜点（如 5）待后续与 alpha/hold 组合再测。
