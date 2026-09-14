# Critical Candidate Pattern Review M0

**文件**：`docs/CRITICAL_CANDIDATE_PATTERN_REVIEW_M0.md`

## 一、文档定位

1. **不是**规则升级、**不是**扩包、**不是** benchmark / triage / hard-fail 修改、**不是**主骨架或 recheck 行为改写。  
2. **是**对 `logs/real_scenario_pack_m15.json` 中已出现的 **`critical_candidate`（7 例）** 的**模式复盘**：把「样本集合」整理为「可命名的模式集合」。  
3. 回答：这 7 例**是否同一种病**、哪些是**稳定共现信号**、与 **`review`** 的**关键分界**在哪、**是否足以**支撑 **future soft-fail 草案**（**不接**自动 gate）。  

**结构化只读产物**：`tools/analyze_critical_candidate_patterns_m15.py` → `logs/critical_candidate_pattern_m15.json`（与本文结论一致，可复跑）。

---

## 二、审查范围

### A. `critical_candidate` 样本（m15，7 例）

`R53_main_task_resumed_but_not_progressed_real`、`R59_multi_inserted_recovery_but_main_not_progressed_real`、`R60_recovery_declared_but_resume_chain_fragile_real`、`R83_resume_declared_main_still_not_progressed_real`、`R84_recovery_chain_repeated_and_global_goal_not_advanced_real`、`R86_resume_target_present_but_outcome_still_overclaimed_real`、`R88_inserted_recovery_resolved_locally_but_main_goal_stagnant_real`。

### B. `review` 对照（本复盘选用）

- **R85**、**R87**（用户指定）：分别代表 **`pc∧lg` 未同帧拉满** 与 **`pc` 缺席**。  
- **R82**、**R10**：**`pc=high` 且 `lg=medium`**（近邻）。  

### C. 低风险 / 基线对照

- **R3**：snapshot，**无** `narrative_evidence_tension_review`（整包中不计入 tension 计数），摘要链字段大量为空 → **低信号基线**。  
- **R1**：**`watch`**，**`pc`/`lg` 均非 high**，复杂但常态波动。

---

## 三、共同模式（7 例是否「同一种病」）

### 3.1 画像层（与 Spec 一致）

依据 `docs/TENSION_SEVERITY_PROFILE_SPEC_M0.md` 与 `tools/tension_severity_profile_map.py`：**`critical_candidate` 当且仅当** 同帧 **`phase_closure_outcome_tension=high` 且 `local_global_progress_tension=high`**（即 **`pc∧lg` raw high**）。7 例**全部**满足。

### 3.2 叙事—证据子理由（7/7 一致）

| 信号 | 7 例中出现频次 |
|------|----------------|
| `tension` **`lg` 子理由** `resume_fragility_declared_main_not_progressed` | **7/7** |
| `tension` **`pc` 子理由** 含 `closure_semantics_misalignment=phase_repair_visible_but_closure_still_none` | **7/7** |
| **`run_summary_reference.resume_chain_fragility_summary`** = `resume_declared_but_main_not_progressed` | **7/7** |
| **`task_chain_progress_summary`** 含 **`resume_main_align=`** | **7/7** |
| **`task_chain_progress_summary`** 含 **`global_main_progress_not_terminal_complete`** | **7/7** |
| **`task_chain_progress_summary`** 含 **`local_only_risk=yes`** | **7/7** |
| **`process_observation_summary`** 含 **`resume_frag=resume_declared_but_main_not_progressed`** | **7/7** |

**结论**：7 例在 **tension 标签 + run_summary/TCS 摘要链** 上**不是松散拼凑**，而是同一语义族：**「已声明 resume / 主链仍卡在子任务或未定 terminal，且 closure 与 outcome 不同步」**。

### 3.3 子簇（定性）

- **主模式（覆盖 7/7）**：**`resume_declared_but_main_not_progressed` × `phase_closure_stall`** — 记作工程名 **`resume_fragility_with_global_main_stall`**。  
- **次要差异（非分裂为另一病种）**：**`m11x_ctx_observed`** 在 **5/7** 出现（**R53、R59** 无）；二者仍为同一 tension 主因，差异来自 **ctx 显式锚点是否进入 process_observation**，**不**改变 **`pc∧lg` high** 的共因。

---

## 四、与 `review` 的关键区别

### 4.1 为什么 **R85** 只是 `review`

