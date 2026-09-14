/**
 * Result Layer — panel for segmentation result candidates. Not observation/segmentation owner.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.ResultLayerCopy || {}; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function renderOcrResultItem(rec) {
    var c = Copy();
    var texts = (rec.text_candidate_list || []).map(function (t) {
      var line = typeof t === "string" ? t : (t.text_candidate || t.text || "—");
      return "<li class='rl-ocr-text-candidate'>" + escapeHtml(line) + "</li>";
    }).join("");
    return (
      "<li class='rl-result-item rl-ocr-result-item'>" +
      "<strong>OCR 结果候选</strong>" +
      "<p class='rl-row'><span class='muted'>" + escapeHtml(c.labelSource) + "：</span>" +
      escapeHtml(rec.source_execution_id || "—") + "</p>" +
      "<p class='rl-row'><span class='muted'>" + escapeHtml(c.labelModel) + "：</span>" +
      escapeHtml(rec.model_source || "OCR") + " · " + escapeHtml(rec.model_version || "—") + "</p>" +
      "<p class='rl-row'><span class='muted'>区域：</span>" + escapeHtml(rec.source_region_id || "—") + "</p>" +
      "<p class='rl-row'><span class='muted'>OCR 文字候选：</span></p>" +
      "<ul class='rl-ocr-text-list'>" + (texts || "<li class='muted'>—</li>") + "</ul>" +
      "<p class='rl-row'><span class='muted'>" + escapeHtml(c.labelConfidence) + "：</span>" +
      escapeHtml(String(rec.confidence != null ? rec.confidence : "—")) + "</p>" +
      "<p class='rl-row'><span class='muted'>" + escapeHtml(c.labelFact) + "：</span>needs_fact_admission</p>" +
      "<p class='rl-notice muted'>未写入事实 · candidate_only · not_fact</p>" +
      "<p class='rl-notice muted'>" + escapeHtml(c.ocrCompletedNotFact || c.notExecutionCompleteFact) + "</p>" +
      "</li>"
    );
  }

  function renderResultItem(rec) {
    if (rec && rec.result_type === "ocr_result_envelope") return renderOcrResultItem(rec);
    var c = Copy();
    return (
      "<li class='rl-result-item'>" +
      "<strong>" + escapeHtml(rec.result_type || "segmentation_result_envelope") + "</strong>" +
      "<p class='rl-row'><span class='muted'>" + escapeHtml(c.labelSource) + "：</span>" +
      escapeHtml(rec.source_execution_id || "—") + "</p>" +
      "<p class='rl-row'><span class='muted'>" + escapeHtml(c.labelModel) + "：</span>" +
      escapeHtml(rec.model_source || "MobileSAM") + " · " + escapeHtml(rec.model_version || "—") + "</p>" +
      "<p class='rl-row'><span class='muted'>结果：</span>Segmentation Result Candidate</p>" +
      "<p class='rl-row'><span class='muted'>模型提供：</span>区域几何信息（非文字/路牌断言）</p>" +
      "<p class='rl-row'><span class='muted'>" + escapeHtml(c.labelConfidence) + "：</span>" +
      escapeHtml(String(rec.confidence != null ? rec.confidence : "—")) + "</p>" +
      "<p class='rl-row'><span class='muted'>" + escapeHtml(c.labelMask) + "：</span>" +
      escapeHtml(rec.mask_ref || rec.payload_ref || "—") + "</p>" +
      "<p class='rl-row'><span class='muted'>" + escapeHtml(c.labelFact) + "：</span>needs_fact_admission</p>" +
      "<p class='rl-notice muted'>" + escapeHtml(c.notExecutionCompleteFact) + "</p>" +
      "<p class='rl-notice muted'>" + escapeHtml(c.noAutoFactLabel) + "</p>" +
      "<p class='rl-notice muted'>调度建议见下方「中台二次理解」— MobileSAM ≠ OCR</p>" +
      "</li>"
    );
  }

  function renderErrorItem(err) {
    var etype = err.error_type || err.envelope_type || "—";
    return (
      "<li class='rl-error-item'>" +
      "<strong>" + escapeHtml(err.envelope_type || "runner_error_candidate") + "</strong>" +
      "<p class='rl-row'><span class='muted'>error：</span>" +
      escapeHtml(etype) + " @ " + escapeHtml(err.error_stage || "—") + "</p>" +
      "<p class='rl-row muted'>" + escapeHtml(err.error_reason || "—") + "</p>" +
      "<p class='rl-row muted'>not_fact · runner_error_not_fact</p></li>"
    );
  }

  function render(host, resultPkg, options) {
    options = options || {};
    if (!host) return;
    var c = Copy();
    var results = (resultPkg && resultPkg.active_results) || [];
    var errors = (resultPkg && resultPkg.errors) || [];
    if (!results.length && !errors.length) {
      host.innerHTML =
        "<section class='rl-panel rl-panel-empty'>" +
        "<h3 class='rl-title'>" + escapeHtml(c.panelTitle) + "</h3>" +
        "<p class='muted'>" + escapeHtml(c.panelNotice) + "</p>" +
        "<p class='muted'>暂无结果候选。受控执行 MobileSAM 后显示于此。</p></section>";
      host.hidden = false;
      return;
    }
    host.hidden = false;
    host.innerHTML =
      "<section class='rl-panel'>" +
      "<h3 class='rl-title'>" + escapeHtml(c.panelTitle) + "</h3>" +
      "<p class='rl-notice muted'>" + escapeHtml(c.panelNotice) + "</p>" +
      (results.length ? "<ol class='rl-list'>" + results.map(renderResultItem).join("") + "</ol>" : "") +
      (errors.length ? "<ol class='rl-error-list'>" + errors.map(renderErrorItem).join("") + "</ol>" : "") +
      "</section>";
  }

  global.ResultLayerPanel = {
    version: "result_layer_panel_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-MobileSAM-Single-Model-Execution-Integration-v1-002",
    resultLayerNotObservationLayer: true,
    result_layer_not_observation_layer: true,
    resultLayerNotSegmentationOwner: true,
    noDirectFactWriteFromRunner: true,
    render: render
  };
})(typeof window !== "undefined" ? window : this);
