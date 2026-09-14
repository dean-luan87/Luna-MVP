/**
 * Luna Agent Planning — bottom summary line.
 */
(function (global) {
  "use strict";

  function summaryLine(pkg) {
    if (!pkg || !pkg.selected_plan) return "";
    var goal = pkg.selected_plan.goal_type || "unknown";
    var tools = ((pkg.tool_plan && pkg.tool_plan.active) || []).map(function (t) {
      return String(t.capability_type || "").toUpperCase();
    });
    var noops = ((pkg.tool_plan && pkg.tool_plan.noop) || []).map(function (t) {
      return String(t.capability_type || "").toUpperCase();
    });
    var scene = (pkg.situation_summary && pkg.situation_summary.scene_type) || "—";
    if (goal === "ask_user") {
      return "plan: ask_user · scene: " + scene + " · no blanket activation · candidate";
    }
    return "plan: " + goal +
      " · scene: " + scene +
      " · active: " + (tools.join("/") || "—") +
      " · noop: " + (noops.slice(0, 3).join("/") || "—") +
      " · candidate_only";
  }

  global.LunaAgentPlanningSummary = {
    version: "luna_agent_planning_summary_v1",
    summaryLine: summaryLine
  };
})(typeof window !== "undefined" ? window : this);
