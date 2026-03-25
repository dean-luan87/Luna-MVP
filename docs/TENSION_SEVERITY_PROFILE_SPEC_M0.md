# Tension Severity Profile Spec M0

**文件**：`docs/TENSION_SEVERITY_PROFILE_SPEC_M0.md`

**定位**：

1. **不是**新增评测规则，**不是**功能开发，**不**改 benchmark / triage / 主骨架。  
2. 在 **`narrative_evidence_tension_review`** 的**原始观测档位**（`none` / `low` / `medium` / `high` / `unknown`，见 `docs/NARRATIVE_EVIDENCE_TENSION_REVIEW_M0.md`）之上，定义一套 **少档位、强语义的工程风险画像**：**`none` / `watch` / `review` / `critical_candidate`**（下称 **severity**）。  
3. **核心声明**：**原始观测值 ≠ 工程风险画像**。交付与复盘应优先引用 **severity 语义**，**不得**把代码里的 `medium/high` 直接等同于「最终病情轻重」而不经本画像翻译。  
4. 依据：**Calibration**（区分力/饱和，`docs/TENSION_AUDIT_CALIBRATION_REVIEW_M0.md`）、**Review/Soft-Fail Spec**（怎么用、`docs/TENSION_REVIEW_TEMPLATE_AND_SOFT_FAIL_SPEC_M0.md`）；本文件回答 **「各档代表什么病症」**。  
5. **复盘**：`m15` 上 **`critical_candidate` 样本模式** 见 **`docs/CRITICAL_CANDIDATE_PATTERN_REVIEW_M0.md`**（**不**改本文映射规则）。

---

## §1. 统一 severity 四档（写死）

| Severity | 工程含义（跨维共性） |
|----------|----------------------|
| **`none`** | 当前**无明显**可叙事化风险；或**证据不足**无法形成画像（含「观测链未建立」）。**不**建议写入交付正文为风险项。 |
| **`watch`** | **轻度**张力，落在**正常复杂度波动**内；**只观察、不介入**；可进附录/日志，**不进**交付正文风险段（除非项目另有约定）。 |
| **`review`** | 张力已具**明确工程意义**；**值得**人工复核或交付「建议核对」；**仍非** harness 失败。 |
| **`critical_candidate`** | 已**接近** future soft-fail / advisory gate 的**候选**；**仍非** hard-fail；**不得**再仅当背景噪声。 |

**与原始档位的区别**：原始档位是 **启发式输出**；severity 是 **解读层**。同一原始 `high` 在不同 tension 上可映射为 **`review` 或 `critical_candidate` 或仅 `watch`**（见 §3），取决于该维是否饱和、是否需配对。

---

## §2. 三份文档分工（避免重复）

| 文档 | 回答的问题 |
|------|--------------|
| **Calibration Review** | 哪些维**有区分力**、哪些**过敏/迟钝**、M1.3 **分布事实**。 |
| **Review / Soft-Fail Spec** | 各维 **L1–L4 使用层级**、**配对规则**、**人工模板**、SF 候选条件。 |
| **Severity Profile（本文）** | 各维在不同 severity 下对应 **何种病症**、**单轮 vs 多轮**、**哪些维暂不能铺满四档**。 |

---

## §3. 五类 tension：观测来源、病症与四档语义

以下 **A/B/C** 每类 tension 独立撰写；**原始档位**见 `decision_monitor/narrative_evidence_tension_review.py` 中启发式。

---

### 3.1 `narrative_trace_support_tension`（nt）

**A. 原始观测来源**  
- `run_summary_reference.mainline_narrative_brief`、`mainline_narrative_alignment.narrative_brief`  
- `structured_event_layer_snapshot.event_count`、`reasoning_timeline_view.events`  
- 叙事长度与事件密度的比值启发式  

**B. 病症（张力偏高时）**  
- **叙事相对顺滑、可读**，但 **structured event / 时间轴可核对锚点偏少**，易出现 **「故事好听、证据链薄」**。  

**C. 四档语义（severity）**

