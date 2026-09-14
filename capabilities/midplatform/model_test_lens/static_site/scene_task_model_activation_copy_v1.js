/**
 * Scene-Task Model Activation — copy v1 (candidate only, not fact).
 */
(function (global) {
  "use strict";

  global.SceneTaskModelActivationCopy = {
    version: "scene_task_model_activation_copy_v1",
    sectionTitle: "模型激活计划",
    sceneTitle: "场景候选",
    taskTitle: "任务意图",
    activatedTitle: "Activated Models",
    noopTitle: "No-op Models",
    followupTitle: "Followup task candidate",
    assignmentTitle: "Model → Region Assignment",
    emptyHint: "上传图像并开始观察后，将生成模型激活计划候选。",
    notExecuted: "未执行 runner · 仅激活计划候选",
    traceHint: "trace_chain 保留 · 不写 fact",
    no_runner_execution: true,
    model_activation_candidate_not_fact: true,
    modelLabels: {
      ocr_text_detector: "OCR text detector",
      ocr_recognizer: "OCR recognizer",
      detection: "Detection",
      depth: "Depth",
      tracking: "Tracking",
      slam: "SLAM",
      vlm_route_enhancer: "VLM route enhancer",
      mobile_sam_region_proposal: "MobileSAM region proposal"
    }
  };
})(typeof window !== "undefined" ? window : this);
