# Mainline Rebaseline & Gap Review — M0

**文件**：`docs/MAINLINE_REBASELINE_GAP_REVIEW_M0.md`  
**性质**：**阶段工程复盘 / Gap Review**（时间戳：主线工程多轮补齐之后）  
**上位与关联**：`docs/LUNA_MAINLINE_ENGINEERING_MAPPING.md`、`docs/MAINLINE_WHITEBOX_LOG_CHAIN_RULE.md`  
**本文不是**：新架构总纲、新功能设计、第十批真实场景扩包方案、实现细节代码说明。

---

## §1. 目标与适用范围

### 1.1 为什么现在需要 Rebaseline

- 近期**连续**落地多轮主骨架补齐：`scheduled_source_state`、调度×白盒同链增强、Trace×Summary 分层、任务链快照与位置解释、记忆调用解释等。  
- 若不做**统一收束**，容易出现「单点交付文档很多、整体基线是否前移」不清晰，后续优先级与扩包节奏容易散。  
- **在工程基线尚未相对稳态之前**，回到第十批真实场景扩包**收益偏低**：问题压出来后，主骨架再变仍会大面积重刷、重解释、重对齐。

### 1.2 本文回答什么

1. 上述补齐项各自形成了**闭环**、**最小接入**，还是**仍偏弱**？  
2. **主线—白盒—日志—Summary—任务链—记忆调用**六条观察链，当前**同链程度**到哪一层？  
3. 相对 `LUNA_MAINLINE_ENGINEERING_MAPPING.md` 中的 **P0 / P1 / P2**，哪些可视为**关闭或降级**，哪些仍成立？  
4. **下一阶段**工程补齐应优先哪几条？  
5. **在什么硬条件下**才建议再回到第十批真实场景扩包？

### 1.3 本文不回答什么

- 不写新模块设计规格、不写 reserve 实现方案、不写场景 JSON 扩包清单。  
- **不替代** `INFORMATION_SOURCE_SCHEDULING_ARCHITECTURE.md`、`TASKCHAIN_MAINLINE_INTEGRATION_ARCHITECTURE.md` 等专题架构文档。

---

## §2. 最近补齐项总表

| 工程项 | 目标 | 当前结果 | 结论 |
|--------|------|----------|------|
| **Scheduled Source State M0** | 数据源调度层**最小显式化**：参与源、主导源、冲突/覆盖/时效/置信等进入 frame | `scheduled_source_state` 由 `information_source_scheduler` 生成，进 `DecisionMonitorFrame`、聚合链、Viewer；与 `task_state` 等参与源可对齐 | **partially_closed** — 显式对象已落地，**非**完整调度引擎与策略空间 |
| **Source Scheduling × Whitebox M0.1** | 白盒第二层对调度事实的**原因/事件/告警**可追溯 | 结构树/时间轴/聚合可读调度摘要；与主链同一 frame 源 | **partially_closed** — 解释力增强，**未**达到架构中「调度层独立模块 + 全量维度」 |
| **Trace × Summary Separation M0.2** | Raw Trace / Structured Event / Summary Reference **工程分层** | `run_summary_reference`、`build_run_summary_reference`、三层 one-liner、聚合与 Console | **partially_closed** — 分层对象已存在，**独立长运行总结服务**仍未有 |
| **Task Chain State Snapshot M0** | 任务链**正式上下文源**进主链与调度 | `task_chain_state_snapshot` 在 builder 中构建，与 env task context / bridge / search 对齐 | **partially_closed** — 快照与 `task_state` 参与源已通，**非**任务链引擎 |
| **TaskChain Position Explanation M0.1** | 任务位置从「可见」到「可解释」 | `task_position_*`、时间轴位置事件、`task_chain_progress_summary`、树 `task_pos=` | **partially_closed** — 轻解释闭环，**熔断/消失/深结束语义**未做 |
| **Memory Invocation Explanation M0.3** | 记忆调用**为何/用了什么/帮助或风险**进同链 | `memory_invocation_explanation`、时间轴、Summary `mem=`、树 `mem=` | **partially_closed** — 解释层成形，**记忆写入/筛选/污染抵抗**未做 |
| **Mainline State / Phase Explicitness M0.4** | 主链四态与六阶段**最小显式化**（非重写主链） | `mainline_state_snapshot`、树 `state=`/`phase=`、时间轴、`run_summary_reference.mainline_state_summary` | **partially_closed** — 观测骨架成形，**非**完整状态机/熔断/深结束 |
| **Summary × Post-Processing Boundary M0.5** | Summary 与后处理链**正式边界契约**（非分类算法） | `post_processing_summary_entry`、回溯提示、`post_processing_intelligence_reserve.summary_post_processing_entry_id`、聚合/Console/Viewer | **partially_closed** — 入口可约束、可审计，**非**真实后处理/图书馆/记忆写入 |
| **Mainline Narrative Alignment M0.6** | 统一主线对象在白盒/日志/Summary/后处理入口的叙事骨架 | `mainline_narrative_alignment`、`run_summary_reference.mainline_narrative_brief`、`post_processing_summary_entry.narrative_readable`、聚合 `mainline_narrative_readable` | **partially_closed** — 口径显著收敛，非新增证据层/算法层 |