| Severity | 含义 |
|----------|------|
| **none** | 叙事与事件层 **量纲匹配**，或叙事过短、无「过满」迹象。 |
| **watch** | 偶发 **略长叙事 / 略少关键事件类型**；仍可能在正常波动内。 |
| **review** | **叙事密度相对事件层明显偏高**，需核对 **trace/event 是否支撑结论**（在 **`NARRATIVE_TRACE_SUPPORT_HEURISTIC_TIGHTENING_M0`** 后，nt 已开始出现少量 `watch/review` 梯度；仍不接 hard-fail）。 |
| **critical_candidate** | **反复**在同类场景出现「叙事远厚于证据」且与其它维（如 `pc`）**同现**；**仅文档层** future 候选（当前 **几乎无观测样本**）。 |

---

### 3.2 `phase_closure_outcome_tension`（pc）

**A. 原始观测来源**  
- `closure_semantics_misalignment_summary`、`phase_closure_alignment_summary`  
- `mainline_state_snapshot.mainline_phase`、`object_search_interaction.search_terminal_status`  
- `confirmation_input_bridge` 等 closure 相关效应  

**B. 病症**  
- **阶段/收口标签**与 **terminal/outcome/完成度叙述** **不同步**：如 **closure 语义过早「像完成」**、或 **phase 在修但 terminal 仍空**。  

**C. 四档语义**

| Severity | 含义 |
|----------|------|
| **none** | phase/closure 与可观测 terminal **无明显错位**（原始多为 `none`）。 |
| **watch** | 轻微口径差，可在下一轮采样中消化（原始偏低档或边界）。 |
| **review** | **明确** closure/outcome 与推进事实 **可能不一致**，应对照 **主链 phase 与 terminal**（原始常为 `high` 且校准认为 **有区分力** → 常映射为此档）。 |
| **critical_candidate** | **多轮**或 **与 resume/fragility 强一致** 的持续错位；或 **与 `lg` 异常同现**（见 §4）；**不**等于 fail。 |

---

### 3.3 `summary_backfill_tension`（sb）

**A. 原始观测来源**  
- `post_processing_summary_entry.requires_*_backfill`、`backfill_reason_summary`  
- 与 `narrative_readable` 长度等的启发式冲突  

**B. 病症**  
- **契约要求回溯**（trace/event/whitebox）与 **summary/entry 可读「闭环感」** 并存 → 易出现 **「读起来完整但仍应 backfill」**。  

**C. 四档语义**

| Severity | 含义 |
|----------|------|
| **none** | 无强制 backfill 或契约未要求多层回溯（当前全量 **极少** 对应原始 `none`，见 §5）。 |
| **watch** | 有 **单一** backfill 提示，属 **常态契约**（原始常为 `high` 但 **画像上降级**为 watch：背景监控）。 |
| **review** | **多类 backfill 同时亮起** 且 **与叙事矛盾可叙述**（需结合 `backfill_reason` 子类；**不宜**仅凭原始 `high` 自动定档）。 |
| **critical_candidate** | **反复**在同一 case 族出现「可读闭环 + 多层 backfill 仍长期未落实」；**当前**更多保留为 **文档叙事**，**不**强绑原始档位。 |

---

### 3.4 `local_global_progress_tension`（lg）

**A. 原始观测来源**  
- `resume_chain_fragility_summary`、`resume_chain_progress_reached_main`  
- `process_observation_summary`、`task_chain_progress_summary`  

**B. 病症**  
- **局部步骤/子任务**看似在推进，**全局主任务**未实质前进或 **resume 链脆弱**。  

**C. 四档语义**

