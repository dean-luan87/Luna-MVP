# Implementation Plan（Architecture Only）

1. 复用 Core State Vector、State Transition、Self Calibration、Dynamic Function、Hive 和 B Route 合同。
2. 先建立只读 Observation/Metric Registry 与 Trace，再设计 Runtime 采样适配器。
3. 质量和 Fitness 只生成候选，禁止自动评分驱动 Action、参数优化或训练。
4. 任何跨 Field 比较、长期校准和 Hive 使用都必须经过 Scope、隐私、证据、风险与 Self Review。

