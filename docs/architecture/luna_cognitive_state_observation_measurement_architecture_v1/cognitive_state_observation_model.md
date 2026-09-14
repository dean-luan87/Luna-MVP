# Cognitive State Observation Model

内部 Core State Vector 记为 `L_t`，观测输出为 `O_t=H(L_t)`。Observation 是有来源、范围、时间和置信度的指标，不等于完整内部状态，也不替代 Reality。

观测必须标注 Field Scope、采样窗口、证据来源、未知和 trace。观测器只能产生 Measurement Candidate，不能写回 State、Memory、Self 或 Parameter。

