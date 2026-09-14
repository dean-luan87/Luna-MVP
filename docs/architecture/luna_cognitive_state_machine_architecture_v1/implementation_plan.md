# Implementation Plan（Architecture Only）

1. 复用 A Route Integration、Cognitive State Management、Self Rhythm、Attention、Decision、Outcome 与 Selective Learning 合同。
2. 首先实现 State/Flow/Field/Trace 的只读适配接口；任何 Runtime 状态机另行立项。
3. 迁移前登记 State Owner、Entry/Exit 条件、允许依赖和负向约束。
4. 后续实现必须由 Runtime Governance 批准；不得把本阶段合同变成 Scheduler、Action Runtime 或 Learning Runtime。

