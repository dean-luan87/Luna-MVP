# Mainline Reasoning Backbone Closure M0（推理主线骨架阶段收口）

## 1. 文档定位（写死）

本文档用于把当前阶段已经完成的“推理主线骨架”统一收口成**清晰、可审计、可继续迭代**的阶段基线。

- **做什么**：明确本阶段“已完成到什么程度”、哪些接口已稳定、哪些是预留不展开
- **不做什么**：不新增新能力、不扩算法、不做图书馆本体/写回/检索/自动注入

## 2. 主线骨架闭环（当前已具备）

### 2.1 交互链（Interaction Chain）

- Search / Grid
- Recheck
- Action Hint
- Confirmation

### 2.2 成长链（Growth Chain）

- Evidence / Hypothesis Whitebox（证据与假设解释）
- Experience Governance Whitebox（经验治理解释）

### 2.3 解释链（Explainability Chain）

- Whitebox（统一五块骨架 + 用户可见解释层）
- Reasoning Structure Tree（总组织结构）
- Spatiotemporal Continuity Reserve（连续性影响摘要进入依据层）

### 2.4 质量链（Quality Chain）

- Reasoning Tree Metrics（结构树质量度量 + issue）
- Optimization Hint（从 issue → 建议方向）
- Optimization Feedback Loop（建议验证闭环：baseline vs current 框架）

### 2.5 知识预留链（Knowledge Reserve Chain）

- Knowledge Dual-Channel Interface Reserve（Persist Candidate / Optimization Candidate / Injection Slot）

## 3. 当前“稳定接口”清单（对外口径）

### 3.1 Frame 输出（DecisionMonitorFrame）

以下字段作为本阶段稳定接口（用于 JSONL/Console/审计消费），后续扩展优先“增字段”而非破坏语义：

- `*_whitebox_trace`（Search/Grid、Recheck、Action Hint、Confirmation、Evidence/Hypothesis、Experience Governance）
- `reasoning_structure_tree`（聚合树视图入口）
- `reasoning_tree_metrics`（树质量指标与 issue）
- `optimization_hint`（规则版建议）
- `optimization_feedback_loop`（验证闭环框架）
- `knowledge_dual_channel_interface`（双通道与注入口预留）
- `spatiotemporal_continuity_reserve`（连续性影响摘要）

## 4. 预留边界（本阶段明确不展开）

- **图书馆本体**：不做写入/检索/策略召回/自动注入/评分系统/替换逻辑
- **连续性引擎**：不做多帧轨迹/衰减模型/继承模型重构/复杂调试台
- **自动优化**：Optimization Hint/Feedback Loop 只做建议与验证框架，不改参数、不自动执行
- **历史趋势系统**：不做长周期统计、AB、实验平台

## 5. 统一入口原则（写死）

- 解释与诊断统一入口：**Reasoning Console**
- 新功能若产生推理分支/排除/反馈驱动/收敛路径：必须接入 **Structure Tree → Metrics → Optimization Hint → Feedback Loop**
- 图书馆正式接入前：必须通过 **Knowledge Dual-Channel Interface Reserve** 预留层承接

## 6. 下一阶段建议（不在本文实现）

优先把“骨架上的质量信号”进一步用于：

- 更明确的 branch_count/branching_node_count 拆分
- 更严格的 feedback 有效性区分（形式有效 vs 质量有效）
- Optimization Feedback Loop 的 baseline 来源规范化（多样本/多帧对照）
- 图书馆本体接入前的“策略模板”规范化（仍通过 dual-channel + injection slot）

## 7. 结论（M0 Closure）

当前阶段主线骨架已形成并可审计：**看见过程 → 看见结构 → 看见质量 → 看见改进方向 → 验证建议 → 预留知识入口 → 预留连续性影响**。

