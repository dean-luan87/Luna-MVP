# D2.2 对抗验证与 D2.3 入场标准（冻结版）

## 一、blind_patch 的两类攻击（只动权重层）

1. **阈值封顶（Threshold Cap）**  
   把触发 CAUTION/DANGER/GUARDED 的阈值推到极端，使「几乎触发不了」：
   - `thresholds.safe_to_caution` / `thresholds.caution_to_danger` → 0.9999（或更大）
   - `thresholds.min_mode_hold_ms` → 极大（若需「难进入保守」则配合使用）

2. **灵敏度归零（Sensitivity Zero）**  
   把风险相关权重压到 0，让引擎对风险输入不敏感：
   - `weights.risk_density`、`redline_hit`、`occlusion_ratio`、`roi_load`、`path_instability`、`motion_instability`、`branch_load`、`speak_pressure`、`reject_pressure` → 0.0  
   - `smoothing.alpha` → 0（EMA 不更新，complexity 不爬升）

**边界**：只改权重/阈值/尺度，不碰逻辑结构、不加 if、不改 runtime。

---

## 二、对抗验证的审计点（落在现有 Scorecard）

| 审计点 | 预期现象 | 含义 |
|--------|----------|------|
| **1）Early Gain 坍塌** | blind_patch 下 `early_conservative_action_gain` 变差（趋近 0 或比 baseline 更晚进 GUARDED） | 系统不再提前避险的语义崩坏信号 |
| **2）Lookahead 异常平稳** | `lookahead_drop_ratio` 可能为负（看起来「效率更好」），因眼瞎策略不缩短前瞻 | 指标被眼瞎策略反向刷高 |
| **3）Regression 语义漏洞** | baseline 有 CAUTION 的帧，candidate 抹成 SAFE；comparator 不判 regression；Gate 仍 **PASS** | 漏洞成立：风险被抹平却被当成变好 |

---

## 三、D2.3 入场标准（硬条件）

**只要同时满足以下，即立刻开 D2.3，D1 冻结：**

- blind_patch 在 **Golden Suite（至少 10 条高价值）** 上 **GATE: PASS**
- 且 candidate 的 `safety_level` **大面积更“安全”**（更多 SAFE），尤其在 baseline 有 CAUTION 的片段
- 且 candidate **没有**对应的「物理缓解信号」（如进入 GUARDED、更短 lookahead、更保守的 control_mode）

含义：系统可以通过「装作看不见风险」拿到好分数，闭环会变成欺骗游戏。

**D2.3 核心原则**：  
若不承认风险，必须用**可验证的物理缓解**证明风险被消解，否则判定为**感知退化**（Reference Risk Stream / 风险守恒检查）。

---

## 四、执行顺序（冻结，不改流程）

1. **Golden Suite**：至少 10 条，其中包含 HAS_CAUTION / CONTROL_MODE_SWITCH / NEGATIVE_PAL_TREND 等高价值样本。
2. **构造 blind_patch**：阈值封顶 + 权重归零（见 `patches/blind_patch.json`）。
3. **跑 Suite**：  
   `python3 tools/run_sim_suite.py --base-dir library_store --version-tag v1.1 --patch patches/blind_patch.json --out-dir outputs`  
   （有 Golden 时加 `--golden`。）
4. **公示结果**：suite_report.json + 各 episode 的 gate_result.json + scorecard 摘要。
5. **按 D2.3 入场标准决策**：  
   - **PASS** → 立刻开 D2.3，D1 冻结。  
   - **FAIL** → 现有侧向防御已能抓到眼瞎作弊，D1 可入场。

---

## 五、Gate 顺序（已冻结）

**Safety → Coverage → Stability → Efficiency → EarlyGain**

理由：Coverage 是元规则，无 coverage 的 volatility/efficiency 易被沉默作弊污染，故 Coverage 在 Stability 之前。

---

*文档版本：D2.2 对抗验证 + D2.3 入场标准 冻结*
