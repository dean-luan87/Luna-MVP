# Resume / Closure Signal Alignment Review M0

**文件**：`docs/RESUME_CLOSURE_SIGNAL_ALIGNMENT_REVIEW_M0.md`

## 一、文档定位

1. **不是**功能开发，**不是** `lg` 再 tightening，**不是** `pc` 启发式调整，**不是** benchmark / 主骨架 / recheck 行为修改。  
2. 本轮是对 **`resume / closure / main progress`** 在 **同帧、可消费摘要** 中为何**无法稳定对齐**的审查，用于解释：在 **`lg` 已拉开梯度** 的前提下，**`pc=high ∧ lg=high` 仍为 0** 的工程根因。  
3. 结构化数据：`logs/resume_closure_signal_alignment_m14.json`（`tools/analyze_resume_closure_signal_alignment_m14.py` 只读生成）；整包与梯度对照仍见 `logs/real_scenario_pack_m14.json`、`logs/local_global_gradient_analysis_m14.json`、`logs/severity_signal_gap_m14_analysis.json`。

---

## 二、聚合事实（81 个真实 ctx，当前主链构建）

| 指标 | 数量 | 说明 |
|------|------|------|
| ctx 层带 **`task_resume_target` 或 `recovery_declared_but_resume_chain_fragile_expected`** | **5** | 场景 JSON 已写意图 |
| **`task_chain_state_snapshot.task_resume_target` 非空** | **1** | 与上项严重不同步 |
| **`resume_chain_fragility_summary` 含 `resume_declared_but_main_not_progressed`** | **1** | 与 `lg=high` 强绑定 |
| **`process_observation_summary` 含 `m11x_ctx_observed`** | **0** | 设计上的「ctx 锚点」前缀从未出现 |
| **`pc=high`** | **61** | 主要来自 **`closure_semantics_misalignment_summary`** |
| **`lg=high`** | **1** | 同上强 resume 子串 |
| **`pc=high ∧ lg=high`** | **0** | — |

**结论预览**：断裂主要不在 **tension 读错字段**，而在 **更上游：`run_summary_reference` 内 `resume_chain_fragility_summary` / `process_observation` 与 ctx、task_chain 不同步**。

---

## 三、信号链分层：resume

### 3.1 各层有什么

| 层 | resume / 恢复相关 |
|----|-------------------|
| **ctx（场景 JSON）** | 部分 case 含 **`task_resume_target`**、**`recovery_declared_but_resume_chain_fragile_expected`**（仅文档/测试意图，**未**保证进入 frame） |
| **`frame.inputs`** | **标准遥测字段**；**不含**上述 expected 类 flag（聚合为 **0 条 `m11x_ctx_observed`**） |
| **`task_chain_state_snapshot`** | **`task_mode` / `task_chain_stage` / `task_resume_target`**；后者多由 **object_search** 等 **主链推导**，**与 ctx 字符串 resume 常不一致** |
| **`run_summary_reference`** | **`task_chain_progress_summary`**（结构化一行）、**`resume_chain_stage_summary`**、**`resume_chain_fragility_summary`**、**`resume_chain_progress_reached_main`**、**`process_observation_summary`** |
| **`mainline_narrative_alignment` / `summary_brief` / `mainline_narrative_brief`** | 将 task/source 等 **拼进叙事**；**「主任务未真正到位」** 多为 **隐式**（stage/mode/subtask），**非**独立强句 |
| **`post_processing_summary_entry.narrative_readable`** | 再经 **post_processing** 塑形；**可读性高** 常与 **backfill 契约** 同显，易 **顺滑** |
| **`narrative_evidence_tension_review`（lg）** | 读 **`rsr`** + **`task_chain_progress_summary`** 等；**`lg=high`** 强路径依赖 **`resume_chain_fragility_summary`** 中 **`resume_declared_but_main_not_progressed`** 或 **结构叠加**（见 Local-Global M0） |

### 3.2 哪里断了

