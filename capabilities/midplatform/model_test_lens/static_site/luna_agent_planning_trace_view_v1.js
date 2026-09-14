/**
 * Luna Agent Planning — L1→L2→L3 chain trace view.
 */
(function (global) {
  "use strict";

  function escapeHtml(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function render(host, pkg) {
    if (!host) return;
    var chain = (pkg && pkg.chain_trace) || [];
    if (!chain.length) {
      host.innerHTML = "";
      host.hidden = true;
      return;
    }
    host.hidden = false;
    var items = chain.map(function (step, i) {
      var arrow = i < chain.length - 1 ? "<div class='lap-trace-arrow'>↓</div>" : "";
      return (
        "<div class='lap-trace-step'>" +
        "<span class='lap-k'>" + escapeHtml(step.stage) + "</span>" +
        "<br>" + escapeHtml(step.summary || "") +
        " · <span class='lap-tag'>candidate_only</span>" +
        "</div>" + arrow
      );
    }).join("");
    host.innerHTML =
      "<div class='lap-trace-block'>" +
      "<h4>决策链 Trace</h4>" +
      "<p class='lap-muted'>L1 Situation → L2 Plan → L3 Tool OS handoff</p>" +
      items +
      "</div>";
  }

  global.LunaAgentPlanTraceView = {
    version: "luna_agent_plan_trace_view_v1",
    render: render
  };
})(typeof window !== "undefined" ? window : this);
