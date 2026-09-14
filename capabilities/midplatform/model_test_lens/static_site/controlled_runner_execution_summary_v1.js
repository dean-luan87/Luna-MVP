/**
 * Controlled Runner Execution — bottom execution candidate summary. No runner execution.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.ControlledRunnerExecutionCopy || {}; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function formatExecutionSummary(executionPkg) {
    if (!executionPkg || !executionPkg.stats) return "";
    var c = Copy();
    var s = executionPkg.stats;
    return (c.summaryPrefix || "受控执行候选") + "：planned_only " + (s.planned_only || 0) +
      " 个，ready_for_review " + (s.ready_for_execution_review || 0) +
      " 个，cancelled " + (s.cancelled || 0) + " 个，blocked " + (s.blocked || 0) + " 个。";
  }

  function appendToMetricsSummary(baseHtml, executionPkg) {
    var line = formatExecutionSummary(executionPkg);
    if (!line) return baseHtml;
    return baseHtml + "｜<span class='crec-summary-inline'>" + escapeHtml(line) +
      " <span class='crec-exec-tag'>受控执行</span></span>";
  }

  global.ControlledRunnerExecutionSummary = {
    version: "controlled_runner_execution_summary_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Controlled-Runner-Execution-UI-Execution-v1-001",
    footerSummaryOnly: true,
    noRunnerExecution: true,
    formatExecutionSummary: formatExecutionSummary,
    appendToMetricsSummary: appendToMetricsSummary
  };
})(typeof window !== "undefined" ? window : this);