- **raw**：**`lg=medium`**（非 high）→ **不满足** `map_severity_profile_m14` 的 **`pc∧lg` 双高**门槛。  
- **摘要链**：**`resume_chain_fragility_summary=none`**，`task_resume_target` 在 OSI 侧为 **空**；**`lg` 子理由**为 **`progress_language_or_structure_but_main_not_reached`**，**非** `resume_fragility_declared_main_not_progressed`。  
- **升级条件归纳**：仅有 **closure/outcome 张力** + **推进语言「像前进但主未达」** → 停在 **`review`**；**缺少** **resume 脆弱性 + lg raw high** 的**同帧共现**。

### 4.2 为什么 **R87** 只是 `review`（健康复杂对照）

- **raw**：**`pc=none`** → **即使** `lg=high`，画像上 **`lg` 维度映射为 `review`**（见 `tension_severity_profile_map.py`：**`lg=high` 且 `pc≠high` → per-dim lg 为 `review`**），**整体** **`overall` 不为 `critical_candidate`**。  
- **摘要链**：**`mainline_state`/`terminal=found`**，**`task_chain_progress_summary` 无** **`global_main_progress_not_terminal_complete`**  token（与 7 例 critical 的「全局未收口」摘要**脱钩**）；**`closure_semantics_misalignment_summary=none`**。  
- **结论**：**`pc` 缺席**或 **全局已 terminal 对齐** 时，**不会** 被抬到 **`critical_candidate`** — **误报风险可控**。

### 4.3 **R82 / R10**（`pc=high`、`lg=medium`）

- 与 **R85** 同类：**`lg` 未达 raw high** → **只能 `review`**。  
- **`resume_chain_fragility_summary`** 为 **`none`**，与 7 例 **rsr 非空** 形成对照。

### 4.4 升级边界（工程化表述）

| 条件 | 结果 |
|------|------|
| **`pc` raw high + `lg` raw high** | 满足 Spec 下 **`critical_candidate`** **必要**条件 |
| **`resume_chain_fragility_summary`** = **`resume_declared_but_main_not_progressed`** 且 **TCS/tcp** 含 **global 未 terminal / resume_main_align** | 7 例 **充分共现**（与 tension 子理由互证） |
| **`lg` 降为 medium** 或 **`pc` 降为 none** | **至多 `review`**（**R85/R82/R10/R87**） |

---

## 五、误报风险

1. **健康复杂样本会不会被推成 `critical`？** **R87** 显示：**不会** — 关键在 **`pc` 不为 high** 且 **terminal/closure 与全局推进摘要** 与「停滞族」**不一致**。  
2. **仅有 closure 错位、无 resume 脆弱性？** **R85/R82** 类：**`rsr` 为 none**，**`lg` 多为 medium** → **review**。  
3. **残余风险**：**`lg` 启发式**仍可能在**真·健康但叙事冗长**场景上给出 **high**（需靠 **`pc`** 与 **摘要链 terminal** 交叉验证）；本轮 **R87** 已作为**显式对照**。

---

## 六、是否已形成稳定模式 & soft-fail 草案

### 1. 是否稳定？

**是。** 7 例共享**同一 tension 子理由 + 同一 `resume_chain_fragility` + 同一 tcp token 族**，**非** 7 种无关组合的偶然 `pc∧lg` high。

### 2. 推荐模式名

- **主模式**：**`resume_fragility_with_global_main_stall`**（resume 已声明 / 主未真正推进 + phase–closure 与 outcome 错位）。  
- **可选子标签**（非独立病种）：**`m11x_ctx_observed`**（ctx 锚点显式进入过程观察）。

### 3. Future soft-fail 草案是否值得启动？

**可以启动草案**（**仍不**自动接入评测）：  
- **触发候选** 可描述为：**`pc∧lg` raw high** 且 **`resume_chain_fragility_summary=resume_declared_but_main_not_progressed`** 且 **tcp 含 `global_main_progress_not_terminal_complete`**（与人审模板对齐）。  
- **下一步**建议：在 **`TENSION_REVIEW_TEMPLATE_AND_SOFT_FAIL_SPEC_M0.md`** 中增加**一节**「**M0 critical 模式 — resume_fragility_with_global_main_stall**」，**不**改代码。

### 4. 本文是否适合作为 critical pattern 复盘收口？

**适合。** 有 **pack 实证 + JSON 结构化复现 + 正/近邻/低风险对照**。

---

## 七、本轮是否通过

**通过。** 完成模式命名、分界、误报与草案建议；**未**改 benchmark / 规则 / 主链。

---

## 主线—白盒—日志 串联检查

- **A 主线**：复盘**只读** pack 与重建 frame 摘要，**不**改决策。  
- **B 白盒**：模式与 **`task_chain_progress_summary` / `process_observation_summary`** 同源。  
- **C 日志**：`logs/real_scenario_pack_m15.json`、`logs/critical_candidate_pattern_m15.json`。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。
