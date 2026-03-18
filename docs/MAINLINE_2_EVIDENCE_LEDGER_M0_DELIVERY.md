# 主线 2 第二阶段：证据账本 M0 交付说明

**依据**：Skeleton Mix M0、Skeleton Filter M0、Spatial Memory Pooling M0、Spatial Forgetting M0  
**目标**：在已有空间记忆与遗忘链路上增加最小证据账本，使当前空间判断具备“支持证据 / 冲突证据 / 缺失证据 / 建议补证动作”的可见记录。本轮只做最小证据账本，不做完整推理引擎、不做 Hypothesis Layer、不做学习。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/evidence_ledger.py` | **新建**。EvidenceLedgerEntry、EvidenceLedger；build_evidence_ledger(smap, relations, mix, filt, pools, forgetting, goal, state) 生成 1～3 条 claim，填充 support/conflict/missing、confidence、risk_if_wrong、suggested_next_check。 |
| `decision_monitor/schema.py` | 引入 EvidenceLedger；DecisionMonitorFrame 新增 evidence_ledger。 |
| `decision_monitor/builder.py` | 引入 evidence_ledger；build 中在 spatial_forgetting 之后调用 build_evidence_ledger，写入 frame.evidence_ledger。 |
| `runtime/context.py` | 新增 evidence_ledger_claim_summary、evidence_ledger_confidence、evidence_ledger_risk_if_wrong、evidence_ledger_suggested_next_check（首条 claim）。 |
| `main.py` | 决策显示器块内，将 frame.evidence_ledger 首条 claim 写入 runtime_ctx。 |
| `tools/decision_monitor_viewer.py` | 新增「证据账本 / Evidence Ledger (M0)」卡片；sections 增加 evidence_ledger。 |
| `decision_monitor/CONTRACT.md` | 补充 evidence_ledger 说明与未实现项。 |

---

## 2. Evidence Ledger 数据结构说明

### EvidenceLedger

| 字段 | 类型 | 含义 |
|------|------|------|
| entries | List[EvidenceLedgerEntry] | 本帧证据账本条目（1～3 条） |

### EvidenceLedgerEntry

| 字段 | 类型 | 含义 |
|------|------|------|
| claim_summary | str | 结论摘要 |
| supporting_evidence | List[str] | 支持证据摘要列表 |
| conflicting_evidence | List[str] | 冲突证据摘要列表 |
| missing_evidence | List[str] | 缺失证据摘要列表 |
| evidence_confidence | float | 证据置信度 0～1 |
| risk_if_wrong | str | 误判风险描述 |
| suggested_next_check | str | 建议补证动作（如 recheck_environment、hold_and_confirm） |

---

## 3. 最小 claim 生成规则说明

- **Claim 1（主导空间关注）**：claim_summary = "当前主导空间关注：{navigation/fine_interaction/observation/safety}"；support 来自 mix（dominant、mix_reason）、filt（keep）；missing 在 safety 主导且无 risk_region 时为「需要风险区域信息」；suggested_next_check 为 hold_and_confirm 或 recheck_environment。
- **Claim 2（主要空间结构）**：claim_summary 由 smap/relations 推导，如「前方可通行主区成立」「存在风险与可通行冲突」「需确认区支撑 focus」「待补充」；support 来自 focus/traversable/confirm 区域与 supports 关系；conflict 来自 risk 区域与 conflicts_with 关系；missing 如「需要 confirm 区支撑 focus」「需要局部空间图」。
- **Claim 3（记忆状态）**：claim_summary 如「当前 working 证据充足」「episode 已塌缩，证据依赖短时池」「证据依赖短时池，working 为空」；support 来自 pools（working/episode 数量）、forgetting 摘要；missing 在 working 为空时为「需要当前帧空间证据」。

---

## 4. supporting / conflicting / missing 规则说明

- **supporting_evidence**：与 claim 一致的摘要——来自 SpatialMap 区域（focus、traversable、confirm）、relations 的 supports、working/episode 数量与 mix/filt 的 keep/dominant。
- **conflicting_evidence**：risk 与 traversable 并存时的 risk 摘要、relations 中 relation_type=conflicts_with 的摘要、filt 的 suppress 与当前 dominant 不一致时的摘要。
- **missing_evidence**：当前 claim 所需但未满足的信息——如「需要风险区域信息」「需要 confirm 区支撑 focus」「需要局部空间图」「需要当前帧空间证据」。

---

## 5. suggested_next_check 生成规则说明

- 规则型生成，不做真正 planner。取值来自：recheck_environment、recheck_close_range、shift_view_left、shift_view_right、look_forward、hold_and_confirm。
- 有 missing_evidence 时优先：hold_and_confirm（主导关注缺失）、recheck_close_range（结构缺失）、recheck_environment（记忆状态缺失）。
- 有 conflicting_evidence 且无缺失时：hold_and_confirm。
- 否则：look_forward 或 recheck_environment（按 claim 类型）。

---

## 6. Viewer 展示说明

- **卡片标题**：证据账本 / Evidence Ledger (M0)。
- **第一行**：首条 claim_summary。
- **第二行**：支持数、冲突数、缺失数、置信度（百分比）。
- **第三行**：误判风险（risk_if_wrong）。
- **第四行**：建议补证（suggested_next_check）。
- 专家折叠面板可展开 evidence_ledger 查看 entries。

---

## 7. 样本运行结果（验收）

- 运行时存在可读的 Evidence Ledger（frame.evidence_ledger、runtime_ctx 首条 claim 相关字段）。
- 至少生成 1～3 条有效 claim。
- 每条 claim 至少包含 supporting_evidence、missing_evidence、evidence_confidence、suggested_next_check（conflicting 可为空）。
- Viewer 能展示当前证据账本。
- 不破坏主线 A、主线 2 第一阶段、M0、M1、M1.5、M2、Skeleton Mix M0、Skeleton Filter M0、Spatial Memory Pooling M0、Spatial Forgetting M0 链路。

---

## 8. 当前哪些账本字段已真实化，哪些仍预留

| 项目 | 状态 |
|------|------|
| EvidenceLedger / EvidenceLedgerEntry、build_evidence_ledger、三类 claim 规则、support/conflict/missing/suggested_next_check 规则型填充、frame/runtime_ctx/Viewer | **真实化**。 |
| 完整候选推理、Hypothesis Layer、学习型证据权重、复杂多 claim 竞争、长期证据账本持久化、detector/OCR/动态策略主链改造 | **未实现**，本轮不做。 |

---

## 9. 本轮是否通过

- **是**。验收满足：运行时存在可读 Evidence Ledger；至少 1～3 条 claim；每条含 support/missing/confidence/suggested_next_check；Viewer 可展示；不破坏既有链路。未实现项已在 CONTRACT 与本文档写明。
