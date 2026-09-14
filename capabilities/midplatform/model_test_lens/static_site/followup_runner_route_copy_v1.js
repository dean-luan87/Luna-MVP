/**
 * Followup Runner Route — UI copy (candidate queue only, not execution).
 */
(function (global) {
  "use strict";

  global.FollowupRunnerRouteCopy = {
    version: "followup_runner_route_copy_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-UI-Queue-Execution-And-Post-Review-v1-001",
    panelTitle: "后续任务候选队列",
    panelNotice: "以下为后续模型任务候选，recommended only，不触发执行，不写 fact。",
    activeQueueTitle: "已入队候选",
    manualOnlyTitle: "manual_only 候选（需手动 pin）",
    excludedTitle: "已排除",
    admissionAuto: "auto_eligible",
    admissionManual: "manual_only",
    admissionRejected: "rejected",
    queueStateCandidate: "candidate",
    queueStatePinned: "pinned",
    queueStateExcluded: "excluded",
    labelAdmission: "准入",
    labelReason: "原因",
    labelStatus: "状态",
    labelRunner: "建议 runner",
    labelRecommendedOnly: "recommended only · candidate route · not executed",
    statusLine: "candidate_only / not_executed / not_fact",
    pinBtn: "Pin 入队",
    unpinBtn: "取消 Pin",
    excludeBtn: "排除",
    restoreBtn: "恢复候选",
    correctionBoost: "由人工指错提升优先级（非 ground truth）",
    summaryPrefix: "后续任务候选",
    noRunnerExecution: true,
    noModelCall: true,
    noFactWrite: true
  };
})(typeof window !== "undefined" ? window : this);
