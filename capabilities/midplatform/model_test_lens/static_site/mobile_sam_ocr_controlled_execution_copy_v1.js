/**
 * MobileSAM → OCR Controlled Execution — UI copy v1.
 */
(function (global) {
  "use strict";

  global.MobileSamOcrControlledExecutionCopy = {
    version: "mobile_sam_ocr_controlled_execution_copy_v1",
    phaseRef: "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Controlled-Execution-UI-Execution-v1-001",
    ocrRequestTitle: "OCR 请求",
    ocrAdmissionTitle: "OCR 准入",
    ocrExecutionCandidateTitle: "OCR 受控执行候选",
    generateOcrRequestBtn: "生成 OCR 请求",
    submitForAdmissionBtn: "送入 OCR 准入检查",
    runAdmissionBtn: "执行 OCR 准入检查",
    runControlledOcrBtn: "受控执行 OCR（Sandbox）",
    prepareOcrExecutionBtn: "准备 OCR 受控执行",
    cancelRequestBtn: "取消 OCR 请求",
    viewTraceBtn: "查看 trace",
    generateExecutionCandidateBtn: "生成 OCR 受控执行候选",
    prepareExecutionBtn: "准备 OCR 受控执行",
    generatePlanBtn: "生成 OCR 执行计划",
    admittedNotice: "admitted · still_not_executed · not_fact",
    notExecutionNotice: "准入通过不等于执行 OCR",
    inputReviewTitle: "OCR 输入审查",
    inputPrinciple: "OCR 只收到「这里值得做文字观察」，不是「这里是什么文字」",
    futureEnvelopeTitle: "未来输出 envelope（本阶段不产生）",
    fusionPlaceholderTitle: "未来多模型融合占位",
    fusionPlaceholder: "MobileSAM 提供 region geometry · OCR 提供 text candidate · 中台生成 multimodal_evidence_candidate · 仍需 Fact Admission",
    dualModelAttributionTitle: "双模型纠错归因",
    emptyRequests: "从「模型协作候选」生成 OCR 请求后显示于此。",
    labelRegion: "区域",
    labelStatus: "状态",
    labelTrace: "Trace",
    summaryOcrRequests: "OCR 请求",
    summaryOcrCandidates: "OCR 受控执行候选",
    ocrExecutedMustBeZero: "OCR executed 必须为 0",
    no_ocr_runner_call: true,
    ocr_copy_must_not_imply_execution: true,
    ocr_copy_must_not_imply_text_recognized: true
  };
})(typeof window !== "undefined" ? window : this);
