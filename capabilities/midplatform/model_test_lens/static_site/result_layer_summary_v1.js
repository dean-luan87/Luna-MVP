/**
 * Result Layer — bottom summary for result candidates.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.ResultLayerCopy || {}; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function formatSummary(resultPkg) {
    if (!resultPkg || !resultPkg.stats) return "";
    var s = resultPkg.stats;
    return "结果候选：" + (s.results || 0) + " 个，错误候选 " + (s.errors || 0) +
      " 个，执行记录 " + (s.executions || 0) + " 个。";
  }

  function appendToMetricsSummary(baseHtml, resultPkg) {
    var line = formatSummary(resultPkg);
    if (!line) return baseHtml;
    return baseHtml + "｜<span class='rl-summary-inline'>" + escapeHtml(line) +
      " <span class='rl-result-tag'>结果层</span></span>";
  }

  global.ResultLayerSummary = {
    version: "result_layer_summary_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-MobileSAM-Single-Model-Execution-Integration-v1-002",
    appendToMetricsSummary: appendToMetricsSummary
  };
})(typeof window !== "undefined" ? window : this);
