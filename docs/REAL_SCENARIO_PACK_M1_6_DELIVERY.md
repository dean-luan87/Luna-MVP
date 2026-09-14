# Real Scenario Pack M1.6 Delivery（第十六批真实场景扩包）

**文件**：`docs/REAL_SCENARIO_PACK_M1_6_DELIVERY.md`

## §1. 本轮定位

1. **M1.6** 在 **M0.6 冻结基线**、**tension / severity** 辅助层之上，**首次**把 **`SF-1′` advisory / 人审高风险候选** 纳入**场景扩包观察**（pack 摘要字段 **`advisory_sf1_prime_audit`**，与 `tools/real_scenario_pack.py` 同帧计算）。  
2. **正式问题判断**仍只服从三类：**`baseline_covered_defect`** / **`baseline_excluded_requirement`** / **`reserve_only_finding`**；**advisory 不参与** harness pass/fail、**不**接自动 gate。  
3. **依据**：`docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md`、`docs/TENSION_SEVERITY_PROFILE_SPEC_M0.md`、`docs/ADVISORY_REVIEW_GATE_DRAFT_M0.md`、`docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md`、`docs/SOFT_FAIL_CANDIDATE_VALIDATION_PACK_M0.md`、`docs/CRITICAL_CANDIDATE_PATTERN_REVIEW_M0.md`、`docs/REAL_SCENARIO_PACK_M1_5_DELIVERY.md`。

---

## §2. 新增 case 清单

| case_id | 方向 |
|---------|------|
| `R89_advisory_candidate_resume_fragility_global_stall_real` | **A**：advisory **正样本**（resume + 全局停滞） |
| `R90_advisory_candidate_near_miss_pc_high_lg_medium_real` | **B**：**近邻**（pc 高、lg 中） |
| `R91_complex_resume_chain_but_healthy_terminal_real` | **C**：**健康复杂**（terminal=found） |
| `R92_critical_like_pattern_but_missing_resume_fragility_real` | **D**：severity/advisory **偏差**（近 critical、`rsr` 不经由 SF-1′） |
| `R93_global_stall_repeated_but_closure_still_not_overclaimed_real` | **E**：主模式**轻量变体**（closure 标志与 R89 族差异） |
| `R94_phase_closure_shifted_but_advisory_boundary_should_hold_real` | **F**：phase/outcome 张力、**无 resume 串**、边界应守 |

---

## §3. 整包结果摘要

命令：

1. `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m16.json`  
2. `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m16.json --out logs/benchmark_triage_board_m16.json`

结果（`logs/real_scenario_pack_m16.json`）：

- 总 case：**94**（`m15`：**88** + 本批 **6**）  
- passed：**94**  
- quality：**acceptable = 94**  
- issue：**none = 94**  
- **Pack 附加**：`summary.advisory_sf1_prime_audit`（**SF-1′** 命中与 **`critical_candidate`** 对照，**不参与**判定）

---

## §4. triage 摘要

来自 `logs/benchmark_triage_board_m16.json`：

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

- advisory / SF-1′ **仍为** reserve 层与人审提示；**不**记为正式失败。

---

## §6. tension / severity 观察摘要

- **`tension_observed_but_not_failed`**：**93 / 94**（**`R3_general_search_real`** snapshot **无** tension 块）。  
- **severity**（`severity_audit`）：**watch = 19**，**review = 65**，**`critical_candidate` = 9**（`m15`：**7** → 本批 **`R89`、`R93`** 进入 **critical**，与 **SF-1′** 设计一致）。  
- **本批 severity**：`R89` **critical**；`R90`、`R92`、`R94` **review**；`R91` **review**；`R93` **critical**。

---

## §7. advisory / review 候选观察摘要（SF-1′）

来源：`summary.advisory_sf1_prime_audit`（与 `docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md` 同逻辑）。

| 指标 | 数值 |
|------|------|
| **`soft_fail_candidate_observed`（SF-1′）命中数** | **9** |
| **与 `critical_candidate` 交集** | **9**（**完全一致**） |
| **仅 advisory 非 critical** | **0** |
| **仅 critical 非 advisory** | **0** |

**本批**：

- **`R89`**：**命中** SF-1′，**且** `critical_candidate`（正样本预期）。  
- **`R90`、`R92`、`R94`**：**未**命中 SF-1′（近邻/边界，`lg` 中或 **`rsr`** 不成立）。  
- **`R91`**：**未**命中（健康 **terminal=found**，**不误伤**）。  
- **`R93`**：**命中** SF-1′ **且** `critical_candidate`（变体仍落主模式）。

**结论**：整包内 **advisory 与 `critical_candidate` 同轨**（数值 **9=9**），与 Validation Pack **边界**一致；近邻与健康样本 **未**误标 advisory。

---

## §8. 六项正式验收 + tension/severity + advisory 观察

**正式六项（冻结口径）**：整包 **acceptable**，**无** harness 新失败；主导源、任务位置、记忆解释、主链 phase、summary/白盒、entry 边界仍可按工程解读。

**tension / severity（辅助）**：分布与 **`m15` 延续**；**critical** **+2**（`R89`、`R93`），与「主模式加压」一致。

**advisory（辅助）**：**SF-1′** 命中 **9** 例，与 **`critical_candidate` 集合相同；** 不产生 **harness** 分支差异。

---

## §9. 当前是否需要开 fix sprint

**不需要**（相对 harness）。若需单独收紧 **`R93` 类变体** 的叙事叙述，可另立专项；**非**本批必开。

---

## §10. 本轮是否通过

**通过。** 第十六批扩包完成，`m16` + triage + **advisory 摘要** 产物齐全；**未**改 benchmark / triage 规则；**未**接 advisory 自动 gate。

---

## 主线—白盒—日志 串联检查

- **A 主线**：新场景仍经 `DecisionMonitorBuilder`；advisory 为 **pack 派生字段**。  
- **B 白盒**：advisory 与 **同帧** `run_summary_reference` / tension **可对齐**。  
- **C 日志**：`logs/real_scenario_pack_m16.json`、`logs/benchmark_triage_board_m16.json`。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。
