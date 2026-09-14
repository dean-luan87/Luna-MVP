/**
 * Observation Attention Layer V1 — UI copy (candidate-only labels).
 */
(function (global) {
  "use strict";

  global.ObservationAttentionCopy = {
    version: "observation_attention_copy_v2_visual_expression_system",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Visual-Expression-System-UI-Execution-Post-Review-And-Minor-Fix-v1-001",
    panelTitle: "优先观察",
    panelHint: "观察调度主入口：点击下方条目高亮主图分割区域，不改变分割边界归属。",
    candidateNotice: "以下为观察调度候选，不是事实判断，不触发模型执行。",
    noAttentionRecord: "该区域暂无优先观察建议",
    fieldType: "类型",
    statusLine: "状态：candidate_only / not_fact",
    correctionBoosted: "指错加权",
    motionState: {
      static_candidate: "静态候选",
      dynamic_candidate: "动态候选",
      scene_structure_candidate: "结构候选",
      unknown_motion_state: "状态未知",
      needs_tracking_review: "需跟踪复核"
    },
    priorityLevel: {
      P0_immediate_attention: "P0",
      P1_high_attention: "P1",
      P2_medium_attention: "P2",
      P3_low_attention: "P3",
      ignore_for_now: "忽略"
    },
    followupModel: {
      detection: "检测",
      ocr: "OCR",
      depth: "深度",
      slam: "SLAM",
      tracking: "跟踪",
      motion_analysis: "运动",
      slam_reference: "SLAM参考",
      walkable_area_review: "通行复核",
      vio: "VIO",
      vlm: "VLM",
      human_review: "人工复核",
      no_followup_required: "—"
    },
    flags: {
      tracking: "跟踪",
      ocr: "OCR",
      depth: "深度",
      detection: "检测"
    },
    whyObserve: "为什么优先",
    nextModel: "建议补测",
    summaryPrefix: "本帧建议优先观察",
    summaryRegions: "个区域",
    singleFrameLimit: "单帧：动态仅为候选标签，不得断言为已确认动态"
  };
})(typeof window !== "undefined" ? window : this);
