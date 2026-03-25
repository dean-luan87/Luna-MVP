# Reasoning Backbone Phase Closure M1（推理主线骨架一期收口）

## §1 文档定位（写死）

本文档是 **推理主线骨架的一期收口基线**，用于固化当前阶段成果与边界：

- 回答“当前推理主线已经完成到什么程度”
- 列出“哪些模块/接口已稳定（轻冻结）”
- 写死“哪些内容明确不做/只预留”
- 指出“下一阶段从哪里继续”

本文档 **不是** roadmap、不是需求池、不是单模块 delivery、不是调试手册。

## §2 当前已完成的主线骨架（按能力域）

### A. 交互决策链（Interaction / Decision Chain）

- `object_search_interaction`
- `local_task_space_grid`
- `grid_search_expansion`
- `recheck_planner`
- `action_hint_copy`
- `confirmation_input_bridge`

### B. 白盒链（Whitebox Chain）

- `grid_search_whitebox_trace`
- `recheck_whitebox_trace`
- `action_hint_whitebox_trace`
- `confirmation_whitebox_trace`
- `evidence_hypothesis_whitebox_trace`
- `experience_governance_whitebox_trace`

### C. 结构与连续性链（Structure + Continuity Chain）

- `reasoning_structure_tree`
- `spatiotemporal_continuity_reserve`

### D. 质量与优化链（Quality + Optimization Chain）

- `reasoning_tree_metrics`
- `optimization_hint`
- `optimization_feedback_loop`

### E. 知识与策略预留链（Knowledge + Strategy Reserve Chain）

- `knowledge_dual_channel_interface`
- `strategy_injection_shadow`

### F. 总控台（Reasoning Console）

- `tools/reasoning_console_aggregator.py`
- `tools/reasoning_console_server.py`
- Console 已包含：总览 / 结构树 / Tree Metrics / Optimization Hint / Optimization Feedback Loop / Knowledge Interface Reserve / Strategy Injection Shadow / Spatiotemporal Continuity / 白盒 tabs（各模块）

## §3 当前形成的“最小完整闭环”（写死）

当前主线已形成可审计的最小闭环：

1. **输入与任务上下文**（runtime_ctx / frame inputs/state）
2. **search / recheck / action / confirmation**（交互决策链）
3. **whitebox**（白盒链：reason/weight/exclusion/interaction/user_visible）
4. **structure tree**（总骨架组织：evidence/hypothesis/decision/feedback/exclusion/resolution）
5. **metrics**（树质量量化 + issue）
6. **optimization hint**（问题 → 建议）
7. **optimization feedback loop**（建议 → 验证 → worth_persisting 占位）
8. **knowledge reserve**（persist/optimization/injection slot 占位）
9. **strategy shadow**（不注入，只做“如果注入会怎样”的影子预估）

## §4 当前已稳定接口（轻冻结清单）

### 4.1 DecisionMonitorFrame 关键字段（对外语义稳定）

- `reasoning_structure_tree`
- `reasoning_tree_metrics`
- `optimization_hint`
- `optimization_feedback_loop`
- `knowledge_dual_channel_interface`
- `strategy_injection_shadow`
- `spatiotemporal_continuity_reserve`
- 以及白盒链字段：
  - `grid_search_whitebox_trace`
  - `recheck_whitebox_trace`
  - `action_hint_whitebox_trace`
  - `confirmation_whitebox_trace`
  - `evidence_hypothesis_whitebox_trace`
  - `experience_governance_whitebox_trace`

### 4.2 轻冻结结果结构（至少）

- `ReasoningStructureTreeResult`
- `ReasoningTreeMetricsResult`
- `OptimizationHintResult`
- `OptimizationFeedbackLoopResult`
- `KnowledgeDualChannelInterfaceResult`
- `StrategyInjectionShadowResult`
- `SpatiotemporalContinuityReserveResult`

**轻冻结原则**：当前字段语义视为稳定；后续如需调整，必须在变更记录/收口文档中显式记录，不允许无声修改。

### 4.3 Console 稳定区块（入口冻结）

Console 作为统一入口，当前至少稳定承载：

- 总览（问题优先）
- 推理结构树（树视图）
- Tree Metrics
- Optimization Hint
- Optimization Feedback Loop
- Knowledge Interface Reserve（占位）
- Strategy Injection Shadow（影子验证，占位）
- Spatiotemporal Continuity（影响摘要，占位）
- 白盒 tabs（各模块，默认摘要 + 可展开）

## §5 当前明确不做 / 只预留的内容（写死）

本阶段明确不做（均为后续阶段能力）：

- **图书馆本体**（写入/检索/召回/策略库）
- **真正策略注入**（真实执行、规则替换、权重改写）
- **复杂连续性系统**（多帧跟踪、评分系统、轨迹重建、时空继承模型）
- **自动优化**（自动调参/自动执行建议/治理层）
- **评分系统/替换逻辑/复杂反馈治理**
- **长周期趋势分析 / 实验平台 / 多版本对照体系**

本阶段仅提供“预留/占位”层：Knowledge Dual-Channel Interface、Strategy Injection Shadow、Spatiotemporal Continuity Reserve。

## §6 当前主线工程边界（分层）

- **主线已完成并可用**：交互决策链、白盒链、结构树、指标、优化建议、优化验证、Console 统一入口。
- **预留接口（不可被误用为真实能力）**：Knowledge / Strategy Shadow / Continuity Reserve。
- **后续阶段才展开的重逻辑**：图书馆本体、真实注入、自动优化、复杂连续性。

## §7 下一阶段入口（少量且清晰）

仅列入口，不展开需求池：

- 图书馆本体接入（基于 Knowledge Dual-Channel Interface）
- 策略正式注入执行层（必须先经 Strategy Injection Shadow）
- 连续性复杂化（保持“前端默认只展示影响摘要”的总原则）
- 自动优化/治理层（基于 metrics + hint + feedback_loop 的闭环信息）

## §8 结论（写死）

推理主线骨架已形成一期基线：**交互链 + 白盒链 + 结构链 + 质量链 + 知识预留链 + 策略影子层 + Console 统一入口**。

后续新增相关能力应优先在该主线骨架内扩展与接入，不应绕开该骨架另起平行推理/解释/优化体系。

