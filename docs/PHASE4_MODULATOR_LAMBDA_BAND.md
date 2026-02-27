# Phase4 调制器 λ 安全带（上界扫描结论）

## 1. 结论（封口径）

- **λ_default**：0.10  
- **λ_verified_safe**：**[0.00, 0.40]**（仅对当前 suite/seed42 有效）  
- 该 safe 区间是「**已验证**」区间，**不是**最终 λ_max。真正上界需在「扩容压力域」（多 seed / 更狠 suite）后再用 p95 gate 定义。

## 2. 上界扫描表（suite=v1.1, seed=42）

| lam  | det  | early_gain | overreact_rate | alpha_p90 | champion_vol |
|------|------|------------|----------------|-----------|--------------|
| 0.25 | PASS | ≥4.0       | ~0.36          | —         | <0.01        |
| 0.30 | PASS | ≥4.0       | ~0.36          | —         | <0.01        |
| 0.40 | PASS | ≥4.0       | ~0.37          | —         | <0.01        |

- 三档 λ 下 gate 全 PASS，overreact 随 λ 单调略升，**未出现拐点**（无红灯）。

## 3. 为什么没扫到上界？

- **测试域偏温柔**：当前 stress suite（golden_stress_v2_powerclips_pulse/sustain）在 seed42 下 risk_density_ema 动态范围有限，α_eff 变化不足以触发 gate 失败。
- **B2 在当前 suite 里 noop**：view_conf 等未把「更凶」场景拉进来。
- 因此：**不是扫描不努力，而是域不够凶**。下一步应优先做 **seed 扩容**（10-seed × λ∈{0.10, 0.40} 快扫），再考虑 **stress suite 增压**（低 view_conf、更长 sustain、更高 min-high-risk 等），才能逼出红灯、得到有意义的 λ_safe_max。

## 4. 参数制度（三件套）

1. **默认值**：λ_default = 0.10  
2. **允许运行范围**：λ ∈ [0, λ_safe_max]  
   - 当前仅能写：**λ_safe_max ≥ 0.40**（seed42, suite=v1.1）  
   - 真正的 λ_safe_max 在扩容压力域后用 **p95 gate** 定义。  
3. **监控与回滚**：CI/线上 gate 失败 → 回滚到 Phase3（λ=0）。

## 5. 相关文件

- 配方：`configs/personality/PHASE4_MODULATOR_RECIPE_v0.1.json`  
- Gate 实现：`tools/monitor_personality_health.py`（支持 `--grade smoke|release`）  
- 上界扫描脚本：`tools/run_d1_phase4_lam_upper_sweep.sh`  
- 10-seed 快扫：`tools/run_d1_phase4_seed_sweep.sh` + `tools/summarize_phase4_seed_sweep.py`

## 6. Gate 分档与结论（管理层可读）

- **smoke**（默认）：determinism 不参与 overall，用于 `--det 1` 的 sweep；**release**：determinism 必须 PASS（det=3 指纹一致），用于 freeze/tag 发布签字。  
- **Smoke 结论**：10-seed×2-lam（0.10/0.40）在 eg、overreact、vol、miss 上一致稳定；λ 提升仅带来轻微 overreact 上升，远低于阈值。  
- **Release 结论**（待 3-seed×2-lam det=3 跑完）：3-seed×2-lam det=3 指纹一致后，Phase4 调制层可进入「可发布策略库」。
