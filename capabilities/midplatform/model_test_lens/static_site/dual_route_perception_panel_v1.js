/**
 * Dual route perception — right panel (Route A / Route B / comparison candidates).
 * No runner execution · candidate_only · not_fact · no boundary clone on main canvas.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.DualRoutePerceptionCopy || {}; };
  var FORBIDDEN_PARTS = ["OCR结果", "导航到"];
  var FORBIDDEN_LABEL_PARTS = ["这是", "确认"];

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function safeText(text) {
    var s = String(text || "");
    for (var i = 0; i < FORBIDDEN_PARTS.length; i++) {
      if (s.indexOf(FORBIDDEN_PARTS[i]) >= 0) return "[文案违规已屏蔽]";
    }
    if (FORBIDDEN_LABEL_PARTS[0] && s.indexOf(FORBIDDEN_LABEL_PARTS[0]) >= 0 &&
        s.indexOf("路牌") >= 0) return "[文案违规已屏蔽]";
    return s || "—";
  }

  function renderGroundingItem(g) {
    if (!g) return "";
    var bbox = g.bbox || {};
    return (
      "<li class='drp-item'>" +
      "<span class='drp-k'>label candidate</span> " + escapeHtml(safeText(g.detected_label_candidate)) +
      " · <span class='drp-k'>confidence</span> " + escapeHtml(String(g.confidence)) +
      "<br><span class='drp-k'>bbox candidate</span> [" +
      escapeHtml([bbox.x1, bbox.y1, bbox.x2, bbox.y2].join(", ")) + "]" +
      " · <span class='drp-tag'>not_fact</span></li>"
    );
  }

  function renderMaskItem(m) {
    if (!m) return "";
    return (
      "<li class='drp-item'>" +
      "<span class='drp-k'>mask candidate</span> " + escapeHtml(safeText(m.mask_candidate_ref)) +
      " · <span class='drp-k'>refine</span> " + escapeHtml(safeText(m.refine_method)) +
      " · <span class='drp-tag'>not_fact</span></li>"
    );
  }

  function renderRouteA(routeA) {
    var c = Copy();
    var grounding = (routeA && routeA.grounding_detection_candidates) || [];
    var masks = (routeA && routeA.sam_refine_mask_candidates) || [];
    if (!grounding.length && !masks.length) {
      return "<p class='muted drp-empty'>Route A miss（无 grounding candidate）</p>";
    }
    return (
      "<div class='drp-block'>" +
      "<h4>" + escapeHtml(c.routeATitle || "Route A") + "</h4>" +
      "<ul class='drp-list'>" + grounding.map(renderGroundingItem).join("") + "</ul>" +
      (masks.length ? "<ul class='drp-list drp-sub'>" + masks.map(renderMaskItem).join("") + "</ul>" : "") +
      "<p class='drp-status'><span class='drp-tag'>candidate_only</span> · <span class='drp-tag'>not_fact</span></p>" +
      "</div>"
    );
  }

  function renderRouteB(routeB) {
    var c = Copy();
    var vlm = routeB && routeB.vlm_route_candidate;
    if (!vlm) return "<p class='muted drp-empty'>Route B 无候选</p>";
    var regions = (vlm.suggested_attention_regions || []).map(function (r) {
      return (
        "<li class='drp-item'>" + escapeHtml(safeText(r.region_description_candidate)) +
        " · <span class='drp-k'>" + escapeHtml(safeText(r.attention_reason_candidate)) + "</span></li>"
      );
    }).join("");
    return (
      "<div class='drp-block'>" +
      "<h4>" + escapeHtml(c.routeBTitle || "Route B") + "</h4>" +
      "<p><span class='drp-k'>scene candidate</span> " + escapeHtml(safeText(vlm.scene_profile_candidate)) + "</p>" +
      "<ul class='drp-list'>" + regions + "</ul>" +
      "<p><span class='drp-k'>followup</span> " +
      escapeHtml((vlm.suggested_followup_models || []).join(" / ")) + "</p>" +
      "<p><span class='drp-k'>uncertainty</span> " + escapeHtml(String(vlm.uncertainty)) + "</p>" +
      "<p class='muted'>" + escapeHtml(safeText(vlm.reasoning_summary)) + "</p>" +
      "<p class='drp-status'><span class='drp-tag'>candidate_only</span> · <span class='drp-tag'>not_fact</span></p>" +
      "</div>"
    );
  }

  function renderComparison(cmp) {
    var c = Copy();
    if (!cmp) return "";
    return (
      "<div class='drp-block drp-comparison'>" +
      "<h4>" + escapeHtml(c.comparisonTitle || "中台对照") + "</h4>" +
      "<p><span class='drp-k'>agreement</span> " + escapeHtml(safeText(cmp.agreement_level)) +
      (cmp.conflict_type && cmp.conflict_type !== "none"
        ? " · <span class='drp-k'>conflict</span> " + escapeHtml(safeText(cmp.conflict_type)) : "") +
      "</p>" +
      "<p><span class='drp-k'>recommended next task</span> " +
      escapeHtml(safeText(cmp.recommended_followup_route)) + "</p>" +
      "<p><span class='drp-k'>admission suggestion</span> " +
      escapeHtml(safeText(cmp.recommended_admission_mode || cmp.priority_signal)) + "</p>" +
      "<p class='drp-status'><span class='drp-tag'>candidate_only</span> · <span class='drp-tag'>not_fact</span></p>" +
      "</div>"
    );
  }

  function render(host, dualRoutePkg, options) {
    if (!host) return;
    options = options || {};
    var c = Copy();
    if (!dualRoutePkg) {
      host.innerHTML = (
        "<section class='drp-panel drp-panel-empty'>" +
        "<h3 class='drp-heading'>" + escapeHtml(c.sectionTitle || "路线对照候选") + "</h3>" +
        "<p class='muted'>" + escapeHtml(c.emptyHint || "") + "</p></section>"
      );
      host.hidden = false;
      return;
    }
    host.innerHTML = (
      "<section class='drp-panel'>" +
      "<h3 class='drp-heading'>" + escapeHtml(c.sectionTitle || "路线对照候选") + "</h3>" +
      renderRouteA(dualRoutePkg.route_a) +
      renderRouteB(dualRoutePkg.route_b) +
      renderComparison(dualRoutePkg.dual_route_comparison_candidate) +
      "<p class='drp-trace muted'>" + escapeHtml(c.traceHint || "") + "</p>" +
      "</section>"
    );
    host.hidden = false;
  }

  global.DualRoutePerceptionPanel = {
    version: "dual_route_perception_panel_v1",
    no_ocr_execution: true,
    no_detection_execution: true,
    no_vlm_execution: true,
    no_fact_write: true,
    segmentationSoleBoundaryOwner: true,
    no_boundary_clone: true,
    render: render
  };
})(typeof window !== "undefined" ? window : this);
