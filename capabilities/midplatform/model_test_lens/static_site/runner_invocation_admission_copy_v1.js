/**
 * Runner Invocation Admission — UI copy (gate only, not execution).
 */
(function (global) {
  "use strict";

  global.RunnerInvocationAdmissionCopy = {
    version: "runner_invocation_admission_copy_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Runner-Invocation-Admission-Execution-And-Post-Review-v1-001",
    runAdmissionBtn: "执行准入检查",
    recheckAdmissionBtn: "重新检查",
    cancelRequestBtn: "取消请求",
    labelAdmissionDecision: "准入判定",
    labelAdmissionReason: "准入原因",
    labelRejectionReason: "拒绝原因",
    labelTraceVerified: "trace 已验证",
    labelRouteMatch: "route 匹配",
    labelPolicyRefs: "策略引用",
    labelExecution: "执行状态",
    admittedNotice: "admitted · 仍 not_executed · 不触发 runner",
    statusLine: "candidate_only / not_executed / not_fact",
    notExecutionNotice: "admission gate only · not runner output · 暂不执行",
    summaryPrefix: "准入请求",
    traceToggle: "查看 trace_chain",
    noRunnerExecution: true,
    admissionCopyMustNotImplyExecution: true
  };
})(typeof window !== "undefined" ? window : this);
