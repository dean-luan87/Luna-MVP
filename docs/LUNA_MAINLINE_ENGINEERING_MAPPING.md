# Luna 完整形态工程映射表（Engineering Mapping）— M0

**文件**：`docs/LUNA_MAINLINE_ENGINEERING_MAPPING.md`  
**版本**：M0（架构 ↔ 工程现状对齐，非新架构、非实现方案）  
**依据架构文档**：

1. `docs/LUNA_MAINLINE_SHAPE_BLUEPRINT.md`  
2. `docs/DECISION_MAINLINE_ARCHITECTURE.md`  
3. `docs/WHITEBOX_OBSERVATION_ARCHITECTURE.md`  
4. `docs/TRACE_LOGGING_AND_SUMMARY_PIPELINE.md`  
5. `docs/LIBRARY_MEMORY_AND_GOVERNANCE_ARCHITECTURE.md`

**本文不写**：新功能、新 reserve 开发、扩包、评分公式、图书馆/记忆正式写入、具体 schema/API。

**状态枚举**：`implemented` | `partially_implemented` | `reserved` | `missing` | `needs_alignment`

---

## §1. 文档目标与适用范围

### 1.1 解决的问题

- 五份架构文档已定稿，需要把 **架构要求 ↔ 当前仓库真实工程** 对齐。  
- 识别：**已实现 / 部分实现 / reserve / 缺失 / 需对齐**。  
- 为下一阶段 **补齐顺序** 提供依据（非实现细节）。

### 1.2 本文不是

- 新架构总纲、新需求 PRD、具体实现方案。

### 1.3 约束效力

后续阶段性开发优先级**宜**以本文为重要参考；与架构文档冲突时以**架构文档**为准。

### 1.4 阶段性 Rebaseline Review（M0）

在 **scheduled_source_state / Trace×Summary / task_chain / memory_invocation** 等主线工程多轮补齐之后，见 **`docs/MAINLINE_REBASELINE_GAP_REVIEW_M0.md`**：统一判断同链基线、P0/P1/P2 变化与「何时回到第十批真实场景」的前置条件。该文档为**阶段时间戳式复盘**，**不替代**本篇 §2–§9 的架构↔工程映射；**缺口列表以本篇为准**，复盘文用于**更新视角与优先级**。

### 1.5 阶段冻结口径（M0.6）

当前主线工程冻结口径见 **`docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md`**：用于回到第十批真实场景前的统一验收标准。该文档是**阶段冻结**，不替代本篇长期映射与架构原则。
并已补充“收纳精度审计”锚点：字段级证据、时间轴事件族、partial/reserve 与不纳入项，避免把半接入误判为正式能力。

---

## §2. 核心架构文档与工程映射总表

| 架构专题 | 核心对象/链 | 当前工程对应模块/文档 | 当前状态 | 备注 |
|----------|---------------|----------------------|----------|------|
| 主线总纲 | 8 链、4 层、边界 | `docs/LUNA_MAINLINE_SHAPE_BLUEPRINT.md`；工程规则 `docs/MAINLINE_WHITEBOX_LOG_CHAIN_RULE.md`、`.cursor/rules/Luna-Core-Mainline-Whitebox-Log-Chain.mdc` | `implemented`（文档） | 代码层为「部分对齐」，见 §7 |
| 决策运行主链 | 决策运行链 + 与调度衔接 | `decision_monitor/builder.py` 及 `decision_monitor/` 下 goal/state/hypothesis/recheck/search/task_chain/mainline 等；**M0.4** `mainline_state_snapshot`（四态/六阶段只读显式化，见 `docs/MAINLINE_STATE_PHASE_EXPLICITNESS_M0_4.md`） | `partially_implemented` | 主链语义强；**显式「数据源调度层」模块缺失**（见 §3.1） |
| 白盒观察链 | 五层白盒 | `reasoning_structure_tree.py`、`reasoning_timeline_view.py`、`reasoning_tree_metrics.py`、`reasoning_tree_quality_overlay.py`、各 `*_whitebox_trace.py`、`memory_novel_information_channel.py`、`environment_task_context_reserve.py` 等 | `partially_implemented` | 主链事实/质量/优化/部分 reserve 已落地；**数据源调度观察层**未单独工程化，仍偏分散字段 |
| 日志落地与总结 | 黑匣子 + 总结 + summary-first | `decision_monitor/schema.py`（`DecisionMonitorFrame`）、`decision_monitor/run_summary_builder.py`、`decision_monitor/post_processing_summary_contract.py`、`decision_monitor/mainline_narrative_alignment.py`、`decision_monitor/logger.py`、`runtime/context.py`、`tools/reasoning_console_aggregator.py`、JSONL 约定、`tools/decision_monitor_viewer.py` | `partially_implemented` | 黑匣子式 frame/JSONL 已通；**M0.2** `run_summary_reference`；**M0.5** `post_processing_summary_entry`；**M0.6** `mainline_narrative_alignment`（见 `docs/MAINLINE_NARRATIVE_ALIGNMENT_M0_6.md`）；独立总结服务与图书馆真接入仍不在本轮 |
| 图书馆/记忆/治理 | 后处理、图书馆、记忆、治理 | `post_processing_intelligence_reserve.py`、`knowledge_dual_channel_interface.py`、`decision_contamination_guard_reserve.py`、`strategy_injection_shadow.py`、`experience_evolution.py`、空间/经验相关模块 | `reserved` + `partially_implemented` | 后处理/污染/策略影子等为 **reserve**；经验/空间池等为**局部能力**，**不等于**架构中的长期记忆代谢与图书馆本体 |

