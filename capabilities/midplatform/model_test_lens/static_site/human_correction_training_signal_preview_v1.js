/**
 * Human Correction Layer V1 — training signal candidate preview (not training data).
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.HumanCorrectionCopy || {}; };

  function typeLabel(typeId) {
    var types = Copy().correctionTypes || [];
    for (var i = 0; i < types.length; i++) {
      if (types[i].id === typeId) return types[i].label;
    }
    return typeId;
  }

  function buildSignal(correction, purifiedOverride) {
    if (!correction) return null;
    if (purifiedOverride) {
      var target = correction.correction_target || {};
      var scene = correction.source_test_case_id || "unknown_scene";
      var err = purifiedOverride.correction_type || "unknown";
      return {
        signal_id: purifiedOverride.signal_id,
        correction_ref: purifiedOverride.correction_ref,
        model_category: correction.source_model_category,
        failure_pattern: err + "_" + (target.target_type || "object"),
        scene_context: scene,
        object_type: target.target_display_name || target.source_object_id || "scene",
        error_type: err,
        recurrence_key: scene + "::" + err + "::" + (target.source_object_id || "panel"),
        suggested_dataset_bucket: "hard_case_" + scene.split("_").slice(0, 3).join("_"),
        needs_owner_review: true,
        not_auto_training_data: true,
        consent_required_if_sensitive: true,
        purified_by_midplatform: true
      };
    }
    var analysis = correction.midplatform_analysis;
    if (!analysis || analysis.training_candidate !== "pending_review") return null;
    if (analysis.purified_training_signal) return buildSignal(correction, analysis.purified_training_signal);
    var target = correction.correction_target || {};
    var scene = correction.source_test_case_id || "unknown_scene";
    var objType = target.target_display_name || target.source_object_id || "scene";
    var err = (correction.correction_types && correction.correction_types.length)
      ? correction.correction_types.join("+")
      : (correction.correction_type || "unknown");
    return {
      signal_id: "training_signal_" + correction.correction_id,
      correction_ref: correction.correction_id,
      model_category: correction.source_model_category,
      failure_pattern: err + "_" + (target.target_type || "object"),
      scene_context: scene,
      object_type: objType,
      error_type: err,
      recurrence_key: scene + "::" + err + "::" + (target.source_object_id || "panel"),
      suggested_dataset_bucket: "hard_case_" + scene.split("_").slice(0, 3).join("_"),
      suggested_benchmark_case: correction.source_test_case_id,
      suggested_prompt_or_runner_adjustment: correction.suggested_fix || "",
      should_add_to_hard_case_set: !!correction.hard_case_candidate,
      should_add_to_regression_test: !!correction.regression_test_candidate,
      needs_owner_review: true,
      not_auto_training_data: true,
      consent_required_if_sensitive: true
    };
  }

  function renderPreview(host, correction, signal) {
    if (!host) return;
    signal = signal || buildSignal(correction);
    if (!signal) {
      host.innerHTML = host.innerHTML || (
        "<p class='muted hc-preview-skip'>中台判定：本次纠错不进入训练候选（可能是策略/优先级/偏好信号）。</p>"
      );
      return;
    }
    var c = Copy();
    host.innerHTML =
      "<div class='hc-training-preview'>" +
      "<h4>" + escapeHtml(c.trainingPreviewTitle || "训练信号候选预览") + "</h4>" +
      "<p class='hc-boundary-notice'>" + escapeHtml(c.trainingPreviewDisclaimer || "") + "</p>" +
      "<dl class='hc-preview-dl'>" +
      "<div><dt>失败模式</dt><dd>" + escapeHtml(signal.failure_pattern) + "</dd></div>" +
      "<div><dt>场景类型</dt><dd>" + escapeHtml(signal.scene_context) + "</dd></div>" +
      "<div><dt>对象类型</dt><dd>" + escapeHtml(signal.object_type) + "</dd></div>" +
      "<div><dt>推荐数据集桶</dt><dd>" + escapeHtml(signal.suggested_dataset_bucket) + "</dd></div>" +
      "<div><dt>Hard case</dt><dd>" + (signal.should_add_to_hard_case_set ? "建议加入" : "否") + "</dd></div>" +
      "<div><dt>Regression test</dt><dd>" + (signal.should_add_to_regression_test ? "建议加入" : "否") + "</dd></div>" +
      "<div><dt>Owner review</dt><dd>需要</dd></div>" +
      "</dl>" +
      "<p class='muted hc-preview-forbidden'>禁止：已进入训练 · 已成为奖励 · 已成为 ground truth</p>" +
      "</div>";
  }

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  global.HumanCorrectionTrainingSignalPreview = {
    version: "human_correction_training_signal_preview_v1",
    buildSignal: buildSignal,
    renderPreview: renderPreview
  };
})(typeof window !== "undefined" ? window : this);