| Severity | 含义 |
|----------|------|
| **none** | 无 **resume/全局停滞** 显影（原始 **极少**，多为 `medium` 时见 §5）。 |
| **watch** | 单次 **轻微** resume 与主目标 **轻微** 不一致；**或** 原始已分出 **`low`**（**Local-Global Progress Gradient Tightening M0** 后：`weak_exploration_main_mixed_not_yet_global_stall` 等，见 `docs/LOCAL_GLOBAL_PROGRESS_GRADIENT_TIGHTENING_M0.md`）。 |
| **review** | **明确**「局部可解释、全局未前进」或 **fragility** 子串命中（原始 `medium` 在画像上常 **保守映射** 为 watch～review 边界，**须配对 `pc` 或文本**）。 |
| **critical_candidate** | **多轮**持续 **resume 声明但主目标未达**；或 **`lg` 原始 `high`** 且与 **`pc` 同向**异常（见 Review Spec 中 R4 类 **异常组合**）。 |

**M0 补记（梯度收紧）**：`task_chain_progress_summary` 中 **`resume=` 字段名** 不再作为「推进语言」命中条件，避免 **假阳性 medium**；原始 **`low` / `medium` / `high`** 在工程上更可分。

---

### 3.5 `memory_bias_tension`（mb）

**A. 原始观测来源**  
- `memory_bias_accumulation_summary`、`memory_invocation_explanation` 的 effect / conflict  
- `scheduled_source_state` 中与 memory 的 override/conflict  

**B. 病症（统一称「个性化语义偏差」，不用「污染」）**  
- 记忆或历史模式 **稳定参与** 推理，**未**出现硬冲突时仍可能 **偏稳、偏惯**。  

**C. 四档语义**

| Severity | 含义 |
|----------|------|
| **none** | 无记忆参与或记忆行 **中性**（当前全量 **极少** 对应原始 `none`，见 §5）。 |
| **watch** | 记忆 **轻量** 参与，无冲突信号（原始高时 **画像降级**为 watch：背景）。 |
| **review** | 出现 **`memory_vs_observation`** 等 **可复核** 子类，或 **人工模板** 勾选「需看 effect」（**不**看档位 alone）。 |
| **critical_candidate** | **多轮**同一熟悉语境下 **偏稳趋势** + **与观测/调度反复拉扯**；仍 **非** fail，**须**人工模板。 |

---

## §4. 单轮高值 vs 多轮持续高值

| Tension | 单轮高值（原始 medium/high）通常意味 | 多轮持续高值通常意味 |
|---------|--------------------------------------|----------------------|
| **nt** | 当前帧 **叙事—事件比** 瞬时失衡；可能为 **单次复杂剪辑**。 | **同类场景反复**「叙事厚、锚点薄」→ 结构性 **叙事—证据** 缺口风险。 |
| **pc** | **当次** phase/closure 与 terminal **瞬时** 不对齐。 | **结构性** 收口语义与完成度叙述 **长期不同步** → 更接近 **review～critical_candidate**。 |
| **sb** | **当次** 契约同时要求多层 backfill。 | **长期**「可读闭环 + backfill 总被推迟」→ 流程风险，非单帧噪声。 |
| **lg** | **当次** resume/局部状态 **瞬时** 与主目标 **摩擦**（原始多为 medium）。 | **稳定**「局部绿、全局不前进」→ **偏结构性**，优先 **与 `pc` 同看**。 |
| **mb** | **当次** 记忆权重或冲突标签 **偶发** 升高。 | **熟悉场景下偏稳** 成趋势 → **个性化语义偏差固化**，贴近 **review～critical_candidate**（仍须模板）。 |

**规则句**：**`critical_candidate` 级叙事默认要求「多轮或跨 case 族可复现」+「与六项验收或另一 tension 可互证」**；**单轮** raw `high` **默认不**直接标为 `critical_candidate`，**除非** Review Spec 已定义的 **异常组合** 或 **人工模板** 明确记载。

---

## §5. 哪些 tension 当前**不能完整使用**四档 severity

**诚实声明**：下述限制 **不改变** 原始字段；仅约束 **交付中 severity 表述**。

