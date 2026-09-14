# Real Scenario Pack M1.4 Delivery（第十四批真实场景扩包）

**文件**：`docs/REAL_SCENARIO_PACK_M1_4_DELIVERY.md`

**本轮定位**：在 **M0.6 冻结基线**、**tension 审计** 与 **`TENSION_SEVERITY_PROFILE_SPEC_M0.md` 风险画像语言** 下继续扩包；**不**将 tension / severity 接入 harness hard-fail。

**依据**：`docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md`、`docs/NARRATIVE_EVIDENCE_TENSION_REVIEW_M0.md`、`docs/TENSION_AUDIT_CALIBRATION_REVIEW_M0.md`、`docs/TENSION_REVIEW_TEMPLATE_AND_SOFT_FAIL_SPEC_M0.md`、`docs/TENSION_SEVERITY_PROFILE_SPEC_M0.md`；映射实现：`tools/tension_severity_profile_map.py`（**文档化**，不参与 `_compute_pass`）。

---

## §1. 本轮定位

第十四批在 **M1.3** 之后，新增 **R77–R82**；整包结果附带 **`severity_audit`**（`overall_severity_profile`：`none` / `watch` / `review` / `critical_candidate`），用于交付与复盘，**不**替代正式三类缺陷分类。

---

## §2. 新增 case 清单

| case_id | 方向 |
|---------|------|
| `R77_phase_outcome_overclaim_review_candidate_real` | A：review 级（phase/outcome 偏满） |
| `R78_local_progress_repeated_but_global_goal_still_weak_real` | B：局部反复 vs 全局弱 + pc/lg 配对压力 |
| `R79_memory_bias_stable_but_kept_under_watch_real` | C：个性化语义偏差稳定、观察为主 |
| `R80_summary_entry_smooth_but_backfill_still_needed_real` | D：顺滑叙事 vs backfill |
| `R81_story_more_complete_than_trace_support_real` | E：`nt` 对照锚点（启发式收紧前） |
| `R82_phase_closure_progress_pair_near_critical_candidate_real` | B：pc+lg 组合压力（命名近 critical；**实证见 §6**） |

---

## §3. 整包结果摘要

命令：

1. `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m14.json`  
2. `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m14.json --out logs/benchmark_triage_board_m14.json`

结果（`logs/real_scenario_pack_m14.json`）：

- 总 case：**82**  
- passed：**82**  
- quality：**acceptable = 82**  
- issue：**none = 82**

---

## §4. triage 摘要

来自 `logs/benchmark_triage_board_m14.json`：

- **最差 case（占位）**：`R1_container_real`、`R2_occlusion_real`、`R4_feedback_effective_real`  
- **top modules**：**—**  
- **top issues**：**—**

---

## §5. 正式问题分类（三类）

### `baseline_covered_defect`

- **本轮**：**无** 新 harness 失败。

### `baseline_excluded_requirement`

- 全局可证明性、任务引擎真实现、图书馆写入等仍为冻结外。

### `reserve_only_finding`

- 将 severity **接入** soft-fail / 自动 gate 仍为后续专题；**本轮不记为正式失败**。

---

## §6. tension + severity 观察摘要（辅助）

### 6.1 `tension_observed_but_not_failed`

- **81 / 82**（**`R3_general_search_real`** 为 snapshot，无 `narrative_evidence_tension_review`，**不**计入）。

### 6.2 `severity_audit`（`map_severity_profile_m14`，仅 passed case）

| overall | 数量（约） | 说明 |
|---------|------------|------|
| **watch** | 19 | 以 **sb/mb** 等背景监控为主、或 **pc** 为 none 且其它为 watch |
| **review** | 62 | **`pc=high` 或 `lg` 在配对下为 review** 等触发 |
| **critical_candidate** | **0** | 条件为 **同帧 `pc=high` 且 `lg=high`**；M1.4 全包 **无** 满足（与 M1.3 一致；**R82** 实证为 `lg=medium`） |
| **none** | 0 | 有 tension 的 case 均映射到 watch 以上 |

### 6.3 第十四批新增 case（R77–R82）

- **全部**映射为 **`overall_severity_profile=review`**（与多数全包 case 一致）。  
- **`nt`（R81）**：原始 **`narrative_trace_support_tension` 仍为 `none`** → 画像上 **未** 形成「叙事—证据」review 信号，**符合** Severity Profile「nt 待启发式收紧」判断。  
- **`sb`/`mb`**：在 **`per_dimension`** 中主要为 **`watch`**（背景），**不**单独升级为 review。  
- **接近 `critical_candidate`**：**无**；**R82** 命名表达意图，**当前** `lg` 未达 `high`，**不**满足 SF-1 文档组合。

---

## §7. 六项正式验收 + severity 观察

**正式六项（冻结口径）**：整包 **acceptable**，**无** harness 新失败；主导源、任务位置、记忆解释、主链 phase、summary/白盒、entry 边界在既有骨架下 **仍可通过** 工程解读。

**severity 观察（与正式六项分开写）**：

7. **进入 `review` 的通过 case**：含 **R77–R82** 及多数历史 case（**62** 例），以 **`pc`→review** 映射为主。  
8. **接近 `critical_candidate`**：**0** 例（**`pc∧lg` 同帧 high** 未出现）。  
9. **主要仍为 `watch`**：**`sb` / `mb`** 及 **`lg=medium` 且 `pc` 非 high** 时的 **`lg`**（**19** 例 overall 为 watch）。

---

## §8. 当前是否需要开 fix sprint

**不需要**（相对 harness）。若下一里程碑要 **抬高 `lg` 梯度** 或 **收紧 `nt`**，可单独立项，**非**本批扩包必开。

---

## §9. 本轮是否通过

**通过。** 第十四批扩包完成，`m14` + triage 产物齐全，**severity_audit** 已落地；**未**改 benchmark / hard-fail。

---

## 主线—白盒—日志

- 新场景经 `DecisionMonitorBuilder` 构建；**severity** 为 **pack 结果字段**，**不**回写主链。  
- **最终判断**：**主线通顺，白盒一致，日志已落地**（`logs/real_scenario_pack_m14.json`）。
