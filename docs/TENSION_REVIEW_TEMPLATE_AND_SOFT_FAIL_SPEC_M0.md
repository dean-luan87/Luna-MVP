# Tension Review Template / Soft-Fail Candidate Spec M0

**文件**：`docs/TENSION_REVIEW_TEMPLATE_AND_SOFT_FAIL_SPEC_M0.md`

**定位**：

1. **不是** benchmark / triage 规则修改文档，**不是**功能实现说明。  
2. 在 **`narrative_evidence_tension_review`**（`docs/NARRATIVE_EVIDENCE_TENSION_REVIEW_M0.md`）与 **M1.3 校准结论**（`docs/TENSION_AUDIT_CALIBRATION_REVIEW_M0.md`，数据：`logs/tension_audit_m13.json`、`logs/tension_audit_m13_analysis.json`）之上，把 **五类 tension 的使用层级、升级边界、配对方式、人工审计模板** **写死**，供 **第十四批及以后** 扩包与交付引用。  
3. **不**将任何条款接入当前 harness / hard-fail；**不**修改主骨架。

**补记**：**Tension Severity Profile**（`docs/TENSION_SEVERITY_PROFILE_SPEC_M0.md`）已形成——将原始 `none/low/medium/high` **映射**为 **`none` / `watch` / `review` / `critical_candidate` 风险语义**（解读层，**非**代码字段）；与本文 **L1–L4 使用层级** 配合使用。

**Soft-Fail 候选条款（M0 草案）**：`docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md` — 在 **`critical_candidate` 模式复盘**（`docs/CRITICAL_CANDIDATE_PATTERN_REVIEW_M0.md`，`m15` **7/7** 同族）之上，将主模式 **`resume_fragility_with_global_main_stall`** 写为 **人审 / advisory / future 观察** 用条款；**不接**自动 gate、**不改** benchmark。

**验证说明**：下文对五维的层级判定 **均对照** M1.3 全量分布（76 cases）复核，**非**照搬预设倾向；与数据冲突处以数据为准（例如 `narrative_trace_support` 在 M1.3 **从未**出现 medium/high，故 **不得**列为有效 review 信号，直至启发式收紧）。

---

## §1. 使用层级体系（Level 1–4）

| Level | 名称 | 含义 |
|-------|------|------|
| **L1** | `observation_only` | 背景审计信号；**不**单独触发「值得复核」结论；可用于长期趋势与上下文。 |
| **L2** | `review_candidate` | 交付/人工审计中**可标为重点**；**不**等价于失败；**不**单独构成 soft-fail。 |
| **L3** | `pair_only_signal` | **禁止单独**作为升级依据；仅在与指定 tension 或结构化字段**配对**时参与判断。 |
| **L4** | `soft_fail_candidate` | **当前不**写入规则；未来可进入 advisory / soft-fail / review gate；**仅**在满足本 spec **配对与前提**时考虑。 |

---

## §2. 五类 tension：分布、区分力、误报与**固化层级**

以下统计来自 **M1.3**（`logs/tension_audit_m13_analysis.json`），**R3**（snapshot）五维记为 `unknown`，不计入有效分档比较。

### 2.1 `narrative_trace_support_tension`（nt）

| 项目 | 内容 |
|------|------|
| **M1.3 分布** | **75** `none`，**1** `unknown`；**medium/high = 0** |
| **区分力** | **极差**（无法区分 case） |
| **误报风险** | 低；**漏报风险高**（产品关心的「叙事顺、证据弱」未触发） |
| **固化层级** | **L1（observation_only）** + **元状态 `needs_heuristic_tightening`**：在启发式收紧前，**不参与** L2/L4 认定。 |
| **单独使用** | **禁止**作为 review/soft-fail 依据（信息量不足）。 |
| **配对** | 仅在未来 **nt≥medium** 且可复现后，方可与 **`phase_closure`** 等讨论 **L4 组合**（见 §4）。 |
| **future soft-fail** | **否**（当前）；收紧启发式后**再评估**。 |

**为何不就高评级**：数据上 **无任何** medium/high 样本，若标为 review_candidate 会与「可观测信号」矛盾。

---

### 2.2 `phase_closure_outcome_tension`（pc）

| 项目 | 内容 |
|------|------|
| **M1.3 分布** | **20** `none`，**55** `high`，**1** `unknown` |
| **区分力** | **相对最强**（约 **26%** 非 high） |
| **误报风险** | 中等（需对照 `mainline_phase` / `closure_semantics_misalignment_summary` / terminal） |
| **固化层级** | **L2（review_candidate）**；满足 §4.2 配对时可为 **L4（soft_fail_candidate）** 的**主维之一**。 |
| **单独使用** | **允许**作为「建议人工看一眼」的**首要 tension**（仍 **不**等于 fail）。 |
| **配对** | 与 **`local_global`**（L3）或未来 **`narrative_trace_support`**（收紧后）组合时，**增强**可解释性。 |
| **future soft-fail** | **是（候选）**：在 **不**改 benchmark 的前提下，可作为 **advisory / review gate** 的**首选维**。 |

