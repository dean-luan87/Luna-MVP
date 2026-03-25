# Severity Signal Gap Review M0

**文件**：`docs/SEVERITY_SIGNAL_GAP_REVIEW_M0.md`

## 文档定位

1. **不是**场景扩包，**不是**规则或 benchmark 变更，**不是**主骨架重构。  
2. 本轮是对 **severity 画像层当前「信号质量」** 的复盘：解释 **review 多而 `critical_candidate` 恒为 0**、**`lg` 梯度拉不开**、**`nt` 无区分力** 的**数据与启发式根因**，并给出**下一阶段工程优先级**（排序，不单列「都重要」）。  
3. 依据：`docs/TENSION_SEVERITY_PROFILE_SPEC_M0.md`、`docs/REAL_SCENARIO_PACK_M1_4_DELIVERY.md`、`logs/real_scenario_pack_m14.json`、`logs/benchmark_triage_board_m14.json`；结构化统计：`logs/severity_signal_gap_m14_analysis.json`（由 `tools/analyze_severity_signal_gap_m14.py` 只读生成）。

---

## §1. M1.4 数据事实（severity 与原始张力）

来源：`logs/severity_signal_gap_m14_analysis.json`（与 `m14` 整包一致）。

### 1.1 `overall_severity_profile` 分布（含 R3 无 tension 对象）

| 档位 | 数量 |
|------|------|
| `review` | 62 |
| `watch` | 19 |
| `critical_candidate` | **0** |
| 无 tension 对象（R3 snapshot） | 1 |

### 1.2 原始 `pc` × `lg` 组合（81 条有 tension）

| 组合 | 数量 |
|------|------|
| `pc=high` **且** `lg=medium` | **61** |
| `pc=none` **且** `lg=medium` | 19 |
| `pc=none` **且** `lg=high` | **1**（`R4_feedback_effective_real`） |
| `pc=high` **且** `lg=high` | **0** |

**结论（数据层）**：在 **M1.4 全量**中，**不存在**「同帧 `phase_closure_outcome_tension=high` 且 `local_global_progress_tension=high`」的样本。  
而 **`map_severity_profile_m14`** 将 **`critical_candidate`** 定义为 **仅当** 上述两维同时为 `high`（见 `tools/tension_severity_profile_map.py`）。因此 **`critical_candidate=0` 在当前数据下是必然结果**，主要不是「再调一档阈值就能出现」的模糊保守问题。

### 1.3 原始 `nt`（narrative_trace_support）

| 取值 | 数量（有 tension 的 81 条） |
|------|------------------------------|
| `none` | **81** |
| `low` / `medium` / `high` | **0** |

**`nt` 原因字符串（81/81 一致）**：`structured_events_plentiful_relative_to_narrative`（见 `decision_monitor/narrative_evidence_tension_review.py` 中 `eff_events >= 18 → narrative_trace_support_tension=none` 分支）。

### 1.4 `sb` + `mb` 共现

- **`summary_backfill_tension=high` 且 `memory_bias_tension=high`**：**81 / 81**（有 tension 的 case）。  
- **含义**：在 M1.4 下，二者作为 **背景高饱和** 几乎**全员共现**，对 case 间**区分力极弱**；severity 映射里对 `sb`/`mb` 的 `high` 多落在 **`watch`**，与 Calibration 中「饱和维」叙述一致。

### 1.5 设计对照样本（R81 / R82）

| case | `nt` | `pc` | `lg` | 说明 |
|------|------|------|------|------|
| `R81_story_more_complete_than_trace_support_real` | **none** | high | medium | 命名意图压「故事顺、证据薄」，**原始 `nt` 仍未离开 `none`** |
| `R82_phase_closure_progress_pair_near_critical_candidate_real` | **none** | high | medium | 命名近 **critical**，**实证仍为 `lg=medium`**，与全包 **无 `pc∧lg` 同 high** 一致 |

---

## §2. 核心问题 1：为什么 `review` 很多，但 `critical_candidate` 仍为 0

### 2.1 `review` 的来源结构

