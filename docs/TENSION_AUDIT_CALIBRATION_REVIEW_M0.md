# Tension Audit Calibration Review M0

**文件**：`docs/TENSION_AUDIT_CALIBRATION_REVIEW_M0.md`

**定位**：

1. **不是**功能开发，**不是** benchmark / triage 规则升级。  
2. 对 **`narrative_evidence_tension_review`**（见 `docs/NARRATIVE_EVIDENCE_TENSION_REVIEW_M0.md`）在 **M1.3** 全量结果上的表现做**有效性校准**：去噪、分级、给出下一阶段用法。  
3. 数据依据：`logs/real_scenario_pack_m13.json`、`logs/benchmark_triage_board_m13.json`（与 `docs/REAL_SCENARIO_PACK_M1_3_DELIVERY.md` 一致）。  
4. 离线统计脚本（只读）：`tools/analyze_tension_audit_m13.py` → 可复现摘要：`logs/tension_audit_m13_analysis.json`。

---

## §1. 为什么 76 例中有 75 例「至少一维 medium/high」

**结论：二者兼有——启发式在若干维度上偏「饱和」，同时真实运行帧在 summary/backfill/记忆行上普遍带轻度契约张力。**

1. **阈值与规则形状**  
   - `summary_backfill_tension`、`memory_bias_tension` 在 **75/76** 例上为 **high**（见下表），与 **`post_processing_summary_entry` 多通道 backfill**、**记忆行非空即抬升** 的启发式强相关 → **单独作为 alarm 时区分力极差**（接近常量）。  
   - `local_global_progress_tension` 在 **74/76** 例为 **medium**、仅 **1** 例为 **high** → 档位几乎钉死在 medium，**区分力弱**。  
2. **真实语义**  
   - 冻结基线下 **hard fail = 0** 并不否定「叙事/契约/过程显影」上存在**可接受的轻度张力**；全绿 + 高张力并存，说明 tension 当前更像 **「复杂度与契约提示」** 而非 **「已证缺陷」**。  
3. **数据缺口**  
   - **`R3_general_search_real`** 使用 **snapshot_json**，构建路径未产生完整 `run_summary_reference` 链 → `narrative_evidence_tension_review` 为 **null**（脚本按空对象计为 **unknown**）。这是 **输入形态差异**，不是业务「低张力」，文档中作**对照标注**，不当作普遍低张力样本。

**回答核心问题**：75 个「中高张力」里，**大部分是规则饱和 + 真实轻度张力叠加**；**不是** 75 个都等价于「即将失败」。

---

## §2. 全量分布（M1.3，76 cases）

统计由 `tools/analyze_tension_audit_m13.py` 从 `logs/real_scenario_pack_m13.json` 逐条读取 `narrative_evidence_tension_review` 汇总（**R3** 为 `null`，五维记为 `unknown`）。

| 维度 | none | low | medium | high | unknown |
|------|------|-----|--------|------|---------|
| `narrative_trace_support_tension` | 75 | 0 | 0 | 0 | 1 |
| `phase_closure_outcome_tension` | 20 | 0 | 0 | 55 | 1 |
| `summary_backfill_tension` | 0 | 0 | 0 | 75 | 1 |
| `local_global_progress_tension` | 0 | 0 | 74 | 1 | 1 |
| `memory_bias_tension` | 0 | 0 | 0 | 75 | 1 |

**解读要点**：

- **`narrative_trace_support`**：在 M1.3 全量中 **从未** 出现 medium/high → **当前启发式对该维几乎「失敏」**（与「叙事顺滑但证据弱」的产品关切**未对齐**）。  
- **`summary_backfill` / `memory_bias`**：**98.7%** 为 high → **过敏（饱和）**，不宜单独作为「值得追」信号。  
- **`phase_closure`**：**72%** high、**26%** none → **唯一具有明显「非高」占比**的维度，**相对最有区分力**。  
- **`local_global`**：**97%** medium → **档位缺乏梯度**，区分力弱。

---

## §3. Case 交叉与极值

- **综合分最高（启发式 rank 求和）**：多例并列 **score=11**（`nt:none | pc:high | sb:high | lg:medium | mb:high`），见 `logs/tension_audit_m13_analysis.json` 中 `top_10_by_tension_score`。  
- **五维全 high**：**0** 例（`narrative_trace_support` 几乎总为 none）。  
- **低分对照**：仅 **`R3_general_search_real`**（snapshot，tension 对象缺失），**不**代表业务上的「理想低张力」，仅作**输入链路边界**对照。

---

## §4. 与 harness 的关系

- **hard fail = 0**，但 **多数维度 high/medium** → 说明当前 tension **不是** harness 的代理指标；更适合标为 **future review / soft-fail 研究输入**，而非「当前失败」。  
- **更像未来问题苗头**的组合：需 **脱离饱和维** 单独看 **`phase_closure_outcome`** 的 high vs none，并 **未来配合收紧后的 `narrative_trace_support`**。  
- **更像叙事复杂度高**：**`summary_backfill`+`memory_bias` 双 high** 在几乎全体成立 → 易与「正常复杂叙事」混淆 → **必须收紧或配对**后再谈 soft-fail。

