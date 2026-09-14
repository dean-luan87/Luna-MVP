/**
 * HUD External Annotation Panel V1 — object details outside the image.
 */
(function (global) {
  "use strict";

  var Policy = function () { return global.HudLabelLayoutPolicy; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function render(host, entities, options) {
    options = options || {};
    var onSelect = options.onSelect || function () {};
    var onHover = options.onHover || function () {};
    var onToggleHidden = options.onToggleHidden || function () {};
    var filterId = options.filterId || "all";
    var selectedId = options.selectedEntityId || null;
    var hoverId = options.hoverEntityId || null;

    var P = Policy();
    if (!P) {
      host.innerHTML = "<p class='muted'>识别对象面板未加载。</p>";
      return null;
    }

    var details = (entities || [])
      .map(function (e, i) { return P.buildExternalDetail(e, i); })
      .filter(function (d) { return !d.hidden; })
      .filter(function (d) {
        var entity = entities.find(function (e) { return e.entity_id === d.entity_id; });
        return entity ? P.matchesFilter(entity, filterId) : true;
      });

    if (!details.length) {
      host.innerHTML =
        "<section class='hud-ext-panel'>" +
        "<h3 class='hud-ext-title'>识别对象</h3>" +
        "<p class='muted hud-ext-empty'>当前筛选下没有可显示对象。</p></section>";
      return { update: function () { render(host, entities, options); } };
    }

    var itemsHtml = details.map(function (d) {
      var active = selectedId === d.entity_id ? " hud-ext-item-active" : "";
      var hover = hoverId === d.entity_id ? " hud-ext-item-hover" : "";
      return (
        "<article class='hud-ext-item" + active + hover + "' data-entity-id='" + escapeHtml(d.entity_id) + "' " +
        "style='--hud-item-color:" + escapeHtml(d.stroke) + "'>" +
        "<header class='hud-ext-item-head'>" +
        "<span class='hud-ext-num' style='color:" + escapeHtml(d.stroke) + "'>" + escapeHtml(d.number_glyph) + "</span>" +
        "<strong class='hud-ext-name'>" + escapeHtml(d.name) + "</strong>" +
        "<button type='button' class='hud-ext-hide-btn' data-hide-id='" + escapeHtml(d.entity_id) + "' title='隐藏此对象'>隐藏</button>" +
        "</header>" +
        "<dl class='hud-ext-meta'>" +
        "<div><dt>置信度</dt><dd>" + escapeHtml(d.confidence_text || "—") + "</dd></div>" +
        "<div><dt>状态</dt><dd>" + escapeHtml(d.status) + "</dd></div>" +
        "</dl>" +
        "<p class='hud-ext-explain'>" + escapeHtml(d.explanation) + "</p>" +
        "<p class='hud-ext-suggest'><span class='muted'>建议：</span>" + escapeHtml(d.suggestion) + "</p>" +
        "</article>"
      );
    }).join("");

    host.innerHTML =
      "<section class='hud-ext-panel'>" +
      "<h3 class='hud-ext-title'>识别对象</h3>" +
      "<div class='hud-ext-list'>" + itemsHtml + "</div>" +
      "</section>";

    host.querySelectorAll(".hud-ext-item").forEach(function (item) {
      var id = item.dataset.entityId;
      item.addEventListener("click", function (ev) {
        if (ev.target.closest(".hud-ext-hide-btn")) return;
        onSelect(id);
      });
      item.addEventListener("mouseenter", function () { onHover(id); });
      item.addEventListener("mouseleave", function () { onHover(null); });
    });

    host.querySelectorAll(".hud-ext-hide-btn").forEach(function (btn) {
      btn.addEventListener("click", function (ev) {
        ev.stopPropagation();
        onToggleHidden(btn.dataset.hideId);
      });
    });

    return {
      update: function (nextOptions) {
        render(host, entities, Object.assign({}, options, nextOptions || {}));
      }
    };
  }

  global.HudExternalAnnotationPanel = {
    version: "hud_external_annotation_panel_v1",
    render: render
  };
})(typeof window !== "undefined" ? window : this);
