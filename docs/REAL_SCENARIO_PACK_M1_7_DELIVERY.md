# Real Scenario Pack M1.7 Delivery（第十七批真实场景扩包）

**文件**：`docs/REAL_SCENARIO_PACK_M1_7_DELIVERY.md`

## §1. 本轮定位

1. **M1.7** 仍属 **M1.x 主线扩包**：在 **`MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6`** 冻结口径下，持续验证 **正式 harness 层**、**tension / severity 画像层**、**advisory（SF-1′）观察层** 三路并行且 **互不替代、不接自动 fail/gate**。  
2. **当前优先级**：把 **`baseline_covered_defect` / `baseline_excluded_requirement` / `reserve_only_finding`** 三类正式归档与 **severity / advisory 辅助观察** 在 **更多真实场景** 下压稳。  
3. **明确不做**：军工级自治闭环、运行态切换设计、图书馆/记忆正式写入、任务链深机制、recheck/closure 行为修改、benchmark & triage 规则修改、advisory 接 block。  
4. **依据**：`docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md`、`docs/TENSION_SEVERITY_PROFILE_SPEC_M0.md`、`docs/ADVISORY_REVIEW_GATE_DRAFT_M0.md`、`docs/ADVISORY_OBSERVATION_INTEGRATION_M0.md`、`docs/REAL_SCENARIO_PACK_M1_6_DELIVERY.md`。

补记：已进入 **M1.x Baseline Consolidation Review**（`docs/M1X_BASELINE_CONSOLIDATION_REVIEW.md`）。

---

## §2. 新增 case 清单

| case_id | 压测方向 |
|---------|----------|
| `R95_advisory_candidate_resume_fragility_repeated_real` | **A**：SF-1′ **正样本**（resume 脆弱性 + 多轮路径，续压 M1.6-A） |
| `R96_advisory_near_miss_resume_present_but_fragility_insufficient_real` | **B**：**近邻**（与 **R90** 同构：`pc` 高、`lg` **medium**，**不**构成 `pc∧lg` raw high；叙述层仍可谈 resume/主链） |
| `R97_complex_recovery_chain_but_terminal_aligned_real` | **C**：**健康复杂**（与 **R91** 同构：`terminal=found`，树质量 **acceptable**） |
| `R98_global_stall_visible_but_closure_not_overclaimed_real` | **B/D**：**全局停滞叙事 + lg 中档**，`severity=review`，**不**命中 advisory |
| `R99_advisory_candidate_with_entry_summary_alignment_real` | **A/D**：SF-1′ **正样本**，用于观察 **scenario 文案** 与 **summary/advisory reason** 同向（`post_processing_summary_entry` 仍守契约边界） |
| `R100_high_tension_review_only_not_advisory_real` | **E**：**高张力仅 review**：`pc` 高、`lg` **medium**，**无** `rsr=resume_declared_but_main_not_progressed`，advisory **未命中** |

**工程注记（ctx 迭代）**：`R96` 首轮曾叠加 `task_resume_target` + `search_subtask_state=main` 以外的组合，曾 **误触发** SF-1′；已改为 **R90 等价结构** 以保证「近邻」稳定。**`R97`** 首轮曾因 **过长 resolution_path** 导致 `blocked` + **`quality_grade=poor`** 不达标；已改为 **R91 等价结构** 以保证 harness 全绿。

---

## §3. 整包结果摘要

命令：

1. `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m17.json`  
2. `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m17.json --out logs/benchmark_triage_board_m17.json`

| 指标 | 数值 |
|------|------|
| 总 case | **100**（`m16`：**94** + 本批 **6**） |
| passed | **100 / 100** |
| quality | **acceptable = 100** |
| issue（`issue_type`） | **none = 100** |
| `tension_observed_but_not_failed` | **99 / 100**（**`R3_general_search_real`** 仍无 tension 块，与历史一致） |

---

## §4. triage 摘要

来自 `logs/benchmark_triage_board_m17.json`：

- **最差 case（占位/low）**：`R1_container_real`、`R2_occlusion_real`、`R4_feedback_effective_real`（规则未改，仍为质量占位排序）。  
- **top modules**：**—**  
- **top issues**：**—**

---

## §5. 正式问题分类（三类）

### `baseline_covered_defect`

- **本轮**：**无**（整包 harness **全通过**）。

### `baseline_excluded_requirement`

- 全局可证明性、真任务引擎、图书馆写入等仍为冻结外需求。

### `reserve_only_finding`

- **SF-1′ / advisory**、severity **`critical_candidate`** 等仍为 **reserve / 观察**，**不**记为正式 harness 失败。

