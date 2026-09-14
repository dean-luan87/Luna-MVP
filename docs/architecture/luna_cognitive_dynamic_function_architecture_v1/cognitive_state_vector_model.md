# Cognitive State Vector Model

## 向量

建议基础分量：`observation_activation`、`understanding_confidence`、`risk_attention`、`exploration_drive`、`memory_activation`、`decision_pressure`。每个分量为有界连续值，并带有时间戳、Field 引用、证据来源和置信度。

向量是当前认知状态的表示，不是 Reality、Decision、Action 或 Memory。未知、冲突和缺失分量必须显式保留，不能用默认高置信度填充。

## 演化候选

函数输出只能是 State Vector Update Candidate、Attention Policy Candidate、Threshold Candidate 或 Reconsideration Candidate。任何实际更新需由未来 Runtime/治理流程批准。

