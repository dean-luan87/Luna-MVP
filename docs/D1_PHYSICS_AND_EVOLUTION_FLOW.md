# D1 物理常数与进化流程（工程标准）

本文档冻结当前 D1 进化系统的**物理常数**与**端到端流程**，作为「进化系统操作手册」。  
若出现 early_gain=0 或 powerclips 建不出，应优先对照本文档检查**风险密度**是否满足点火条件，而非怀疑引擎/Scorer/Gate 代码。

---

## 一、物理常数

| 名称 | 值 | 来源 |
|------|-----|------|
| **safe_to_caution** | **0.38** | `a3/config.py` 默认阈值；EMA ≥ 0.38 时由 SAFE 进入 CAUTION |
| caution_to_danger | 0.65 | 同上 |
| hysteresis | 0.02 | 回滞，避免边界抖动 |

- **不通过改阈值来“点火”**：降低 0.38 会破坏安全哲学，视为作弊。
- D1 进化应在**固定阈值**下，通过**数据强度**（高应力片段）或**权重/平滑**（在候选空间内）产生分化。

---

## 二、Base Physics Patch 作用域

- **文件**：`patches/physics/stress_v2_phys_v1.json`
- **内容**：仅包含 **smoothing.*** 与 metadata，不包含 weights.\* 或 thresholds.\*
  - `smoothing.peak_hold_frames`: 3
  - `smoothing.peak_decay`: 0.92
  - `smoothing.alpha_high`: 0.45
  - `smoothing.alpha_switch_at`: 0.85
- **作用**：在 recompute 时与候选 patch 做 **deep_merge**，保证所有候选在同一套「物理常数 + 平滑」下评测；候选仅允许 **weights.\*** 与 metadata 白名单，不允许 smoothing.\*，避免 Goodhart。
- **结论**：base_patch 固定「实验室/应力路径」的物理，D1 只进化权重与决策边界附近的响应，不进化阈值本身。

---

## 三、Golden Suite 预期风险范围

- **当前 golden_stress_v2**：在 base_patch 下 recompute 后，观测到 **risk_used_max ≈ 0.108**，远低于 0.38。
- **含义**：Golden 片段在物理上属于「中低密度」风险，**不足以触发 high_risk 帧**（即 risk_used_for_decision ≥ 0.38 的帧数为 0）。
- **这不是 Bug**：引擎链路、replay 字段、Gate、Scorer 均已验证；问题归结为**样本物理强度不够**。
- **设计预期**：
  - 若希望 early_gain 在 D1 中起作用，Golden（或 powerclips）中至少部分 episode 需满足 **risk_used_max ≥ 0.38**，且 **high_risk_frames > 0**。
  - 若仅用当前 golden_stress_v2，early_gain 会恒为 0，排名由 L2/L3（dwell、volatility、guarded_ratio）主导。

---

## 四、early_gain 生效条件

- **定义**：early_gain 衡量「在 high_risk 区间内，candidate 相对 baseline 是否更早进入 GUARDED」。
- **硬条件**：
  1. **risk_used_for_decision ≥ threshold_safe_to_caution（0.38）** 的帧被记为 high_risk；
  2. replay 中必须存在 **high_risk == True** 的帧，否则无 high_risk 区间，early_gain 恒为 0；
  3. risk_used_for_decision 必须来自 A3 **决策用 EMA**（hold + conditional alpha 之后），与 threshold 同口径，不得用 complexity_score 等替代。
- **数据要求**：至少一条 episode 在 recompute 后满足 **risk_used_max ≥ 0.38** 且 **high_risk_frames_count > 0**，early_gain 才有物理意义。

---

## 五、Powerclips 构建标准

- **目标**：从 stress 源中筛出「能跨阈值」的片段，构成 **golden_stress_v2_powerclips**，供 D1 使用。
- **工具**：`tools/build_powerclips_golden.py`
  - 输入：`--stress-dir`（含 records.jsonl 的 episode 目录）、`--out-suite`、`--top-k`（默认 24）、`--base-patch`（同上）。
  - 逻辑：对每个 episode 用 base_patch 做 **recompute**，读 replay_output.jsonl，统计 risk_used_max、high_risk_frames（risk_used ≥ threshold）；**仅保留 high_risk_frames > 0** 的 episode，按 risk_used_max 降序取 TopK，复制 records + replay + meta.json 到 out-suite。
- **校验**：`tools/validate_powerclips_suite.py` 要求 **ignition_rate = 100%**（即每条 episode 的 high_risk_frames > 0）。
- **标准**：powerclips 中每条 episode 的 meta.json 必须包含 `risk_used_max`、`high_risk_frames`、`powerclip: true`，且 risk_used_max ≥ 0.38。

---

## 六、D1 点火条件（总结）

| 条件 | 说明 |
|------|------|
| **risk_used_max ≥ 0.38** | 至少一条 episode 内决策用 EMA 曾达到或超过 safe_to_caution |
| **high_risk_frames_count > 0** | 该 episode 内存在 risk_used_for_decision ≥ threshold 的帧 |
| **replay 含字段** | risk_used_for_decision、threshold_safe_to_caution、high_risk 已写入 replay，由 recompute 链路保证 |
| **base_patch 已加载** | tournament 需带 `--base-patch patches/physics/stress_v2_phys_v1.json`，与 powerclips 构建时一致 |

当上述条件不满足时，early_gain 为 0 是**正确物理结果**，应通过引入更高风险密度数据（如 sweep 中的高压片段）解决，而非改阈值或改代码逻辑。

---

## 七、完整闭环流程（已验证)

1. **Base Physics Patch** 固定物理常数（smoothing.*），与候选 weights.* 合并为 effective_patch。
2. **Golden Suite** 作为评测输入（每条 episode 含 records.jsonl，可选 meta.json）。
3. **Recompute**：对每条 episode 用 A3 Headless + effective_patch 逐帧 tick，生成 replay。
4. **risk_used / high_risk 注入**：replay 每行写入 risk_used_for_decision、threshold_safe_to_caution、high_risk（risk_used ≥ threshold）。
5. **early_gain 计算**：Scorer 基于 replay 中的 high_risk 区间，比较 baseline 与 candidate 的「首次 GUARDED」时机。
6. **Guardian Discipline 审计**：exit latency 等门禁，与 early_gain 独立。
7. **D1 Lexicographic 排序**：L0 淘汰 → L1 early_gain↑ → L2 dwell_p95_delta/volatility↓ → L3 guarded_ratio_delta↓，产出 rank_report.json / .md、champion_bundle。

此链路已通过「golden_stress_v2 + base_patch + recompute」全流程验证；在现有低风险密度下 early_gain=0 为预期行为。

---

## 八、后续策略（不修改本文档即视为未变更）

- **不推荐**：通过降低阈值或人为放大权重来制造 early_gain。
- **推荐**：从 sweep / stress pipeline 中筛选 **risk_raw 高峰** 或 **ema 可突破 0.38** 的片段，构建 powerclips；或先做「单片点火实验」：用一条 sweep 高压 replay 单独跑 D1，确认 early_gain 非 0 后再规模化。
- **进化哲学**（战略选择，非本文档范围）：D1 核心驱动力可选——(A) 极端应力下的快速反应、(B) 常规应力下的稳定边界、(C) 双通道评测；该选择影响 powerclips 与 suite 设计，而非物理常数本身。

---

*文档版本：与当前代码库一致；物理常数以 a3/config.py 与 patches/physics/stress_v2_phys_v1.json 为准。*
