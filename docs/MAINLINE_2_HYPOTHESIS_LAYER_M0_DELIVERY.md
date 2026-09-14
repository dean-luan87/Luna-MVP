# 主线 2 第二阶段：假设层 M0 交付说明

**依据**：Evidence Ledger M0 + 已有空间记忆/过滤/分池/遗忘链路  
**目标**：在 Evidence Ledger 基础上增加最小 Hypothesis Layer，在“证据不足但又不能什么都不说”时生成少量、受约束、可回溯、可验证的候选解释。本轮只做最小候选解释层，不做完整场景推理、不做学习、不做经验沉淀。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/hypothesis_layer.py` | **新建**。Hypothesis、HypothesisLayer；HYPOTHESIS_TYPES/STATUSES/VERIFICATION_HINTS；build_hypothesis_layer(ledger, smap, relations, mix, filt, pools, state) 生成 1～3 条受约束假设；风险闸门 _apply_risk_gate。 |
| `decision_monitor/schema.py` | 引入 HypothesisLayer；DecisionMonitorFrame 新增 hypothesis_layer。 |
| `decision_monitor/builder.py` | 引入 hypothesis_layer；build 中在 evidence_ledger 之后调用 build_hypothesis_layer，写入 frame.hypothesis_layer。 |
| `runtime/context.py` | 新增 hypothesis_summary、hypothesis_type、hypothesis_confidence、hypothesis_verification_hint、hypothesis_status。 |
| `main.py` | 决策显示器块内，将 frame.hypothesis_layer 首条假设写入 runtime_ctx。 |
| `tools/decision_monitor_viewer.py` | 新增「假设层 / Hypothesis Layer (M0)」卡片；sections 增加 hypothesis_layer。 |
| `decision_monitor/CONTRACT.md` | 补充 hypothesis_layer 说明与未实现项。 |

---

## 2. Hypothesis 数据结构说明

### Hypothesis

| 字段 | 类型 | 含义 |
|------|------|------|
| hypothesis_summary | str | 假设摘要 |
| hypothesis_type | str | container_candidate / path_continuation_candidate / occluded_object_candidate / interaction_target_candidate |
| supporting_evidence_refs | List[str] | 支持证据轻量引用（claim 索引、key、摘要） |
| missing_evidence | List[str] | 缺失证据描述 |
| hypothesis_confidence | float | 假设置信度 0～1 |
| risk_if_wrong | str | 误判风险描述 |
| verification_hint | str | 验证建议（见 VERIFICATION_HINTS） |
| hypothesis_status | str | candidate / needs_check / rejected / promoted |

### HypothesisLayer

| 字段 | 类型 | 含义 |
|------|------|------|
| hypotheses | List[Hypothesis] | 本帧候选假设列表 |
| dominant_hypothesis_type | str | 首条假设类型（可选） |
| hypothesis_reason_summary | str | 生成原因摘要 |

---

## 3. 最小 hypothesis_type 与生成规则说明

- **path_continuation_candidate**：当 focus/traversable 存在但 confirm 不足，或 relations 存在 supports/adjacent_to 时生成；supporting_evidence_refs 来自 claim:空间结构；missing_evidence：需 confirm 或 anchor 支撑路径延续；verification_hint：recheck_close_range / look_forward。
- **interaction_target_candidate**：当 dominant==fine_interaction 且存在 confirm 或 focus 时生成；missing：目标未完全确认；verification_hint：recheck_close_range。
- **occluded_object_candidate**：当 evidence_ledger 的 missing_evidence 含“需要/遮挡/近场/覆盖/证据”或无 focus 时生成；missing：目标可能被遮挡或未进入视野；verification_hint：recheck_environment；status 默认 needs_check。
- **container_candidate**：当 ledger claim 含“容器/portal/可见性/消失”时生成；或当 missing 含“区域/空间图”且假设数<3 时补一条弱 container；missing：需确认是否进入容器或区域；verification_hint：recheck_environment / hold_and_confirm。

---

## 4. 风险闸门规则说明

- 当以下任一成立时视为高风险：dominant==safety；runtime_domain_state 为 degraded 或 frozen；risk_if_wrong 含“高”或“严重”。
- 高风险时：hypothesis_status 不得为 promoted，改为 needs_check；若 verification_hint 为空则设为 hold_and_confirm。
- 高风险假设不得直接写入事实层，仅作候选或待验证。

---

## 5. verification_hint 生成规则说明

- 取值：recheck_environment、recheck_close_range、shift_view_left、shift_view_right、look_forward、hold_and_confirm、ask_user_for_clarification。
- 按缺失证据与假设类型规则型分配：路径延续缺 confirm → recheck_close_range 或 look_forward；交互目标未确认 → recheck_close_range；遮挡 → recheck_environment；容器/区域 → recheck_environment 或 hold_and_confirm。风险闸门触发时补 hold_and_confirm。

---

## 6. Viewer 展示说明

- **卡片标题**：假设层 / Hypothesis Layer (M0)。
- **第一行**：首条 hypothesis_summary。
- **第二行**：类型、置信度、状态。
- **第三行**：误判风险、验证建议。
- **第四行**：假设条数、hypothesis_reason_summary。
- 专家折叠面板可展开 hypothesis_layer 查看 hypotheses、dominant_hypothesis_type、hypothesis_reason_summary。

---

## 7. 样本运行结果（验收）

- 运行时存在可读的 Hypothesis Layer（frame.hypothesis_layer、runtime_ctx 首条假设字段）。
- 至少生成 1～3 条有效 hypothesis。
- 每条含 hypothesis_summary、hypothesis_type、missing_evidence、hypothesis_confidence、verification_hint、hypothesis_status。
- Viewer 能展示当前假设层。
- 高风险场景下（如 dominant==safety 或 runtime_domain_state degraded/frozen）假设不会直接 promoted。
- 不破坏主线 A、主线 2 第一阶段、M0、M1、M1.5、M2、Skeleton Mix M0、Skeleton Filter M0、Spatial Memory Pooling M0、Spatial Forgetting M0、Evidence Ledger M0 链路。

---

## 8. 当前哪些 hypothesis 字段已真实化，哪些仍预留

| 项目 | 状态 |
|------|------|
| Hypothesis/HypothesisLayer、build_hypothesis_layer、四类 type 生成规则、风险闸门、verification_hint 规则、frame/runtime_ctx/Viewer | **真实化**。 |
| promoted/rejected 完整生命周期、学习型假设排序、长期 hypothesis ledger、假设升级为事实的完整流程、经验沉淀联动、完整场景推理、对象级因果追踪、开放世界无限候选 | **未实现**，本轮不做。 |

---

## 9. 本轮是否通过

- **是**。验收满足：运行时可读 Hypothesis Layer；至少 1～3 条 hypothesis；每条含 summary/type/missing/confidence/verification_hint/status；Viewer 可展示；高风险下不 promoted；不破坏既有链路。未实现项已在 CONTRACT 与本文档写明。
