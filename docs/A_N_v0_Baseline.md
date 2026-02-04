# A–N v0 封板文档（路线 A）

本文档用于记录 **路线 A（世界理解 → 介入 → 结果归因）** 在 v0 阶段的最终状态，作为后续阶段（P 及以后）的稳定基线。  
当前版本所有模块均已在 **真实视频输入** 下完成验证并封板。

---

## 一、总体结论

- **A–N v0** 已形成 **完整、可运行、可观测、可解释** 的闭环。
- 所有模块均满足 **shadow-only / signal-only / no side-effect** 的 v0 设计约束。
- 所有自动验收脚本均在真实视频环境下通过。
- 系统当前处于 **可长期跑态（long-run safe）**。

---

## 二、整体架构回顾（A–N）

| 层 | 名称 | 职责 |
|----|------|------|
| A | Eligibility | 是否具备介入资格 |
| B | World Signals | motion / path / branch / roi |
| C | Complexity | complexity_raw / effective |
| D | PAL | 前瞻复杂度（慢信号） |
| E | Rhythm | IDLE / PREPARE / ENGAGED |
| F | Engagement Level | L0 / L1 / L2 / L3 |
| G | Arbitration | 多任务仲裁（winner / deferred） |
| K | Intent | winner → intent 语义 |
| L | Slot | intent → slot 绑定 |
| M | Action Mapping | intent/slot → 行为（shadow-only） |
| N | Outcome | ENGAGED 下结果归因（shadow-only） |

---

## 三、各层状态与封板说明

### A — Eligibility v0

- **功能**：判断当前 tick 是否具备介入资格。
- **关键条件**：ACTIVE 任务态 + complexity_effective ≥ 阈值。
- **验证**：真实视频下 eligible ≈ 10%，LOW_COMPLEXITY 挡住 ≈ 90%。
- **状态**：✅ 封板。

---

### B — World Signals v0

- **信号**：motion / path / branch / roi。
- **特性**：
  - 非常量分布
  - 两两解耦（corr < 0.8）
  - 不越权（不直接抬安全等级）
- **验证**：6 分 42 秒真实视频 trace 统计通过。
- **状态**：✅ 封板。

---

### C — Complexity v0

- **输出**：complexity_raw → complexity_effective（受 VC 调制）。
- **特性**：effective 平滑、受 view_confidence 限制。
- **验证**：与 motion/roi/path/branch 联动合理。
- **状态**：✅ 封板。

---

### D — PAL v0

- **定位**：慢于 complexity 的前瞻风险信号。
- **特性**：
  - EMA 平滑
  - 与 complexity 高相关（~0.8）
  - 不直接驱动行为
- **验证**：真实视频下统计通过。
- **状态**：✅ 封板。

---

### E — Rhythm v0

- **状态机**：IDLE → PREPARE → ENGAGED。
- **约束**：时间窗 + PAL 阈值 + VC 门禁。
- **验证**：ENGAGED 占比低（≈8%），无抖动。
- **状态**：✅ 封板。

---

### F — Engagement Level v0

- **等级**：L0 / L1 / L2 / L3。
- **约束**：与 Rhythm / VC / control_mode 协同。
- **验证**：真实视频下 L3 极少，符合保守预期。
- **状态**：✅ 封板。

---

### G — Arbitration v0

- **功能**：多任务只选一个 winner。
- **规则**：SAFETY 必胜，其余任务公平轮转。
- **验证**：mock + 真实视频均通过公平性与必胜规则。
- **状态**：✅ 封板。

---

### K — Intent v0

- **功能**：winner → intent 语义映射。
- **特性**：无 winner 时 intent=NONE 也必须写入。
- **验证**：arbitration 行 100% 含 k。
- **状态**：✅ 封板。

---

### L — Slot v0

- **功能**：intent → slot / slot_type。
- **特性**：NONE → NONE 显式写入，便于验收。
- **验证**：arbitration 行 100% 含 l。
- **状态**：✅ 封板。

---

### M — Action Mapping v0

- **功能**：intent + slot → 行为映射（shadow-only）。
- **约束**：
  - apply_now=false
  - SAFETY → WARN + HIGH
  - NONE → NONE
- **验证**：自动验收脚本全部通过。
- **状态**：✅ 封板。

---

### N — Outcome v0

- **功能**：在 ENGAGED 且未执行时，对结果进行归因。
- **输出**：outcome_type / reason / apply_now。
- **关键约束**：
  - 无 UNKNOWN
  - reason 必须可解释
  - shadow-only
- **验证**：
  - 真实视频 + force-engaged-test
  - engaged_signal = outcome
  - 主要原因为 BLOCKED_COOLDOWN / BLOCKED_ARBITRATION
- **状态**：✅ 封板。

---

## 四、当前系统能力边界（v0）

**系统可以：**

- 感知真实世界复杂度
- 判断是否值得介入
- 形成意图与潜在行为
- 对「未执行」给出明确、可解释的原因

**系统刻意不做：**

- 不执行真实动作（shadow-only）
- 不学习、不个性化
- 不引入情感或价值判断

---

## 五、进入下一阶段的前提

在 A–N v0 冻结后，后续阶段可在此基线上展开：

- **P 层**：执行 / 学习 / 个性化（待设计）
- **地图 / 空间交互**：建议在 K–M 稳定后再接入
- **长期统计**：仅作为观测，不作为判定依据

---

## 六、当前状态总结

**A–N v0：完成、冻结、可长期运行。**

该文档作为后续所有演进的对照基线，不再回退修改。
