# Mainline Engineering Baseline Freeze — M0.6

**文件**：`docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md`  
**性质**：阶段冻结文档（Baseline Freeze）  
**适用阶段**：回到第十批真实场景前的统一工程验收口径  
**关联文档**：`docs/MAINLINE_REBASELINE_GAP_REVIEW_M0.md`、`docs/LUNA_MAINLINE_ENGINEERING_MAPPING.md`、`docs/MAINLINE_WHITEBOX_LOG_CHAIN_RULE.md`

**本文回答**：

1. 当前 M0.6 基线到底包含什么；  
2. 哪些对象已进入主骨架并形成同链；  
3. 哪些能力仍不属于当前基线；  
4. 回到第十批真实场景前应按什么硬口径验收。

**本文不是**：新架构总纲、新实现方案、新扩包计划。

---

## §1. 目标与适用范围

近期已经连续完成多轮主线工程补齐（M0 → M0.6）。在这一节点继续“边补工程边扩场景”会导致反复重刷与口径漂移。  
因此需要把当前可用主骨架冻结为 **Mainline Engineering Baseline M0.6**，作为回到第十批真实场景前的统一判断标准。

本冻结文档适用于：

- 场景回归前的工程 readiness 判断；
- review / gap review / rebaseline 的基线判定；
- 新问题归因时区分“超出基线”与“基线内退化”。

---

## §2. M0.6 基线纳入范围总表

| 基线对象/能力 | 当前状态 | 是否纳入 M0.6 基线 | 备注 |
|--------------|----------|--------------------|------|
| `scheduled_source_state` | 已工程化（最小对象） | `baseline_included_minimal` | 已进 frame/白盒/日志；非完整调度引擎 |
| Source Scheduling × Whitebox 对齐 | 已增强（M0.1） | `baseline_included_minimal` | 原因/事件/告警可见；非全维调度解释 |
| Raw Trace / Structured Event / Summary Reference 分层 | 已工程化（M0.2） | `baseline_included` | 三层语义已可追溯；非独立总结服务 |
| `task_chain_state_snapshot` | 已工程化（M0） | `baseline_included` | 正式上下文源已入主链 |
| TaskChain Position Explanation | 已增强（M0.1） | `baseline_included_minimal` | 位置 reason/warn/事件可见；非深任务机制 |
| `memory_invocation_explanation` | 已增强（M0.3） | `baseline_included` | 调用原因/效果可见；非记忆系统写入 |
| `mainline_state_snapshot` | 已工程化（M0.4） | `baseline_included` | 四态/六阶段最小显式化；非完整状态机 |
| `post_processing_summary_entry` | 已工程化（M0.5） | `baseline_included` | Summary→后处理边界契约成立；非分类算法 |
| `mainline_narrative_alignment` | 已工程化（M0.6） | `baseline_included_minimal` | 叙事骨架统一；非新证据层 |
| `run_summary_reference.mainline_narrative_brief` | 已落地字段 | `baseline_included_minimal` | Summary 叙事骨架锚点（字段级证据） |
| `post_processing_summary_entry.narrative_readable` | 已落地字段 | `baseline_included_minimal` | Entry 与 Summary 叙事对齐锚点 |
| `post_processing_intelligence_reserve.summary_post_processing_entry_id` | 已落地字段 | `baseline_included_minimal` | Contract × Reserve 交叉引用锚点 |
| 图书馆正式接入 | 未实现 | `not_included` | 仅 reserve/接口层 |
| 记忆正式写入 | 未实现 | `not_included` | 仅解释层与占位 |
| 污染抵抗深实现 | reserve | `reserved_only` | 无强判定与治理闭环实现 |

---

## §3. 当前 M0.6 基线能力摘要

### A. 主链上下文源

- 调度层：`scheduled_source_state` 已作为最小显式对象进入主链同帧。  
- 任务链：`task_chain_state_snapshot` 与位置解释（M0.1）已可追溯。  
- 记忆调用：`memory_invocation_explanation` 可说明“为何调用/作用倾向”。  
- 主链状态/阶段：`mainline_state_snapshot` 已显式化并入 frame。

