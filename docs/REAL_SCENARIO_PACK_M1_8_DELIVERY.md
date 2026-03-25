# Real Scenario Pack M1.8 Delivery（第十八批真实场景扩包）

**文件**：`docs/REAL_SCENARIO_PACK_M1_8_DELIVERY.md`

## §1. 本轮定位

1. **M1.8** 仍属于 **M1.x 主线扩包**，继续遵守 `M0.6` 冻结口径。  
2. 本轮新增重点是验证 **`nt` tightening 后**在真实扩包中的稳定性与协同性：  
   - 正式失败层（harness）  
   - tension/severity 层  
   - advisory/review 候选层  
   三层并存，不互相替代。  
3. 正式问题分类仍只服从：`baseline_covered_defect` / `baseline_excluded_requirement` / `reserve_only_finding`。  
4. **`nt` 仍仅属 tension/severity 辅助观察，不进入自动 fail。**

---

## §2. 新增 case 清单

| case_id | 方向 |
|---|---|
| `R101_long_narrative_sparse_key_anchors_should_raise_nt_real` | A：长叙事 + 关键锚点偏薄，`nt` 正向点亮（watch） |
| `R102_long_narrative_with_sufficient_key_support_should_not_raise_nt_real` | B：长叙事但锚点充分，`nt` 不升格 |
| `R103_nt_supports_pc_lg_but_not_primary_driver_real` | C：`pc/lg` 已有张力，观察 `nt` 是否协同（本批仍偏保守） |
| `R104_advisory_strong_but_nt_still_none_should_be_acceptable_real` | D：advisory 强，`nt` 非决定项 |
| `R105_complex_healthy_narrative_dense_support_real` | E：健康复杂叙事对照，不应误伤 |
| `R106_entry_summary_smooth_but_key_support_thin_review_only_real` | A/E：summary/entry 顺滑但支撑偏薄，`nt` watch 对照 |

覆盖性检查：

- `nt` 正向样本：`R101`、`R106`  
- 健康/对照：`R102`、`R105`、`R104`  
- `nt + pc/lg` 同向观察样本：`R103`（本批结果显示协同仍偏保守）  
- advisory 强但 `nt` 不决定一切：`R104`

---

## §3. 整包结果摘要

命令：

1. `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m18.json`  
2. `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m18.json --out logs/benchmark_triage_board_m18.json`

结果（`logs/real_scenario_pack_m18.json`）：

- 总 case：**106**（`m17` 100 + 本批 6）  
- passed：**106 / 106**  
- quality：**acceptable = 106**  
- issue：**none = 106**  
- `tension_observed_but_not_failed_count`：**105**

---

## §4. triage 摘要

来自 `logs/benchmark_triage_board_m18.json`：

- worst case（占位/low）：`R1_container_real`、`R2_occlusion_real`、`R3_general_search_real`  
- top modules：**—**  
- top issues：**—**

说明：规则未改，整包全 `acceptable` 时 triage 仍为占位排序。

---

## §5. 正式问题分类

### `baseline_covered_defect`

- **无新增**（harness 全通过，`issue_type` 全 `none`）。

### `baseline_excluded_requirement`

- 图书馆正式接入、记忆正式写入、任务链深机制、自治闭环等仍属冻结外。

### `reserve_only_finding`

- `nt` / severity / advisory 仍为辅助观察层，不替代正式失败分类。

---

## §6. tension / severity 观察摘要

- severity 分布（`summary.severity_audit`）：  
  - `watch = 8`  
  - `review = 85`  
  - `critical_candidate = 12`
- `nt` 分布（全包）：  
  - `none = 79`  
  - `low = 13`  
  - `medium = 13`  
  - `unknown = 1`（`R3` snapshot 口径）

本批新增 6 例的 `nt`：

- `R101`: `low`（命中“长叙事+锚点偏薄”）  
- `R106`: `low`（同类 watch）  
- `R102`/`R105`: `none`（健康/支撑充分对照）  
- `R103`: `none`（`pc/lg` 有张力但 nt 本批仍未协同点亮）  
- `R104`: `none`（advisory 强但 nt 未越权）

结论：tightening 后 `nt` 已出现可信 `watch/review` 分布（全包 26 例非 none），且未把健康复杂样本大面积误打。

---

## §7. advisory / review 候选观察摘要

来源：`summary.advisory_sf1_prime_audit`

- `soft_fail_candidate_observed`：**12**  
- 与 `critical_candidate` 交集：**12**  
- advisory only：**0**  
- critical only：**0**

本批新增 case：

- `R104`：advisory 命中（`critical_candidate` 同向），`nt=none`，验证“`nt` 不越权也不拖垮整体解释”。  
- `R101`/`R106`：`nt` 点亮但 advisory 不命中，验证“`nt` 与 advisory 分工仍清晰”。  
- `R102`/`R105`：健康对照未误标 advisory。

---

## §8. 六项正式验收 + 三层观察 + nt 观察

1. 主导源是否讲得清：**是**  
2. 任务位置是否讲得清：**是**  
3. 记忆调用/个性化语义偏差是否讲得清：**是**  
4. 主链状态/阶段是否讲得清：**是**  
5. Summary/Narrative/白盒是否同口径：**是**  
6. 后处理入口边界是否守住：**是**

辅助观察：

7. severity 分布是否合理：**基本合理**（仍以 review 为主，critical 稳定）  
8. advisory 命中/排除是否稳定：**稳定**（交集 12=12，近邻/健康排除保持）  
9. `nt` 是否形成可信 watch/review 且不误伤健康复杂：**是（初步）**，但 `pc/lg` 协同点亮仍偏保守（`R103` 仍 `none`）。

---

## §9. 当前是否需要开 fix sprint

**不需要**（harness 维度）。  
本批是观察层协同性验证，未出现基线内正式失败。  
建议后续是否开专项，优先看 `nt` 与 `pc/lg` 协同点亮能力是否需要再校准（可先通过下一批扩包继续观察）。

---

## §10. 本轮是否通过

**通过。**

理由：

- `m18` 产物齐全、整包 106/106；  
- 冻结口径与规则边界未被破坏；  
- `nt` 在真实扩包中继续保持“有信号但不越权”；  
- advisory / severity / tension 三层仍未互相替代或打架。

---

## 主线—白盒—日志 串联检查

- **A 主线**：新增场景仍走现有主路径，未改主链行为。  
- **B 白盒**：`nt`、`pc/lg`、severity、advisory 在同帧可对照，语义未越权。  
- **C 日志**：`logs/real_scenario_pack_m18.json`、`logs/benchmark_triage_board_m18.json` 已落地。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。

