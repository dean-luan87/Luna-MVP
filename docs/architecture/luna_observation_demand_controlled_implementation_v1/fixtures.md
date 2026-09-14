# Controlled Fixtures

Evaluation package `capabilities/evaluation/observation_demand_controlled/` 覆盖：

1. 单个 admitted perception strategy；
2. 两个独立 admitted strategies；
3. deferred、blocked dependency、suppressed redundant、incompatible；
4. zero strategy 与 requirement-already-satisfied；
5. 多 cognitive gaps 的独立 lineage；
6. Scenario 12 的 signage / human-flow 双 demand shape；
7. unsupported acquisition mode；
8. invalid coordination input。

Fixtures 只提供 explicit governed observation mappings。它们不把 target 从字符串
或 fixture 名称推断出来，也不启动 Sandbox 或真实 acquisition。
