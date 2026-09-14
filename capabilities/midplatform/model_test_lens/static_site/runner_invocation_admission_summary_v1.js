/**
 * Runner Invocation Admission — bottom admission summary (executed must be 0).
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.RunnerInvocationAdmissionCopy || {}; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function formatAdmissionSummary(requestPkg) {
    if (!requestPkg || !requestPkg.admission_stats) return "";
    var c = Copy();
    var s = requestPkg.admission_stats;
    return (c.summaryPrefix || "准入请求") + "：admitted " + (s.admitted || 0) +
      " 个，rejected " + (s.rejected || 0) + " 个，pending " + (s.pending || 0) +
      " 个，cancelled " + (s.cancelled || 0) + " 个，executed " + (s.executed || 0) + " 个。";
  }

  function appendToMetricsSummary(baseHtml, requestPkg) {
    var line = formatAdmissionSummary(requestPkg);
    if (!line) return baseHtml;
    return baseHtml + "｜<span class='ria-summary-inline'>" + escapeHtml(line) +
      " <span class='ria-admission-tag'>准入闸门</span></span>";
  }

  global.RunnerInvocationAdmissionSummary = {
    version: "runner_invocation_admission_summary_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Runner-Invocation-Admission-Execution-And-Post-Review-v1-001",
    footerSummaryOnly: true,
    noRunnerExecution: true,
    formatAdmissionSummary: formatAdmissionSummary,
    appendToMetricsSummary: appendToMetricsSummary
  };
})(typeof window !== "undefined" ? window : this);
