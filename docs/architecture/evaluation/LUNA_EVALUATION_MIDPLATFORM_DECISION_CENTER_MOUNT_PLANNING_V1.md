# Luna Evaluation — Decision Center Mount Planning v1

**Verifier**：`verify_midplatform_decision_center_mount_planning_v1.py`  
**MIN_CHECKS**：420

## 必检项

### 上游

- II Foundation Handoff DryRunAndReview verifier=GO
- foundation_id=midplatform_information_integration_foundation_v1
- depends_on=midplatform_micro_os_foundation_v1
- runtime_status=not_enabled
- primary route = Decision Center Mount Planning

### Mount Contract

- 10 段模块合同齐全
- layer=L7，role 声明非 executor / 非 output layer
- 不得重新定义 Information Integration

### Input / Output

- core input = decision_context_candidate
- 全部输出为 candidate
- decision_candidate ≠ final action
- decision_candidate ≠ user output

### State Machine & Placement

- 15 个 decision states，全部 candidate-level
- model_invoked_now=false
- rule/algorithm placement 无越权

### Boundaries

- governance / health / II dependency boundary 完整
- downstream handoff direct_mount=false
- boundary matrix 全 false
- sample flows ≥ 6，failure routes ≥ 14

## 预期

`verifier: GO` → `MIDPLATFORM_DECISION_CENTER_MOUNT_PLANNING_READY_FOR_DRYRUN_AND_REVIEW`