结论：主链上下文源已达到 **M0 级最小显式化**，但仍非完整引擎级建模。

### B. 白盒解释层

- 调度解释：Source Scheduling 在树/时间轴可见。  
- 任务位置解释：位置 reason/warn 与事件进入白盒视图。  
- 记忆调用解释：可见“支持/风险”语义。  
- 主链状态解释：state/phase 已并入白盒叙事。

结论：白盒已能覆盖主要上下文源解释，但仍属 **最小可解释层**。

### C. 日志落地层

- `DecisionMonitorFrame` / JSONL 主链落地已稳定。  
- Raw / Event / Summary 三层语义已可被统一读取。  
- `scheduled_source_state`、`task_chain_state_snapshot`、`memory_invocation_explanation`、`mainline_state_snapshot`、`post_processing_summary_entry`、`mainline_narrative_alignment` 可同帧追溯。

结论：日志层已具备 **M0 级同链追溯能力**，但不是多存储形态的成熟日志服务。

### D. Summary 与后处理入口

- `run_summary_reference` 作为 summary 入口已成立；  
- `post_processing_summary_entry` 作为后处理边界契约已成立；  
- M0.6 叙事对齐使 summary / entry 口径收敛。

结论：已形成 **最小 summary→后处理合法入口闭环**，非真实后处理分类链。

---

## §4. 当前 M0.6 基线边界（硬句）

以下内容**属于当前基线**：

- 最小上下文显式化（调度/任务链/记忆调用/主链状态）；  
- 最小主线—白盒—日志同链闭环；  
- 最小白盒解释可见性；  
- 最小日志落地与三层语义可追溯；  
- 最小 Summary 入口与后处理入口契约；  
- 最小叙事统一（M0.6）。

以下内容**不属于当前基线**：

- 图书馆正式接入；  
- 记忆正式写入与筛选链；  
- 污染抵抗与治理深实现；  
- 任务链深机制（熔断/消失/归类/结束）；  
- 管控宪法实现；  
- 第三方证据源正式接入；  
- 高阶评分模型；  
- 多模型议会实现。

**硬句**：M0.6 冻结的是“最小工程同链基线”，不是“完整形态能力”。

---

## §4.1 M0.6 可检查锚点（验收信号）

以下锚点用于验证“可追溯”不是口头描述，而是可检查工程事实：

### A. 字段级锚点（已纳入）

- `run_summary_reference.mainline_narrative_brief`  
- `post_processing_summary_entry.narrative_readable`  
- `post_processing_intelligence_reserve.summary_post_processing_entry_id`

### B. 时间轴事件锚点族（已纳入）

- **source 族**：`scheduled_source_state_formed`、`dominant_source_selected`、`source_conflict_detected`、`priority_override_applied`  
- **task 族**：`task_chain_state_snapshot_formed`、`task_chain_position_interpreted`  
- **memory 族**：`memory_invocation_explained`、`memory_invocation_supports_mainline`、`memory_invocation_risk_detected`  
- **mainline 族**：`mainline_state_snapshot_formed`、`mainline_phase_identified`、`mainline_state_transition_observed`

### C. 边界锚点（已纳入）

- `summary_brief_hint_only=true`（Summary 仅提示）  
- `summary_not_substitute_for_raw_trace=true`（Summary 不替代证据本体）  
- `memory_write_forbidden_from_summary_only=true`（禁止仅凭 summary/entry 写记忆）

---

## §4.2 partial / reserve（明确不误收正式能力）

以下对象在 M0.6 中属于 **有对象 + 有链路 + 有展示，但非完整能力**，统一按 partial/reserve 处理：

- `post_processing_intelligence_reserve`  
- `environment_task_context_reserve`  
- `decision_contamination_guard_reserve`  
- `memory_novel_information_channel`  
- `runtime/context` 占位字段（M0.5/M0.6）

**硬句**：上述对象不得按“正式能力已完成”解释。

---

## §4.3 不纳入项（明确排除，防止基线膨胀）

以下内容不属于 M0.6 工程能力基线：

