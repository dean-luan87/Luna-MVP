# Real Scenario Pack M1.5 Delivery（第十五批真实场景扩包）

**文件**：`docs/REAL_SCENARIO_PACK_M1_5_DELIVERY.md`

## §1. 本轮定位

1. **resume-progress 摘要链补强**（`docs/RESUME_PROGRESS_SUMMARY_ALIGNMENT_M0.md`）之后的**首次整包扩包验证**：观察 **`run_summary` / TCS / process_observation** 与 **`pc`（phase_closure_outcome）`、`lg`（local_global_progress）** 在更多复杂场景下是否**稳定同帧可读**。  
2. **正式问题判断**仍服从 **M0.6 冻结口径**（`docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md`）：**不**将 **`critical_candidate`** 或 tension 接入 harness hard-fail。  
3. **tension / severity**（`docs/TENSION_SEVERITY_PROFILE_SPEC_M0.md`）仅为**辅助观察层**：`tension_observed_but_not_failed`、`watch`、`review`、`critical_candidate`；其中 **`critical_candidate` 仍不是正式失败**，仅表示**接近未来 soft-fail 候选**的工程画像。

**依据**：`docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md`、`docs/TENSION_SEVERITY_PROFILE_SPEC_M0.md`、`docs/RESUME_PROGRESS_SUMMARY_ALIGNMENT_M0.md`；前置整包 `logs/real_scenario_pack_m14.json`（对齐后已出现非零 **`pc∧lg` high** 与 **`critical_candidate`**）。

---

## §2. 新增 case 清单

| case_id | 压测方向 |
|---------|----------|
| `R83_resume_declared_main_still_not_progressed_real` | **A**：恢复已声明 + 主任务仍未推进 |
| `R84_recovery_chain_repeated_and_global_goal_not_advanced_real` | **C**：多轮恢复 / 全局未前进 |
| `R85_phase_closure_progress_pair_reappeared_real` | **B/D**：`pc+lg` 再施压（与 **R82** 同族；实证见 §6） |
| `R86_resume_target_present_but_outcome_still_overclaimed_real` | **D**：resume / closure / outcome 复合张力 |
| `R87_complex_but_healthy_resume_and_global_progress_real` | **E**：复杂但**健康对照**（避免本批「全盘 critical」） |
| `R88_inserted_recovery_resolved_locally_but_main_goal_stagnant_real` | **C**：inserted + 局部恢复成立、主目标停滞 |

**输入**：`tests/real_scenarios/ctx/R83_*` … `R88_*`；注册于 `tools/real_scenario_pack.py`。

---

## §3. 整包结果摘要

命令：

1. `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m15.json`  
2. `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m15.json --out logs/benchmark_triage_board_m15.json`

结果（`logs/real_scenario_pack_m15.json`）：

- 总 case：**88**（`m14`：**82** + 本批 **6**）  
- passed：**88**  
- quality：**acceptable = 88**  
- issue：**none = 88**

---

## §4. triage 摘要

来自 `logs/benchmark_triage_board_m15.json`：

- **最差 case（占位）**：`R1_container_real`、`R2_occlusion_real`、`R4_feedback_effective_real`（与既有 triage 规则一致；**无** harness 级 issue 分层时模块/issue 为空）  
- **top modules**：**—**  
- **top issues**：**—**  
- **next_focus**：`R1`、`R2`、`R3`（占位）

---

## §5. 正式问题分类（三类）

### `baseline_covered_defect`

- **本轮**：**无** 新 harness 失败（整包仍 **acceptable / issue none**）。

### `baseline_excluded_requirement`

- 全局可证明性、任务引擎真实现、图书馆写入、污染深实现等仍为冻结外。

### `reserve_only_finding`

- 将 **`critical_candidate`** 或 tension 接入 **soft-fail / 自动 gate** 仍为后续专题；**本轮不记为正式失败**。

---

## §6. tension + severity 观察摘要（辅助）

### 6.1 `tension_observed_but_not_failed`

- **87 / 88**（**`R3_general_search_real`** 为 snapshot，无 `narrative_evidence_tension_review`，**不**计入）。

### 6.2 `severity_audit`（仅 passed case）

| overall | m15 数量 | m14 数量 | 说明 |
|---------|----------|----------|------|
| **watch** | **19** | **19** | 持平 |
| **review** | **61** | **59** | +2（本批 **R85**、**R87**） |
| **critical_candidate** | **7** | **3** | **上升**（见下表）；**仍非** harness fail |
| **none** | 0 | 0 | — |

### 6.3 `case_ids_critical_candidate`（m15）

与 **`m14`** 相比，**保留** 原 **3** 例，**新增** **4** 例（均为本批刻意加压的 **resume / global stagnation** 族）：

- **沿用**：`R53_main_task_resumed_but_not_progressed_real`、`R59_multi_inserted_recovery_but_main_not_progressed_real`、`R60_recovery_declared_but_resume_chain_fragile_real`  
- **新增**：`R83_resume_declared_main_still_not_progressed_real`、`R84_recovery_chain_repeated_and_global_goal_not_advanced_real`、`R86_resume_target_present_but_outcome_still_overclaimed_real`、`R88_inserted_recovery_resolved_locally_but_main_goal_stagnant_real`

### 6.4 `pc=high ∧ lg=high`（同帧 tension brief）

与 **`critical_candidate`** 计数一致：**7** 例（上表 **7** 个 case_id）；**`m14` 为 3 例**。说明在 **摘要链补强 + 本批场景设计** 下，**`pc∧lg` 配对从「少量旧 case」扩展为「同一语义族可重复出现」**，但仍需与人审 **soft-fail** 模板对照，**不**自动升格为正式缺陷。

### 6.5 本批个案（`pc` / `lg` / severity）

| case | 方向 | `tension_review_brief`（节选） | `overall_severity_profile` |
|------|------|-------------------------------|----------------------------|
| **R83** | A | `pc:high` … `lg:high` | **critical_candidate** |
| **R84** | C | `pc:high` … `lg:high` | **critical_candidate** |
| **R85** | B/D | `pc:high` … `lg:medium` | **review**（**未**进 critical；**lg** 未同帧 high） |
| **R86** | D | `pc:high` … `lg:high` | **critical_candidate** |
| **R87** | E 健康 | `pc:none` … `lg:high` | **review**（**未**进 critical；**无** `pc∧lg`） |
| **R88** | C | `pc:high` … `lg:high` | **critical_candidate** |

### 6.6 `nt`（叙事—证据）

- 在 **87** 条有 tension 的 case 中，brief 仍为 **`nt:none`** 占满 → **区分力仍弱**；**本轮只观察，不处理**（与 `SEVERITY_SIGNAL_GAP_REVIEW_M0` 结论一致）。

---

## §7. 六项正式验收 + severity 观察

**正式六项（冻结口径）**：整包 **acceptable**，**无** harness 新失败；在既有骨架下 **主导源、任务位置、记忆解释、主链 phase、summary/白盒同口径、后处理 entry 边界** 仍可通过工程解读（与 `m14` 一致）。

**severity 观察（与正式六项分开写）**：

7. **`critical_candidate` 模式**：由 **3 → 7**，**新增 4 例**与**旧 3 例**同属 **「resume/全局推进/closure 张力」** 语义族；**开始呈现可重复性**，但仍**不接**正式 fail。  
8. **`pc + lg` 复现性**：**`pc∧lg` high** 与 **`critical_candidate`** **同数**（**7**），**R85** 显示 **`lg=medium`** 时 **不会** 误抬到 critical → **梯度**仍在起作用。  
9. **健康复杂样本**：**R87** 为 **`review`**（**`pc:none`、lg high**），**未**进入 **`critical_candidate`** → **未**过拟合为「全批 critical」。

---

## §8. 当前是否需要开 fix sprint

**不需要**（相对 harness / 冻结基线）。若下一里程碑要 **收紧 `nt`**、或 **人审 soft-fail 候选池**，可单独立项；**非**本批扩包必开。

---

## §9. 本轮是否通过

**通过。** 第十五批扩包完成，`m15` + triage 产物齐全；**未**改 benchmark / triage 规则；**未**将 **`critical_candidate`** 接入 hard-fail。

---

## 主线—白盒—日志 串联检查

- **A 主线**：新场景经 **`DecisionMonitorBuilder`** 构建；**severity** 为 **pack 摘要字段**，**不**回写主链拍板。  
- **B 白盒**：与 **task_chain / process_observation / run_summary** 同链可读；**R87** 等对照样本 **未** 被 severity 误杀为 critical。  
- **C 日志**：`logs/real_scenario_pack_m15.json`、`logs/benchmark_triage_board_m15.json` 已落地且一致。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。
