/**
 * MobileSAM → OCR Controlled Execution — bottom summary stats.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.MobileSamOcrControlledExecutionCopy || {}; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function buildStatsLine(ocrPkg) {
    var c = Copy();
    if (!ocrPkg || !ocrPkg.stats) return "";
    var s = ocrPkg.stats;
    return (
      "｜" + escapeHtml(c.summaryOcrRequests) + " pending=" + (s.pending || 0) +
      " admitted=" + (s.admitted || 0) + " rejected=" + (s.rejected || 0) +
      " cancelled=" + (s.cancelled || 0) +
      "｜" + escapeHtml(c.summaryOcrCandidates) + " planned=" + (s.candidates_planned || 0) +
      " not_executed=" + (s.candidates_not_executed || 0) +
      "｜OCR executed=" + (s.executed || 0) + " (" + escapeHtml(c.ocrExecutedMustBeZero) + ")"
    );
  }

  function appendToMetricsSummary(base, ocrPkg) {
    var line = buildStatsLine(ocrPkg);
    return line ? base + line : base;
  }

  function buildPackage(store) {
    if (!store) {
      return { requests: [], candidates: [], stats: { executed: 0 }, candidate_only: true };
    }
    var requests = store.getRequests ? store.getRequests() : [];
    var candidates = store.getCandidates ? store.getCandidates() : [];
    var stats = store.getStats ? store.getStats() : { executed: 0 };
    return {
      phase_ref: "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Controlled-Execution-UI-Execution-v1-001",
      requests: requests,
      candidates: candidates,
      stats: stats,
      candidate_only: true,
      not_fact: true,
      no_ocr_runner_call: true,
      no_ocr_execution: true,
      ocr_executed_must_be_zero: stats.executed === 0
    };
  }

  global.MobileSamOcrControlledExecutionSummary = {
    version: "mobile_sam_ocr_controlled_execution_summary_v1",
    appendToMetricsSummary: appendToMetricsSummary,
    buildPackage: buildPackage
  };
})(typeof window !== "undefined" ? window : this);