- smoke 工具脚本（`tools/smoke_*.py`）  
- smoke 产物（`logs/*.jsonl`）  
- benchmark/triage 一次性结果文件  
- 一次性评测输出与临时分析文件  
- viewer/console 历史展示残留  
- 仅“存在测试”但不在本轮冻结范围内的模块

**硬句**：验证工件与评测产物不等于基线能力。

---

## §5. 当前主线—白盒—日志—Summary—后处理状态结论

当前主线已具备 M0 级同链追溯能力：主要上下文对象在同一 frame 可被主线、白盒、日志、summary 与后处理入口一致读取。  
白盒已能对主要上下文源给出一致解释；日志已承载关键对象；Summary/后处理入口边界已合法化并可审计。  
因此，当前整体**足以作为扩场景前的工程基线**，前提是明确遵守本文件定义的边界与验收口径。

---

## §6. 回到第十批真实场景的验收前提

回到第十批真实场景前，后续评测与 review 应遵循以下硬规则：

1. 先以 **M0.6 冻结基线**作为固定主骨架；  
2. 新问题优先判定为“场景新问题”或“超出基线覆盖范围问题”；  
3. 不再把已冻结对象反复视为“未定义”；  
4. 若要突破 M0.6 边界，必须先更新基线文档，再推进场景归因；  
5. 不允许用单次场景结果直接推翻已冻结基线定义。

---

## §7. 当前仍未冻结的缺口

### P1（仍需继续补，但不阻碍本次冻结）

- 调度层更强因果解释（当前仅最小层）；  
- 主链状态/阶段更深判定精度；  
- 任务链语义更强判定（但不含深机制）；  
- Summary 独立服务化程度提升；  
- 后处理真实分类链。

### P2（future / reserve）

- 图书馆正式接入；  
- 记忆写入与筛选链；  
- 污染抵抗与线程治理深实现；  
- 管控宪法；  
- 第三方证据源正式接入；  
- 多模型议会。

---

## §8. 冻结后的下一阶段建议

判断：**当前已足以形成“可回第十批真实场景的工程基线”**。  
建议顺序：先按 M0.6 冻结口径回场景验证；新增问题按“基线内退化 / 基线外需求”分层处理；若涉及边界外需求，先更新基线再扩执行。

---

## §9. 与现有文档的关系

- 与 `MAINLINE_REBASELINE_GAP_REVIEW_M0.md`：前者是**阶段冻结口径**，后者是**阶段复盘视角**；两者互补不互替。  
- 与 `LUNA_MAINLINE_ENGINEERING_MAPPING.md`：前者是**当前冻结标准**，后者是**长期架构↔工程映射总表**。  
- 与五份架构文档：冻结基线不替代架构原则，仅定义“当前可验收工程落点”。

---

## 主线—白盒—日志 串联检查

- **A 主线**：主线对象已进入同帧主路径并可追溯。  
- **B 白盒**：白盒解释已覆盖主要上下文源且口径基本一致。  
- **C 日志**：关键对象与 summary/entry 均已落 frame/JSONL。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**；M0.6 可作为阶段工程冻结基线。

补记：已按该冻结口径进入 `M1.0` 真实场景回归压测（`docs/REAL_SCENARIO_PACK_M1_0_DELIVERY.md`），并进入 `M1.1` 扩包压测（`docs/REAL_SCENARIO_PACK_M1_1_DELIVERY.md`），以及 `M1.2` 第十二批扩包压测（`docs/REAL_SCENARIO_PACK_M1_2_DELIVERY.md`）、`M1.3` 第十三批扩包压测（`docs/REAL_SCENARIO_PACK_M1_3_DELIVERY.md`）、`M1.4` 第十四批扩包压测（`docs/REAL_SCENARIO_PACK_M1_4_DELIVERY.md`，含 `TENSION_SEVERITY_PROFILE_SPEC_M0` 画像实压，**不**改 harness 失败判定）。另：叙事—证据张力审计（`docs/NARRATIVE_EVIDENCE_TENSION_REVIEW_M0.md`）为**仅读观察层**，不扩展本冻结文件的验收义务。
