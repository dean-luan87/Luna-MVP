# Luna Evaluation — Information Integration Foundation Handoff Planning v1

**Verifier**：`verify_midplatform_information_integration_foundation_handoff_planning_v1.py`  
**MIN_CHECKS**：300

## 必检项

### 上游

- Post-DryRun Review verifier=GO
- 17 个上游 artifact 可消费

### Version Tag

- foundation_id=midplatform_information_integration_foundation_v1
- depends_on=midplatform_micro_os_foundation_v1
- version=1.0.0-skeleton
- runtime_status=not_enabled

### Frozen Interfaces

- 9 类 candidate type（candidate_id / trace_ref / fact_status 必备，磁盘验证）
- 10 个 pure function（candidate only）
- 9 个 static validator（downstream 可复用）

### Contracts

- handoff contract：禁止下游把 candidate 当 fact / decision / output
- downstream output contract：6 consumer，output_gate_ready=false
- forbidden mutation 10 项
- change control 7 步，本阶段不执行 change

### Boundary & Route

- files_created=true，其余 runtime/model/provider/write/output/mount=false
- primary next = Decision Center Mount Planning
- secondary = Health Watchdog Mount Planning
- deferred 4 项

## 预期

`verifier: GO` → `MIDPLATFORM_INFORMATION_INTEGRATION_FOUNDATION_HANDOFF_PLANNING_READY_FOR_DRYRUN_AND_REVIEW`
