# Cognitive State Machine Architecture v1

## 定位

Cognitive State 描述 Luna 当前以何种认知模式处理现实。它不是 Field、Flow、Runtime Scheduler 或 Action Command。本阶段只冻结状态模型和迁移合同。

## 六类状态

`Observation → Understanding → Decision → Action → Reflection → Learning → Observation`

- Observation：收集 Evidence、建立或更新 Field。
- Understanding：组合 Context、Hypothesis、Belief 与 Validation。
- Decision：组织 Goal、Value、Candidate 并进行 Arbitration。
- Action：承载已批准行动的观察窗口；不在本阶段执行。
- Reflection：比较 Expected/Actual Outcome，形成评价候选。
- Learning：识别 Pattern、Schema 与 Growth Candidate；必须经过 Self Review。

## 状态边界

State 只输出 State Candidate、Entry/Exit Candidate 和 Attention Policy Candidate。它不能自动切换、执行 Action、修改 Reality/Memory/Schema/Self，也不能启动 Learning Runtime 或 B Route。

