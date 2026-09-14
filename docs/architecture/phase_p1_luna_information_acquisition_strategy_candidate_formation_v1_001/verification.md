# Verification

状态：`WAITING_FOR_USER_TERMINAL_VERIFICATION`

Runner marker：
`CONTROLLED_INFORMATION_ACQUISITION_STRATEGY_CANDIDATE_FORMATION_TEST`

本阶段由用户终端执行 controlled synthetic evaluation。Agent 不执行 Python、
Runner 或 Verifier；本阶段尚未宣称 PASS、GO 或 VERIFIED。

## Required cases

- `ONE_BRANCH_ONE_STRATEGY`：一个 admitted Branch、一个 explicit basis 形成一个 candidate；
- `ONE_BRANCH_MULTIPLE_STRATEGIES`：同一 Branch / Need 的三个 basis 形成三个 distinct candidates，不 winner-take-all；
- `MULTIPLE_BRANCHES_MULTIPLE_STRATEGIES`：多个 Branch 保留各自 strategy lineage；
- `NO_GOVERNED_ACQUISITION_BASIS`：无 basis 时零策略，不猜测；
- `DEFERRED_BRANCH` / `REJECTED_BRANCH`：非 admitted Branch 不形成策略；
- `IRRELEVANT_CONTEXT_CHANGE`：opaque context 改变不改变 strategy semantics；
- `SAME_NEED_DIFFERENT_GOVERNED_BASES`：basis 改变导致策略集合改变；
- `UNKNOWN_MODE`：缺失 mode 归一为 `UNKNOWN`；
- `CAPABILITY_CLASS_REF_PRESERVATION` / `OPPORTUNITY_REF_PRESERVATION`：refs 保留但不执行下游治理；
- `NO_BRANCHES` / `INVALID_INPUT`：空集合与 invalid candidate fail closed。

## Expected checks

Verifier 应检查多策略、admitted-only、basis sensitivity、context stability、
candidate/input immutability、lineage 与 ref preservation，以及所有 negative
guards。特别包括：无 strategy coordination、priority、resource merge/acquisition、
Attention、Observation Demand、Capability Requirement/Resolution、Provider / Model、
Decision / Task / Action、Field / Current World / Memory / PCN mutation 或 Truth
promotion。

用户终端命令：

```text
python -m capabilities.evaluation.information_acquisition_strategy_candidate_formation.runner_v1
python -m capabilities.evaluation.information_acquisition_strategy_candidate_formation.verifier_v1
```
