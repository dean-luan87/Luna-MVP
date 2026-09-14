/**
 * Midplatform Single Model Interaction Validation — UI copy v1.
 */
(function (global) {
  "use strict";

  global.MidplatformInteractionCopy = {
    version: "midplatform_interaction_copy_v1",
    phaseRef: "Phase-P1-Midplatform-Single-Model-Interaction-Validation-UI-Execution-v1-001",
    sectionTitle: "中台二次理解",
    sectionNotice: "midplatform analysis · candidate_only · 非模型输出 · 非 fact",
    resultCandidateTitle: "Result Candidate",
    analysisCardTitle: "中台分析记录",
    correctionSectionTitle: "纠错分析",
    correctionRecordTitle: "Human Correction",
    attributionTitle: "中台归因",
    traceTitle: "Trace",
    labelModel: "模型",
    labelResultType: "结果",
    labelRegion: "区域",
    labelModelProvides: "模型提供",
    labelConfidence: "confidence",
    labelStatus: "状态",
    labelMidplatformJudgment: "中台判断",
    labelRegionFeatures: "区域特征",
    labelScheduleSuggestion: "调度建议",
    labelReason: "原因",
    labelUserFeedback: "用户反馈",
    labelAttribution: "纠错类型",
    labelImpactTarget: "影响对象",
    labelSuggestedExits: "建议出口",
    labelTraining: "是否训练",
    labelProcessing: "处理",
    modelProvidesGeometry: "区域几何信息",
    resultTypeSegmentation: "Segmentation Result Candidate",
    statusCandidateOnly: "candidate_only",
    scheduleOcrRoute: "OCR route candidate",
    scheduleReasonTextLikely: "该区域值得进一步文字观察（非 MobileSAM 断言文字）",
    mobileSamNotOcr: "MobileSAM ≠ OCR · 中台未确认路牌/文字内容",
    noOcrRunner: "本阶段不跑 OCR · route candidate only · ocr_runner_forbidden",
    trainingYes: "training_candidate pending_review",
    trainingNo: "否",
    forbiddenFactLabel: "禁止：确认路牌/文字内容 · 勿送入训练管线 · 修改 mask",
    emptyAnalysis: "受控执行 MobileSAM 后，中台将在此解释结果如何触发下一步观察调度。",
    emptyCorrection: "用户指错后，中台将在此展示归因与分流（须经中台治理）。"
  };
})(typeof window !== "undefined" ? window : this);
