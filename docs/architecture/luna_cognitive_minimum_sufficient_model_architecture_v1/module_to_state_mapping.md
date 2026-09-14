# Module to State Mapping

| 模块 | Core State 作用 |
|---|---|
| Field | 写入/更新 Field State |
| Self Model / Regulation | 约束 Self State 与 Resource State |
| Belief / Hypothesis / Understanding | 更新 Understanding State Candidate |
| Intent / Goal / Task | 更新 Goal State Candidate |
| Value Utility | 计算 Value State Candidate |
| Memory | 提供 Memory Influence State |
| Attention / Runtime | 影响 Resource 分配与转移候选 |
| Decision / Action | 产生 State → Action Candidate |
| Outcome / Learning | 产生 Understanding、Memory、Adaptive Update Candidate |

映射是唯一 Core State 入口，不改变既有模块 Owner。