---

## §6. tension / severity 观察摘要

- **severity**（`summary.severity_audit`）：**watch = 19**，**review = 69**，**`critical_candidate` = 11**（`m16`：**9** → 本批 **`R95`、`R99`** 进入 **critical**，与 SF-1′ **正样本**一致）。  
- **本批 severity**：`R95`、`R99` → **`critical_candidate`**；`R96`、`R98`、`R100` → **review**；`R97` → **review**（lg 维 **high** 但聚合画像为 **review**，与 **R91** 族一致）。  
- **`tension_observed_but_not_failed`**：延续「**只观察、不 fail**」策略。

---

## §7. advisory / review 候选观察摘要（SF-1′）

来源：`summary.advisory_sf1_prime_audit`（与 frame 顶层 `advisory_review_observation` / pack 附加字段 **同逻辑**）。

| 指标 | 数值 |
|------|------|
| **`soft_fail_candidate_observed`（SF-1′）命中数** | **11** |
| **与 `critical_candidate` 交集** | **11**（**完全一致**） |
| **仅 advisory 非 critical** | **0** |
| **仅 critical 非 advisory** | **0** |

**本批个案**：

- **`R95`、`R99`**：**命中** SF-1′ 且 **`critical_candidate`**（**2** 条正样本，符合本轮 **A**）。  
- **`R96`、`R98`、`R100`**：**未命中**（**近邻 / review-only**；排除 **lg raw high** 或 **rsr/tcp** 缺一）。  
- **`R97`**：**未命中**（**健康 terminal**；`exclusion` 与 **R91** 同源：`pc_not_high`、`tcp_missing_global...`）。  
- **summary / entry / advisory**：在 **`R99`** 上：`tension`·`lg` **high** + `rsr`/`tcp` 与 **`soft_fail_candidate_reason_summary`** **同指**「停滞 + resume 脆弱 + 主链未至终局」；**未**发现观察层 **反义**（仅 **backfill/sb** 高为契约层提示，**非** advisory 触发）。

---

## §8. 六项正式验收 + tension/severity + advisory 观察

1. **主导源是否讲得清**：**是**（整包仍走统一 builder / 调度侧摘要链）。  
2. **任务位置是否讲得清**：**是**（`task_chain_state_snapshot` / `run_summary_reference` 可复读）。  
3. **记忆调用/偏差是否讲得清**：**是**（`memory_invocation_explanation` + tension `mb` 维仍可读）。  
4. **主链状态/阶段是否讲得清**：**是**（`mainline_state_snapshot` + narrative 张力仍可对齐）。  
5. **Summary / Narrative / 白盒是否同口径**：**是**（无 harness 断裂；**sb 高** 仍为 backfill 提示，**不接** fail）。  
6. **后处理入口边界是否守住**：**是**（未扩写后处理裁决）。  

**辅助三层**：  
7. **severity**：**watch / review / critical_candidate** 分布与 **m16** 延续，本批 **critical +2** 均与 **SF-1′** 同集合。  
8. **advisory**：正样本 **稳定命中**；**近邻/健康/对照** **未误标**。  
9. **summary / entry / advisory 同向**：**R99** 抽样 **一致**；其余命中族与 **m16** 行为一致。

---

## §9. 当前是否需要开 fix sprint

**不需要**（相对 **harness / 冻结主线**）。**`R96`/`R97` ctx** 已就地收敛为 **R90/R91 证明结构**，避免误触发 SF-1′ 或 **quality_floor** 失败；若未来要 **专门折磨**「`task_resume_target` + `main` mode」的 **更不透明** 边界，可另立 **扩包批次**（**非**本批必开）。

---

## §10. 本轮是否通过

**通过。** 第十七批扩包完成，`m17` + triage + **`advisory_sf1_prime_audit`** 产物齐全；**100/100** 场景 **`scenario_passed`**；**未**改 benchmark/triage 规则；**未**接 advisory 自动 gate；**advisory 与 `critical_candidate` 仍 1:1 同轨（11=11）**。

---

## 主线—白盒—日志 串联检查

- **A 主线**：新场景仍经 **`DecisionMonitorBuilder`** 主路径；advisory 为 **同帧只读派生**（frame + pack 摘要一致）。  
- **B 白盒**：`narrative_evidence_tension_review` / `severity_profile` / **`advisory_sf1_prime_observation`** 均锚定 **同一 `run_summary_reference` 与 tcp/rsr**。  
- **C 日志**：`logs/real_scenario_pack_m17.json`、`logs/benchmark_triage_board_m17.json` 已落盘。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。