**验证**：与校准文档一致——**有梯度**，与 closure 语义错位显影**对齐**。

---

### 2.3 `summary_backfill_tension`（sb）

| 项目 | 内容 |
|------|------|
| **M1.3 分布** | **75** `high`，**1** `unknown` |
| **区分力** | **极差**（接近常量 high） |
| **误报风险** | **高**（常态契约即可 high） |
| **固化层级** | **L1（observation_only）** |
| **单独使用** | **禁止**作为 review/soft-fail 触发条件。 |
| **配对** | 仅作 **背景**；若与 **`memory_bias`** 同现，**仍不**自动升级，仅提示「契约+记忆行均活跃」。 |
| **future soft-fail** | **否（单独）**；若未来收紧为「子类 backfill 原因 / 与 narrative 矛盾」后再议。 |

**验证**：与「倾向 observation」一致，**理由为数据饱和**而非主观。

---

### 2.4 `local_global_progress_tension`（lg）

| 项目 | 内容 |
|------|------|
| **M1.3 分布** | **74** `medium`，**1** `high`，**1** `unknown` |
| **区分力** | **弱**（档位钉死在 medium） |
| **误报风险** | 高（大量正常帧标 medium） |
| **固化层级** | **L3（pair_only_signal）** |
| **单独使用** | **禁止**作为 review/soft-fail 依据。 |
| **配对** | **必须**：与 **`phase_closure_outcome=high`** 或 **`resume_chain_fragility_summary` / `process_observation_summary` 中明确 stall 子串** 同现时，方可进入 **L2 组合审查**。 |
| **future soft-fail** | **仅组合**：`pc=high` **且** `lg=high`（**M1.3** 曾长期 **0** 例同帧双高；**Local-Global Gradient Tightening M0** 与 **`RESUME_PROGRESS_SUMMARY_ALIGNMENT_M0`** 后 **`m14`/`m15`** 已出现同帧双高 + **`critical_candidate`**；**结构化人审条款**见 `docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md`）。 |

**验证**：与「pair_only」倾向一致；**必须写成规则句**（见 §3）。

---

### 2.5 `memory_bias_tension`（mb）

| 项目 | 内容 |
|------|------|
| **M1.3 分布** | **75** `high`，**1** `unknown` |
| **区分力** | **极差** |
| **误报风险** | **高** |
| **固化层级** | **L1（observation_only）** + **强制引用 `needs_manual_review_template`**（§5）：人工看 **`memory_invocation_effect_summary` / `source_conflict`**，**不看** tension 档位 alone。 |
| **单独使用** | **禁止**。 |
| **配对** | 与 **人工模板字段** 配对，**不**与单一 tension 自动组合升级。 |
| **future soft-fail** | **否（单独）**。 |

---

### 2.6 五维层级摘要表

| tension | 固化 Level | 单独使用 | soft-fail（当前单独） |
|---------|------------|----------|------------------------|
| nt | L1 + needs_heuristic_tightening | 否 | 否 |
| pc | L2；配对时可贡献 L4 | **可**（仅作 review 提示） | 候选（advisory） |
| sb | L1 | 否 | 否 |
| lg | L3 | 否 | 仅组合 |
| mb | L1 + manual template | 否 | 否 |

---

## §3. 配对使用规则（明确句）

### 3.1 **禁止单独使用**（不得仅因该维 medium/high 标为 review_needed）

- **`summary_backfill_tension`**  
- **`memory_bias_tension`**  
- **`local_global_progress_tension`**  
- **`narrative_trace_support_tension`**（且当前几乎恒为 none，单独无意义）

### 3.2 **允许单独作为「review 提示」**

- **`phase_closure_outcome_tension=high`**：**允许**在交付中标注「建议核对 phase/closure/outcome 口径」（仍 **非** fail）。

### 3.3 **推荐配对（满足其一即可进入「组合 review」）**

1. **`phase_closure_outcome=high` + `local_global_progress`≥medium**（并核对 `run_summary_reference` 中 resume/fragility 文本是否支持）。  
2. **`phase_closure_outcome=high` +（未来）`narrative_trace_support`≥medium**（启发式收紧后启用）。  
3. **`memory_bias` 不参与自动配对升级**；改为在 §5 模板中 **必填 memory 行 + effect**，由人判断。