---

## §3. 即时运行层工程映射

### 3.1 数据源调度层

| 问题 | 工程现状 |
|------|----------|
| 是否有显式「数据源调度层」模块？ | **无**独立模块；输入以 `ctx` 字典进入 `DecisionMonitorBuilder`，在 `builder` 与各子模块中**隐式**消化与分流。 |
| 输入源是否已进主链？ | **部分**：用户确认（`confirmation_input_bridge`）、视觉/搜索（`object_search_interaction`、`visual_candidate_audit`）、任务链（`task_chain_bridge`、`task_arbitration`）、记忆/新信息（`memory_novel_information_channel`）、环境任务前提（`environment_task_context_reserve`）等均有对应字段。 |
| 主导源切换/冲突/优先级/时效性是否工程化？ | **部分**：通道与前提层有**粗粒度**表达；**未**形成统一「调度状态对象」与白盒强制展示面（与架构 §6 仍有差距）。 |

**状态**：`partially_implemented`（逻辑分散在 `decision_monitor` + `ctx`），**缺口**：显式调度层抽象、统一可观测调度事实、与主链文档 Phase 的**一一映射表**。

### 3.2 决策运行链

| 架构阶段（概念） | 工程对应（示意） |
|------------------|------------------|
| 场景整理 | `goal_resolver`/`state_tracker`/`scene_gate`/`local_goal_state` 等 |
| 候选路径 | `hypothesis_layer`、`grid_search_expansion`、`task_arbitration` 等 |
| 主路径选择 | `decision`/`mainline_integration`/`object_search_interaction` 等 |
| 修正与再判断 | `recheck_planner`、各 whitebox trace、confirmation |
| 收口 | `action_hint_copy`、`recheck_planner`、search 终端态等 |
| 结果回流 | `frame` 内后果与 `mainline_integration` 等摘要 |

**已实现支柱**：`DecisionMonitorBuilder.build` 串联的 **DecisionMonitorFrame** 主链、**mainline_integration**、**recheck/search/hypothesis** 闭环在工具链与测试中大量使用。

**未完全显式化**：架构文档中的 **候选态/执行态/恢复态/暂停态** 未在代码中统一为单一状态机枚举；多数字段为**语义等价**而非**命名等价**。

**状态**：`partially_implemented`，**needs_alignment**：主链阶段与状态模型在工程中的**显式命名与可测试性**。

---

## §4. 伴随观察层工程映射

### 4.1 白盒观察链

| 白盒五层（架构） | 工程对应 | 状态 |
|------------------|----------|------|
| 主链事实层 | `reasoning_structure_tree`、`reasoning_timeline_view` | `implemented` |
| 数据源调度观察层 | `memory_novel_information_channel`、`environment_task_context_reserve`、部分 `confirmation`/任务链字段 | `partially_implemented` |
| 质量与偏移层 | `reasoning_tree_metrics`、`reasoning_tree_quality_overlay` | `implemented` |
| 优化与验证层 | `optimization_hint`、`optimization_feedback_loop` | `implemented` |
| 预留治理层 | `decision_contamination_guard_reserve`、`post_processing_intelligence_reserve`、`strategy_injection_shadow`、`spatiotemporal_continuity_reserve` 等 | `reserved`（多数为占位） |

**Console/Viewer**：`tools/reasoning_console_aggregator.py`、`tools/reasoning_console_server.py`、`tools/decision_monitor_viewer.py` 已聚合 frame 与多模块。

**缺口**：数据源调度层在**白盒中的独立一层**与架构文档**严格对齐**（参与源/主导源/切换/冲突的**统一视图**）仍不足 → `needs_alignment`。

### 4.2 日志落地链

