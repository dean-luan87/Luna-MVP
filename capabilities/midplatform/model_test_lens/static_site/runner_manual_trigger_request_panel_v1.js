/**
 * Runner Manual Trigger — pending invocation request panel. No runner execution.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.RunnerManualTriggerCopy || {}; };
  var AdmPanel = function () { return global.RunnerInvocationAdmissionPanel; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function formatTrace(trace) {
    if (!trace || !trace.length) return "";
    return trace.map(function (t) {
      return t.stage + ":" + t.ref + (t.queue_state ? "(" + t.queue_state + ")" : "");
    }).join(" → ");
  }

  function renderRequestItem(req, options) {
    var c = Copy();
    var active = options.selectedRegionId === req.source_region_id ? " rmt-request-item-active" : "";
    var boost = req.correction_boosted
      ? "<span class='rmt-badge rmt-badge-hc'>人工指错加权（非 ground truth）</span>" : "";

    var admissionHtml = AdmPanel() ? AdmPanel().renderAdmissionSection(req) : "";
    var actions = AdmPanel() ? AdmPanel().renderActions(req) : "";

    return (
      "<li class='rmt-request-item" + active + "' data-region-id='" + escapeHtml(req.source_region_id) + "' " +
      "data-rir-id='" + escapeHtml(req.invocation_request_id) + "' role='button' tabindex='0'>" +
      "<div class='rmt-request-head'>" +
      "<strong>" + escapeHtml(req.invocation_request_id) + "｜" +
      escapeHtml(req.requested_runner_type) + "｜" +
      escapeHtml(req.region_display_name || req.source_region_id) + "</strong>" + boost +
      "</div>" +
      "<p class='rmt-request-meta'><span class='muted'>" + escapeHtml(c.labelAdmission) + "：</span>" +
      escapeHtml(req.admission_status) + " · " + escapeHtml(c.labelExecution) + ": " +
      escapeHtml(req.execution_status) + " · trigger: " + escapeHtml(req.trigger_mode) + "</p>" +
      "<p class='rmt-request-meta'><span class='muted'>" + escapeHtml(c.labelRequestedBy) + "：</span>" +
      escapeHtml(req.requested_by) + "</p>" +
      "<p class='rmt-request-reason'><span class='muted'>" + escapeHtml(c.labelReason) + "：</span>" +
      escapeHtml(req.route_reason) + "</p>" +
      "<p class='rmt-request-notice muted'>" + escapeHtml(c.notExecutionNotice) + "</p>" +
      "<p class='rmt-request-status'>" + escapeHtml(c.statusLine) + "</p>" +
      admissionHtml +
      "<p class='rmt-request-trace muted'>" + escapeHtml(c.labelTrace) + "：rtc " +
      escapeHtml(req.source_runner_task_candidate_id) + " · region " +
      escapeHtml(req.source_region_id) + " · attention " +
      escapeHtml(req.source_attention_record_id) + "</p>" +
      "<details class='rmt-trace-details'><summary>" + escapeHtml(c.traceToggle) + "</summary>" +
      "<pre class='rmt-trace-pre'>" + escapeHtml(formatTrace(req.trace_chain)) + "</pre></details>" +
      (actions ? "<div class='rmt-request-actions'>" + actions + "</div>" : "") +
      "</li>"
    );
  }

  function render(host, requestPkg, options) {
    options = options || {};
    if (!host) return;
    var c = Copy();
    var list = (requestPkg && requestPkg.active_requests) || [];
    if (!list.length) {
      host.innerHTML =
        "<section class='rmt-request-panel rmt-request-panel-empty'>" +
        "<h3 class='rmt-request-title'>" + escapeHtml(c.panelTitle) + "</h3>" +
        "<p class='muted'>" + escapeHtml(c.panelNotice) + "</p>" +
        "<p class='muted'>暂无待准入请求。请从 pinned 任务候选生成。</p></section>";
      host.hidden = false;
      return;
    }
    host.hidden = false;
    host.innerHTML =
      "<section class='rmt-request-panel'>" +
      "<h3 class='rmt-request-title'>" + escapeHtml(c.panelTitle) + "</h3>" +
      "<p class='rmt-request-notice muted'>" + escapeHtml(c.panelNotice) + "</p>" +
      "<ol class='rmt-request-list'>" +
      list.map(function (r) { return renderRequestItem(r, options); }).join("") +
      "</ol></section>";

    host.querySelectorAll("[data-req-action]").forEach(function (btn) {
      btn.addEventListener("click", function (ev) {
        ev.stopPropagation();
        if (options.onRequestAction) {
          options.onRequestAction(btn.dataset.reqAction, btn.dataset.rir);
        }
      });
    });

    host.querySelectorAll(".rmt-request-item").forEach(function (li) {
      var regionId = li.dataset.regionId;
      li.addEventListener("click", function (ev) {
        if (ev.target.closest("[data-req-action]") || ev.target.closest("details")) return;
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

  global.RunnerManualTriggerRequestPanel = {
    version: "runner_manual_trigger_request_panel_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Runner-Manual-Trigger-UI-Execution-And-Post-Review-v1-001",
    noRunnerExecution: true,
    requestCopyMustNotImplyExecution: true,
    render: render
  };
})(typeof window !== "undefined" ? window : this);
