# Soft-Fail Candidate Validation Pack M0

**文件**：`docs/SOFT_FAIL_CANDIDATE_VALIDATION_PACK_M0.md`

## 一、阶段定位

1. **不是**继续抽象定义条款、**不是**把 soft-fail 接入 benchmark / triage、**不是**第十六批无差别扩包、**不是**动 `nt` 或再写 tension 长文。  
2. **是**对 **`docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md`（SF-1′）** 做 **边界验证**：正样本命中率、近邻误伤率、健康/低信号排除率、轻量变体是否「一碰就进候选」。  
3. **验证实现**：`tools/validate_soft_fail_candidate_clause_m0.py`（只读构建 frame、对照条款打标），产物 **`logs/soft_fail_candidate_validation_m0.json`**。

---

## 二、验证条款（与草案一致）

在同一帧上判定 **SF-1′**：

- **`pc∧lg` raw high**  
- **`resume_chain_fragility_summary`** = **`resume_declared_but_main_not_progressed`**  
- **`task_chain_progress_summary`** 含 **`global_main_progress_not_terminal_complete`**  

并记录草案 **§五** 类排除在输出 `exclusion_reasons` 中（脚本同时给出 **`human_candidate_per_draft`**）。

---

## 三、样本矩阵（本包固定集）

| 类别 | case_id | 目的 |
|------|---------|------|
| **正样本** | `R53`、`R59`、`R60`、`R83`、`R84`、`R86`、`R88` | 条款应 **稳定命中** |
| **近邻** | `R85`、`R82`、`R10` | 应 **不**命中 SF-1′（多为 `lg=medium`、`rsr=none`） |
| **健康 / 基线** | `R87`、`R4`、`R1`、`R3` | 应 **不**误标（`pc` 低或 **terminal=found** 且无全局未收口 token 等） |
| **轻量变体（独立 ctx）** | `SFV01_just_below_threshold_pc_high_lg_medium_real`、`SFV02_healthy_terminal_found_like_real` | 分别贴近 **R85 族** / **R87 族**，验证 **阈值下** 不误进候选 |

**说明**：轻量 **SFV** 场景 **未** 并入 `tools/real_scenario_pack.py` 默认整包，避免无差别扩包；仅由验证脚本 **按路径加载**。

---

## 四、如何运行

```bash
python3 tools/validate_soft_fail_candidate_clause_m0.py --out logs/soft_fail_candidate_validation_m0.json
```

---

## 五、当前一次跑通结果摘要（可复现）

来源：`logs/soft_fail_candidate_validation_m0.json`（与脚本同步生成）。

| 桶 | SF-1′ 命中 | `human_candidate_per_draft` |
|----|------------|-----------------------------|
| 正样本（7） | **7/7** | **7/7** |
| 近邻（3） | **0/3** | **0/3** |
| 轻量变体（2） | **0/2** | **0/2** |

**解读（简）**：

- **正样本**：条款与 **m15 `critical_candidate` 主模式** 对齐，**命中原因一致**（`pc∧lg` + `rsr` + `tcp` token）。  
- **近邻**：**`lg_not_high`** 与 **`rsr=none`** 阻断 SF-1′，**不误伤 R85/R82/R10**。  
- **健康**：**R87 / R4** 为 **`pc=none`** 或 **tcp 无全局未收口 token**（**R87/R4** 且 **`terminal=found`**），**不误标**；**R1/R3** 张力不足或快照无 tension。  
- **SFV01**：与 **R85** 同族，**`lg=medium`** → **不**进候选。  
- **SFV02**：与 **R87** 同族，**`pc=none`** + **无 tcp 全局未收口 token** → **不**进候选。

---

## 六、结论与是否保留条款

**后续**：**SF-1′** 的 **review / advisory 使用方式**（权限、落点、模板）见 **`docs/ADVISORY_REVIEW_GATE_DRAFT_M0.md`**。

1. **条款在当前矩阵下稳定**：正样本 **全命中**，近邻与健康/轻量 **全未** 标为 `human_candidate_per_draft`。  
2. **可继续保留**为 **「人审高风险候选」** 文档条款；**仍不**接自动 gate。  
3. **是否再向 advisory / review gate 走一步**：需产品约定；工程上建议 **先** 在交付中 **人工引用 SF-1′**，**再** 观察多轮复跑与真实链路。

---

## 七、本轮是否通过

**通过。** 完成 **验证包矩阵 + 可复现脚本 + JSON 产物**；**未**改 benchmark、**未**改 hard-fail、**未**扩默认真实场景整包。

---

## 主线—白盒—日志 串联检查

- **A 主线**：仅重建 frame 读字段，**不**改决策。  
- **B 白盒**：与 `narrative_evidence_tension_review` / `run_summary_reference` **同链**。  
- **C 日志**：`logs/soft_fail_candidate_validation_m0.json`。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。