### 3.4 **当前最好不要升级（含 soft-fail 叙事）的维**

- **`narrative_trace_support`**：在 M1.3 **零** medium/high 证据前，**不得**写入任何「有效 soft-fail 候选」条款。  
- **`summary_backfill`、`memory_bias`**：**不得**单独绑定 soft-fail。

---

## §4. Soft-fail candidate（仅文档层、未来用）

**定义**：以下 **不**进入当前 benchmark；供产品/评测升级草案使用。

| 候选 ID | 条件（全部满足） | 说明 |
|---------|------------------|------|
| **SF-1** | `phase_closure_outcome=high` **且** `local_global_progress=high` | 与 **`TENSION_SEVERITY_PROFILE_SPEC_M0`** 下 **`critical_candidate`** 同帧必要条件；**m15** 上 **7** 例均满足，且 **7/7** 归为同一主模式（见 **`docs/CRITICAL_CANDIDATE_PATTERN_REVIEW_M0.md`**）。**边注**：`R4_feedback_effective_real` 为 `lg=high` 且 `pc=none`，**不**等同 SF-1。 |
| **SF-1′（M0 草案）** | SF-1 **且** `resume_chain_fragility_summary=resume_declared_but_main_not_progressed` **且** `task_chain_progress_summary` 含 `global_main_progress_not_terminal_complete` **且**不满足健康对照排除 | **人审 / advisory 高风险候选** 的**可操作条款**（必要条件 + 排除 + 近邻混淆）：**`docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md`**。**不接**自动 gate。 |
| **SF-2** | `phase_closure_outcome=high` **且** `narrative_trace_support≥medium` | **依赖 nt 启发式收紧**，收紧前 **不适用**。 |

---

## §5. 最小人工 review 模板（短、可粘贴）

### A. 基本信息

- **case_id**：  
- **harness hard fail**：是 / 否  
- **medium/high 维**（列维名=档位）：  

### B. 六项正式验收回看（是/否/一句注）

| 项 | 结论 |
|----|------|
| 主导源是否讲得清 | |
| 任务位置是否讲得清 | |
| 记忆/个性化偏差是否讲得清 | |
| 主链 state/phase 是否讲得清 | |
| Summary / narrative / 白盒是否同口径 | |
| 后处理 entry 边界是否守住 | |

### C. tension 核心问题（选一或多）

- [ ] 叙事过满 / 证据不足（**若 nt 仍为 none，标「待启发式」**）  
- [ ] phase/closure 与 outcome 不一致（**优先看 pc**）  
- [ ] 契约要求 backfill 但与叙事冲突（**sb 仅作背景**）  
- [ ] 局部 vs 全局推进（**lg 须与 pc 或 resume 文本同看**）  
- [ ] 记忆偏稳（**填 memory effect，不看 mb 档位**）

### D. 当前判断（选一）

`observation_only` | `review_needed` | `soft_fail_candidate` | `needs_heuristic_tightening` | `not_useful`

### E. 后续动作（选一）

保留观察 | 下轮加压同类 case | 收紧启发式 | future benchmark 候选 | 不继续追

---

## §6. 与第十四批的关系

### 1. 第十四批前是否必须先有本 spec？

**是。** 第十四批应以本文件为 **tension 使用口径**；否则易重复「tension 一大片、不知信谁」。

### 2. 第十四批如何使用？

- **不**把 tension 直接接成 harness fail。  
- 交付文档中：按 §5 模板标注 **`review_needed` / `soft_fail_candidate`**（仅文档层）。  
- 场景设计：优先围绕 **`phase_closure`** 梯度 + **未来 nt 收紧** 可验证的叙事—证据张力。

### 3. 第十四批前是否建议改启发式？

- **默认**：**先不改代码**，仅按本 spec **读 tension**。  
- **唯一例外建议**：若下一里程碑专门做「校准落地」，可 **仅收紧 `narrative_trace_support`** 的灵敏度（**单维**），**不**动 benchmark；**不**在本轮实施。

---

## §7. 是否适合作为 tension 使用规范

**适合。** 条款与 M1.3 数据一致，并区分「观察 / 复核 / 配对 / 未来 soft-fail」；**不**替代三类正式缺陷分类（`baseline_covered_defect` 等）。

---

## §8. 本轮是否通过

**通过。** 已形成可执行的层级、配对规则、人工模板与第十四批前置约定；**未**改 benchmark、triage、主骨架。

---

## 主线—白盒—日志

- 本文件为 **口径与模板**，不改变主链与白盒实现。  
- 复盘时仍以 **同帧** `run_summary` / entry / 时间轴为准，tension **不**替代证据本体。
