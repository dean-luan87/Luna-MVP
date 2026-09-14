/**
 * Model Test Lens — Perception HUD Reasoning Panel v1 (result-first, compressed).
 */
(function (global) {
  "use strict";

  function renderReasoningPanel(host, panel, options) {
    options = options || {};
    if (global.HudReasoningCompression && global.HudReasoningCompression.renderCompressedPanel) {
      global.HudReasoningCompression.renderCompressedPanel(host, panel, options);
      return;
    }
    host.innerHTML = "<p class='muted'>观察面板模块未加载。</p>";
  }

  global.PerceptionHUDReasoningPanel = {
    render: renderReasoningPanel
  };
})(typeof window !== "undefined" ? window : this);
