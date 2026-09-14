# Luna Evaluation — Information Integration Mount Planning v1

**Verifier**：`verify_midplatform_information_integration_mount_planning_v1.py`  
**MIN_CHECKS**：360

## 必检项

### 上游

- Foundation Freeze DryRunAndReview verifier=GO
- `foundation_id=midplatform_micro_os_foundation_v1`
- `runtime_status=not_enabled`
- Information Integration 为 primary route

### Mount Contract

- 10 段合同齐全（module_definition_template_v1）
- L6 层级、planning_only、all_candidate

### Input Contract

- Event / WorkingMemoryEntry / SchedulingDecisionCandidate
- trace / health_tag / ttl / source_chain / candidate_not_fact

### Output Contract

- 全部 candidate，禁止 fact / runtime action / user output / memory write / worldmodel write

### Model / Rule / Algorithm Placement

- 模型用于语义整合与 candidate 草拟
- 规则用于 candidate/fact 边界、P0/P1、governance、TTL
- 算法用于 relevance / conflict / allocation
- 本阶段 `no_model_in_mount_planning_now=true`

### Boundaries

- governance / health / WorldModel-Memory feedback 明确
- downstream handoff 8 条，`mount_now=false`
- sample flow ≥ 5
- failure route ≥ 12
- health metric scope 存在
- boundary matrix 15 项全 false

### Non-Claims

- Mount Planning ≠ implemented / mounted / runtime / model / output / write

## 预期

`verifier: GO` → `MIDPLATFORM_INFORMATION_INTEGRATION_MOUNT_PLANNING_READY_FOR_DRYRUN_AND_REVIEW`