1. **ctx → `task_chain_state_snapshot.task_resume_target`**  
   - 例：**R60** ctx 含 **`task_resume_target: resume_main_search_route`** 与 **`recovery_declared_but_resume_chain_fragile_expected: true`**，但 **TCS `task_resume_target` 为 `null`**。  
   - **`run_summary_builder._build_process_observation`** 中 **`resume_frag`** 需 **`resume_target`（来自 TCS）** 为真且 **`task_mode` ∈ {subtask, recovering, inserted}** 等才会设为 **`resume_declared_but_main_not_progressed`**；**TCS 无 target → `resume_chain_fragility_summary` 恒为 `none`**。  
   - **这是「inputs/summary 链」与「场景意图」的硬断点**，不是 tension 读错。

2. **ctx expected flags → `inputs` → `m11x_ctx_observed`**  
   - **`_build_process_observation`** 仅在 **`frame.inputs`** 上出现 **`recovery_declared_but_resume_chain_fragile_expected` 等** 时，为 **`process_observation_summary` 加 `m11x_ctx_observed` 前缀**。  
   - **DecisionMonitorBuilder 不把 ctx 顶层 flag 写入 `inputs`** → **全包 0 次 m11x 前缀** → **tension / 人工锚点** 都看不到「ctx 声明的脆弱恢复」。

**判定**：**resume 强信号**当前**最强**仍在 **task_chain + OSI 推导**；**ctx 与 TCS 的 resume 语义**、**expected flag**，**没有稳定进入同帧 `run_summary_reference` 的可消费字段**。

---

## 四、信号链分层：closure

### 4.1 各层有什么

| 层 | closure 相关 |
|----|----------------|
| **`mainline_state_snapshot.mainline_phase`** | **recheck_or_repair / closure** 等，与 terminal 等共用于 **phase 语义** |
| **`run_summary_reference.closure_semantics_misalignment_summary`** | 由 **phase + terminal + recheck** 等推导（如 **`phase_repair_visible_but_closure_still_none`**） |
| **`process_observation_summary`** | **`phase_closure=...`**，可与上同向 |
| **`summary_brief` / `mainline_narrative_brief`** | **长串拼接**；closure 与 task/source **混在一行**，**偏「阶段/口径」叙述** |
| **`post_processing_summary_entry.narrative_readable`** | **入口可读**强，**不保证**单独展开「恢复已声明但主目标未前进」 |

### 4.2 语义偏置

- **closure 当前更强表达「阶段/收口机制是否一致」**（**pc** 侧），**不是**「主任务结果已达成」。  
- **与 resume/main progress 的「结果层」** 常在 **不同子串**；**narrative** 层又 **压缩** 为统一 brief → **「恢复脆弱 + 主未推进」细语义** 易被 **压平**。

---

## 五、main progress 为何不足以单独抬高 `lg`

- **「主任务未真正到位」** 在 **`task_chain_progress_summary`** 中多体现为 **`main_push_hint=mixed`、`local_only_risk=yes`、`mode=subtask`** 等 **结构化 token**（Local-Global M0 已用其区分 **medium / low / high**）。  
- **`resume_chain_fragility_summary` 强子串** 仍依赖 **TCS `task_resume_target` 非空** 等条件；**该路不通时**，**`lg` 很难到 `high`**，即便 **pc 已为 high**。  
- 故：**不是**「main progress 语言完全不存在」，而是 **「强 resume 声明」与「closure 强错位」不同步进入 **同一套 rsr 强字段****。

---

## 六、同帧对齐与压缩损失（A–D）

### A. 信号出现层级图

- **closure 错位**：在 **`closure_semantics_misalignment_summary`** 与 **`process_observation` 的 phase_closure** 中 **高频、稳定**。  
- **resume 强声明**：在 **ctx** 中 **偶发**；在 **`resume_chain_fragility_summary`** 中 **几乎仅 1 例**（与 **`lg=high`** 同现）。  
- **「只在 process 里能讲、summary 未单独带走」**：**m11x 设计**本为补此洞，但 **因 inputs 无 flag** → **全包 0**。

### B. 同帧对齐

- **closure（pc）与 task 结构（lg）** 常 **同帧存在**（如 R82/R60：**pc=high，lg=medium**）。  
- **resume 强 frag（`resume_chain_fragility_summary`≠none 的强形式）与 pc=high** **几乎不同帧**：**强 frag 依赖 TCS resume**，**pc 高依赖 closure 字符串**；**二者来源独立**，**未**在 rsr 层 **强制共显为「双高」**。

### C. 压缩损失点

