/**
 * Model Test Lens — Visual Overlay controls v1.
 */
(function (global) {
  "use strict";

  function createOverlayControls(root, state, onChange) {
    root.innerHTML =
      "<div class='vov-controls'>" +
      "<label class='vov-check'><input type='checkbox' id='vov-show-layers' checked /> 显示识别层</label>" +
      "<label class='vov-check'><input type='checkbox' id='vov-show-labels' checked /> 显示标签</label>" +
      "<label class='vov-opacity'>透明度 " +
      "<input type='range' id='vov-opacity' min='0' max='100' value='45' /></label>" +
      "<label>视图模式<select id='vov-mode'>" +
      "<option value='compare'>对比视图</option>" +
      "<option value='overlay'>识别叠加</option>" +
      "<option value='original'>只看原图</option>" +
      "<option value='mask_only'>仅识别层</option>" +
      "</select></label>" +
      "</div>" +
      "<div id='vov-layer-toggles' class='vov-layer-toggles'></div>" +
      "<p class='vov-boundary muted'>测试结果，仅供模型评估，不作为事实结果。</p>";

    var showLayers = root.querySelector("#vov-show-layers");
    var showLabels = root.querySelector("#vov-show-labels");
    var opacity = root.querySelector("#vov-opacity");
    var mode = root.querySelector("#vov-mode");
    var layerHost = root.querySelector("#vov-layer-toggles");

    function sync() {
      state.showLayers = showLayers.checked;
      state.showLabels = showLabels.checked;
      state.opacity = parseInt(opacity.value, 10) / 100;
      state.mode = mode.value;
      onChange(state);
    }

    showLayers.addEventListener("change", sync);
    showLabels.addEventListener("change", sync);
    opacity.addEventListener("input", sync);
    mode.addEventListener("change", sync);

    function renderLayerToggles(layers) {
      layerHost.innerHTML = "<span class='vov-layer-title'>识别区域：</span>";
      (layers || []).forEach(function (layer, i) {
        var id = "vov-layer-" + i;
        var label = document.createElement("label");
        label.className = "vov-layer-chip";
        label.innerHTML =
          "<input type='checkbox' id='" + id + "' " + (layer.visible !== false ? "checked" : "") + " />" +
          "<span style='border-left:3px solid " + (layer.outline_color || "#fff") + ";padding-left:6px'>" +
          layer.label + "</span>";
        label.querySelector("input").addEventListener("change", function (ev) {
          layer.visible = ev.target.checked;
          onChange(state);
        });
        layerHost.appendChild(label);
      });
    }

    return { renderLayerToggles: renderLayerToggles, sync: sync };
  }

  global.VisualOverlayControls = { create: createOverlayControls };
})(typeof window !== "undefined" ? window : this);
