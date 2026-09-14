# Phase-P1 Luna Required Cognitive Condition Formation v1

状态：`WAITING_FOR_USER_TERMINAL_VERIFICATION`

本 Phase 只补齐 A-Route 的第一个上游 formation 缺口：
`REQUIRED_COGNITIVE_CONDITION_FORMATION_GAP`。

目标主链为：

```text
Goal / Intent / Concern
  + governed Role / Context / Field
  + current governed cognitive situation
  → Required Cognitive Condition Candidate
  → Minimum Relevant Cognitive View
  → Current Cognitive Coverage
  → Information Need
```

Required Cognitive Condition 不是 Information Need。它表示当前
cognitive objective 为继续推进而需要成立、确认或获知的最小条件；已被
coverage 满足的条件仍然是 required，只在独立 satisfaction 集合中标记。
Need 仍由既有 `required conditions - current coverage` adapter 形成。

本实现是 `Governed State-Sensitive Required Cognitive Condition Formation`。
它消费由 Goal/Intent/Concern governance 提供的显式条件规则，在 A-Route
内对当前选定的认知情况执行 objective applicability、activation、suppression、
satisfaction 与 minimum-set 选择。它不解析 goal、context 或 scenario 字符串。

本 Phase 不实现 Observation Demand、Pre-observation Attention、Capability
Resolution、Meaning、Planning、Identity、Memory、PCN、Decision、Task 或
Action。
