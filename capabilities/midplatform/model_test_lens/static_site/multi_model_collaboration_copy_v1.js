/**
 * Multi-model collaboration copy — exploration smoke UI.
 */
(function (global) {
  "use strict";

  global.MultiModelCollaborationCopy = {
    version: "multi_model_collaboration_copy_v1",
    phaseRef: "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Exploration-Smoke-v1-001",
    sectionTitle: "模型协作候选",
    labelRegion: "区域",
    midplatformAnalysis: "中台分析",
    detectedPrefix: "检测到",
    staticCandidate: "静态区域候选",
    nextSuggestion: "下一建议",
    statusCandidate: "candidate_only",
    notExecuted: "未执行 OCR",
    emptyHint: "中台判定值得文字观察时，将在此展示 MobileSAM → OCR 协作候选（不跑 OCR）。",
    traceHint: "trace: region → result_candidate → analysis → route → task"
  };
})(typeof window !== "undefined" ? window : this);
