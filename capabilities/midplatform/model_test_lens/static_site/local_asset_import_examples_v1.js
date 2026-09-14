/**
 * Model Test Lens — local asset import constants v1.
 * Candidate-only. No model execution. No external fetch.
 */
(function (global) {
  "use strict";

  var ASSET_TYPES = ["image", "video", "frame_sequence", "audio", "text"];

  var MODEL_CATEGORIES = [
    "segmentation",
    "ocr",
    "slam_vio",
    "depth_world",
    "detection_tracking",
    "asr",
    "tts",
    "speaker",
    "face_expression_gesture",
    "multimodal_vlm"
  ];

  var DEFAULT_MODEL_ID_BY_CATEGORY = {
    segmentation: "mobile_sam",
    ocr: "ocr_placeholder",
    slam_vio: "orb_slam_or_vins_placeholder",
    depth_world: "depth_placeholder",
    detection_tracking: "detection_tracking_placeholder",
    asr: "asr_placeholder",
    tts: "tts_placeholder",
    speaker: "speaker_placeholder",
    face_expression_gesture: "face_expression_gesture_placeholder",
    multimodal_vlm: "vlm_placeholder"
  };

  var RUNNER_TYPE_BY_CATEGORY = {
    segmentation: "segmentation_runner",
    ocr: "ocr_runner",
    slam_vio: "slam_runner",
    depth_world: "depth_runner",
    detection_tracking: "tracking_runner",
    asr: "asr_runner",
    tts: "tts_runner",
    speaker: "speaker_runner",
    face_expression_gesture: "segmentation_runner",
    multimodal_vlm: "vlm_runner"
  };

  var EXPECTED_ADAPTER_BY_CATEGORY = {
    segmentation: "segmentation_evaluation_adapter_v1",
    ocr: "ocr_evaluation_adapter_v1",
    slam_vio: "slam_evaluation_adapter_v1",
    depth_world: "depth_evaluation_adapter_v1",
    detection_tracking: "tracking_evaluation_adapter_v1",
    asr: "asr_evaluation_adapter_v1",
    tts: "tts_evaluation_adapter_v1",
    speaker: "speaker_evaluation_adapter_v1",
    face_expression_gesture: "face_expression_evaluation_adapter_v1",
    multimodal_vlm: "vlm_evaluation_adapter_v1"
  };

  var FILE_ACCEPT_BY_ASSET_TYPE = {
    image: "image/*",
    video: "video/*",
    audio: "audio/*",
    text: ".txt,.json,.md,text/plain,application/json",
    frame_sequence: "image/*"
  };

  var SLAM_HINT_LINES = [
    "本页面不会直接运行 ORB-SLAM / VINS / Kimera。",
    "需要独立 runner phase 与 owner approval。",
    "有 ground truth 时可计算 ATE / RPE / drift heatmap。",
    "无 GT 时仅 limited diagnostics：轨迹可视化、tracking timeline、smoothness proxy、lost frame ratio。",
    "无 GT 不得计算 ATE，不得与 GT benchmark 直接比较。"
  ];

  var IMAGE_HINT_LINES = [
    "页面只登记图片，不直接推理。",
    "MobileSAM / OCR / Depth / VLM 需要独立 runner phase。",
    "输出必须通过 adapter 转成 model_test_result_envelope_v1 后再展示。",
    "当前图片是 candidate test asset，不是 fact source。"
  ];

  global.LocalAssetImportExamples = {
    ASSET_TYPES: ASSET_TYPES,
    MODEL_CATEGORIES: MODEL_CATEGORIES,
    DEFAULT_MODEL_ID_BY_CATEGORY: DEFAULT_MODEL_ID_BY_CATEGORY,
    RUNNER_TYPE_BY_CATEGORY: RUNNER_TYPE_BY_CATEGORY,
    EXPECTED_ADAPTER_BY_CATEGORY: EXPECTED_ADAPTER_BY_CATEGORY,
    FILE_ACCEPT_BY_ASSET_TYPE: FILE_ACCEPT_BY_ASSET_TYPE,
    SLAM_HINT_LINES: SLAM_HINT_LINES,
    IMAGE_HINT_LINES: IMAGE_HINT_LINES,
    EXPECTED_ENVELOPE_SCHEMA: "model_test_result_envelope_v1",
    CREATED_BY: "model_test_lens_static_site",
    CREATED_BY_PHASE_UI_PATCH:
      "Phase-P1-Midplatform-Model-Test-Lens-Local-Asset-Import-UI-Patch-Execution-And-Post-Review-v1-001"
  };
})(typeof window !== "undefined" ? window : this);
