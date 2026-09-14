/**
 * HUD Object Chip Bar V1 — horizontal object summary chips.
 */
(function (global) {
  "use strict";

  var LabelPolicy = function () { return global.HudLabelLayoutPolicy; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function formatChip(entity) {
    var P = LabelPolicy();
    if (!P) return { text: entity.display_name || "对象", stroke: "#4d9fff" };
    var label = P.formatInImageLabel(entity);
    return {
      text: label.glyph + " " + label.shortName + (label.percent ? " " + label.percent : ""),
      badgeHtml: "",
      stroke: entity.hud_stroke || "#8b9cb3",
      entity_id: entity.entity_id
    };
  }

  function render(host, entities, options) {
    options = options || {};
    var onSelect = options.onSelect || function () {};
    var onHover = options.onHover || function () {};
    var onCorrect = options.onCorrect || null;
    var selectedId = options.selectedEntityId || null;
    var attentionPkg = options.attentionPkg || null;
    var visible = (entities || []).filter(function (e) { return !e._hidden; });
    if (attentionPkg && attentionPkg.sorted_entities) {
      visible = attentionPkg.sorted_entities.filter(function (e) { return !e._hidden; });
    }

    if (!visible.length) {
      host.innerHTML = "<div class='hud-chip-bar hud-chip-bar-empty'><span class='muted'>识别对象：等待观察结果…</span></div>";
      return { update: function () { render(host, entities, options); } };
    }

    var chips = visible.map(function (e) {
      var chip = formatChip(e, attentionPkg);
      var active = selectedId === chip.entity_id ? " hud-chip-active" : "";
      var correctBtn = onCorrect
        ? "<button type='button' class='hud-chip-correct' data-correct-id='" + escapeHtml(chip.entity_id) +
          "' title='指错' aria-label='指错'>指错</button>"
        : "";
      return (
        "<span class='hud-chip-wrap'>" +
        "<button type='button' class='hud-chip" + active + "' data-entity-id='" + escapeHtml(chip.entity_id) + "' " +
        "style='--chip-color:" + escapeHtml(chip.stroke) + "'>" +
        escapeHtml(chip.text) + (chip.badgeHtml || "") + "</button>" + correctBtn + "</span>"
      );
    }).join("");

    host.innerHTML =
      "<div class='hud-chip-bar'>" +
      "<span class='hud-chip-label'>识别对象：</span>" +
      "<div class='hud-chip-scroll'>" + chips + "</div></div>";

    host.querySelectorAll(".hud-chip").forEach(function (btn) {
      var id = btn.dataset.entityId;
      btn.addEventListener("click", function () { onSelect(id); });
      btn.addEventListener("mouseenter", function () { onHover(id); });
      btn.addEventListener("mouseleave", function () { onHover(null); });
    });

    host.querySelectorAll(".hud-chip-correct").forEach(function (btn) {
      btn.addEventListener("click", function (ev) {
        ev.stopPropagation();
        if (onCorrect) onCorrect(btn.dataset.correctId);
      });
    });

    return {
      update: function (next) {
        render(host, entities, Object.assign({}, options, next || {}));
      }
    };
  }

  global.HudObjectChipBar = {
    version: "hud_object_chip_bar_v1",
    formatChip: formatChip,
    render: render
  };
})(typeof window !== "undefined" ? window : this);
