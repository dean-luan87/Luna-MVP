# Verification

状态：`GO — VERIFIED — PHASE CLOSED`

用户终端真实验证结果：

- `all_checks_passed=true`
- `cognitive_logic_result=PASS`
- `operational_result=PASS`
- `failed_checks=[]`
- `final_decision=GO`

结论：`COGNITIVE_BRANCH_GOVERNANCE_GAP = CLOSED`。

Runner marker：
`CONTROLLED_COGNITIVE_BRANCH_GOVERNANCE_TEST`

## Required cases

- `MULTIPLE_VALID_BRANCHES`：两个有效 Branch 同时 `ADMITTED`，证明 no winner-take-all；
- `ONE_VALID_ONE_INVALID_BASIS`：无效 basis 只使对应 Branch `REJECTED`；
- `CURRENTLY_NOT_NEEDED_BUT_VALID`：合法但当前无需继续探索时为 `DEFERRED`；
- `NO_CANONICAL_EQUIVALENCE_RETAIN_BOTH`：当前没有 canonical equivalence 时，
  不进行人工 dedup，两个独立 Branch 都保留；
- `NO_BRANCHES`：空输入保持空 admitted/deferred/rejected 集合；
- `IRRELEVANT_CONTEXT_CHANGE`：opaque Context 改变不改变治理结果；
- `BASIS_REMOVED`：basis 从 current state 移除后变为 `REJECTED`；
- `NEED_BECOMES_CURRENTLY_SATISFIED`：Need 满足且明确当前无需继续时变为 `DEFERRED`，
  不是 `REJECTED`；
- `RESOURCE_AVAILABILITY_CHANGE`：resource marker 变化不改变治理结果；
- `INVALID_CANDIDATE`：candidate contract 边界失效时局部 `REJECTED`。

Verifier 必须检查：

- `ADMITTED` / `DEFERRED` / `REJECTED` 语义正确；
- 多个有效 Branch 可同时 admitted；
- valid Branch 不受另一个 Branch rejection 影响；
- deferred 保留 identity、candidate 与 recoverability；
- original candidate snapshot 前后一致；
- Formation、Resource、Observation、Capability、Lifecycle 与执行边界均未触发；
- 没有 Truth、Field、Current World、Memory / PCN mutation。

真实验证确认：

1. Multiple valid branches can all be `ADMITTED`，Governance 不是 winner-take-all；
2. invalid basis 只局部 `REJECTED`，不影响无关 valid Branch；
3. `DEFERRED != REJECTED`；currently-not-needed Branch 为 `DEFERRED`；
4. satisfied Need 相关 Branch 被 deferred 而非销毁；
5. candidate identity、lineage、provenance、recoverability 保留；
6. `CognitiveBranchCandidateV1` 在 Governance 前后保持 immutable；
7. 无 canonical equivalence 时保留 distinct candidates，不发明 semantic dedup；
8. resource availability 改变不影响治理结果；
9. 没有重跑 Branch Formation、生成新 Branch、Merge、Convergence、Close、Reopen
   或 execution priority；
10. 没有 Resource Governance / Acquisition、Observation Demand、Capability
    Requirement、Decision、Task、Action、Provider、Model、Memory、PCN、Field 或
    Current World mutation，也没有 Truth promotion。

阶段 closure 后，Branch 主链为：

```text
Branch Formation
→ CognitiveBranchCandidateV1
→ Branch Governance
→ Governed Exploration Branch Set
```

下一边界记录为：

`NEXT_BOUNDARY = GOVERNED_BRANCH_TO_INFORMATION_ACQUISITION_CONTINUITY`

该边界仅记录，不在本阶段实现。

用户终端命令：

```text
python -m capabilities.evaluation.cognitive_branch_governance.runner_v1
python -m capabilities.evaluation.cognitive_branch_governance.verifier_v1
```

Agent 未执行上述命令。
