/**
 * Dual route perception — copy v1 (candidate only, not fact).
 */
(function (global) {
  "use strict";

  global.DualRoutePerceptionCopy = {
    version: "dual_route_perception_copy_v1",
    sectionTitle: "路线对照候选",
    routeATitle: "Route A：Grounding / Detection → SAM refine",
    routeBTitle: "Route B：VLM route",
    comparisonTitle: "中台对照",
    labelCandidate: "label candidate",
    bboxCandidate: "bbox candidate",
    maskCandidate: "mask candidate",
    sceneCandidate: "scene candidate",
    attentionCandidate: "suggested attention",
    followupCandidate: "suggested followup",
    agreement: "agreement",
    conflict: "conflict",
    admissionSuggestion: "admission suggestion",
    statusCandidate: "candidate_only",
    notFact: "not_fact",
    notExecuted: "未执行 runner · 仅对照候选",
    emptyHint: "上传图像并开始观察后，将生成 Route A/B 对照候选。",
    no_slam_for_text: "SLAM 不参与文字发现",
    no_vlm_fact_generation: true,
    no_grounding_label_fact_upgrade: true,
    no_sam_mask_fact_upgrade: true,
    traceHint: "trace_chain 保留 · 不写 fact"
  };
})(typeof window !== "undefined" ? window : this);
