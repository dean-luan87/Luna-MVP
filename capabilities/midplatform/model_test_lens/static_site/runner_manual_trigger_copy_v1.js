/**
 * Runner Manual Trigger — UI copy (invocation request only, not execution).
 */
(function (global) {
  "use strict";

  global.RunnerManualTriggerCopy = {
    version: "runner_manual_trigger_copy_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Runner-Manual-Trigger-UI-Execution-And-Post-Review-v1-001",
    panelTitle: "待准入请求",
    panelNotice: "以下为 runner_invocation_request，准备申请执行，not_executed，不触发模型。",
    generateDetectionBtn: "生成检测请求",
    generateOcrBtn: "生成 OCR 请求",
    sendToAdmissionBtn: "送入准入检查",
    cancelRequestBtn: "取消请求",
    admitBtn: "标记 admitted",
    rejectBtn: "标记 rejected",
    hintNeedPin: "需先 Pin 入队",
    hintExcluded: "已排除，不能生成请求",
    hintStale: "需复核后再生成请求",
    hintBlocked: "策略阻止",
    hintNotDetectionOcr: "本阶段仅支持 Detection / OCR 请求",
    hintRouteMismatch: "路由不匹配，不能生成请求",
    hintDuplicate: "已有待处理请求",
    labelAdmission: "准入",
    labelExecution: "执行状态",
    labelRunner: "请求 runner",
    labelReason: "原因",
    labelTrace: "追溯",
    labelRequestedBy: "触发方",
    statusLine: "candidate_only / not_executed / not_fact",
    notExecutionNotice: "recommended only · not executed · 暂不执行",
    summaryPrefix: "待准入请求",
    traceToggle: "查看 trace_chain",
    noRunnerExecution: true,
    noModelCall: true,
    noFactWrite: true
  };
})(typeof window !== "undefined" ? window : this);
