# Stress_v2 D1：Peak Hold + Scale Sweep 设计与问题总结

## 一、设计总结

### 1. 目标（验收标准）

- **不是**“更安全/更效率”，而是更底层的验收：
  1. 在 stress_v2 上出现**稳定分叉**（`diff_frames > 0`）
  2. 分叉**不靠抖动**（`volatility_delta` 不能飙）
  3. **不引入 Goodhart**（不能靠全程 GUARDED 刷分）

### 2. 根因（一句话）

- **clamp(…, 1.0) 放在 EMA 之前，且风险是稀疏尖峰** → EMA 永远上不去（单帧峰值 ema ≈ alpha×1.0 ≈ 0.25，跨不过阈值 0.38）。
- 因此要动的不是 scale（scale 已因 clamp 触顶失效），而是**让尖峰有持续性**或**让 EMA 更能跟踪峰值**。

### 3. 方案选型

| 方案 | 做法 | 结论 |
|------|------|------|
| **A. Peak Hold** | clamp 后、EMA 前：`x_hold = max(x, prev_hold * decay)`，峰值保持 N 帧后缓慢衰减 | ✅ 已实现，sweep 验证有效 |
| **B. Conditional Alpha** | 高压段（x_hold ≥ switch_at）用更大 alpha，其余用 base | ✅ 已实现，可选 |
| **C. 把 clamp 移到 EMA 后** | 改变 risk 量纲定义，牵涉门限/审计 | ❌ 不推荐，未做 |

- **原则**：先 A 后 B；不改主阈值、不改门禁、不污染主线物理法则（仅实验室/应力路径启用）。

### 4. 实现落点

- **risk → EMA 链路**：`a3/engine.py` 的 `tick()` 内  
  `raw_effective` → clamp → **`_apply_peak_hold()`** → `_ema(x_hold)`。
- **配置**：`a3/config.py` 的 `A3Smoothing`（`peak_hold_frames`, `peak_decay`, `alpha_high`, `alpha_switch_at`），通过 patch 的 `smoothing.*` 传入。
- **Sweep 脚本**：`tools/run_stress_v2_divergence_sweep_v2.py`，输出 `report.json` / `report.md`，PASS 规则：divergence_rate ≥ 30%、avg_volatility_delta < 0.02、avg_guarded_ratio_delta < 0.15。

---

## 二、问题总结

### 1. 你遇到的唯一报错

- **现象**：执行  
  `python3 tools/run_stress_v2_divergence_sweep_v2.py ... --write-debug-trace`  
  报错 `unrecognized arguments: ...`。
- **原因**：文档里用 `...` 表示“前面参数照抄”，但命令行里**字面量 `...` 会被当成参数**，脚本不认识。
- **解决**：不要输入 `...`，直接写完整参数。**推荐**写 debug trace 时用下面这条（单 combo，只生成 1 个 trace 文件）：
  ```bash
  python3 tools/run_stress_v2_divergence_sweep_v2.py \
    --peak-hold-frames 2 --peak-decay 0.9 \
    --out-dir outputs/stress_v2_sweep_v2 \
    --write-debug-trace
  ```
  若要对多个 combo 都写 trace，把 `--peak-hold-frames` 写成列表即可，例如：`--peak-hold-frames 2,3 --peak-decay 0.9`。

### 2. 其他（当前无问题）

- Peak Hold sweep（0,1,2,3 × 0.85,0.9,0.92）、Conditional Alpha sweep（hold2/3 + ah0.45）均按预期跑通，多个 combo PASS，D1 可进入。

---

## 三、分析

### 1. 为何 hold0 全 0 分叉？

- hold0 = 关闭 Peak Hold，等价于原先链路：effective 被 clamp 到 1.0 后直接进 EMA，稀疏尖峰只活 1 帧，ema_max ≈ 0.27，跨不过 0.38，故 diff_frames 全 0。与 STEP 1 结论一致。

### 2. 为何 hold≥1 后出现分叉？

- 峰值被保持 1～3 帧并缓慢衰减，EMA 有足够输入累加，ema_max 升到 0.65～0.89，跨过 0.38，baseline 与 aggressive/conservative 在边界附近产生决策差异，divergence_rate 上升。

### 3. 为何 volatility_delta / guarded_ratio_delta 仍为 0？

- 当前 stress_v2 片段与权重差异下，分叉主要体现在**是否进入 CAUTION/GUARDED**，而 guarded_ratio 和 volatility 在 scorer 里对整段统计，可能尚未敏感；或 baseline 与 candidate 在这些聚合指标上仍接近。需要更长时间或更多片段时再观察是否出现非零。

### 4. 甜点区（从你贴的 sweep 结果）

- **仅 Peak Hold**：hold2_decay0.92、hold3_decay0.9/0.92 等均为 divergence_rate=1.00、vol_delta=0、guard_delta=0，可作默认实验室配置。
- **加 Conditional Alpha**：hold2/3_decay0.9_ah0.45 进一步拉高 ema_max（0.89～0.95），分叉更稳；若后续发现抖动再微调 alpha_high 或 alpha_switch_at。

---

## 四、建议

### 1. 文档与 CLI

- 在脚本 docstring 或 `--help` 的示例里**避免用 `...` 占位**，改为写一条完整示例，例如：
  ```text
  Example with debug trace:
    python3 tools/run_stress_v2_divergence_sweep_v2.py --peak-hold-frames 2,3 --peak-decay 0.9 --out-dir outputs/stress_v2_sweep_v2 --write-debug-trace
  ```
- 可在 README 或 playbook 中注明：“`...` 仅表示省略，实际运行请替换为具体参数。”

### 2. 后续跑法（最省时间）

1. **常规 sweep（不写 trace）**：  
   `--peak-hold-frames 0,1,2,3 --peak-decay 0.85,0.9,0.92` 已跑过，结果以 report.json/report.md 为准。
2. **需要逐帧 trace 时**：  
   任选一个 combo，补全参数并加 `--write-debug-trace`（不要写 `...`）。
3. **若将来 volatility 或 guarded_ratio 敏感**：  
   再根据 report 里的 `avg_volatility_delta` / `avg_guarded_ratio_delta` 微调 decay 或 alpha_high，避免用抖动/过度保守换分叉。

### 3. 审计与复现

- report 中已含 `risk_processing`、`risk_processing_audit`（peak_hold_frames, peak_decay, alpha_high_enabled, clamp_hit_ratio），便于区分“实验室模式”与主线，避免日后把 Peak Hold/conditional alpha 当主线 bug 查。

---

## 五、结论

- **设计**：Peak Hold（+ 可选 Conditional Alpha）落在 clamp 后、EMA 前，只延长尖峰、不碰阈值与门禁，符合“最小改造、实验室逼分叉”的目标。
- **问题**：当前唯一操作问题是命令行中**字面量 `...` 导致报错**；改为完整参数即可。
- **状态**：sweep 结果支持“在 stress_v2 上稳定出现分叉且不靠抖动”，D1 可据此进入下一阶段；若需逐帧审计，用完整命令加 `--write-debug-trace` 即可。
