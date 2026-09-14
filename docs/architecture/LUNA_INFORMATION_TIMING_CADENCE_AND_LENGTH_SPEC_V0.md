# Luna — Information Timing, Cadence, and Length Spec v0（信息对象时效/节奏/长度约束规范：占位）

Protocol/Spec Name: LUNA_INFORMATION_TIMING_CADENCE_AND_LENGTH_SPEC_V0  
Version: v0  
Status: Draft (Placeholder)  
Owner: System / Mid-Platform Governance (placeholder)  
Last Updated: 2026-04-15  
Change Summary: 初版占位：冻结信息对象在跨模块流动时的时效/节奏/长度约束维度与分类思路；不定参数、不接线。  
Where Used: docs-level system governance; future output governance and cross-module constraints (placeholder)  

---

## A. 文档定位（写死）

- 这是信息对象时间/节奏/长度约束的系统级占位文档。
- 当前先定义约束方向，不展开实现。
- 当前不等同于语音输出治理；它是高于单一语音模块的“信息流约束”。

---

## B. 为什么不能只放在语音层

- 很多信息在到达语音之前就可能已经：过期、过密、过长、重复。
- 因此必须在“信息对象层”先有传输约束；否则输出治理层将被迫承接全部系统性问题。
- 输出治理层只是后续消费阶段，不足以承担全部约束来源与一致性。

---

## C. 未来应纳入的信息约束维度（概念占位）

> 当前只写概念与作用：不定真实数值，不定实现细节。

- **ttl_ms / 时效窗口**：对象在跨模块流动时的有效期；过期应降级/丢弃/转慢链（占位语义）。
- **cadence_class / 节奏等级**：对象允许的更新频率等级（高频/中频/低频，占位）。
- **length_budget / 表达长度预算**：对象在“传输与消费前”的长度预算（不是语音播报长度）。
- **dedupe_window_ms / 去重窗口**：在一定窗口内相同/近似对象的去重原则（占位）。
- **latency_tolerance_ms / 延迟容忍度**：对象从产生到消费的最大可容忍延迟（占位）。
- **priority_band / 优先级带**：对象在队列/合并/延迟时的优先级分层（占位）。

---

## D. 约束应按对象类型分层（分类思路占位）

> 不同对象的时间、节奏、长度约束不能完全一样；本节只冻结分类思路，不展开策略表。

- **风险类对象**：强调低延迟与强时效（占位原则）。
- **任务关键对象**：与当前任务紧耦合，节奏与去重窗口需受任务阶段影响（占位）。
- **环境碎片对象**：更偏慢链沉淀，允许更大延迟容忍度与更低更新频率（占位）。
- **建议/承接/裁决对象**：必须避免高频漂移；强调可追踪与去重窗口（占位）。

---

## E. 与输出治理层的关系（写死）

- 本文档不等于语音输出治理。
- 本文档定义的是“信息对象在传输与消费前的约束”。
- 未来语音输出治理层应消费这些约束，而不是重新发明一套。

---

## F. 当前不做（写死）

- 不做真实参数配置
- 不做真实限流实现
- 不做真实输出调度器
- 不做和语音模块的真实代码接线
- 不做系统级去重实现

---

## G. 后续专题入口（占位）

- Output Governance Layer v0
- Object Expiry Policy v0
- Dedupe and Cadence Control v0
- User State Driven Output Budget v0

