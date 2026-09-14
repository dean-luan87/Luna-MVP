/**
 * Controlled Runner Execution — execution candidate panel. No runner execution.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.ControlledRunnerExecutionCopy || {}; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function formatTrace(trace) {
    if (!trace || !trace.length) return "";
    return trace.map(function (t) {
      return t.stage + ":" + t.ref;
    }).join(" → ");
  }

  function renderInputReview(review) {
    if (!review) return "";
    var forbidden = (review.forbidden_inputs || []).map(function (f) {
      return "<li>" + escapeHtml(f) + "</li>";
    }).join("");
    var allowed = (review.allowed_inputs || []).map(function (a) {
      return "<li>" + escapeHtml(a) + "</li>";
    }).join("");
    var hc = review.human_correction_note
      ? "<p class='crec-input-hc muted'>" + escapeHtml(review.human_correction_note) + "</p>" : "";
    return (
      "<div class='crec-input-review'>" +
      "<h4 class='crec-input-title'>" + escapeHtml(review.title) + "</h4>" +
      "<p class='crec-input-row'><span class='muted'>" + escapeHtml(Copy().labelInput) + "区域：</span>" +
      escapeHtml(review.region_label) + "</p>" +
      "<p class='crec-input-row'><span class='muted'>" + escapeHtml(Copy().labelSourceAttention) + "：</span>" +
      escapeHtml(review.source_label) + "</p>" +
      "<p class='crec-input-row'><span class='muted'>" + escapeHtml(Copy().labelReason) + "：</span>" +
      escapeHtml(review.reason_label) + "</p>" +
      "<p class='crec-input-row'><span class='muted'>" + escapeHtml(Copy().labelInput) + "：</span>" +
      escapeHtml(review.input_label) + "</p>" +
      hc +
      "<details class='crec-input-details'><summary>" + escapeHtml(Copy().labelAllowedInput) + "</summary>" +
      "<ul class='crec-input-list'>" + allowed + "</ul></details>" +
      "<details class='crec-input-details'><summary>" + escapeHtml(Copy().labelForbiddenInput) + "</summary>" +
      "<ul class='crec-input-list crec-forbidden-list'>" + forbidden + "</ul></details>" +
      "</div>"
    );
  }

  function renderCandidateItem(candidate, options) {
    var c = Copy();
    var active = options.selectedRegionId === candidate.source_region_id ? " crec-item-active" : "";
    var outputType = candidate.output_envelope_type || "—";
    var regionLabel = candidate.region_display_name || ("region crop #" + candidate.source_region_id);

    return (
      "<li class='crec-item" + active + "' data-region-id='" + escapeHtml(candidate.source_region_id) + "' " +
      "data-crec-id='" + escapeHtml(candidate.execution_candidate_id) + "' role='button' tabindex='0'>" +
      "<div class='crec-head'><strong>" + escapeHtml(candidate.execution_candidate_id) + "</strong></div>" +
      "<p class='crec-row'><span class='muted'>" + escapeHtml(c.labelSource) + "：</span>" +
      "runner_invocation_request " + escapeHtml(candidate.source_invocation_request_id) + "</p>" +
      "<p class='crec-row'><span class='muted'>" + escapeHtml(c.labelTask) + "：</span>" +
      escapeHtml(candidate.requested_runner_type) + "</p>" +
      "<p class='crec-row'><span class='muted'>" + escapeHtml(c.labelInput) + "：</span>" +
      escapeHtml(regionLabel) + "</p>" +
      "<p class='crec-row'><span class='muted'>" + escapeHtml(c.labelStrategy) + "：</span>" +
      escapeHtml(candidate.execution_mode) + "</p>" +
      "<p class='crec-row'><span class='muted'>" + escapeHtml(c.labelStatus) + "：</span>" +
      "<strong class='crec-status-" + escapeHtml(candidate.execution_status) + "'>" +
      escapeHtml(candidate.execution_status) + "</strong></p>" +
      "<p class='crec-row'><span class='muted'>" + escapeHtml(c.labelOutput) + "：</span>" +
      escapeHtml(outputType) + "</p>" +
      "<p class='crec-row'><span class='muted'>" + escapeHtml(c.labelFact) + "：</span>needs_fact_admission</p>" +
      "<p class='crec-row muted'>" + escapeHtml(c.labelNotExecuted) + " · not_executed · not_fact</p>" +
      "<p class='crec-notice muted'>" + escapeHtml(c.notExecutionNotice) + "</p>" +
      "<p class='crec-status-line muted'>" + escapeHtml(c.statusLine) + "</p>" +
      renderInputReview(candidate.input_review) +
      "<details class='crec-trace-details'><summary>" + escapeHtml(c.traceToggle) + "</summary>" +
      "<pre class='crec-trace-pre'>" + escapeHtml(formatTrace(candidate.trace_chain)) + "</pre></details>" +
      "<div class='crec-actions'>" +
      (candidate.execution_status === "planned_only"
        ? "<button type='button' class='crec-btn' data-exec-action='mark-ready' data-crec='" +
          escapeHtml(candidate.execution_candidate_id) + "'>" + escapeHtml(c.markReadyBtn) + "</button>"
        : "") +
      (global.ControlledRunnerExecutionUI && global.ControlledRunnerExecutionUI.canRunControlledMobileSam(candidate)
        ? "<button type='button' class='crec-btn crec-btn-run' data-exec-action='run-controlled-mobilesam' data-crec='" +
          escapeHtml(candidate.execution_candidate_id) + "'>" +
          escapeHtml((global.ResultLayerCopy && global.ResultLayerCopy.runControlledMobileSamBtn) ||
            "受控执行 MobileSAM") + "</button>"
        : "") +
      (candidate.execution_status !== "cancelled"
        ? "<button type='button' class='crec-btn crec-btn-ghost' data-exec-action='cancel' data-crec='" +
          escapeHtml(candidate.execution_candidate_id) + "'>" + escapeHtml(c.cancelCandidateBtn) + "</button>"
        : "<span class='muted'>已取消</span>") +
      "</div></li>"
    );
  }

  function render(host, executionPkg, options) {
    options = options || {};
    if (!host) return;
    var c = Copy();
    var list = (executionPkg && executionPkg.active_candidates) || [];
    if (!list.length) {
      host.innerHTML =
        "<section class='crec-panel crec-panel-empty'>" +
        "<h3 class='crec-title'>" + escapeHtml(c.panelTitle) + "</h3>" +
        "<p class='muted'>" + escapeHtml(c.panelNotice) + "</p>" +
        "<p class='muted'>暂无受控执行候选。请从 admitted request 生成。</p></section>";
      host.hidden = false;
      return;
    }
    host.hidden = false;
    host.innerHTML =
      "<section class='crec-panel'>" +
      "<h3 class='crec-title'>" + escapeHtml(c.panelTitle) + "</h3>" +
      "<p class='crec-notice muted'>" + escapeHtml(c.panelNotice) + "</p>" +
      "<ol class='crec-list'>" +
      list.map(function (item) { return renderCandidateItem(item, options); }).join("") +
      "</ol></section>";

    host.querySelectorAll("[data-exec-action]").forEach(function (btn) {
      btn.addEventListener("click", function (ev) {
        ev.stopPropagation();
        if (options.onExecutionAction) {
          options.onExecutionAction(btn.dataset.execAction, btn.dataset.crec);
        }
      });
    });

    host.querySelectorAll(".crec-item").forEach(function (li) {
      var regionId = li.dataset.regionId;
      li.addEventListener("click", function (ev) {
        if (ev.target.closest("[data-exec-action]") || ev.target.closest("details")) return;
        if (options.onSelectRegion) options.onSelectRegion(regionId);
      });
      li.addEventListener("mouseenter", function () {
        if (options.onHoverRegion) options.onHoverRegion(regionId);
      });
      li.addEventListener("mouseleave", function () {
        if (options.onHoverRegion) options.onHoverRegion(null);
      });
    });
  }

  global.ControlledRunnerExecutionPanel = {
    version: "controlled_runner_execution_panel_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Controlled-Runner-Execution-UI-Execution-v1-001",
    noRunnerExecution: true,
    noExecutionCandidateBoxOnCanvas: true,
    executionCopyMustNotImplyExecution: true,
    render: render,
    renderInputReview: renderInputReview
  };
})(typeof window !== "undefined" ? window : this);