**总括**：上表工程项均为 **partially_closed**：在 **DecisionMonitor 主路径**上已形成**可审计的 M0 级同链基线**，但距离架构文档中的「完整形态」仍有系统级距离，**不得**理解为「全部完成」。

---

## §3. 当前主线同链状态复盘

### A. 主线

- **已进入 frame 的显式状态**：决策六层、`mainline_integration`、`task_chain_bridge` / `task_arbitration` / `object_search_interaction`、`scheduled_source_state`、`task_chain_state_snapshot`、`memory_novel_information_channel`、`memory_invocation_explanation`、`mainline_state_snapshot`（M0.4）、`run_summary_reference`、`post_processing_summary_entry`（M0.5）、`mainline_narrative_alignment`（M0.6）等（随 builder 顺序落地）。  
- **关键上下文源**：环境/任务前提（`environment_task_context_reserve`）、任务链快照、调度主导源、记忆通道与记忆调用解释，均已能在**同一帧**串联读取。  
- **收口与拍板语义**：单步决策收口仍在既有 decision/后果层；**未**引入新的拍板者。主链**语义仍稳定**，变化集中在**可观测性与解释层**。

### B. 白盒

- **调度（第二层）**：`scheduled_source_state` + M0.1 增强摘要，树/时间轴/聚合可读到**同一调度事实**。  
- **任务位置**：`task_chain_state_snapshot` + M0.1 字段与事件，树与时间轴可对齐。  
- **记忆调用**：M0.3 对象 + 树/时间轴/Summary 片段，与 `memory_novel_information_channel` 同源 frame。  
- **是否仍解释同一条主链**：在 **DecisionMonitorBuilder → frame** 路径上 **是**；若存在未走 builder 的旁路集成，需单独评审（不在本文展开）。

### C. 日志

- **三层语义**：M0.2 已为 raw / structured event / summary reference 提供**工程切片**（`run_summary_builder` + 聚合 one-liner）。  
- **任务链与记忆**：上述字段随 `DecisionMonitorFrame` **可序列化**进入 JSONL；benchmark / triage / rebaseline **可以**读同一落地文件——前提是工具链**固定读 JSONL/结果文件**，而非仅以 Console 为真（与工程规则一致）。  
- **偏弱处**：「黑匣子 vs 解释型字段」在同一 frame 内仍**共存**，边界依赖规范与评审，**非**两套物理存储的机械分离。

### D. Summary

- **已从「零散摘要字符串」推进为**：frame 内 **`run_summary_reference`** 作为**系统内总结入口对象**，并带 `summary_brief`、任务链进度行、记忆行等。  
- **当前能承载的轻摘要**：主线一句、调度一句、任务链进度、记忆调用一行、风险/issue 拼接等。  
- **仍偏弱**：**独立总结服务**、与图书馆的 **summary-first 真对接**、后处理对 summary 的**强契约**，仍属 P1/P2。

### E. 结论（硬句）

**当前已达到**：在 **DecisionMonitor 主路径**上，**主线事实、白盒（调度+任务位置+记忆调用）、日志落地、轻量 Summary 入口**可在**同一 frame** 内形成 **M0 级同链追溯**——可作为**新的阶段工程基线**。  
**尚未达到**：独立调度服务形态、独立总结服务形态、完整任务链引擎、记忆库与治理深实现——这些**不**因本轮补齐而自动关闭。

---

## §4. 当前 P0 / P1 / P2 缺口复盘

（对照 `LUNA_MAINLINE_ENGINEERING_MAPPING.md` §8，**按当前工程事实重评**。）

### P0

- **原 P0「数据源调度层未显式工程化」**：已通过 **`scheduled_source_state` 最小对象 + 白盒/日志同链**得到**阶段性缓解**；但「与架构六类源/五维调度**完全**对齐、独立服务化」**仍未**达成。  
- **原 P0「主链状态模型未显式化」**（候选/执行/恢复/暂停与可测试单一状态机）：**仍未关闭**，宜视为 **P1 头部**或「P0 降级后的强缺口」。  
- **硬句**：**原「调度层零对象」级 P0 已降级**；**状态机显式化**仍是**强缺口**，不宜再标为「已全无 P0」若团队将「可测试主链状态模型」仍定义为 P0，则 **P0 仍有一项未关**——建议团队在路线图二选一：**接受 M0 基线**并将该项降为 P1，或**继续将其列为唯一 P0**直至可测试封装完成。

### P1（最值得继续补的强关联项）

