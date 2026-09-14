# Module Interaction Contract

| 模块 | 输入 | 输出 | 权限边界 |
|---|---|---|---|
| Reality/Evidence | 外部观察 | Evidence Candidate | 不产生意义 |
| Cognitive Field | Evidence、Self、Social、Memory、Knowledge | Current Field Candidate | 不覆盖 Reality |
| Attention | Field、Goal、Risk、Resource | Attention Candidate | 不执行、不写 Memory |
| Context | Field、Attention、Memory、Knowledge | Context Package | 不成为事实 |
| Hypothesis/Belief | Context、Evidence、Unknown | Hypothesis/Belief Candidate | 可并存、可被反驳 |
| Understanding | Field、Hypothesis、Belief、Knowledge | Understanding Candidate | 不替代 Reality |
| Goal | Understanding、Self、Value | Goal Candidate | 不直接生成 Action |
| Value Utility | Goal、Cost、Risk、Self | Utility/Priority Candidate | 不作最终决策 |
| Decision Arbitration | Candidates、Constraints | Selected Decision Candidate | 不执行 |
| Action Boundary | Approved Candidate | Action Request Candidate | 是执行闸门 |
| Outcome Evaluation | Actual Outcome、Expected Outcome | Evaluation/Experience Candidate | 不自动学习 |
| Memory/Schema | Validated Experience | Memory/Schema Candidate | 不覆盖 Reality |
| Selective Learning | Pattern、Utility、Evidence | Growth Candidate | 需 Self Review |
| Self Governance | Candidate、Constitution、Self State | Review/Veto Candidate | 不替代 Brain/Runtime |

所有跨模块传递必须带有 `field_ref`、`provenance`、`confidence` 或 `unknowns`（适用时）以及 trace 引用。

