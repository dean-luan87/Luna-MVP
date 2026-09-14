# Soft-Fail Candidate Draft M0

**文件**：`docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md`

## 一、文档定位

1. **只做**文档与口径：**不**接自动 gate、**不**改 harness hard-fail、**不**改 benchmark / triage、**不**改变**冻结基线**（`docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md`）下的正式三类缺陷分类。  
2. **把** `docs/CRITICAL_CANDIDATE_PATTERN_REVIEW_M0.md` 中已固化的 **主模式** **`resume_fragility_with_global_main_stall`** **写成**可引用的 **future soft-fail 候选条款**（人审 / advisory / 规则观察用）。  
3. **依据**：`docs/TENSION_SEVERITY_PROFILE_SPEC_M0.md`、`docs/TENSION_REVIEW_TEMPLATE_AND_SOFT_FAIL_SPEC_M0.md`、`docs/CRITICAL_CANDIDATE_PATTERN_REVIEW_M0.md`、`logs/critical_candidate_pattern_m15.json`。

---

## 二、适用范围（写死）

| 用途 | 是否允许 |
|------|----------|
| **人工 review** 标注「高风险候选」 | **是** |
| **advisory / 交付附录** 风险标签 | **是** |
| **future 规则观察**（对照跑分、不自动执行） | **是** |
| **自动 fail / CI gate** | **否** |
| **benchmark / triage 规则修改** | **否** |
| **替代** `baseline_covered_defect` / `baseline_excluded_requirement` / `reserve_only_finding` | **否** |

---

## 三、主模式名称（工程名）

**`resume_fragility_with_global_main_stall`**（resume 脆弱性 × 全局主任务未收口 × phase/closure 错位）

- **语义**：同一决策帧内，**叙事层**已出现 **resume 目标** 与 **主任务未向 terminal 收口** 的张力，且 **phase/closure** 与 **outcome** 存在可复核错位；**不是**七种无关异常，**m15 上 7/7 `critical_candidate` 均落此族（见模式复盘文档）。

---

## 四、候选条款（正式表述）

**当同一帧同时满足以下必要条件，且不满足 §五 排除条件时**，样本可标记为：

> **`future soft-fail candidate` / 人审高风险候选`**（**仅文档与人工语义**，**非** harness 失败）。

### 4.1 必要条件（建议同时满足再标）

1. **`pc∧lg` raw high**  
   - 即 `narrative_evidence_tension_review` 中 **`phase_closure_outcome_tension=high`** 且 **`local_global_progress_tension=high`**（与 **`TENSION_SEVERITY_PROFILE_SPEC_M0`** 下 **`critical_candidate`** 画像一致）。

2. **`run_summary_reference.resume_chain_fragility_summary`** = **`resume_declared_but_main_not_progressed`**

3. **`task_chain_progress_summary`** 含 **`global_main_progress_not_terminal_complete`**（与同帧 **`resume_main_align=`** 等 token 互证，具体以 `run_summary_builder` / TCS 产出为准）。

### 4.2 骨架句（可直接进 Review/Soft-Fail Spec 交叉引用）

当同一帧同时满足：
1）**`pc∧lg` raw high**；  
2）**`resume_chain_fragility_summary`** = **`resume_declared_but_main_not_progressed`**；  
3）**`task_chain_progress_summary`** 含 **`global_main_progress_not_terminal_complete`**；  
且 **无** §五 健康对照型排除条件（如 **terminal 已达成主目标**、**`pc` 低**、**全局目标已收口** 等），

则该样本可标记为 **`future soft-fail candidate` / 人审高风险候选**。

---

## 五、排除条件（健康对照 / 近邻不误标）

满足 **任一** 时，**不应**单独依本条款标为「高风险候选」（可仍用 **`review`** 等其它口径）：

| 排除情形 | 说明（来自 m15 对照） |
|----------|------------------------|
| **`pc` 非 high**（如 **`pc=none`**） | 即使 **`lg=high`**，severity 画像 **不为** `critical_candidate`；例：**R87** |
| **`lg` 非 high**（如 **`lg=medium`**） | 与 **`pc=high`** 同帧亦 **仅** `review`；例：**R85、R82、R10** |
| **主任务已 terminal 对齐**（如 **`terminal=found`** 且 **tcp 无** `global_main_progress_not_terminal_complete`） | 例：**R87** |
| **`resume_chain_fragility_summary=none`** 且 **无** 与 resume 目标一致的脆弱性摘要 | 近邻 **closure/推进语言** 张力，**非** 本主模式；例：**R85/R82** |

---

## 六、近邻混淆项（易与主模式混淆，但非同一条款）

| 近邻 | 特征 | 为何不是本条款 |
|------|------|----------------|
| **仅 `pc=high` + `lg=medium`** | closure 错位 + 「推进语言但未达主目标」 | **`lg` 未 raw high**，**rsr** 常为 **none** |
| **仅 `lg=high` + `pc=none`** | 局部/全局推进语言强、**phase/closure 未报强错位** | **无 `pc∧lg` 双高**，**不**进 `critical_candidate` |
| **高 `sb`/`mb` 饱和** | 契约与记忆行常 high | **单独**不构成 soft-fail 候选（见原 Spec §2.3–2.5） |

---

## 七、与 `TENSION_REVIEW_TEMPLATE_AND_SOFT_FAIL_SPEC_M0.md` 的关系

- 原 **SF-1**（**`pc∧lg` 双高**）为 **severity 层** 的**必要条件**；**本草案** 在 SF-1 之上增加 **结构化摘要链**（**rsr + tcp**）与 **排除**，形成 **可操作的「人审高风险候选」条款**。  
- **不**替代原 §5 人工模板；**在**模板 **D** 中可选用 **`soft_fail_candidate`** 时，**优先**核对是否满足 **§四** 与 **§五**。

---

## 八、边界验证（Validation Pack M0）

条款是否误伤近邻、是否稳定命中正样本：见 **`docs/SOFT_FAIL_CANDIDATE_VALIDATION_PACK_M0.md`** 与 **`logs/soft_fail_candidate_validation_m0.json`**（`tools/validate_soft_fail_candidate_clause_m0.py`）。

**进入 advisory/review gate 草案**：验证通过后，**SF-1′** 的工程使用方式见 **`docs/ADVISORY_REVIEW_GATE_DRAFT_M0.md`**（**提示权、无裁决权**）。

---

## 九、本轮是否通过

**通过。** 条款已落笔；**未**改代码、benchmark、冻结口径。

---

## 主线—白盒—日志

- 条款仅依赖 **已落地** frame 字段与 tension；**不**改主链。  
- **最终判断**：**主线通顺，白盒一致，日志已落地**（复盘数据见 `logs/real_scenario_pack_m15.json`、`logs/critical_candidate_pattern_m15.json`）。