| 能力 | 工程对应 | 状态 |
|------|----------|------|
| 原始运行记录（黑匣子） | `DecisionMonitorFrame`、JSONL 写入（`decision_monitor/logger.py` 等路径） | `implemented` |
| 结构化事件 | `reasoning_timeline_view.events`、frame 内多模块 dict | `partially_implemented`（有事件与时间轴；M0.2 增加 `structured_event_layer_snapshot` 语义切片） |
| 摘要引用层 | `post_processing_summary` 等 snapshot 字段、`integration_summary` | `partially_implemented` |
| 总结链独立产物 | **M0.2**：`run_summary_reference`（`build_run_summary_reference`）作为最小工程对象；仍**非**独立长运行总结服务 | `partially_implemented`（相对 M0 有**工程对象**；完整 summary feed 仍缺） |

**日志 vs 总结**：

- **原则**已在 `TRACE_LOGGING_AND_SUMMARY_PIPELINE.md` 定稿；**工程上** frame 同时承载大量解释型字段，**边界**依赖规范与评审，**非**完全机械分离的两套存储。

**benchmark/triage/rebaseline**：`tools/scenario_benchmark_harness.py`、`tools/benchmark_triage_board.py`、`tools/real_scenario_pack.py` 等读 JSONL/结果——**在走通路径上**与 frame 对齐；**需**保证读的是**落地文件**而非仅 Console。

**状态**：日志主链 `implemented`；**总结链独立化** `partially_implemented` / `missing`。

---

## §5. 事后加工层工程映射

### 5.1 运行总结链

| 问题 | 结论 |
|------|------|
| 是否有正式「运行总结链」？ | **无**独立长运行服务；**M0.2** 已落地最小 **`run_summary_reference`**（派生自主链/时间轴/通道/调度等已有字段，见 `docs/TRACE_SUMMARY_SEPARATION_M0_2.md`）。仍存 **mainline_integration** 的 `integration_summary`、benchmark 摘要等**并行**产物。 |
| summary feed | **部分**：M0.2 起 frame 含 **summary 入口对象** + 聚合层三层 one-liner；**未**形成独立总结服务或与图书馆的**真对接**（见 `TRACE_LOGGING_AND_SUMMARY_PIPELINE.md` §10）。 |

**状态**：`partially_implemented` / `missing`（作为**独立链**）。

### 5.2 后置信息处理链

| 项 | 状态 |
|----|------|
| `post_processing_intelligence_reserve` | `reserved`（M0 占位：规则生成、frame/runtime/Console/Viewer 轻接入） |
| 归类/归因/筛选/去向决策 | **未**实现；与架构中的「加工厂」差距大 |

**状态**：`reserved`；归类为 `partially_implemented` 仅当强调「已有占位骨架」时。

---

## §6. 长期沉淀与治理层工程映射

### 6.1 图书馆

- **定位**：文档/架构已定义；**工程**侧为 `knowledge_dual_channel_interface` 等 **reserve**（接口与候选语义，**非**真实图书馆服务）。  
- **状态**：`reserved`；真实多实例共享后台 **missing**。

### 6.2 记忆

- **工程中有**：`spatial_memory_pools`、`experience_evolution`、**Memory vs Novel** 通道等——多为**运行时/经验候选**语义。  
- **架构「长期高质量记忆层 + 代谢」**：**未**作为独立系统实现；**原始信息不得直通记忆**在工程上靠**未接自动写库**与架构约束，**非**完整门禁实现。  
- **状态**：`partially_implemented`（局部）+ `missing`（架构级记忆层）。

### 6.3 治理与免疫链

| 项 | 状态 |
|----|------|
| `decision_contamination_guard_reserve` | `reserved`（占位） |
| `strategy_injection_shadow` | `reserved`（影子） |
| 线程报损/切换/消耗 | **未**见主工程实现，**missing** |
| 多模型/议会/Whitebox Plus | **占位**于文档与 reserve 语义 | `reserved` |

**结论**：治理链在工程上 **仍以 reserve 为主**；**轻量**已接入 frame/Console/Viewer。

---

## §7. 主线—白盒—日志 串联映射

### A. 主线

- **构成**：`decision_monitor` 主路径（`DecisionMonitorBuilder` + 各层模块）为当前 **Reasoning/决策显示器** 主线工程核心；**主运行**（如 `main.py` / `core_snapshot`）与 DecisionMonitor 的接法依集成路径而异。  
- **验证**：大量场景与单测走 `DecisionMonitorBuilder.build()`；**已**在开发路径上跑通。  
- **文档阶段模型**：**部分**仍停留在文档层，未完全以**显式状态机**固化。

### B. 白盒

- **是否解释同一条主链**：在 **DecisionMonitor frame** 路径上，**是**（树/时间轴/metrics/quality 同源 frame）。  
- **缺口**：**数据源调度层**的**统一白盒面**仍弱于架构要求。

### C. 日志

