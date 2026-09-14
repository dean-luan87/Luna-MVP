/**
 * Midplatform Interaction Panel — Result Candidate + Analysis + Correction + Trace.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.MidplatformInteractionCopy || {}; };
  var HCAnalyzer = function () { return global.HumanCorrectionMidplatformAnalyzer; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function renderTrace(chain) {
    if (!chain || !chain.length) return "";
    return "<ol class='mpa-trace'>" + chain.map(function (step, idx) {
      var arrow = idx < chain.length - 1 ? "" : "";
      return "<li><span class='mpa-trace-stage'>" + escapeHtml(step.stage) + "</span>" +
        (step.ref ? " <span class='muted mpa-trace-ref'>" + escapeHtml(step.ref) + "</span>" : "") +
        arrow + "</li>";
    }).join("") + "</ol>";
  }

  function renderResultCandidateCard(rc) {
    var c = Copy();
    if (!rc) return "";
    return (
      "<article class='mpa-card mpa-card-result'>" +
      "<h4 class='mpa-card-title'>" + escapeHtml(c.resultCandidateTitle) + "</h4>" +
      "<dl class='mpa-dl'>" +
      "<div><dt>" + escapeHtml(c.labelModel) + "</dt><dd>" + escapeHtml(rc.model) + "</dd></div>" +
      "<div><dt>" + escapeHtml(c.labelResultType) + "</dt><dd>" + escapeHtml(rc.result_type) + "</dd></div>" +
      "<div><dt>" + escapeHtml(c.labelRegion) + "</dt><dd>" + escapeHtml(rc.region_id) + "</dd></div>" +
      "<div><dt>" + escapeHtml(c.labelModelProvides) + "</dt><dd>" + escapeHtml(rc.model_provides) + "</dd></div>" +
      "<div><dt>mask</dt><dd class='mpa-mono'>" + escapeHtml(rc.mask_ref) + "</dd></div>" +
      "<div><dt>" + escapeHtml(c.labelConfidence) + "</dt><dd>" + escapeHtml(String(rc.confidence)) + "</dd></div>" +
      "<div><dt>" + escapeHtml(c.labelStatus) + "</dt><dd><span class='mpa-tag'>" +
      escapeHtml(rc.status) + "</span></dd></div>" +
      "</dl></article>"
    );
  }

  function renderAnalysisCard(analysis, taskCandidate) {
    var c = Copy();
    if (!analysis) return "";
    var features = (analysis.region_features || []).map(function (f) {
      return "<li>" + escapeHtml(f) + "</li>";
    }).join("");
    return (
      "<article class='mpa-card mpa-card-analysis'>" +
      "<h4 class='mpa-card-title'>" + escapeHtml(c.analysisCardTitle) + "</h4>" +
      "<dl class='mpa-dl'>" +
      "<div><dt>来源</dt><dd>" + escapeHtml(analysis.source_region_id) + "</dd></div>" +
      "<div><dt>输入</dt><dd>" + escapeHtml(analysis.source_input) + "</dd></div>" +
      "<div><dt>判断</dt><dd><span class='mpa-tag mpa-tag-judge'>" +
      escapeHtml(analysis.midplatform_judgment) + "</span></dd></div>" +
      "</dl>" +
      (features ? "<p class='mpa-subhead'>" + escapeHtml(c.labelRegionFeatures) + "</p><ul class='mpa-feature-list'>" +
        features + "</ul>" : "") +
      (analysis.route_label ? (
        "<p class='mpa-subhead'>" + escapeHtml(c.labelScheduleSuggestion) + "</p>" +
        "<p class='mpa-route'>" + escapeHtml(analysis.route_label) + "</p>" +
        "<p class='mpa-reason muted'>" + escapeHtml(analysis.route_reason || c.scheduleReasonTextLikely) + "</p>"
      ) : "<p class='muted'>" + escapeHtml(analysis.route_reason || "—") + "</p>") +
      "<p class='mpa-boundary muted'>" + escapeHtml(c.mobileSamNotOcr) + "</p>" +
      "<p class='mpa-boundary muted'>" + escapeHtml(c.noOcrRunner) + "</p>" +
      "<div><dt class='mpa-inline-dt'>" + escapeHtml(c.labelTraining) + "</dt> " +
      "<span class='mpa-tag'>" + escapeHtml(c.trainingNo) + "</span></div>" +
      (taskCandidate ? "<p class='mpa-task muted'>task: " + escapeHtml(taskCandidate.task_candidate_id) +
        " · " + escapeHtml(taskCandidate.recommended_runner_type) + " candidate</p>" : "") +
      "</article>"
    );
  }

  function isTextReadoutComplaint(correction) {
    var note = (correction.manual_annotation || correction.user_note || "").toLowerCase();
    return /文字|读不出|没读|ocr|识别不出|看不清字/.test(note);
  }

  function renderDualModelAttribution(correction) {
    var ocrCopy = global.MobileSamOcrControlledExecutionCopy || {};
    var title = ocrCopy.dualModelAttributionTitle || "双模型纠错归因";
    if (!isTextReadoutComplaint(correction)) return "";

    var hints = [
      { id: "ocr_model_error", label: "OCR model_error", dest: "OCR training_candidate · pending_review" },
      { id: "mobile_sam_region_selection_error", label: "MobileSAM region_selection_error",
        dest: "MobileSAM rerun_candidate" },
      { id: "ocr_route_strategy_error", label: "OCR route_strategy_error",
        dest: "OCR route policy update" },
      { id: "attention_priority_error", label: "attention_priority_error",
        dest: "priority_update_signal" },
      { id: "user_preference", label: "user_preference", dest: "preference_memory candidate" }
    ];
    var rows = hints.map(function (h) {
      return "<li><strong>" + escapeHtml(h.label) + "</strong> → " + escapeHtml(h.dest) + "</li>";
    }).join("");

    return (
      "<article class='mpa-card mpa-card-dual-model'>" +
      "<h4 class='mpa-card-title'>" + escapeHtml(title) + "</h4>" +
      "<p class='muted'>用户反馈「文字没读出来」时，不默认判定 OCR 错。可能归因：</p>" +
      "<ul class='mpa-dual-model-list'>" + rows + "</ul>" +
      "<p class='mpa-boundary muted'>禁止：直接训练 OCR · 直接改 OCR result · 直接改 MobileSAM mask · " +
      "把用户输入当 OCR truth</p></article>"
    );
  }

  function renderCorrectionBlock(correction) {
    var c = Copy();
    var Analyzer = HCAnalyzer();
    if (!correction || !Analyzer) return "";
    var analysis = correction.midplatform_analysis || Analyzer.analyzeCorrection(correction);
    if (!analysis) return "";

    var types = (correction.correction_types || []).join(", ") || correction.correction_type || "—";
    var note = correction.manual_annotation || correction.user_note || "—";
    var exits = (analysis.routing_destinations || []).map(function (d) {
      return "<li>✓ " + escapeHtml(d) + "</li>";
    }).join("");

    var trainingLabel = analysis.training_candidate === "pending_review"
      ? c.trainingYes : c.trainingNo;
    var processing = analysis.attribution_id === "attention_priority_error"
      ? "priority_update_signal" : (analysis.impact || "—");

    var trace = [
      { stage: "User Correction", ref: correction.correction_id },
      { stage: "Correction Record", ref: types },
      { stage: "Attribution", ref: analysis.attribution_id },
      { stage: analysis.training_candidate === "pending_review"
        ? "Training Candidate" : "Policy Update", ref: processing }
    ];

    return (
      "<div class='mpa-correction-block'>" +
      "<article class='mpa-card mpa-card-correction'>" +
      "<h4 class='mpa-card-title'>" + escapeHtml(c.correctionRecordTitle) + "</h4>" +
      "<dl class='mpa-dl'>" +
      "<div><dt>" + escapeHtml(c.labelUserFeedback) + "</dt><dd>" + escapeHtml(note) + "</dd></div>" +
      "<div><dt>类型</dt><dd>" + escapeHtml(types) + "</dd></div>" +
      "<div><dt>区域</dt><dd>" + escapeHtml(analysis.target_region_id || "—") + "</dd></div>" +
      "</dl></article>" +
      "<article class='mpa-card mpa-card-attribution'>" +
      "<h4 class='mpa-card-title'>" + escapeHtml(c.attributionTitle) + "</h4>" +
      "<dl class='mpa-dl'>" +
      "<div><dt>" + escapeHtml(c.labelAttribution) + "</dt><dd>" + escapeHtml(analysis.attribution_id) +
        " · " + escapeHtml(analysis.attribution_label_zh) + "</dd></div>" +
      "<div><dt>" + escapeHtml(c.labelImpactTarget) + "</dt><dd>" +
        escapeHtml(correction.source_model_id || "MobileSAM") + " segmentation</dd></div>" +
      "<div><dt>" + escapeHtml(c.labelSuggestedExits) + "</dt><dd><ul class='mpa-exit-list'>" +
        exits + "</ul></dd></div>" +
      "<div><dt>" + escapeHtml(c.labelTraining) + "</dt><dd>" + escapeHtml(trainingLabel) + "</dd></div>" +
      "<div><dt>" + escapeHtml(c.labelProcessing) + "</dt><dd>" + escapeHtml(processing) + "</dd></div>" +
      "</dl>" +
      "<p class='mpa-boundary muted'>" + escapeHtml(c.forbiddenFactLabel) + "</p>" +
      "</article>" +
      renderDualModelAttribution(correction) +
      "<details class='mpa-trace-details'><summary>" + escapeHtml(c.traceTitle) + " (Case 2)</summary>" +
      renderTrace(trace) + "</details></div>"
    );
  }

  function render(host, midplatformPkg, options) {
    options = options || {};
    if (!host) return;

    var c = Copy();
    var case1 = midplatformPkg && midplatformPkg.case1;
    var corrections = (midplatformPkg && midplatformPkg.corrections) || [];

    var html = "<section class='mpa-panel'>";
    html += "<h3 class='mpa-title'>" + escapeHtml(c.sectionTitle) + "</h3>";
    html += "<p class='mpa-notice muted'>" + escapeHtml(c.sectionNotice) + "</p>";

    var hasCase1 = case1 && case1.items && case1.items.length;
    var hasCorr = corrections.length > 0;

    if (!hasCase1 && !hasCorr) {
      html += "<p class='muted'>" + escapeHtml(c.emptyAnalysis) + "</p>";
      html += "<p class='muted'>" + escapeHtml(c.emptyCorrection) + "</p>";
      html += "</section>";
      host.innerHTML = html;
      host.hidden = false;
      return;
    }

    if (hasCase1) {
      case1.items.forEach(function (item, idx) {
        html += "<div class='mpa-flow'>";
        html += renderResultCandidateCard(item.result_candidate);
        html += "<div class='mpa-flow-arrow muted'>↓ 中台如何理解？</div>";
        html += renderAnalysisCard(item.analysis, item.task_candidate);
        if (case1.trace_chains && case1.trace_chains[idx]) {
          html += "<details class='mpa-trace-details'><summary>" + escapeHtml(c.traceTitle) +
            " (Case 1)</summary>" + renderTrace(case1.trace_chains[idx]) + "</details>";
        }
        html += "</div>";
      });
    }

    if (hasCorr) {
      html += "<h4 class='mpa-subsection'>" + escapeHtml(c.correctionSectionTitle) + "</h4>";
      corrections.slice(0, 5).forEach(function (corr) {
        html += renderCorrectionBlock(corr);
      });
    }

    html += "</section>";
    host.innerHTML = html;
    host.hidden = false;
  }

  global.MidplatformInteractionPanel = {
    version: "midplatform_interaction_panel_v1",
    phaseRef: "Phase-P1-Midplatform-Single-Model-Interaction-Validation-UI-Execution-v1-001",
    result_candidate_not_fact: true,
    result_analysis_not_fact: true,
    midplatform_analysis_not_model_output: true,
    midplatform_analysis_not_training_directive: true,
    correction_analysis_not_mask_mutation: true,
    correction_training_requires_review: true,
    route_candidate_not_execution: true,
    ocr_candidate_not_ocr_result: true,
    user_preference_not_training_data: true,
    priority_signal_not_ground_truth: true,
    render: render
  };
})(typeof window !== "undefined" ? window : this);