| Tension | 限制 | 原因 |
|---------|------|------|
| **nt** | **不宜**声称已具备 **完整 watch→critical** 梯度 | M1.3 全量 **无** medium/high 原始样本；**多数 case severity 只能标 `none` + 备注「画像待启发式收紧」**。 |
| **sb** | **不宜**用四档 **强判病症** | 原始 **近乎恒 high**（饱和）；**默认**将 raw `high` **映射为 `watch`（背景监控）**，仅当 **backfill 子类/矛盾** 可叙述时升到 **`review`**。 |
| **mb** | **不宜**单靠档位升到 **`critical_candidate`** | 原始 **近乎恒 high**；**必须**结合 **人工模板**（effect / conflict）与 **多轮** 再定 **`review`～`critical_candidate`**。 |
| **lg** | **不宜**仅用 raw 区分 **`review` vs `critical_candidate`** | 原始 **钉死在 medium** 为主；**须**配对 **`pc`** 或 **resume 文本** 再定档。 |
| **pc** | **相对最可** 使用四档 | 校准显示 **唯一明显梯度**；仍建议 **单轮 vs 多轮** 区分 **review** 与 **critical_candidate**。 |

---

## §6. 最小 severity 使用规则（规则句）

### 1. `watch`

- **不默认进入**交付正文「须处理」段；**可**记为 **观察附录 / 内部日志**。  
- **不要求**人工跟踪；**可**在 **多轮对比**时升级为 `review`。

### 2. `review`

- **须**进入 **§5 人工模板**（见 Review Spec）或交付「**建议核对**」列表。  
- **须**与 **六项正式验收** 至少 **一项** 交叉阅读；**须**遵守 **配对规则**（如 `lg` 须与 `pc` 或结构化 resume 字段同看）。  
- **不要求**与 soft-fail 绑定。

### 3. `critical_candidate`

- **可**列为 **future soft-fail / advisory** 的 **文档候选**；**仍不是** hard-fail。  
- **默认要求**：**多轮出现**或 **与 case 现象/六项验收可对齐**；**单轮 raw 高** **不足**单独定档。  
- **须**与 Review Spec 中 **SF-1 / SF-2 / 异常组合** 叙述 **兼容**，**不**自相矛盾。

---

## §7. 使用建议（含 M1.4 场景实压）

1. **解读顺序**：原始 `narrative_evidence_tension_review` → **本文 severity 画像** → Review Spec **配对与模板** → Calibration **是否饱和**。  
2. **禁止**：把 **`pc=high` / `lg=medium`** 直接念成「病情终判」；应说 **「当前映射为以 `review` 为主的 phase/closure 语义张力」** 等。  
3. **优先**：在交付中突出 **`pc`** 的 severity；**`sb`/`mb` 原始 high** 默认叙述为 **背景监控（watch）** 除非有 **可叙述子类**。  
4. **下一里程碑（非本轮）**：若实现 **代码级 severity 映射**，须 **单列变更集**，**仍不**自动改 benchmark。  
5. **M1.4（第十四批真实场景扩包）**：已进入场景实压；交付见 `docs/REAL_SCENARIO_PACK_M1_4_DELIVERY.md`；整包 `82` case，`severity_audit`（`watch` / `review` / `critical_candidate`）与本文 §4–§5 叙述一致；**仍不**参与 harness hard-fail。  
6. **Severity Signal Gap Review（M0）**：已完成；见 `docs/SEVERITY_SIGNAL_GAP_REVIEW_M0.md` 与 `logs/severity_signal_gap_m14_analysis.json`（**不**改变本文档位定义，仅记录当前信号瓶颈与下一阶段优先级）。

---

## §8. 是否适合作为 tension 分层画像规范

**适合**，但须与 §5 **「部分维度暂不铺满四档」** 一并阅读；**不**与 Calibration 数字矛盾。

---

## §9. 本轮是否通过

**通过。** 已形成统一四档、五维病症语义、单轮/多轮、部分适用说明与使用规则；**未**改评测与代码。

---

## 主线—白盒—日志

- 本文件为 **解读规范**；**不**替代 frame 中原始字段。  
- 白盒 / 日志仍以一帧 **同链** 事实为准；severity 为 **复盘与交付语言层**。
