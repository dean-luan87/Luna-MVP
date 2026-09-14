# Negative Guards

本阶段禁止：

- 修改 Requirement satisfaction、Need、Branch、Strategy、Coordination、Demand；
- Provider/Model selection、binding、invocation；
- OCR、Camera、SLAM、FPO、Observation Gateway、Perception routing/runtime；
- capability activation、reservation、scheduling、execution；
- ranking、scoring、priority、winner、best-fit、fallback、substitution inference；
- string/keyword/semantic inference；
- Resource acquisition、Evidence Fusion、Conflict Resolution；
- Goal、Intent、Decision、Task、Action；
- Current World、Field、Memory/PCN 或 Truth mutation。

Only explicit Demand→single capability-class mappings and exact controlled inventory
matching are allowed. Invalid, missing, unavailable, not-admitted and ambiguous
multi-class inputs fail closed without fallback.
