/**
 * Multi-model collaboration — minimal OCR route candidate display (exploration smoke).
 * No OCR runner · no OCR result · candidate_only
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.MultiModelCollaborationCopy || {}; };

  var FORBIDDEN_UI = /已识别文字|OCR结果|发现路牌|读取成功|确认这是路牌/;

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function assertSafeCopy(text) {
    if (FORBIDDEN_UI.test(text)) return "[文案违规已屏蔽]";
    return text;
  }

  function renderCollaborationItem(item, options) {
    options = options || {};
    if (!item || !item.ocr_task_candidate) return "";
    var c = Copy();
    var ocrCopy = global.MobileSamOcrControlledExecutionCopy || {};
    var rc = item.result_candidate || {};
    var analysis = item.midplatform_analysis_record || {};
    var task = item.ocr_task_candidate || {};
    var features = (analysis.appearance_signals || analysis.region_features || []).slice(0, 4);
    var taskId = task.task_candidate_id || "";
    var hasActive = options.activeOcrTaskIds && options.activeOcrTaskIds[taskId];
    var btnLabel = ocrCopy.generateOcrRequestBtn || "生成 OCR 请求";
    var actions = hasActive
      ? "<p class='mmc-action muted'>已有活跃 OCR 请求</p>"
      : "<button type='button' class='mmc-btn' data-ocr-collab-action='generate-request' " +
        "data-task-id='" + escapeHtml(taskId) + "' data-region-id='" +
        escapeHtml(item.region_id || rc.source_region_id) + "'>" +
        escapeHtml(btnLabel) + "</button>";

    return (
      "<article class='mmc-card'>" +
      "<h4 class='mmc-title'>" + escapeHtml(c.sectionTitle) + "</h4>" +
      "<div class='mmc-flow'>" +
      "<p class='mmc-step'><strong>MobileSAM Result</strong><br>" +
      escapeHtml(c.labelRegion) + "：<span class='mmc-mono'>" + escapeHtml(rc.source_region_id || item.region_id) + "</span></p>" +
      "<p class='mmc-arrow muted'>↓</p>" +
      "<p class='mmc-step'><strong>" + escapeHtml(c.midplatformAnalysis) + "</strong><br>" +
      escapeHtml(c.detectedPrefix) + " " + escapeHtml(features.join(" · ") || c.staticCandidate) + "</p>" +
      "<p class='mmc-arrow muted'>↓</p>" +
      "<p class='mmc-step'><strong>" + escapeHtml(c.nextSuggestion) + "</strong><br>" +
      "OCR Task Candidate · <span class='mmc-mono'>" + escapeHtml(taskId) + "</span></p>" +
      "</div>" +
      "<p class='mmc-status'><span class='mmc-tag'>" + escapeHtml(c.statusCandidate) + "</span> · " +
      escapeHtml(c.notExecuted) + "</p>" +
      "<div class='mmc-actions'>" + actions + "</div>" +
      "<p class='mmc-trace muted'>" + escapeHtml(c.traceHint) + "</p>" +
      "</article>"
    );
  }

  function render(host, collaborationPkg, options) {
    if (!host) return;
    var c = Copy();
    var items = (collaborationPkg && collaborationPkg.items) || [];
    var withOcr = items.filter(function (it) { return it && it.ocr_task_candidate; });

    if (!withOcr.length) {
      host.innerHTML = (
        "<section class='mmc-panel mmc-panel-empty'>" +
        "<h3 class='mmc-heading'>" + escapeHtml(c.sectionTitle) + "</h3>" +
        "<p class='muted'>" + escapeHtml(assertSafeCopy(c.emptyHint)) + "</p></section>"
      );
      host.hidden = false;
      return;
    }

    host.innerHTML = (
      "<section class='mmc-panel'>" +
      withOcr.map(function (it) { return renderCollaborationItem(it, options); }).join("") +
      "</section>"
    );
    host.hidden = false;
  }

  global.MultiModelCollaborationPanel = {
    version: "multi_model_collaboration_panel_v1",
    phaseRef: "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Controlled-Execution-UI-Execution-v1-001",
    no_ocr_runner_call: true,
    no_ocr_execution: true,
    no_text_fact_generation: true,
    render: render
  };
})(typeof window !== "undefined" ? window : this);
