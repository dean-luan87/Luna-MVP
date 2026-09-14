/**
 * Luna Agent Planning — governance copy v1 (explainable, candidate-only).
 */
(function (global) {
  "use strict";

  global.LunaAgentPlanningCopy = {
    version: "luna_agent_planning_copy_v1",
    sectionTitle: "行动计划",
    sectionSubtitle: "Agent Planning · L2 plan candidate",
    goalTitle: "目标理解",
    competitionTitle: "计划竞争",
    selectedTitle: "当前选择",
    reasonTitle: "为什么选择这个计划",
    toolPlanTitle: "工具计划",
    handoffTitle: "Tool OS 交接候选",
    activeTitle: "Active",
    noopTitle: "Noop",
    emptyHint: "生成 L1 处境理解后，将展开 L2 计划竞争与工具计划候选。",
    selectedBadge: "selected_plan_candidate",
    candidateBadge: "candidate",
    notExecuted: "not executed",
    evidenceSupports: "evidence supports",
    wordingNote: "展示的是 plan candidate，不是已确认的事实。",
    forbiddenParts: [
      "Luna decided", "Model chose", "OCR required", "This is a shop",
      "这是店", "已确认为店", "模型已经判定", "必须执行 OCR", "confirmed shop"
    ],
    modelLabels: {
      ocr: "OCR", detection: "Detection", depth: "Depth",
      tracking: "Tracking", slam: "SLAM", vlm: "VLM", sam: "SAM"
    }
  };
})(typeof window !== "undefined" ? window : this);
