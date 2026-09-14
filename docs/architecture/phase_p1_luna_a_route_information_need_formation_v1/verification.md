# Verification Plan

状态：`GO — VERIFIED — PHASE CLOSED`

`INFORMATION_NEED_FORMATION_GAP = CLOSED`。

用户终端结果：

```text
all_checks_passed=true
check_count=99
cognitive_logic_result=PASS
operational_result=PASS
failed_checks=[]
final_decision=GO
```

用户终端应运行 controlled runner and verifier only. Agent does not run them。

Marker:
`CONTROLLED_A_ROUTE_INFORMATION_NEED_FORMATION_TEST`

## Required contrasts

1. `SAME_GOAL_DIFFERENT_CURRENT_WORLD`：相同目标在不同 Current World coverage
   下产生不同 necessary unknowns。
2. `SAME_GOAL_NEED_ALREADY_SATISFIED`：coverage 覆盖全部目标条件时返回
   `NO_ACTIVE_NEED`。
3. `SAME_GOAL_PARTIAL_COGNITIVE_COVERAGE`：已覆盖一部分时只保留下一必要未知。
4. `SAME_GOAL_DIFFERENT_GOVERNED_ROLE`：同目标/Field/World 使用不同的、明确
   governed role condition signal，形成不同 unknowns。
5. `SAME_GOAL_IRRELEVANT_CONTEXT_CHANGE`：仅改变 opaque Context ref 时，Need
   behavior/id 保持稳定。
6. `DIFFERENT_GOAL_SAME_CURRENT_WORLD`：同一 Current World 对不同目标条件形成
   不同 Need 行为。

## Expected proof

- Need candidate 由 objective condition 与 Current World coverage 的差集形成，
  不是 static Goal→Need lookup，也不读取 scenario id。
- `CognitiveNeedCandidateV1` 通过既有 validator，state version 来自 Current
  World。
- 目标、Intent、Concern、Field、Current World 都不被修改。
- candidate-only；没有 Truth、Memory/PCN、Decision/Task/Action side effect。
- 没有 Observation Demand formation、Capability selection、Provider 或 Model
  invocation。
- 无关 Context 不改变认知结果；相关 Current World coverage 会改变结果。
- 已满足目标条件不会产生重复 Need。

Negative controlled cases include non-candidate input rejection and a mutated
Current World boundary rejection. These are guards, not Runtime observations。

本阶段不验证 Observation Demand、Capability Resolution、Information Gap、
Re-observation 或 Stop 的新语义；这些 owner 和 contract 保持不变。

已验证成熟度仅为：governed objective conditions − Current Cognitive Coverage
→ Necessary Unknown → `CognitiveNeedCandidateV1`。Self 如何参与 objective
formation、Goal-conditioned Minimum Self/External View、required condition 的
更上游自主形成、pre-observation Attention 和 Observation Demand Formation
仍未验证。
