/**
 * Runner Invocation Admission — policy constants (no runner execution).
 */
(function (global) {
  "use strict";

  var REQUIRED_TRACE_STAGES = [
    "segmentation_region",
    "observation_attention_record",
    "followup_model_route_candidate",
    "runner_task_candidate",
    "runner_invocation_request"
  ];

  var POLICY_REFS = [
    "RunnerInvocationAdmissionPolicyV1",
    "ManualRunnerTriggerAdmissionPolicyV1",
    "DetectionOcrManualTriggerRoutePolicyV1"
  ];

  var REJECTION_CODES = {
    orphan_request: "orphan request：无法关联 source task",
    trace_chain_incomplete: "trace_chain 不完整",
    source_task_not_pinned: "source task 未 pinned",
    source_task_excluded: "source task 已 excluded",
    source_task_blocked_by_policy: "source task 被策略阻止",
    stale_candidate_without_reconfirmation: "stale_candidate 未复核",
    route_type_mismatch: "requested_runner_type 与 route 不匹配",
    execution_status_not_not_executed: "execution_status 不是 not_executed",
    missing_candidate_boundary_flags: "缺少 candidate_only / not_fact 标记",
    bypass_runner_task_candidate: "试图绕过 runner_task_candidate"
  };

  global.RunnerInvocationAdmissionPolicy = {
    version: "runner_invocation_admission_policy_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Runner-Invocation-Admission-Execution-And-Post-Review-v1-001",
    REQUIRED_TRACE_STAGES: REQUIRED_TRACE_STAGES,
    POLICY_REFS: POLICY_REFS,
    REJECTION_CODES: REJECTION_CODES,
    admittedDoesNotExecuteRunner: true,
    executionStatusOnAdmit: "not_executed"
  };
})(typeof window !== "undefined" ? window : this);