- **`summary_brief` / `mainline_narrative_brief`**：信息 **混排**，**主任务未推进** 少 **独立句**。  
- **`post_processing_summary_entry`**：**可读性与 backfill** 并行，**更易「顺」** 而 **不突出** 全局停滞。  
- **最大损失点**：**ctx resume / expected → TCS / inputs**（**未进可消费摘要**），其次才是 narrative 压缩。

### D. `pc∧lg=0` 根因（排序）

1. **信号缺失 / 不同步（主因）**：**TCS `task_resume_target` 与 ctx 不一致** → **`resume_chain_fragility_summary` 强形式几乎不出现** → **`lg` 难到 high**。  
2. **inputs 与 run_summary 契约**：**expected flags 未进 `inputs`** → **m11x 锚点 0** → **无法用轻量规则对齐「场景意图」与 rsr**。  
3. **规则定义（次因）**：**`critical_candidate` 要求 `pc∧lg` 同帧 raw high**；在 **(1)(2)** 未解决前，**结构上仍易为 0**。  
4. **非** tension 读错 `summary_reference_applied` 或 **lg 公式单点 bug**（Local-Global 已验证）。

---

## 七、焦点样本（摘录，详见 JSON）

| 样本 | ctx | TCS `task_resume_target` | `resume_chain_fragility_summary` | pc | lg |
|------|-----|--------------------------|-----------------------------------|-----|-----|
| **R82** | `recovery…=true`，phase misalign expected | **null** | **none** | high | medium |
| **R60** | `task_resume_target` + recovery expected | **null** | **none** | high | medium |
| **R53** | `task_resume_target` 有 | **null** | **none** | high | medium |
| **R1**（lg low 对照） | 无 recovery | — | **none** | none | low |
| **R4** | （使 TCS/rf 对齐） | （使 **rf** 强） | **含强子串** | none | **high** |

---

## 八、下一阶段优先级（必须排序）

### 第一优先级：**补 `run_summary_reference` / `task_chain` 与叙事中对「主任务未真正推进 / resume 目标有效」的显式、同帧可消费表达**

- **重点**：让 **`task_resume_target`（或等价字段）** 在 **TCS** 与 **`resume_chain_fragility_summary`** 中与 **主链事实** 一致，或 **单独增加** 一行 **「global main progress: not_reached」** 类 **derived** 摘要（仍须派生自已存在字段，符合 run_summary 定位）。  
- **理由**：**`lg` 已依赖 rsr**；当前 **断在 ctx→TCS→rf**，补这层 **收益最大**。

### 第二优先级：**再看 `post_processing_summary_entry` 是否对「全局停滞」压得过平**

- **在** run_summary **已能显式表达** 后，再审 **entry** 是否 **过度顺滑** 掩盖 **main progress**。  
- **理由**：否则先改 entry 容易 **与契约层缠斗**。

### 明确不优先（本轮结论）

- **继续改 `lg` 规则本身**（Local-Global M0 已收口一轮）。  
- **提前动 `nt`**（仍为第二梯队）。

---

## 九、与用户预期方向的对照

- **预期「先补 run_summary / task_chain / narrative 显式 main progress」** → **与数据一致**（**第一优先级**）。  
- **预期「再看 post_processing 压缩」** → **作为第二优先级** 成立。

---

## 十、本轮是否适合作为信号对齐复盘文档

**适合。** 有 **聚合统计**、**分层表**、**断点归因**、**焦点样本**、**主次优先级**。

---

## 十一、本轮是否通过

**通过。** **只读审查** + 分析脚本与 JSON 产物；**未**改 benchmark、主骨架、recheck、**未**改 `lg`/`nt` 规则。

---

## 主线—白盒—日志

- **主线**：未改主链。  
- **白盒**：审查对象与 **run_summary / task_chain** 同链。  
- **日志**：`logs/resume_closure_signal_alignment_m14.json`。  
- **最终判断**：**主线通顺，白盒一致，日志已落地**。

---

## 补记（Resume Progress Summary Alignment M0）

后续已落地 **`docs/RESUME_PROGRESS_SUMMARY_ALIGNMENT_M0.md`**（**ctx→inputs→TCS→run_summary** 摘要链补强）；**§七 焦点样本表** 中 **R60/R53** 等「**TCS null / rf none**」状态已随该 sprint **更新**（见新交付文与 **`logs/real_scenario_pack_m14.json`**）。
