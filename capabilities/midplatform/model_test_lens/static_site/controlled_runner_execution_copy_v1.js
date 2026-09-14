/**
 * Controlled Runner Execution — UI copy (execution candidate only, not runner execution).
 */
(function (global) {
  "use strict";

  global.ControlledRunnerExecutionCopy = {
    version: "controlled_runner_execution_copy_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Controlled-Runner-Execution-UI-Execution-v1-001",
    panelTitle: "受控执行候选",
    panelNotice: "execution candidate only · planned_only · not_executed · not_fact · 模型尚未被调用",
    generateExecutionCandidateBtn: "生成受控执行候选",
    prepareDetectionBtn: "准备 Detection 执行",
    prepareOcrBtn: "准备 OCR 执行",
    cancelCandidateBtn: "取消候选",
    markReadyBtn: "标记待执行审查",
    labelSource: "来源",
    labelTask: "任务",
    labelInput: "输入",
    labelStrategy: "执行策略",
    labelStatus: "状态",
    labelOutput: "输出",
    labelFact: "Fact",
    labelNotExecuted: "尚未运行",
    labelInputReview: "输入审查",
    labelAllowedInput: "允许输入",
    labelForbiddenInput: "禁止输入",
    labelSourceAttention: "来源",
    labelReason: "原因",
    detectionCandidateTitle: "Detection Candidate",
    ocrCandidateTitle: "OCR Candidate",
    notExecutionNotice: "受控执行候选 · 不是 runner 结果 · 不触发模型",
    statusLine: "candidate_only / not_executed / not_fact / needs_fact_admission",
    admittedGenerateHint: "admitted request · 可生成受控执行候选 · 仍不触发 runner",
    inputForbiddenDetection: "禁止输入：fact label · confirmed object name · navigation context",
    inputForbiddenOcr: "禁止输入：fact text · 预填真实文字 · human correction as ground truth",
    humanCorrectionPriorityOnly: "human correction 仅 priority signal · 非 ground truth",
    hintNeedAdmitted: "需 admitted request 才能生成执行候选",
    hintDuplicate: "该 request 已有活跃执行候选",
    hintCancelled: "request 已取消，不能生成执行候选",
    hintRejected: "request 已拒绝，不能生成执行候选",
    hintPending: "request 待准入，不能生成执行候选",
    summaryPrefix: "受控执行候选",
    traceToggle: "查看 trace_chain",
    noRunnerExecution: true,
    executionCopyMustNotImplyExecution: true
  };
})(typeof window !== "undefined" ? window : this);
