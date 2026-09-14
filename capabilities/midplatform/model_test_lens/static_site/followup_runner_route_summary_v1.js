/**
 * Followup Runner Route — bottom queue summary (stats only, no execution results).
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.FollowupRunnerRouteCopy || {}; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function formatQueueSummary(queuePkg) {
    if (!queuePkg || !queuePkg.stats) return "";
    var c = Copy();
    var s = queuePkg.stats;
    return (c.summaryPrefix || "后续任务候选") + "：auto_eligible " + (s.auto_eligible || 0) +
      " 个，manual_only " + (s.manual_only || 0) + " 个，pinned " + (s.pinned || 0) +
      " 个，excluded " + (s.excluded || 0) + " 个，已入队 " + (s.active || 0) + " 个。";
  }

  function appendToMetricsSummary(baseHtml, queuePkg) {
    var line = formatQueueSummary(queuePkg);
    if (!line) return baseHtml;
    return baseHtml + "｜<span class='frr-summary-inline'>" + escapeHtml(line) +
      " <span class='frr-candidate-tag'>候选队列</span></span>";
  }

  global.FollowupRunnerRouteSummary = {
    version: "followup_runner_route_summary_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-UI-Queue-Execution-And-Post-Review-v1-001",
    footerSummaryOnly: true,
    noRunnerExecution: true,
    formatQueueSummary: formatQueueSummary,
    appendToMetricsSummary: appendToMetricsSummary
  };
})(typeof window !== "undefined" ? window : this);
