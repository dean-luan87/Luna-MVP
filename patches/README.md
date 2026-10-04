# Patches

- **empty_patch.json**：空 patch，用于 baseline 或对比。
- **threshold_probe_30down.json**：仅用于**诊断与 calibration**的临时阈值 probe（safe_to_caution ×0.7 等）。**不进入 D1 候选空间**，不参与 Experience Ledger。

## 阈值 Probe 验收口径

跑完后看 `diff_frames` 与诊断里的 `ema_p95` / `effective_guarded`：

| 结果 | 结论 | 下一步 |
|------|------|--------|
| diff_frames 明显 > 0（如 5%+ 帧） | 阈值真空区确认；权重是有效旋钮 | 做 calibration，再 D1 weights-only |
| diff_frames 很少但非 0（1~2 帧） | 阈值开始触边，Golden 仍偏温和 | 再做 -20%/-40% probe 或高压 slice |
| diff_frames = 0 | risk_score 尺度被压扁或 obs 极温和 | 查 risk_score 链路：clip/归一化/alpha 等 |

纪律：threshold_probe 只用于诊断与标定，不改“性格”，不进入 D1 搜索空间。
