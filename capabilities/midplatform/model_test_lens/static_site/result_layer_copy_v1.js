/**
 * Result Layer — copy for segmentation result candidates (not fact, not observation layer).
 */
(function (global) {
  "use strict";

  global.ResultLayerCopy = {
    version: "result_layer_copy_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-MobileSAM-Single-Model-Execution-Integration-v1-002",
    panelTitle: "结果候选区",
    panelNotice: "result layer only · candidate_only · needs_fact_admission · 非 observation layer",
    labelSource: "来源",
    labelModel: "模型",
    labelConfidence: "置信度",
    labelMask: "Mask",
    labelExecution: "执行",
    labelFact: "Fact",
    labelTrace: "Trace",
    runControlledMobileSamBtn: "受控执行 MobileSAM",
    prepareMobileSamCandidateBtn: "生成 MobileSAM 受控执行候选",
    notExecutionCompleteFact: "completed 仅表示模型运行完成，不代表 fact=true",
    noAutoFactLabel: "禁止自动命名物体或生成事实标签",
    resultLayerNotObservationLayer: true,
    ocrCompletedNotFact: "OCR completed 仅表示候选文字完成，不是事实完成",
    ocrTextCandidateLabel: "OCR 文字候选",
  };
})(typeof window !== "undefined" ? window : this);
