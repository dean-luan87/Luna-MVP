/**
 * MobileSAM → OCR Controlled Execution — panel (request / admission / candidate).
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.MobileSamOcrControlledExecutionCopy || {}; };
  var FORBIDDEN_UI = /已识别文字|OCR结果|发现路牌|读取成功|确认这是路牌|开始 OCR|立即识别|执行 OCR|运行模型/;

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function safe(text) {
    if (FORBIDDEN_UI.test(text || "")) return "[文案违规已屏蔽]";
    return text;
  }

  function formatTrace(chain) {
    if (!chain || !chain.length) return "";
    return chain.map(function (t) { return t.stage + ":" + t.ref; }).join(" → ");
  }

  function renderInputReview(review) {
    if (!review) return "";
    var allowed = (review.allowed_inputs || []).map(function (a) {
      return "<li>" + escapeHtml(a) + "</li>";
    }).join("");
    var forbidden = (review.forbidden_inputs || []).map(function (f) {
      return "<li>" + escapeHtml(f) + "</li>";
    }).join("");
    return (
      "<div class='ocec-input-review'>" +
      "<h5 class='ocec-input-title'>" + escapeHtml(review.title || Copy().inputReviewTitle) + "</h5>" +
      "<p class='ocec-input-principle muted'>" + escapeHtml(review.principle || Copy().inputPrinciple) + "</p>" +
      "<details class='ocec-input-details'><summary>允许输入</summary><ul class='ocec-input-list'>" +
      allowed + "</ul></details>" +
      "<details class='ocec-input-details'><summary>禁止输入</summary><ul class='ocec-input-list ocec-forbidden-list'>" +
      forbidden + "</ul></details></div>"
    );
  }

  function renderFutureEnvelope(preview) {
    if (!preview) return "";
    var fields = (preview.fields || []).map(function (f) {
      return "<li>" + escapeHtml(f) + "</li>";
    }).join("");
    return (
      "<div class='ocec-future-envelope'>" +
      "<h5 class='ocec-subtitle'>" + escapeHtml(Copy().futureEnvelopeTitle) + "</h5>" +
      "<p class='muted ocec-mono'>" + escapeHtml(preview.envelope_type || "ocr_result_envelope") + "</p>" +
      "<ul class='ocec-field-list'>" + fields + "</ul>" +
      "<p class='muted'>planning_only · not_fact · needs_fact_admission</p></div>"
    );
  }

  function renderFusionPlaceholder(fp) {
    if (!fp) return "";
    return (
      "<div class='ocec-fusion-placeholder'>" +
      "<h5 class='ocec-subtitle'>" + escapeHtml(Copy().fusionPlaceholderTitle) + "</h5>" +
      "<p class='muted'>" + escapeHtml(Copy().fusionPlaceholder) + "</p></div>"
    );
  }

  function renderRequestItem(req) {
    var c = Copy();
    var adm = req.admission_result;
    var admDecision = adm ? adm.admission_decision : req.admission_status;
    var actions = "";
    if (req.admission_status === "pending_admission") {
      actions +=
        "<button type='button' class='ocec-btn' data-ocr-action='run-admission' data-oir='" +
        escapeHtml(req.ocr_invocation_request_id) + "'>" + escapeHtml(c.runAdmissionBtn) + "</button>" +
        "<button type='button' class='ocec-btn ocec-btn-ghost' data-ocr-action='cancel' data-oir='" +
        escapeHtml(req.ocr_invocation_request_id) + "'>" + escapeHtml(c.cancelRequestBtn) + "</button>";
    } else if (req.admission_status === "admitted") {
      actions +=
        "<button type='button' class='ocec-btn ocec-btn-generate' data-ocr-action='generate-candidate' data-oir='" +
        escapeHtml(req.ocr_invocation_request_id) + "'>" + escapeHtml(c.generateExecutionCandidateBtn) + "</button>";
    }
    actions +=
      "<button type='button' class='ocec-btn ocec-btn-ghost' data-ocr-action='toggle-trace' data-oir='" +
      escapeHtml(req.ocr_invocation_request_id) + "'>" + escapeHtml(c.viewTraceBtn) + "</button>";

    var admBlock = "";
    if (adm && adm.admission_decision === "admitted") {
      admBlock =
        "<p class='ocec-admitted'>" + escapeHtml(c.admittedNotice) + "</p>" +
        "<p class='muted'>trace_verified · route_match_verified · still_not_executed</p>";
    } else if (adm && adm.admission_decision === "rejected") {
      admBlock =
        "<p class='ocec-rejected'>rejected · " + escapeHtml(adm.rejection_reason || "—") + "</p>" +
        "<p class='muted'>policy_refs: " + escapeHtml((adm.policy_refs || []).join(", ")) + "</p>";
    }

    return (
      "<li class='ocec-request-item' data-oir='" + escapeHtml(req.ocr_invocation_request_id) + "'>" +
      "<div class='ocec-head'><strong class='ocec-mono'>" + escapeHtml(req.ocr_invocation_request_id) + "</strong></div>" +
      "<p class='ocec-row muted'>" + escapeHtml(c.labelRegion) + ": " + escapeHtml(req.source_region_id) + "</p>" +
      "<p class='ocec-row muted'>" + escapeHtml(c.labelStatus) + ": " + escapeHtml(req.admission_status) +
      " · " + escapeHtml(req.execution_status) + " · candidate_only · not_fact</p>" +
      "<p class='ocec-row muted'>task: " + escapeHtml(req.source_ocr_task_candidate_id) + "</p>" +
      admBlock +
      "<details class='ocec-trace-details' id='ocec-trace-" + escapeHtml(req.ocr_invocation_request_id) + "'>" +
      "<summary>" + escapeHtml(c.labelTrace) + "</summary>" +
      "<pre class='ocec-trace-pre'>" + escapeHtml(formatTrace(req.trace_chain)) + "</pre></details>" +
      "<div class='ocec-actions'>" + actions + "</div></li>"
    );
  }

  function renderCandidateItem(candidate) {
    var c = Copy();
    return (
      "<li class='ocec-candidate-item' data-ocec='" + escapeHtml(candidate.ocr_execution_candidate_id) + "'>" +
      "<div class='ocec-head'><strong class='ocec-mono'>" +
      escapeHtml(candidate.ocr_execution_candidate_id) + "</strong></div>" +
      "<p class='ocec-row muted'>request: " + escapeHtml(candidate.source_ocr_invocation_request_id) + "</p>" +
      "<p class='ocec-row muted'>" + escapeHtml(c.labelRegion) + ": " +
      escapeHtml(candidate.source_region_id) + "</p>" +
      "<p class='ocec-row muted'>" + escapeHtml(c.labelStatus) + ": " +
      "<strong class='ocec-status-planned'>" + escapeHtml(candidate.execution_status) + "</strong>" +
      " · not_executed · not_fact · needs_fact_admission</p>" +
      "<p class='ocec-row muted'>input_crop_ref: " + escapeHtml(candidate.input_crop_ref) + "</p>" +
      "<p class='ocec-row muted'>geometry_ref: " + escapeHtml(candidate.input_region_geometry_ref) + "</p>" +
      "<p class='ocec-notice muted'>" + escapeHtml(c.notExecutionNotice) + "</p>" +
      renderInputReview(candidate.input_review) +
      renderFutureEnvelope(candidate.future_envelope_preview) +
      renderFusionPlaceholder(candidate.fusion_placeholder) +
      "<details class='ocec-trace-details'><summary>" + escapeHtml(c.labelTrace) + "</summary>" +
      "<pre class='ocec-trace-pre'>" + escapeHtml(formatTrace(candidate.trace_chain)) + "</pre></details>" +
      "<div class='ocec-actions'>" +
      (candidate.execution_status === "planned_only" || candidate.execution_status === "ready_for_execution_review"
        ? "<button type='button' class='ocec-btn ocec-btn-run' data-ocr-action='run-controlled-ocr' data-ocec='" +
          escapeHtml(candidate.ocr_execution_candidate_id) + "'>" + escapeHtml(c.runControlledOcrBtn) + "</button>"
        : "") +
      "</div></li>"
    );
  }

  function render(host, ocrPkg, options) {
    options = options || {};
    if (!host) return;
    var c = Copy();
    var requests = (ocrPkg && ocrPkg.requests) || [];
    var candidates = (ocrPkg && ocrPkg.candidates) || [];

    if (!requests.length && !candidates.length) {
      host.innerHTML =
        "<section class='ocec-panel ocec-panel-empty'>" +
        "<h3 class='ocec-title'>" + escapeHtml(c.ocrRequestTitle) + " / " +
        escapeHtml(c.ocrAdmissionTitle) + " / " + escapeHtml(c.ocrExecutionCandidateTitle) + "</h3>" +
        "<p class='muted'>" + escapeHtml(safe(c.emptyRequests)) + "</p></section>";
      host.hidden = false;
      return;
    }

    var html = "<section class='ocec-panel'>";
    if (requests.length) {
      html += "<h3 class='ocec-title'>" + escapeHtml(c.ocrRequestTitle) + " · " +
        escapeHtml(c.ocrAdmissionTitle) + "</h3>" +
        "<p class='ocec-notice muted'>" + escapeHtml(c.notExecutionNotice) + "</p>" +
        "<ol class='ocec-list'>" + requests.map(renderRequestItem).join("") + "</ol>";
    }
    if (candidates.length) {
      html += "<h3 class='ocec-title ocec-title-candidate'>" + escapeHtml(c.ocrExecutionCandidateTitle) + "</h3>" +
        "<ol class='ocec-list'>" + candidates.map(renderCandidateItem).join("") + "</ol>";
    }
    html += "</section>";
    host.innerHTML = html;
    host.hidden = false;
  }

  function bindActions(host, onOcrAction) {
    if (!host || !onOcrAction) return;
    host.addEventListener("click", function (ev) {
      var btn = ev.target.closest("[data-ocr-action]");
      if (!btn) return;
      ev.preventDefault();
      var action = btn.getAttribute("data-ocr-action");
      var oir = btn.getAttribute("data-oir");
      var ocec = btn.getAttribute("data-ocec");
      if (action === "toggle-trace" && oir) {
        var det = host.querySelector("#ocec-trace-" + oir);
        if (det) det.open = !det.open;
        return;
      }
      onOcrAction(action, oir, ocec);
    });
  }

  global.MobileSamOcrControlledExecutionPanel = {
    version: "mobile_sam_ocr_controlled_execution_panel_v1",
    no_ocr_runner_call: true,
    no_ocr_execution: true,
    render: render,
    bindActions: bindActions
  };
})(typeof window !== "undefined" ? window : this);
