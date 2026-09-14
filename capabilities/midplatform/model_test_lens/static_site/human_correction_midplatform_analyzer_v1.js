/**
 * Human Correction — Midplatform Analysis Layer.
 * Raw correction MUST pass through here before training signal / policy routing.
 */
(function (global) {
  "use strict";

  var MODEL_ERROR = {
    false_positive: 1, false_negative: 1, wrong_label: 1, boundary_inaccurate: 1,
    confidence_mismatch: 1, duplicate_detection: 1
  };
  var TASK_STRATEGY = { task_relevance_error: 1, recommendation_error: 1 };
  var ATTENTION = { priority_wrong: 1 };
  var ENVIRONMENT = {
    low_light: 1, occlusion: 1, motion_blur: 1, reflective_glare: 1,
    crowded_scene: 1, small_or_far_target: 1, background_interference: 1, image_quality_poor: 1
  };

  function noteText(c) {
    return String(c.manual_annotation || c.user_note || "");
  }

  function correctionTypes(c) {
    if (c.correction_types && c.correction_types.length) return c.correction_types;
    return c.correction_type ? [c.correction_type] : [];
  }

  function targetRegionId(c) {
    var t = c.correction_target || {};
    return t.source_object_id || t.target_id || c.target_region_id || "";
  }

  function matchAny(text, patterns) {
    for (var i = 0; i < patterns.length; i++) {
      if (patterns[i].test(text)) return true;
    }
    return false;
  }

  var PREF = [/更关注/, /想看/, /偏好/, /优先看/, /我关心/, /我主要/];
  var IGNORE = [/不用看/, /不重要/, /忽略/, /别关注/, /优先级.*不对/, /不用管/];
  var TASK = [/不是我要/, /任务.*错/, /找错/, /应该看/, /我想看/];

  function classifyAttribution(correction) {
    var note = noteText(correction);
    var types = correctionTypes(correction);
    var i, t;

    if (matchAny(note, PREF)) {
      return {
        attribution_id: "user_preference",
        attribution_label_zh: "用户偏好",
        attribution_reason: "用户表达个体关注偏好，非模型错误断言"
      };
    }
    for (i = 0; i < types.length; i++) {
      if (ATTENTION[types[i]]) break;
    }
    if (i < types.length || matchAny(note, IGNORE)) {
      return {
        attribution_id: "attention_priority_error",
        attribution_label_zh: "关注度/优先级问题",
        attribution_reason: "纠错指向关注度或优先级，非分割/识别本身"
      };
    }
    for (i = 0; i < types.length; i++) {
      if (TASK_STRATEGY[types[i]]) break;
    }
    if (i < types.length || matchAny(note, TASK)) {
      return {
        attribution_id: "task_strategy_error",
        attribution_label_zh: "任务/策略问题",
        attribution_reason: "纠错指向任务目标或路由策略"
      };
    }
    var hasModel = false;
    var hasEnv = false;
    for (i = 0; i < types.length; i++) {
      if (MODEL_ERROR[types[i]]) hasModel = true;
      if (ENVIRONMENT[types[i]]) hasEnv = true;
    }
    if (hasEnv && !hasModel) {
      return {
        attribution_id: "environment_limitation",
        attribution_label_zh: "环境/成像限制",
        attribution_reason: "环境因素为主，不直接作为模型训练标签"
      };
    }
    if (hasModel) {
      return {
        attribution_id: "model_error",
        attribution_label_zh: "模型问题",
        attribution_reason: "纠错类型指向模型输出问题"
      };
    }
    return {
      attribution_id: "attention_priority_error",
      attribution_label_zh: "关注度/优先级问题",
      attribution_reason: "未明确模型错误，默认作为 priority/context 信号"
    };
  }

  function routeDestinations(attributionId) {
    var map = {
      model_error: ["model_training_data_candidate", "model_rerun_candidate", "new_task_candidate"],
      task_strategy_error: ["routing_policy_update_candidate", "decision_layer_review_candidate"],
      attention_priority_error: ["attention_policy_update_candidate", "priority_update_signal", "new_task_candidate"],
      user_preference: ["user_preference_update_candidate", "knowledge_memory_update_candidate"],
      environment_limitation: ["attention_policy_update_candidate", "human_review_candidate"]
    };
    return (map[attributionId] || ["human_review_candidate"]).slice();
  }

  function impactFor(attributionId) {
    var m = {
      model_error: "training_signal_pending_review",
      task_strategy_error: "task_routing_signal",
      attention_priority_error: "priority_signal",
      user_preference: "preference_signal",
      environment_limitation: "context_signal"
    };
    return m[attributionId] || "priority_signal";
  }

  function trainingStatus(attributionId) {
    return attributionId === "model_error" ? "pending_review" : "not_applicable";
  }

  function analyzeCorrection(correction) {
    if (!correction || !correction.correction_id) return null;
    var attr = classifyAttribution(correction);
    var types = correctionTypes(correction);
    var rerun = attr.attribution_id === "model_error" &&
      (types.indexOf("boundary_inaccurate") >= 0 || types.indexOf("false_negative") >= 0);

    var analysis = {
      analysis_id: "cma_" + correction.correction_id,
      correction_ref: correction.correction_id,
      source_model_id: correction.source_model_id,
      target_region_id: targetRegionId(correction),
      attribution_id: attr.attribution_id,
      attribution_label_zh: attr.attribution_label_zh,
      attribution_reason: attr.attribution_reason,
      routing_destinations: routeDestinations(attr.attribution_id),
      impact: impactFor(attr.attribution_id),
      training_candidate: trainingStatus(attr.attribution_id),
      model_rerun_candidate: rerun,
      new_task_candidate_refs: [],
      candidate_only: true,
      not_fact: true,
      not_ground_truth: true,
      not_auto_training_data: true,
      must_not_modify_model_output: true,
      analyzed_at: new Date().toISOString()
    };

    if (attr.attribution_id === "model_error") {
      analysis.purified_training_signal = {
        signal_id: "training_signal_" + correction.correction_id,
        correction_ref: correction.correction_id,
        correction_type: types[0] || "unknown",
        target_region_id: targetRegionId(correction),
        source_model: correction.source_model_id,
        confirmed_by: "human",
        training_candidate: true,
        needs_owner_review: true,
        not_auto_training_data: true,
        not_ground_truth: true,
        user_feedback: noteText(correction)
      };
    }
    return analysis;
  }

  function renderRoutingPreview(host, analysis) {
    if (!host || !analysis) return;
    var dest = (analysis.routing_destinations || []).map(function (d) {
      return "<li>" + d + "</li>";
    }).join("");
    host.innerHTML =
      "<div class='hc-midplatform-preview'>" +
      "<h4>中台纠错分析</h4>" +
      "<p class='muted'>纠错先进入中台治理，不直送训练管线。</p>" +
      "<dl class='hc-preview-dl'>" +
      "<div><dt>归因</dt><dd>" + analysis.attribution_label_zh + " (" + analysis.attribution_id + ")</dd></div>" +
      "<div><dt>影响</dt><dd>" + analysis.impact + "</dd></div>" +
      "<div><dt>训练候选</dt><dd>" + analysis.training_candidate + "</dd></div>" +
      "<div><dt>复跑候选</dt><dd>" + (analysis.model_rerun_candidate ? "是" : "否") + "</dd></div>" +
      "</dl>" +
      "<p><strong>路由去向</strong></p><ul class='hc-route-list'>" + dest + "</ul>" +
      "<p class='muted hc-preview-forbidden'>禁止：送入训练管线 · 修改 mask · 写 fact</p>" +
      "</div>";
  }

  global.HumanCorrectionMidplatformAnalyzer = {
    version: "human_correction_midplatform_analyzer_v1",
    phaseRef: "Phase-P1-Midplatform-Single-Model-Interaction-Validation-v1-001",
    noDirectTraining: true,
    midplatformEntryRequired: true,
    analyzeCorrection: analyzeCorrection,
    classifyAttribution: classifyAttribution,
    renderRoutingPreview: renderRoutingPreview
  };
})(typeof window !== "undefined" ? window : this);
