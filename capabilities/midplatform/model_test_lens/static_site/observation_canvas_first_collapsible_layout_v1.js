/**
 * Observation Canvas-First Collapsible Layout V1 — main canvas priority orchestrator.
 */
(function (global) {
  "use strict";

  var LAYOUT_CLASS = "lol-layout-canvas-first";

  function apply(rootEl) {
    var root = rootEl || document.getElementById("lol-app");
    if (root) root.classList.add("lol-canvas-first-root");
    document.body.classList.add(LAYOUT_CLASS);
    setLeftExpanded(false);
    if (global.LunaBottomDrawerStateGuard) {
      var dock = document.getElementById("lol-bottom-dock");
      global.LunaBottomDrawerStateGuard.ensureCollapsed(dock);
    }
    return { root: root };
  }

  function setLeftExpanded(expanded) {
    document.body.classList.toggle("lol-left-expanded", !!expanded);
    document.body.classList.toggle("lol-left-collapsed", !expanded);
  }

  function isLeftExpanded() {
    return document.body.classList.contains("lol-left-expanded");
  }

  global.ObservationCanvasFirstLayout = {
    version: "observation_canvas_first_collapsible_layout_v1",
    LAYOUT_CLASS: LAYOUT_CLASS,
    apply: apply,
    setLeftExpanded: setLeftExpanded,
    isLeftExpanded: isLeftExpanded
  };
})(typeof window !== "undefined" ? window : this);
