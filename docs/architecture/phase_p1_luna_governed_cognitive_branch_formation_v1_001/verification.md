# Verification

状态：`GO — VERIFIED — PHASE CLOSED`

用户终端真实验证结果：

- `all_checks_passed=true`
- `operational_result=PASS`
- `cognitive_logic_result=PASS`
- `failed_checks=[]`
- `final_decision=GO`

结论：`COGNITIVE_BRANCH_FORMATION_GAP = CLOSED`。

Runner marker：
`CONTROLLED_GOVERNED_COGNITIVE_BRANCH_FORMATION_TEST`

## Cases

- `SINGLE_SUFFICIENT_EXPLANATION`：单一显式解释只形成至多一个 candidate，不强制 fan-out；
- `MULTIPLE_HYPOTHESIS_ALTERNATIVES`：两个显式 Hypothesis 形成两个 distinct Branch；
- `MULTIPLE_UNRESOLVED_GAPS`：两个显式 Gap/Need 形成两个独立 Branch；
- `EXPLICIT_CONFLICT_WITH_EXISTING_ALTERNATIVES`：Conflict 只引用已有 alternatives；
- `IRRELEVANT_CONTEXT_CHANGE`：opaque Context 改变不改变 Branch set；
- `SAME_PROBLEM_DIFFERENT_EXISTING_ALTERNATIVES`：basis 改变导致 Branch set 改变；
- `NO_EXPLICIT_BRANCH_BASIS`：没有 governed basis 时不生成 Branch。

Verifier 应检查：

- Branch refs distinct、basis 与 canonical Hypothesis / Need refs 保留；
- lineage、trace、provenance 完整；
- formation-only status，不产生 governance result；
- candidate-only / read-only / non-Truth；
- 没有 resource acquisition、Observation Demand、Capability Requirement、Decision、Task、Action、Provider、Model 或 autonomous child runtime；
- 现有 Minimum Sufficient Cognition Loop 的 Sufficiency、Stop、Re-observation 语义未被改变。

已验证行为：

- multiple hypotheses → distinct branches；
- multiple gaps → distinct branches；
- explicit conflict 只使用已有 alternatives；
- no explicit basis → no generated branches；
- irrelevant context stable；
- cognitive basis change → branch set changes。

边界确认：Branch Formation != Branch Governance。Branch 仍为
candidate-only / read-only / non-Truth，不产生 admission、priority、resource
acquisition、execution 或生命周期治理结果。

后续认知断点：

```text
Branch Candidates
→ Governance Decisions
→ Governed Active Exploration Set
```

用户终端命令：

```text
python -m capabilities.evaluation.governed_cognitive_branch_formation.runner_v1
python -m capabilities.evaluation.governed_cognitive_branch_formation.verifier_v1
```

上述结果来自用户终端；Agent 未执行 Runner 或 Verifier。
