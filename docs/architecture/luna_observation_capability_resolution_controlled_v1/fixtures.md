# Controlled Fixtures

Evaluation package：
`capabilities/evaluation/observation_capability_resolution_controlled/`

覆盖：

1. 单 Demand 单匹配；
2. 单 Demand 多匹配且全部保留；
3. 两个独立 Demand；
4. 无 Demand；
5. 缺失 governed mapping；
6. 无 class match；
7. unavailable capability；
8. not-admitted capability；
9. Scenario 12 signage；
10. Scenario 12 human-flow；
11. 相同 class 的多个 Demand 不合并；
12. invalid Demand；
13. multi-class requirement fail-closed；
14. deterministic replay。

Scenario 12 使用 synthetic opaque capability class refs，不扩展正式 capability
taxonomy，也不将 signage 自动映射为 OCR 或将 flow 自动映射为某个模型。
