/**
 * Luna Capability Grid Trigger V1 — 3×3 icon drawer toggle (not input-like).
 */
(function (global) {
  "use strict";

  var GRID_SVG =
    "<svg class='lol-cap-grid-icon' viewBox='0 0 24 24' width='20' height='20' aria-hidden='true'>" +
    "<circle cx='5' cy='5' r='1.75' fill='currentColor'/>" +
    "<circle cx='12' cy='5' r='1.75' fill='currentColor'/>" +
    "<circle cx='19' cy='5' r='1.75' fill='currentColor'/>" +
    "<circle cx='5' cy='12' r='1.75' fill='currentColor'/>" +
    "<circle cx='12' cy='12' r='1.75' fill='currentColor'/>" +
    "<circle cx='19' cy='12' r='1.75' fill='currentColor'/>" +
    "<circle cx='5' cy='19' r='1.75' fill='currentColor'/>" +
    "<circle cx='12' cy='19' r='1.75' fill='currentColor'/>" +
    "<circle cx='19' cy='19' r='1.75' fill='currentColor'/>" +
    "</svg>";

  function renderButton(options) {
    options = options || {};
    var expanded = !!options.expanded;
    var title = expanded ? "收起能力面板" : "展开能力面板";
    return (
      "<button type='button' class='lol-cap-grid-trigger" + (expanded ? " active" : "") + "' " +
      "id='lol-cap-grid-trigger' title='" + title + "' aria-label='" + title + "' " +
      "aria-expanded='" + (expanded ? "true" : "false") + "'>" +
      GRID_SVG +
      "</button>"
    );
  }

  function bind(button, onToggle) {
    if (!button) return;
    button.addEventListener("click", function (ev) {
      ev.preventDefault();
      if (onToggle) onToggle();
    });
  }

  global.LunaCapabilityGridTrigger = {
    version: "luna_capability_grid_trigger_v1",
    renderButton: renderButton,
    bind: bind,
    GRID_SVG: GRID_SVG
  };
})(typeof window !== "undefined" ? window : this);