---

## §5. 分维校准（表现 / 意义 / 风险 / 建议）

| 维度 | 当前表现 | 工程意义 | 误报/风险 | 下一阶段建议 |
|------|----------|----------|-----------|----------------|
| **narrative_trace_support** | 几乎全 **none**，区分力 **极低** | 与 M1.3 目标 B 相关，但 **未触发** | 低误报，但 **漏报** 高 | **`tighten_heuristic`**（提高叙事/事件比灵敏度或分层）；**`soft_fail_candidate`：否（单独）** |
| **phase_closure_outcome** | **20 none / 55 high**，相对有梯度 | 与 closure 显影、语义错位 **对齐度较高** | 中等；需结合 terminal/phase 真值复核 | **`review_candidate`**；可 **`pair_with_another_tension`**（如与收紧后的 nt 或 lg 异常） |
| **summary_backfill** | **75 high**，饱和 | 忠实反映「契约要求回溯」的频度，但 **作 alarm 无区分力** | **高误报**（把常态契约当异常） | **`tighten_heuristic`**（例如仅当 backfill 原因子类命中 / 与 narrative 长度矛盾时升级）；**`keep_as_observation`** 保留聚合展示 |
| **local_global_progress** | **74 medium**，几乎无梯度 | 概念对（局部 vs 全局），但 **档位失效** | 把大量正常帧标成「中等张力」 | **`tighten_heuristic`**（提高 high 门槛、引入 resume_fragility 子标签）；**`pair_with_another_tension`** |
| **memory_bias** | **75 high**，饱和 | 提示记忆行参与，但 **无法区分** 偏稳与正常 | **高误报** | **`tighten_heuristic`**；**`needs_manual_review_template`**（模板化看 memory_effect / source_conflict） |

### 三类归档（与文档要求对齐）

- **`keep_as_observation`**：`summary_backfill`、`memory_bias`（保留展示，**不**单独升级 soft-fail，直至收紧）。  
- **`review_candidate`**：`phase_closure_outcome`（优先演化）。  
- **`soft_fail_candidate`（未来，需配对/收紧后）**：**组合信号**，例如 `phase_closure=high` **且** `narrative_trace_support≥medium`（在 nt 启发式修复后）；或 **`local_global=high`**（在 lg 梯度修复后）**且** 非 snapshot 输入。

---

## §6. 阶段结论（必须回答的四点）

### 1. 当前 tension 审计层是否值得保留？

**值得保留**，但应以 **「分层展示 + 校准后阈值」** 方式保留：  
- 保留 **五维对象**与 **brief/readable**（审计可追溯）；  
- **报表层**默认突出 **有区分力的维**（当前主要是 **`phase_closure`**），饱和维降级为 **上下文**或 **子计数**。

### 2. 哪些维度最值得继续演化？

- **优先**：`phase_closure_outcome_tension`、`local_global_progress_tension`（后者需 **恢复档位梯度**）。  
- **次优先**：`narrative_trace_support_tension`（**提高灵敏度**，否则与 M1.3 目标脱节）。  
- **需先收紧再谈升级**：`summary_backfill_tension`、`memory_bias_tension`。

### 3. 哪些不适合直接升级？

- **`summary_backfill`、`memory_bias`**：当前 **单独** 不适合作为 soft-fail。  
- **`narrative_trace_support`**：在 **未收紧前** 不适合升级（几乎恒为 none，**区分力不足**）。

### 4. 第十四批前是否先补 review / soft-fail 草案？

**建议先补一层轻量文档化产出，再开第十四批（或并行但文档优先）**：  
- 至少一份 **`tension review template` / `soft-fail candidate spec`**（定义：配对规则、输入形态 snapshot 与 ctx_json 的差异、以及「饱和维」如何降级展示）。  
- **不建议**在未校准启发式前，把第十四批扩包当作「验证 tension」的主手段——否则易重复 M1.3 的 **75/76 泛化**现象。

---

补记：已形成 **tension 使用层级 / 配对 / 人工模板** 定稿：`docs/TENSION_REVIEW_TEMPLATE_AND_SOFT_FAIL_SPEC_M0.md`（**不**替代本校准结论中的分布数字）。

---

## §7. 本轮是否通过

**通过。**  
理由：已完成 M1.3 全量拆解、分维结论、保留/收紧/配对建议与第十四批前置条件；**未**修改 benchmark、未新增 hard-fail、未扩场景。

---

## 主线—白盒—日志

- 本轮仅 **离线统计 + 文档**，不改主链与白盒实现。  
- 统计可复现：`tools/analyze_tension_audit_m13.py`、`logs/tension_audit_m13_analysis.json`。  
- **最终判断**：审计结论**落地为文档与可复现数字**，无运行链路边界变更。