- **能否承载主线与白盒**：**能**——frame/JSONL 含主链与白盒模块输出。  
- **benchmark/triage/rebaseline**：依赖**读落地 JSONL/结果文件**；**禁止**仅 Console 当唯一真相（与规则一致）。  
- **缺口**：**总结链**独立化与**日志三层**语义**工程化**不足。

### D. 总体判断（硬结论）

**当前主线—白盒—日志在 DecisionMonitor 主路径上基本同链；仍存在「数据源调度层显式化不足、运行总结链未独立、后处理/图书馆/治理多为 reserve」等脱钩点。**

---

## §8. 当前工程缺口列表

**（近期主线补齐后的阶段性判断，见 `docs/MAINLINE_REBASELINE_GAP_REVIEW_M0.md` §4；以下仍以架构完整形态为参照列举。）**

### P0（主线级缺口）

1. **数据源调度层未显式工程化**：缺少统一「整理后的数据源状态」对象与主链/白盒**强制对齐**，易导致架构要求与代码散落实现不一致。  
   - **专项设计文档（M0）**：`docs/INFORMATION_SOURCE_SCHEDULING_ARCHITECTURE.md`（调度层显式化对象、维度、接口与落地顺序；**非实现**）。  
   - **同链增强交付（M0.1）**：`docs/SOURCE_SCHEDULING_WHITEBOX_ALIGNMENT_M0_1.md`（白盒第二层解释增强：原因/事件/告警；主线-白盒-日志同链）。  
2. **主链状态模型未显式化**：候选/执行/恢复/暂停与架构文档**未**一一对应到可测试的单一状态模型。

### P1（强关联缺口）

1. **白盒「数据源调度观察层」**与主链**同链增强**（字段/视图/校验）。  
2. **日志链**：结构化事件层与摘要引用层与**黑匣子**的**机械分离**（在不大改前提下至少**规范 + 校验**）。  
3. **运行总结链**：从 `integration_summary`/benchmark 摘要**升级为**独立 summary feed 语义（仍非实现细节）。  
4. **记忆调用可解释**：白盒/日志/总结**三方**对同一套问题的**最小对象**仍缺统一工程表达。  
5. **任务链 × 主链接口**：长期任务结构 vs 单步主链拍板边界需工程对齐；**专题工程设计（M0）**：`docs/TASKCHAIN_MAINLINE_INTEGRATION_ARCHITECTURE.md`（接口与边界基线，非任务引擎实现）。**最小接入（M0）**：`docs/TASK_CHAIN_STATE_SNAPSHOT_MINIMAL_INSERT_M0.md`（`task_chain_state_snapshot` 与调度层/白盒/summary 同链）。

### P2（未来层缺口）

1. 后处理链真实归类/归因/去向（当前 **reserve**）。  
2. 图书馆本体与 summary-first **接入**。  
3. 治理链全量能力与线程/污染深实现。  
4. 第十批场景等——**在架构对齐前**不优先（与本轮指令一致）。

---

## §9. 下一阶段工程优先级建议

**建议顺序（工程优先级，非实现细节）**：

1. **数据源调度层显式化**（最小可观测对象 + 与 builder/白盒对齐）  
2. **白盒与数据源调度层同链增强**（满足 `WHITEBOX_OBSERVATION_ARCHITECTURE` 第二层）  
3. **日志 / 总结进一步分离与结构化**（summary feed 与黑匣子边界可审计）  
4. **任务链与主链深整合**（约束见 **`docs/TASKCHAIN_MAINLINE_INTEGRATION_ARCHITECTURE.md`**；在 `DECISION_MAINLINE_ARCHITECTURE` 接口语义下推进最小 `task_chain_state_snapshot` → 调度层 → 主链入口 → 白盒/日志/summary）  
5. **再评估**是否扩真实场景批次或接更高层治理/图书馆

**不建议在 1–3 未稳前**：盲目扩场景、上统一评分模型、或深做图书馆写入。

---

## §10. 与后续文档和开发节奏的关系

- 本文是 **总纲与专题架构 → 仓库现状** 的**桥梁**；后续迭代应先更新映射或补缺口，再大规模扩功能。  
- 真实场景扩包、主线补齐、治理落地，**宜**以 §8–§9 为序。  
- 代码开发仍须遵守 **主线 → 白盒 → 日志** 串联检查（见 `MAINLINE_WHITEBOX_LOG_CHAIN_RULE.md`）。

---

## 修订记录

- **M0**：首版工程映射表；对齐五份架构文档与当前 `decision_monitor`/工具链/日志现状。  
- **M0+**：增补 P1 任务链 × 主链专题入口；§9 第 4 步与 `TASKCHAIN_MAINLINE_INTEGRATION_ARCHITECTURE.md` 对齐。  
- **M0++**：增加 §1.4 指向 `MAINLINE_REBASELINE_GAP_REVIEW_M0.md`；§8 增加与阶段复盘文档的交叉引用。
