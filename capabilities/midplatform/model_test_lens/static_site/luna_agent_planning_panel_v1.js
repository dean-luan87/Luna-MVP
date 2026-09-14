/**
 * Luna Agent Planning — right panel v1 (goal / competition / selected / tools / handoff).
 */
(function (global) {
  "use strict";

  function Copy() { return global.LunaAgentPlanningCopy || {}; }

  function escapeHtml(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function safeText(text) {
    var s = String(text || "");
    var forbidden = Copy().forbiddenParts || [];
    for (var i = 0; i < forbidden.length; i++) {
      if (s.indexOf(forbidden[i]) >= 0) return "[文案违规已屏蔽]";
    }
    return s || "—";
  }

  function modelLabel(cap) {
    return (Copy().modelLabels || {})[cap] || String(cap || "").toUpperCase();
  }

  function renderGoals(goals) {
    if (!goals || !goals.length) return "";
    var items = goals.map(function (g, idx) {
      return (
        "<li class='lap-item'>" +
        "<span class='lap-k'>" + (idx + 1) + ".</span> " +
        "<strong>" + escapeHtml(safeText(g.goal_type)) + "</strong>" +
        " · confidence: " + escapeHtml(String(g.confidence)) +
        "<br><span class='lap-muted'>source: " + escapeHtml(safeText(g.source)) +
        " · <span class='lap-tag'>candidate</span></span></li>"
      );
    }).join("");
    return "<div class='lap-block'><h4>" + escapeHtml(Copy().goalTitle || "目标理解") + "</h4>" +
      "<p class='lap-muted'>Candidate goals（多目标候选，非最终事实）</p>" +
      "<ul class='lap-list'>" + items + "</ul></div>";
  }

  function renderCompetition(cards) {
    if (!cards || !cards.length) return "";
    var blocks = cards.map(function (c) {
      var selected = c.status === "selected";
      return (
        "<div class='lap-plan-card" + (selected ? " lap-plan-selected" : "") + "'>" +
        "<div class='lap-plan-head'>" +
        "<strong>" + escapeHtml(safeText(c.label || c.slot)) + "</strong>" +
        " <span class='lap-tag'>" + escapeHtml(selected ? (Copy().selectedBadge || "selected_plan_candidate") : "candidate") + "</span>" +
        "</div>" +
        "<p><span class='lap-k'>目标</span> " + escapeHtml(safeText(c.goal_type)) + "</p>" +
        "<p><span class='lap-k'>策略</span> " + escapeHtml(safeText(c.strategy_type)) + "</p>" +
        "<p><span class='lap-k'>工具</span> " + escapeHtml((c.tools || []).map(modelLabel).join(", ") || "—") + "</p>" +
        "<p><span class='lap-k'>评分</span> " + escapeHtml(String(c.score != null ? c.score : "—")) + "</p>" +
        "</div>"
      );
    }).join("");
    return "<div class='lap-block'><h4>" + escapeHtml(Copy().competitionTitle || "计划竞争") + "</h4>" + blocks + "</div>";
  }

  function renderSelected(selected, reason) {
    if (!selected) return "";
    var steps = (selected.steps || []).map(function (s) {
      return "<li class='lap-item'>" + escapeHtml(String(s.step_order)) + ". " +
        escapeHtml(safeText(s.step_type)) + " — " + escapeHtml(safeText(s.step_goal)) + "</li>";
    }).join("");
    var reasonHtml = "";
    if (reason) {
      var pos = (reason.positives || []).map(function (p) {
        return "<li class='lap-plus'>+ " + escapeHtml(safeText(p)) + "</li>";
      }).join("");
      var neg = (reason.negatives || []).map(function (n) {
        return "<li class='lap-minus'>- " + escapeHtml(safeText(n)) + "</li>";
      }).join("");
      reasonHtml =
        "<div class='lap-reason'>" +
        "<h5>" + escapeHtml(Copy().reasonTitle || "为什么选择这个计划") + "</h5>" +
        "<ul class='lap-list'>" + pos + neg + "</ul>" +
        "<p><span class='lap-k'>Final</span> " + escapeHtml(safeText(reason.final_label)) + "</p>" +
        "</div>";
    }
    return (
      "<div class='lap-block lap-selected-block'>" +
      "<h4>" + escapeHtml(Copy().selectedTitle || "当前选择") + "</h4>" +
      "<p><span class='lap-k'>Selected Plan</span> " + escapeHtml(safeText(selected.goal_type)) +
      " · <span class='lap-tag'>selected_plan_candidate</span></p>" +
      "<p><span class='lap-k'>strategy</span> " + escapeHtml(safeText(selected.strategy_type)) + "</p>" +
      (steps ? "<ul class='lap-list'>" + steps + "</ul>" : "") +
      reasonHtml +
      "</div>"
    );
  }

  function renderToolPlan(toolPlan) {
    if (!toolPlan) return "";
    var active = (toolPlan.active || []).map(function (t) {
      return "<li class='lap-item'><span class='lap-k'>" + escapeHtml(modelLabel(t.capability_type)) + "</span>" +
        "<br>purpose: " + escapeHtml(safeText(t.purpose)) +
        "<br>execution: " + escapeHtml(safeText(t.execution_mode || "request_tool_os_admission")) +
        " · <span class='lap-tag'>candidate</span></li>";
    }).join("");
    var noop = (toolPlan.noop || []).map(function (n) {
      return "<li class='lap-item'><span class='lap-k'>" + escapeHtml(modelLabel(n.capability_type)) + "</span>" +
        "<br>reason: " + escapeHtml(safeText(n.noop_reason)) + "</li>";
    }).join("");
    return (
      "<div class='lap-block'>" +
      "<h4>" + escapeHtml(Copy().toolPlanTitle || "工具计划") + "</h4>" +
      "<div class='lap-tool-col'><h5>" + escapeHtml(Copy().activeTitle || "Active") + "</h5>" +
      (active ? "<ul class='lap-list'>" + active + "</ul>" : "<p class='lap-muted'>—</p>") + "</div>" +
      "<div class='lap-tool-col lap-noop'><h5>" + escapeHtml(Copy().noopTitle || "Noop") + "</h5>" +
      (noop ? "<ul class='lap-list'>" + noop + "</ul>" : "<p class='lap-muted'>—</p>") + "</div>" +
      "<p class='lap-muted'>" + escapeHtml(Copy().notExecuted || "not executed") + "</p>" +
      "</div>"
    );
  }

  function renderHandoff(handoff) {
    if (!handoff) return "";
    var checks = (handoff.required_checks || []).map(function (c) {
      return "<li class='lap-item'>" + escapeHtml(safeText(c)) + "</li>";
    }).join("");
    return (
      "<div class='lap-block lap-handoff'>" +
      "<h4>" + escapeHtml(Copy().handoffTitle || "Tool OS 交接候选") + "</h4>" +
      "<p><span class='lap-k'>Request</span> " + escapeHtml((handoff.request_capabilities || []).map(modelLabel).join(", ") || "—") + "</p>" +
      "<p><span class='lap-k'>should_handoff</span> " + escapeHtml(String(!!handoff.should_handoff)) + "</p>" +
      "<p><span class='lap-k'>Required</span></p><ul class='lap-list'>" + checks + "</ul>" +
      "<p class='lap-status'><span class='lap-tag'>candidate_only</span> · <span class='lap-tag'>not_fact</span> · <span class='lap-tag'>not executed</span></p>" +
      "</div>"
    );
  }

  function render(host, pkg, options) {
    options = options || {};
    if (!host) return;
    if (!pkg) {
      host.innerHTML = "<div class='lap-panel'><p class='muted'>" + escapeHtml(Copy().emptyHint || "") + "</p></div>";
      host.hidden = false;
      return;
    }
    host.hidden = false;
    var traceHostId = "lap-trace-" + Math.random().toString(36).slice(2, 8);
    host.innerHTML =
      "<div class='lap-panel'>" +
      "<h3 class='lap-heading'>" + escapeHtml(Copy().sectionTitle || "行动计划") + "</h3>" +
      "<p class='lap-sub'>" + escapeHtml(Copy().sectionSubtitle || "") + "</p>" +
      "<p class='lap-muted'>" + escapeHtml(Copy().wordingNote || "") + "</p>" +
      renderGoals(pkg.goal_candidates) +
      renderCompetition(pkg.plan_competition_cards) +
      renderSelected(pkg.selected_plan, pkg.selection_reason) +
      renderToolPlan(pkg.tool_plan) +
      renderHandoff(pkg.tool_os_handoff) +
      "<div id='" + traceHostId + "'></div>" +
      "</div>";
    var traceHost = host.querySelector("#" + traceHostId);
    if (traceHost && global.LunaAgentPlanTraceView) {
      global.LunaAgentPlanTraceView.render(traceHost, pkg, options);
    }
  }

  global.LunaAgentPlanningPanel = {
    version: "luna_agent_planning_panel_v1",
    render: render
  };
})(typeof window !== "undefined" ? window : this);
