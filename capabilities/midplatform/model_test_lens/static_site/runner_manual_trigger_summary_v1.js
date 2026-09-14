/**
 * Runner Manual Trigger — bottom request summary (stats only, executed must be 0).
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.RunnerManualTriggerCopy || {}; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function formatRequestSummary(requestPkg) {
    if (!requestPkg || !requestPkg.stats) return "";
    var c = Copy();
    var s = requestPkg.stats;
    return (c.summaryPrefix || "待准入请求") + "：pending " + (s.pending || 0) +
      " 个，admitted " + (s.admitted || 0) + " 个，rejected " + (s.rejected || 0) +
      " 个，cancelled " + (s.cancelled || 0) + " 个，executed " + (s.executed || 0) + " 个。";
  }

  function appendToMetricsSummary(baseHtml, requestPkg) {
    var line = formatRequestSummary(requestPkg);
    if (!line) return baseHtml;
    return baseHtml + "｜<span class='rmt-summary-inline'>" + escapeHtml(line) +
      " <span class='rmt-request-tag'>待准入</span></span>";
  }

  global.RunnerManualTriggerSummary = {
    version: "runner_manual_trigger_summary_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Runner-Manual-Trigger-UI-Execution-And-Post-Review-v1-001",
    footerSummaryOnly: true,
    noRunnerExecution: true,
    formatRequestSummary: formatRequestSummary,
    appendToMetricsSummary: appendToMetricsSummary
  };
})(typeof window !== "undefined" ? window : this);
