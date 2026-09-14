# Real Scenario Pack M1.2 Delivery（第十二批真实场景扩包）

**文件**：`docs/REAL_SCENARIO_PACK_M1_2_DELIVERY.md`  
**本轮定位**：在 `M0.6` 冻结基线经 **M1.0 + M1.0.x** 与 **M1.1 + M1.1.x** 两轮稳定后的**进一步扩包压测**（非系统重定义）。  
**冻结基线依据**：`docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md`

**硬约束声明**：

- 本轮判断仍服从 M0.6 冻结口径；  
- 问题仅分类为 `baseline_covered_defect` / `baseline_excluded_requirement` / `reserve_only_finding`；  
- 不因单个新场景重解释 M0.6 边界；  
- 未改 benchmark / triage 工具规则，未改主骨架。

---

## §1. 本轮定位

在已冻结且经两轮定点修复后的工程基线上，第十二批重点压测：

1. 多跳任务链下**跨层叙事一致性**（局部可解释 vs 全局是否前进）  
2. **调度—任务—主链**三方耦合下的叙事滞后  
3. **个性化语义偏差**在熟悉语境中的慢性稳定化（不用“污染”表述）  
4. **Narrative / summary / entry** 的“顺滑叙事 vs 证据支撑”张力  
5. **Phase / closure / outcome** 三层口径一致性（相对 M1.1 的二层压力再升级）

---

## §2. 新增 case 清单

新增 `R65`–`R70`，均为 `ctx_json` 场景：

| case_id | 压测方向 |
|---------|----------|
| `R65_multi_recovery_chain_locally_valid_but_globally_stalled_real` | A 多跳恢复链整体一致性 |
| `R66_task_state_shifted_but_mainline_story_lagged_real` | B 调度—任务—主链耦合 |
| `R67_familiar_context_bias_stabilized_without_explicit_conflict_real` | C 熟悉语境下偏差稳定化 |
| `R68_narrative_smooth_but_trace_support_weak_real` | D 叙事顺滑、证据偏弱 |
| `R69_phase_and_closure_aligned_but_outcome_summary_misaligned_real` | E phase/closure vs outcome/summary |
| `R70_entry_backfill_should_trigger_but_story_looked_complete_real` | D/E 后处理入口 vs 叙事闭环感 |

五类方向（A–E）均已覆盖。

---

## §3. 整包结果摘要

运行命令：

1. `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m12.json`  
2. `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_m12.json --out logs/benchmark_triage_board_m12.json`

结果（`logs/real_scenario_pack_m12.json` 摘要）：

- 总 case：**70**  
- passed：**70**  
- failed：**0**  
- quality：**acceptable = 70**  
- issue 分布：**none = 70**（无 `blocked_without_resolution`）

第十二批新增 `R65`–`R70`：**全部通过**（与整包一致）。

---

## §4. triage 摘要

来自 `logs/benchmark_triage_board_m12.json`：

- **最差 case（rank 靠前）**：`R1_container_real`、`R2_occlusion_real`（与全包均为 `acceptable`、无 issue 时 triage 的**占位排序**，不代表新回归热点）。  
- **top modules**：**—**（无优化提示聚合热点）。  
- **top issues**：**—**（无 `blocked_without_resolution` 等突出 issue 类型）。

---

## §5. 问题分类（按冻结口径）

### A. `baseline_covered_defect`

- **本轮 harness 指标下**：未新增可归类项（整包无 `poor`、无 `blocked_without_resolution`）。  
- **说明**：M1.1.x 已对 `R60/R61/R64` 等语境做 `recheck_planner` 最小收口；本批新场景在相同冻结规则下**未复现**新的基线内指标失败。

### B. `baseline_excluded_requirement`

- **全局任务推进的严格可证明性**、**正式任务引擎/熔断/消失归类**、**图书馆真写入**、**污染深治理**等仍为 M0.6 明确边界外；  
- 不因本批叙事字段更复杂而自动升格为“当前正式失败”。

### C. `reserve_only_finding`

- **叙事—证据细粒度对齐**、** outcome 行与 summary 的自动判错**等，若需超出当前结构树 + overlay + summary 骨架的判定，仍属观察/后续专题（与架构文档中的 reserve 叙述一致）；  
- **benchmark/smoke 产物**本身不单独升格为能力基线（与 M0.6 收纳精度一致）。

---

## §6. 六项验收重点判断

1. **主导源是否讲得清**：整包与 `R66` 在动态源/任务切换语境下仍为 **acceptable**；主导源相关字段在既有骨架内可消费。未出现 harness 级新失败。  
2. **任务位置是否讲得清**：`R65` 等多跳语境下 **acceptable**；**全局“主目标是否真推进”的严格证明**仍属基线外能力，本轮不据此判失败。  
3. **记忆调用 / 个性化语义偏差是否讲得清**：`R67` **acceptable**；与 `R61` 同属熟悉偏差族，本批强调“无显式冲突下的稳定化”，**语义风险标定深度**仍以当前 M0.6 落点为界。  
4. **主链状态 / 阶段是否讲得清**：`R69` **acceptable**；**phase/closure 与 outcome 的第三层一致性**更多依赖叙事与 outcome 字段的人工/后续 viewer 复核，**自动 harness 未单独判错**。  
5. **Summary / Narrative / 白盒是否同口径**：`R68`、`R70` **acceptable**；**“顺滑但证据弱 / 看似闭环但仍应 backfill”** 属于本轮刻意加压的**语义张力**，当前以 **acceptable + 无 issue** 通过，**不表示**已在全链路自动检出所有“合理化过度”个案。  
6. **后处理入口边界是否守住**：未出现新的 harness 级越权或 entry 替代证据本体的指标失败；**entry 是否应在更强证据规则下必触发**属 reserve/后续契约细化。

---

## §7. 当前是否需要开 fix sprint

**不需要（针对 M1.2 扩包结果本身）。**

理由：

- 整包 **70/70**，**无** `blocked_without_resolution`、**无** `poor`；  
- 与 M1.1 不同，本批**未压出**新的、可归为 `baseline_covered_defect` 的指标型缺陷。

若后续要在**叙事—证据自动对打**或 **outcome 第三层**上提高判别力，可作为**新专题**评估，但不属于本轮扩包必开 sprint。

---

## §8. 本轮是否通过

**结论：通过（扩包目标达成，整包指标通过）。**

理由：

- 已新增 `R65`–`R70` 并覆盖 A–E 五类方向；  
- 已重跑整包与 triage，产物路径符合要求；  
- 冻结口径下分类稳定，**未将 reserve/边界外需求误判为 harness 失败**。

---

## 主线—白盒—日志一致性检查

- **A 主线**：新增场景均经 `DecisionMonitorBuilder` 构建并进入整包主路径，无 `ctx_json build failed`。  
- **B 白盒**：质量覆盖仍为单链 overlay 口径；本批侧重语义叙事压力，**隐蔽错位需结合 frame 人工阅读**，非本轮 harness 否定项。  
- **C 日志**：整包输出写入 `logs/real_scenario_pack_m12.json` / `logs/benchmark_triage_board_m12.json`，与工具链一致。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**（在 M0.6 冻结能力范围内）。
