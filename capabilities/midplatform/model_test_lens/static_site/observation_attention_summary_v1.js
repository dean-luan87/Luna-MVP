/**
 * Observation Attention Layer V1 — bottom summary line builder.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.ObservationAttentionCopy || {}; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function formatSchedulingSummary(attentionPkg) {
    if (!attentionPkg || !attentionPkg.records || !attentionPkg.records.length) return "";
    var c = Copy();
    var priLabels = c.priorityLevel || {};
    var motionLabels = c.motionState || {};
    var buckets = {};
    attentionPkg.records.forEach(function (rec) {
      if (rec.priority_level === "ignore_for_now" || rec.priority_level === "P3_low_attention") return;
      var pri = priLabels[rec.priority_level] || rec.priority_level;
      var motion = motionLabels[rec.motion_state_candidate] || rec.motion_state_candidate;
      var key = pri + " " + motion;
      buckets[key] = (buckets[key] || 0) + 1;
    });
    var parts = Object.keys(buckets).map(function (k) { return k + " " + buckets[k] + " 个"; });
    var total = attentionPkg.priority_panel ? attentionPkg.priority_panel.length : parts.length;
    if (!parts.length) return attentionPkg.summary || "";
    return (c.summaryPrefix || "本帧建议优先观察") + " " + total +
      (c.summaryRegions || " 个区域") + "：" + parts.join("，") + "。";
  }

  function appendToMetricsSummary(baseHtml, attentionPkg) {
    var line = formatSchedulingSummary(attentionPkg);
    if (!line) return baseHtml;
    return baseHtml + "｜<span class='oa-summary-inline'>" + escapeHtml(line) +
      " <span class='oa-candidate-tag'>候选调度</span></span>";
  }

  function buildStandalone(attentionPkg) {
    var line = formatSchedulingSummary(attentionPkg);
    if (!line) return "<span class='muted'>暂无观察调度候选。</span>";
    return "<span class='oa-summary-inline'>" + escapeHtml(line) +
      " <span class='oa-candidate-tag'>候选调度</span></span>";
  }

  global.ObservationAttentionSummary = {
    version: "observation_attention_summary_v2_visual_expression_system",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Visual-Expression-System-UI-Execution-And-Post-Review-v1-001",
    footerSummaryOnly: true,
    noRunnerExecution: true,
    noFactWrite: true,
    formatSchedulingSummary: formatSchedulingSummary,
    appendToMetricsSummary: appendToMetricsSummary,
    buildStandalone: buildStandalone
  };
})(typeof window !== "undefined" ? window : this);
