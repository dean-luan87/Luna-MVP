/**
 * Luna Situation Understanding — right panel v1 (L1 candidate display, no canvas overlay).
 */
(function (global) {
  "use strict";

  function Copy() { return global.LunaSituationUnderstandingCopy || {}; }

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function safeText(text) {
    var s = String(text || "");
    var forbidden = Copy().forbiddenParts || [];
    for (var i = 0; i < forbidden.length; i++) {
      if (s.toLowerCase().indexOf(String(forbidden[i]).toLowerCase()) >= 0) return "[文案违规已屏蔽]";
    }
    return s || "—";
  }

  function modelLabel(cap) {
    var labels = Copy().modelLabels || {};
    return labels[cap] || String(cap || "").toUpperCase();
  }

  function renderBadges(badges) {
    return (badges || ["candidate_only", "not_fact"]).map(function (b) {
      return "<span class='lsu-tag'>" + escapeHtml(b) + "</span>";
    }).join(" · ");
  }

  function renderSummaryCard(pkg) {
    var c = Copy();
    var scene = pkg.scene_profile_candidate || {};
    var runner = pkg.runner_scene_hint_evidence || {};
    var tasks = (pkg.task_clue_candidates || []).length;
    var likely = ((pkg.model_need_hint_summary || {}).likely_needed || []).length;
    var hasConflict = (pkg.conflict_trace || []).some(function (t) { return t.stage === "runner_scene_hint_conflict"; });
    var resolution = hasConflict
      ? "Situation Layer overrides runner hint as candidate-level scene resolution"
      : "scene owned by situation_understanding_layer";
    return (
      "<div class='lsu-block lsu-summary-card'>" +
      "<h4>" + escapeHtml(c.summaryCardTitle || "处境候选摘要") + "</h4>" +
      "<p><span class='lsu-k'>" + escapeHtml(c.sceneLabel || "场景候选") + "</span> " +
      escapeHtml(safeText(scene.scene_type)) + " candidate</p>" +
      "<p><span class='lsu-k'>" + escapeHtml(c.ownerLabel || "scene owner") + "</span> " +
      escapeHtml(scene.owned_by || "situation_understanding_layer") + "</p>" +
      "<p><span class='lsu-k'>confidence</span> " + escapeHtml(String(scene.confidence != null ? scene.confidence : "—")) + "</p>" +
      (runner.value ? "<p><span class='lsu-k'>" + escapeHtml(c.runnerHintLabel || "Runner hint") + "</span> " + escapeHtml(runner.value) + " <span class='lsu-tag'>runner hint as evidence</span></p>" : "") +
      "<p><span class='lsu-k'>" + escapeHtml(c.resolutionLabel || "Resolution") + "</span> " + escapeHtml(resolution) + "</p>" +
      "<p class='lsu-muted'>task clues: " + tasks + " · likely needed: " + likely + " · conflict: " + (hasConflict ? "yes" : "no") + "</p>" +
      "<p class='lsu-status'>" + renderBadges(pkg.badges) + " · <span class='lsu-tag'>no_runner_invocation</span> · <span class='lsu-tag'>no_fact_write</span></p>" +
      "</div>"
    );
  }

  function renderSurvival(survival) {
    if (!survival) return "";
    var fields = ["environment_type", "risk_level", "mobility_relevance", "information_relevance", "social_relevance", "task_pressure", "uncertainty_level"];
    var lines = fields.map(function (f) {
      return "<p><span class='lsu-k'>" + escapeHtml(f) + "</span> " + escapeHtml(safeText(survival[f])) + "</p>";
    }).join("");
    return "<div class='lsu-block'><h4>" + escapeHtml(Copy().survivalTitle || "生存语境") + "</h4>" + lines + "</div>";
  }

  function renderTaskClues(clues) {
    if (!clues || !clues.length) return "";
    var items = clues.map(function (tc) {
      return "<li class='lsu-item'><span class='lsu-k'>" + escapeHtml(tc.task_type) + " " + escapeHtml(tc.priority || "") + "</span><br>" +
        escapeHtml(safeText(tc.reason)) + " <span class='lsu-tag'>candidate_only</span> · <span class='lsu-tag'>not_fact</span></li>";
    }).join("");
    return "<div class='lsu-block'><h4>" + escapeHtml(Copy().taskCluesTitle || "任务线索") + "</h4><ul class='lsu-list'>" + items + "</ul></div>";
  }

  function renderMissing(missing) {
    if (!missing || !missing.length) return "";
    var items = missing.map(function (m) {
      return "<li class='lsu-item'><span class='lsu-k'>" + escapeHtml(m.info_type) + "</span> → " +
        escapeHtml(safeText(m.suggested_capability)) + "<br>" + escapeHtml(safeText(m.reason)) + "</li>";
    }).join("");
    return "<div class='lsu-block'><h4>" + escapeHtml(Copy().missingInfoTitle || "缺失信息") + "</h4><ul class='lsu-list'>" + items + "</ul></div>";
  }

  function renderAttention(hints, options) {
    if (!hints || !hints.length) return "";
    var items = hints.map(function (h) {
      var cls = "lsu-item lsu-attn-item";
      if (h.region_ref_optional) cls += " lsu-attn-selectable";
      return "<li class='" + cls + "' data-lsu-target='" + escapeHtml(h.target_hint_id) + "' " +
        "data-lsu-region-ref='" + escapeHtml(h.region_ref_optional || "") + "'>" +
        "<span class='lsu-k'>" + escapeHtml(h.target_type) + " " + escapeHtml(h.priority || "") + "</span><br>" +
        escapeHtml(safeText(h.reason)) + "</li>";
    }).join("");
    return "<div class='lsu-block'><h4>" + escapeHtml(Copy().attentionTitle || "关注目标提示") + "</h4><ul class='lsu-list'>" + items + "</ul></div>";
  }

  function renderModelBucket(title, items) {
    if (!items || !items.length) return "<p class='lsu-muted lsu-empty'>—</p>";
    return "<ul class='lsu-list'>" + items.map(function (h) {
      return "<li class='lsu-item'><span class='lsu-k'>" + escapeHtml(modelLabel(h.capability_type)) + "</span><br>" +
        escapeHtml(safeText(h.reason)) + (h.policy_ref ? "<br><span class='lsu-k'>policy_ref</span> " + escapeHtml(h.policy_ref) : "") + "</li>";
    }).join("") + "</ul>";
  }

  function renderModelNeeds(hints) {
    hints = hints || {};
    var c = Copy();
    return (
      "<div class='lsu-block lsu-model-needs'>" +
      "<h4>" + escapeHtml(c.modelNeedTitle || "能力需求提示") + "</h4>" +
      "<div class='lsu-model-col'><h5>" + escapeHtml(c.likelyNeededTitle || "Likely Needed") + "</h5>" + renderModelBucket("", hints.likely_needed) + "</div>" +
      "<div class='lsu-model-col'><h5>" + escapeHtml(c.optionalTitle || "Optional") + "</h5>" + renderModelBucket("", hints.optional) + "</div>" +
      "<div class='lsu-model-col lsu-noop-col'><h5>" + escapeHtml(c.notNeededTitle || "Not Needed") + "</h5>" + renderModelBucket("", hints.not_needed) + "</div>" +
      "<p class='lsu-muted'>" + escapeHtml(c.notExecuted || "未触发工具执行") + "</p>" +
      "</div>"
    );
  }

  function renderUncertainty(u) {
    if (!u) return "";
    return (
      "<div class='lsu-block lsu-uncertainty'>" +
      "<p><span class='lsu-k'>needs_manual_review</span> " + escapeHtml(String(!!u.needs_manual_review)) + "</p>" +
      (u.fallback_suggestion ? "<p><span class='lsu-k'>fallback</span> " + escapeHtml(safeText(u.fallback_suggestion)) + "</p>" : "") +
      "</div>"
    );
  }

  function render(host, pkg, options) {
    options = options || {};
    if (!host) return;
    if (!pkg) {
      host.innerHTML = "<div class='lsu-panel'><p class='muted'>" + escapeHtml(Copy().emptyHint || "") + "</p></div>";
      host.hidden = false;
      return;
    }
    host.hidden = false;
    var traceHostId = "lsu-trace-host-" + Math.random().toString(36).slice(2, 8);
    host.innerHTML =
      "<div class='lsu-panel'>" +
      "<h3 class='lsu-heading'>" + escapeHtml(Copy().sectionTitle || "处境理解") + "</h3>" +
      "<p class='lsu-sub'>" + escapeHtml(Copy().sectionSubtitle || "") + "</p>" +
      renderSummaryCard(pkg) +
      renderSurvival(pkg.survival_context) +
      renderTaskClues(pkg.task_clue_candidates) +
      renderMissing(pkg.missing_information_candidates) +
      renderAttention(pkg.attention_target_hints, options) +
      renderModelNeeds(pkg.model_need_hints) +
      renderUncertainty(pkg.uncertainty) +
      "<div id='" + traceHostId + "'></div>" +
      "</div>";
    var traceHost = host.querySelector("#" + traceHostId);
    if (traceHost && global.LunaSituationUnderstandingTraceView) {
      global.LunaSituationUnderstandingTraceView.render(traceHost, pkg, options);
    }
    host.querySelectorAll(".lsu-attn-selectable").forEach(function (el) {
      el.addEventListener("click", function () {
        var regionRef = el.getAttribute("data-lsu-region-ref");
        if (regionRef && options.onSelectAttentionHint) options.onSelectAttentionHint(regionRef);
      });
    });
  }

  global.LunaSituationUnderstandingPanel = {
    version: "luna_situation_understanding_panel_v1",
    render: render
  };
})(typeof window !== "undefined" ? window : this);
