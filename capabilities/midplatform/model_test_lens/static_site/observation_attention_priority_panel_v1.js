/**
 * Observation Attention Layer V1 — priority panel (Visual Expression System: scheduling primary expression).
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.ObservationAttentionCopy || {}; };

  var PRIORITY_ORDER = {
    P0_immediate_attention: 0,
    P1_high_attention: 1,
    P2_medium_attention: 2,
    P3_low_attention: 3,
    ignore_for_now: 9
  };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function entityGlyph(options, regionId) {
    if (!options || !options.getEntityGlyph) return "";
    return options.getEntityGlyph(regionId) || "";
  }

  function panelRecords(attentionPkg) {
    if (!attentionPkg || !attentionPkg.records || !attentionPkg.records.length) return [];
    return attentionPkg.records.filter(function (rec) {
      return rec.priority_level !== "ignore_for_now";
    }).slice().sort(function (a, b) {
      var pa = PRIORITY_ORDER[a.priority_level] != null ? PRIORITY_ORDER[a.priority_level] : 9;
      var pb = PRIORITY_ORDER[b.priority_level] != null ? PRIORITY_ORDER[b.priority_level] : 9;
      return pa - pb;
    });
  }

  function normalizePanelTitleName(raw) {
    var name = String(raw || "区域").replace(/候选$/g, "").trim();
    if (!name) name = "区域";
    if (/区域$/.test(name)) return name + "候选";
    return name + "候选";
  }

  function recordHeadline(rec, glyph, pri, options) {
    var short = options.getEntityShortLabel ? options.getEntityShortLabel(rec.region_id) : null;
    var name = normalizePanelTitleName(short || rec.region_display_name || rec.region_id);
    return (glyph ? glyph + " " : "") + pri + " " + name;
  }

  function renderRecordItem(rec, options, c) {
    var pri = (c.priorityLevel || {})[rec.priority_level] || rec.priority_level;
    var motion = (c.motionState || {})[rec.motion_state_candidate] || rec.motion_state_candidate;
    var follow = (rec.recommended_followup_model || []).slice(0, 4).map(function (m) {
      return (c.followupModel || {})[m] || m;
    }).join(" / ");
    var glyph = entityGlyph(options, rec.region_id);
    var selectedId = options.selectedRegionId || null;
    var active = selectedId === rec.region_id ? " oa-priority-item-active" : "";
    var boost = rec._correction_boosted
      ? " <span class='oa-badge oa-badge-hc'>" + escapeHtml(c.correctionBoosted || "指错加权") + "</span>"
      : "";
    var headline = recordHeadline(rec, glyph, pri, options);

    return (
      "<li class='oa-priority-item" + active + "' data-region-id='" + escapeHtml(rec.region_id) + "' " +
      "role='button' tabindex='0' aria-label='优先观察 " + escapeHtml(rec.region_display_name) + "'>" +
      "<div class='oa-priority-head'>" +
      "<strong>" + escapeHtml(headline) + "</strong>" + boost +
      "</div>" +
      "<p class='oa-priority-type'>" + escapeHtml(c.fieldType || "类型") + "：" + escapeHtml(motion) + "</p>" +
      "<p class='oa-priority-why'>" + escapeHtml(c.whyObserve || "为什么优先") + "：" +
      escapeHtml(rec.attention_summary || rec.priority_reason || "—") + "</p>" +
      "<p class='oa-priority-next'>" + escapeHtml(c.nextModel || "建议补测") + "：" + escapeHtml(follow || "—") + "</p>" +
      "<p class='oa-priority-status'>" + escapeHtml(c.statusLine || "状态：candidate_only / not_fact") + "</p>" +
      "</li>"
    );
  }

  function render(host, attentionPkg, options) {
    options = options || {};
    if (!host) return;
    var c = Copy();
    var records = panelRecords(attentionPkg);
    if (!records.length) {
      host.innerHTML = "";
      host.hidden = true;
      return;
    }
    host.hidden = false;

    var noAttentionHtml = "";
    if (options.noAttentionRegionId) {
      noAttentionHtml =
        "<div class='oa-no-attention-notice' role='status'>" +
        escapeHtml(c.noAttentionRecord || "该区域暂无优先观察建议") +
        "</div>";
    }

    var items = records.map(function (rec) {
      return renderRecordItem(rec, options, c);
    }).join("");

    host.innerHTML =
      "<section class='oa-priority-panel'>" +
      "<h3 class='oa-priority-title'>" + escapeHtml(c.panelTitle || "优先观察") + "</h3>" +
      "<p class='oa-candidate-notice muted'>" + escapeHtml(c.candidateNotice || "") + "</p>" +
      "<p class='oa-panel-hint muted'>" + escapeHtml(c.panelHint || "观察调度主入口：点击下方条目高亮主图分割区域。") + "</p>" +
      (attentionPkg.video_or_single_frame_context === "single_frame"
        ? "<p class='oa-single-frame muted'>" + escapeHtml(c.singleFrameLimit || "") + "</p>" : "") +
      noAttentionHtml +
      "<ol class='oa-priority-list'>" + items + "</ol></section>";

    var onSelect = options.onSelectRegion || function () {};
    var onHover = options.onHoverRegion || function () {};
    host.querySelectorAll(".oa-priority-item").forEach(function (li) {
      var id = li.dataset.regionId;
      li.addEventListener("click", function () { onSelect(id); });
      li.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter" || ev.key === " ") {
          ev.preventDefault();
          onSelect(id);
        }
      });
      li.addEventListener("mouseenter", function () { onHover(id); });
      li.addEventListener("mouseleave", function () { onHover(null); });
    });
  }

  function scrollToRegion(host, regionId) {
    if (!host || !regionId) return;
    var item = host.querySelector("[data-region-id='" + regionId + "']");
    if (!item) return;
    host.querySelectorAll(".oa-priority-item-active").forEach(function (el) {
      el.classList.remove("oa-priority-item-active");
    });
    item.classList.add("oa-priority-item-active");
    item.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  global.ObservationAttentionPriorityPanel = {
    version: "observation_attention_priority_panel_v3_visual_expression_post_review",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Visual-Expression-System-UI-Execution-Post-Review-And-Minor-Fix-v1-001",
    panelContainsFullAttentionExplanation: true,
    panelCopyNoDuplicateCandidateSuffix: true,
    render: render,
    scrollToRegion: scrollToRegion,
    panelRecords: panelRecords,
    normalizePanelTitleName: normalizePanelTitleName
  };
})(typeof window !== "undefined" ? window : this);