1. **主链阶段/四态与工程字段的显式对齐**（可测试、可命名、减少「语义等价但名字分散」）。  
2. **调度层与主链更深对齐**：`scheduled_source_state` 与 recheck/search/任务切换的**一致叙事**（仍非大算法）。  
3. **Summary 链**：`run_summary_reference` 与后处理/图书馆的**契约化**（仍可不真写库）。  
4. **任务链**：在**不**上熔断/结束深机制前提下，**加深**位置与成功语义（与 M0.1 同向）。  
5. **白盒**：高阶溯源仍偏规则与轻量；可按需增强，但**不**替代主链。

### P2（仍属 future / reserve）

- 图书馆正式接入、记忆写入与筛选、污染抵抗深实现、线程报损/切换/消耗、任务链熔断/归类/结束/消失、管控宪法级实现、统一高阶评分模型等——**与 `LUNA_MAINLINE_ENGINEERING_MAPPING.md` §8 P2 一致**，本轮**不**因 rebaseline 而消失。

---

## §5. 当前阶段最值得继续补的工程点（优先级）

**工程补齐优先级（仅列 3 项，顺序即建议执行序）：**

1. **主链状态与阶段语义的可测试显式化**（缩小「文档阶段 vs 代码字段」漂移；不必一步做成全状态机服务）。  
2. **调度层事实与主链关键转折的叙事对齐**（在已有 `scheduled_source_state` 上加强**一致性检查**与文档/测试，而非先扩调度算法）。  
3. **Summary 与后处理占位之间的边界契约**（仍可在不接入图书馆的前提下，把「谁读 summary、谁只读 trace」写死到工程规则与最小校验）。

---

## §6. 返回第十批真实场景的前置条件

以下**同时**满足时，才建议重新投入 **第十批真实场景扩包**（或大规模压测式扩包）：

1. **主线关键上下文源**（任务链快照、调度状态、记忆调用解释、Summary 入口）在 **DecisionMonitor 主路径**上已稳定若干迭代，**无**频繁字段重命名或主链挂点迁移。  
2. **主线—白盒—日志—Summary** 同链检查在**工具链与单测**上可重复通过，**不**依赖人工 Console 肉眼对齐。  
3. **新增场景用例**不会因「主骨架字段搬家」而**大面积失效**——即扩包所依赖的 frame 契约**相对冻结**（允许增量字段，不允许核心键随意删改）。  
4. **P0 级缺口**：至少达到团队共识的 **「调度最小对象已落地 + 状态机/阶段缺口已明确承接计划」**；若仍将状态机显式化列为 P0，则**应先关闭或显式降级**再扩包。  
5. **硬句**：**在工程基线未书面冻结、主链挂点仍在频繁调整时，不应以扩包代替工程补齐。**

---

## §7. 下一阶段工程顺序建议

1. **继续补主骨架剩余强关联缺口**（见 §5），**不**并行开第十批场景大批量扩包。  
2. **阶段性冻结 frame 契约**（对外部工具：benchmark/triage/scenario pack 的输入假设），变更走小步与迁移说明。  
3. **待 §6 前置条件满足后**，再回压真实场景批次，并把扩包结果**回灌**映射表与 gap review 的下一轮（非本文）。

---

## §8. 与现有文档的关系

| 文档 | 关系 |
|------|------|
| `LUNA_MAINLINE_ENGINEERING_MAPPING.md` | **总映射表**；本篇是其在**特定时间点**的复盘与 P0/P1/P2 **更新视角**，**不替代**总表结构。 |
| `INFORMATION_SOURCE_SCHEDULING_ARCHITECTURE.md` | 调度专题**架构**；本篇承认 M0/M0.1 **工程进展**，**不**改写该文档的完整形态定义。 |
| `TASKCHAIN_MAINLINE_INTEGRATION_ARCHITECTURE.md` | 任务链×主链**边界**专题；本篇对齐「快照+位置解释」的**实际落地深度**。 |
| `WHITEBOX_OBSERVATION_ARCHITECTURE.md` | 白盒五层**定稿**；本篇描述调度/任务/记忆在白盒中的**当前可达观察面**。 |
| `TRACE_LOGGING_AND_SUMMARY_PIPELINE.md` | 日志与总结**分层**；本篇确认 M0.2/M0.3 后的**工程分层现状**与仍弱项。 |

**强调**：本文是 **阶段 rebaseline 与 gap review**，**不替代**任何上位架构文档；下次主骨架大动时，应**更新**本文或新增 M0.1 版 review。

---

## §9. 本轮复盘元信息

- **基线判定**：可作为 **Mainline Engineering Baseline M0（post scheduled/taskchain/trace-summary/memory-invocation）** 的**文字锚点**。  
- **诚实声明**：**未**宣称架构 P0 全部关闭；**已**宣称在 DecisionMonitor 工具链上形成**可继续迭代的工程同链基线**。

---

## §10. 修订记录

- **M0**：首版，收束 scheduled_source ~ memory_invocation 连续补齐后的阶段判断与扩包前置条件。
