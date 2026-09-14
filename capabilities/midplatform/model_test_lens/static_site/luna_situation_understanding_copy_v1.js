/**
 * Luna Situation Understanding — copy v1 (candidate-only wording).
 */
(function (global) {
  "use strict";

  global.LunaSituationUnderstandingCopy = {
    version: "luna_situation_understanding_copy_v1",
    sectionTitle: "处境理解",
    sectionSubtitle: "Situation Understanding · L1 candidate",
    summaryCardTitle: "处境候选摘要",
    sceneLabel: "场景候选",
    ownerLabel: "scene owner",
    runnerHintLabel: "Runner hint",
    resolutionLabel: "Resolution",
    survivalTitle: "生存语境",
    taskCluesTitle: "任务线索",
    missingInfoTitle: "缺失信息",
    attentionTitle: "关注目标提示",
    modelNeedTitle: "能力需求提示",
    likelyNeededTitle: "Likely Needed",
    optionalTitle: "Optional",
    notNeededTitle: "Not Needed",
    conflictTitle: "Runner 冲突记录",
    emptyHint: "上传图像后，将基于 job/envelope dry-run 生成处境理解候选。",
    candidateOnly: "candidate_only",
    notFact: "not_fact",
    noRunnerInvocation: "no_runner_invocation",
    noFactWrite: "no_fact_write",
    sceneOwnedBy: "scene owned by Situation Layer",
    runnerHintAsEvidence: "runner hint as evidence",
    notExecuted: "未触发工具执行",
    forbiddenParts: [
      "已识别为店招", "已确认场景", "OCR 已执行", "SLAM 已关闭",
      "模型已经判断", "最终结论", "confirmed", "已识别为", "读取成功", "导航到", "fact"
    ],
    modelLabels: {
      ocr: "OCR",
      detection: "Detection",
      slam: "SLAM",
      depth: "Depth",
      tracking: "Tracking",
      vlm: "VLM",
      sam: "SAM"
    }
  };
})(typeof window !== "undefined" ? window : this);