- **`pc` 驱动 `per["pc"]==review`**：**61** 条（与 `pc=high` 条数一致）。  
- **`lg` 在 `per_dimension` 上进入 `review` 或更高**：**62** 条（= 61 条「`pc=high`∧`lg=medium`」映射为 `lg→review」，加 **1** 条「`pc=none`∧`lg=high`」→ `lg→review`）。  
- **`nt` 驱动 `review`**：**0** 条（`nt_review=0`）。

因此：**`review` 的主体叙事**是 **「closure/phase 与 outcome 口径张力（`pc`）」+ 在配对规则下被抬升的「局部/全局推进（`lg`）」**；**不是** `nt` 抬出来的。

### 2.2 `critical_candidate=0` 的根因（三者兼有，权重不同）

1. **配对规则（硬条件）**：`critical_candidate` **仅**允许 **`pc=high` 且 `lg=high`** 同帧。  
2. **数据事实（主因）**：M1.4 **没有任何一条**满足该组合 → **不是「差一点」而是「零样本」**。  
3. **上游启发式结构（根因）**：  
   - **`lg=high`** 在实现上**几乎只**来自 `resume_chain_fragility_summary` 含 `resume_declared_but_main_not_progressed`（见 `_score_local_global_progress`）。  
   - **`pc=high`** 主要来自 **closure 语义错位**（如 `closure_semantics_misalignment=...`）。  
   - 当 **`pc=high`** 时，当前 61 条里 **`lg` 全部为 `medium`**（原因几乎均为 `progress_language_but_main_not_reached`），**从未**走到 **`resume_fragility_declared...` → `lg=high`** 分支。  
   - 唯一 **`lg=high`** 的 **`R4`** 为 **`pc=none`**（closure 无强错位）→ **与 `pc=high` 互斥**，无法触发配对。

**判断**：**不是**单纯「阈值再松一点」就能稳定产出 `critical_candidate`；**首要矛盾**是 **原始 `pc` 与 `lg` 的触发路径在观测上「错配」**：**closure 强信号**与 **resume 链强声明**在 **同一帧**几乎**不共现**。

---

## §3. 核心问题 2：为什么 `lg` 梯度拉不开

1. **档位事实**：81 条里 **`lg` 仅 `medium`（80）与 `high`（1）**，**无** `low` 等中间丰富梯度；与 **`pc=high` 同帧时 `lg` 恒为 `medium`**。  
2. **启发式形状**：`lg` 的 **`high`** 路径**窄**（强依赖特定 resume 摘要子串）；**`medium`** 路径**宽**（`task_chain_progress_summary` 中含推进语但 `resume_chain_progress_reached_main is False` 等）。  
3. **与 `pc` 配对的增益**：在 severity 映射里，`lg` 在 **`pc=high`** 时 **`medium` 即可映射为 `per["lg"]=review`**，**已参与**把 **overall** 推到 **`review`**；但要进入 **`critical_candidate`**，**必须** **`lg=high`**，而当前数据 **在 `pc=high` 条件下从未出现 `lg=high`**。  
4. **R82 为何仍非 `high`**：命名表达「近 critical」，但 **frame 上仍落在** `progress_language_but_main_not_reached` → **`medium`**；**未**满足 **`resume_fragility_declared_main_not_progressed`** 的 **`lg=high`** 条件。

**工程判断**：`lg` **有价值**（已支撑 **review** 与人工叙事），但作为 **「与 `pc` 同帧共 escalated」** 的信号，**当前更像「宽 medium 平台 + 极少 high 尖峰」**，**与 `pc` 的强信号不同步**。

---

## §4. 核心问题 3：为什么 `nt` 区分力仍弱

1. **全量塌缩**：M1.4 有 tension 的 **81** 条 **`narrative_trace_support_tension` 全部为 `none`**，且原因 **全部为**「结构化事件相对叙事偏多」— **启发式在「事件足够多」时直接把张力归零**。  
2. **与场景设计的关系**：即便命名上强调「故事比 trace 更满」（如 **R81**），只要 **事件计数 / 时间轴事件** 仍触发 **「plentiful」** 分支，**`nt` 就不会升高** → **不是**「再多扩几包就能撞出 medium/high」的统计问题为主，而是 **判别式先把变量钉死在 `none`**。  
3. **与 trace/event 密度的关系**：当前实现里 **高密度事件**反而成为 **「无张力」** 的充分条件之一 → **信号被「事件多」掩盖**，与 Spec 中「叙事—证据失衡」的直觉 **需再对齐**（后续若改，应动 **启发式**，而非先堆场景）。

---

## §5. 下一阶段优先级（必须排序）

### 第一优先级：**先拉 `lg` 梯度（及与 `pc` 的共现结构）**

**理由（与数据一致）**：

- **`lg` 已在** `map_severity_profile_m14` **的配对规则**与 **`critical_candidate`** 定义中占位；**瓶颈**是 **原始档位从未出现 `pc=high∧lg=high`**。  
- 调整 **`lg` 的档位生成**（例如在 **`pc=high`** 时如何区分 **medium / high**、是否引入 **与 closure 同帧的 resume 强声明** 等）**直接作用于**「能否产生 **非零** `critical_candidate` 样本」— **比**先动 `nt` **更贴近**当前 severity 叙事与 SF-1 文档组合。  
- **`nt` 在 m14 全为 `none`**：先收紧 `nt` **不会**解决 **`pc∧lg` 零样本** 问题。

### 第二优先级：**再收紧 / 重塑 `nt` 启发式**

**理由**：

- 在 **不改代码** 的前提下，**扩包难以**让 `nt` 离开 `none`；**收益**依赖 **重写比值与「plentiful」门闩** 或 **引入与叙事长度无关的锚点**。  
- 适合在 **`lg` 梯度**有可见区分后，再把 **`nt`** 从「全员 none」拉成 **可分层** 的观测维。

**明确结论**：**先 `lg`，后 `nt`**（**不是**「都重要」并列）。

---

## §6. 本轮文档是否适合作为 severity 层「信号缺口」复盘

**适合。** 它用 **可复现统计**（`logs/severity_signal_gap_m14_analysis.json`）把 **「review 多 / critical 为 0」** 分解为 **配对规则 + 零组合数据 + 启发式错配**，并单独解释 **`nt` 塌缩** 机制。

---

## §7. 本轮是否通过

**通过。** 已完成 **signal gap** 复盘与只读分析脚本、产物路径明确；**未**改 benchmark、triage、主骨架与 soft-fail。

---
## §8. 补记（Local-Global Progress Gradient Tightening M0）

针对本文 **§3** 所述 **`lg` 梯度与 `pc∧lg` 零样本** 问题，已单独立项 **`docs/LOCAL_GLOBAL_PROGRESS_GRADIENT_TIGHTENING_M0.md`** 收紧 **`local_global_progress_tension`** 启发式（**不**改 benchmark）；**`pc=high∧lg=high` 同帧仍为 0** 的结论与本文 **配对规则** 一致，**下一动因**见该文档 **§六**。

---

## 主线—白盒—日志

- 本复盘 **只读** `m14` 落地结果；**不**回写主链。  
- **最终判断**：**主线通顺，白盒一致，日志已落地**（统计与 `logs/real_scenario_pack_m14.json` 同源）。
