/**
 * Luna Situation Understanding — bottom summary v1.
 */
(function (global) {
  "use strict";

  function taskTypes(pkg) {
    return (pkg.task_clue_candidates || []).map(function (c) { return c.task_type; });
  }

  function caps(pkg, bucket) {
    var summary = pkg.model_need_hint_summary || {};
    if (summary[bucket]) return summary[bucket];
    var hints = pkg.model_need_hints || {};
    return (hints[bucket] || []).map(function (h) { return h.capability_type; });
  }

  function summaryLine(pkg) {
    if (!pkg || !pkg.scene_profile_candidate) return "";
    var scene = pkg.scene_profile_candidate.scene_type || "unknown";
    var tasks = taskTypes(pkg);
    var likely = caps(pkg, "likely_needed");
    var noop = caps(pkg, "not_needed");
    var taskStr = tasks.slice(0, 2).join("/") || "—";
    var needStr = likely.join("/") || "—";
    var noopStr = noop.length ? noop.map(function (c) { return c.toUpperCase(); }).join("/") : "—";
    if (scene === "unknown_scene") {
      var fb = (pkg.uncertainty && pkg.uncertainty.fallback_suggestion) || "ask_user";
      return "situation: unknown · fallback: " + fb + " · no blanket activation";
    }
    return "situation: " + scene + " · task: " + taskStr + " · need: " + needStr.toUpperCase() + " · noop: " + noopStr;
  }

  global.LunaSituationUnderstandingSummary = {
    version: "luna_situation_understanding_summary_v1",
    summaryLine: summaryLine
  };
})(typeof window !== "undefined" ? window : this);
