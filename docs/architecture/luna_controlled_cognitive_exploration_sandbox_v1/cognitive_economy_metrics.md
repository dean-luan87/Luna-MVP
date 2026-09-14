# Cognitive Economy Metrics

每个 round 记录原始、可解释指标：

- required condition count；
- Information Need count；
- Branch count；
- admitted / deferred / rejected Branch count；
- Strategy candidate count；
- active strategy candidate count（本阶段等同于形成的 candidate 数，不表示 lifecycle active）；
- unresolved gap count；
- branches per Need；
- strategies per admitted Branch。

这些指标不组成“越少越好”的总分。它们用于比较：

- 场景复杂度增加时，候选是否按显式 cognitive basis 增长；
- 无关环境变化是否导致不必要扩张；
- simulated evidence 回流后 Need / Branch / Strategy 是否变化；
- zero-strategy 场景是否被诚实保留。
