/**
 * Model Test Lens — Perception HUD controls v1 (HUD Visual Policy + readability filters).
 */
(function (global) {
  "use strict";

  var Policy = global.HudVisualPolicy;
  var LabelPolicy = global.HudLabelLayoutPolicy;
  var RouteFilter = global.OverlayRouteFilter;
  var AttentionEngine = global.ObservationAttentionEngine;
  var I18n = global.LunaObservationLabelI18n;

  function createHUDControls(root, state, onChange, options) {
    options = options || {};
    var debugMode = !!options.debugMode;
    var compact = !!options.compact;

    root.innerHTML =
      "<div class='phud-controls'>" +
      "<label class='phud-check'><input type='checkbox' id='phud-show-box' checked /> 显示识别框</label>" +
      "<label class='phud-check'><input type='checkbox' id='phud-show-labels' checked /> 显示观察浮标</label>" +
      (compact ? (
        "<label class='phud-check'><input type='checkbox' id='phud-show-all-markers' /> 显示全部候选浮标</label>" +
        "<span class='phud-route-sep muted' aria-hidden='true'>|</span>" +
        "<label class='phud-check phud-route-check'><input type='checkbox' id='phud-route-ocr' /> 仅 OCR 候选框</label>" +
        "<label class='phud-check phud-route-check'><input type='checkbox' id='phud-route-slam' /> 仅 SLAM 候选框</label>"
      ) : (
        "<label class='phud-check'><input type='checkbox' id='phud-show-uncertainty' checked /> 显示不确定提示</label>" +
        "<label class='phud-check'><input type='checkbox' id='phud-show-fill' /> 显示区域填充</label>"
      )) +
      "<span class='phud-color-rule muted'>浮标格式：编号 + 优先级 + 区域名（默认仅 P0/P1）</span>" +
      (compact ? "" : (
        "<label class='phud-opacity' id='phud-opacity-wrap' hidden>区域填充透明度 " +
        "<input type='range' id='phud-opacity' min='10' max='80' value='35' /></label>"
      )) +
      "</div>" +
      (compact ? "" : (
        "<div class='phud-filter-bar' id='phud-filter-bar'>" +
        "<span class='phud-layer-title'>筛选：</span>" +
        "<button type='button' class='phud-filter-btn active' data-filter='all'>全部</button>" +
        "<button type='button' class='phud-filter-btn' data-filter='task'>任务相关</button>" +
        "<button type='button' class='phud-filter-btn' data-filter='risk'>风险</button>" +
        "<button type='button' class='phud-filter-btn' data-filter='uncertain'>不确定</button>" +
        "</div>" +
        "<div id='phud-layer-toggles' class='phud-layer-toggles'></div>"
      ));

    var showBox = root.querySelector("#phud-show-box");
    var showLabels = root.querySelector("#phud-show-labels");
    var showAllMarkers = root.querySelector("#phud-show-all-markers");
    var routeOcr = root.querySelector("#phud-route-ocr");
    var routeSlam = root.querySelector("#phud-route-slam");
    var showUncertainty = root.querySelector("#phud-show-uncertainty");
    var showFill = root.querySelector("#phud-show-fill");
    var opacityWrap = root.querySelector("#phud-opacity-wrap");
    var opacity = root.querySelector("#phud-opacity");
    var layerHost = root.querySelector("#phud-layer-toggles");
    var filterBtns = root.querySelectorAll(".phud-filter-btn");

    if (Policy && Policy.createDefaultState) {
      var defaults = Policy.createDefaultState();
      Object.keys(defaults).forEach(function (k) {
        if (state[k] === undefined) state[k] = defaults[k];
      });
    }
    if (state.entityFilter == null) state.entityFilter = "all";
    if (state.routeFilter == null) state.routeFilter = "all";
    state.showAllAttentionMarkers = state.showAllAttentionMarkers === true;

    showBox.checked = state.showLineBox !== false;
    showLabels.checked = state.showLabels !== false;
    if (showAllMarkers) showAllMarkers.checked = state.showAllAttentionMarkers === true;
    if (routeOcr) routeOcr.checked = state.routeFilter === "ocr";
    if (routeSlam) routeSlam.checked = state.routeFilter === "slam";
    if (showUncertainty) showUncertainty.checked = state.showUncertainty !== false;
    if (showFill) showFill.checked = !!state.showMaskFill;
    if (opacity) opacity.value = Math.round((state.maskFillOpacity || 0.35) * 100);
    if (opacityWrap) opacityWrap.hidden = !showFill || !showFill.checked;

    if (filterBtns.length) {
      filterBtns.forEach(function (btn) {
        btn.classList.toggle("active", btn.dataset.filter === state.entityFilter);
        btn.addEventListener("click", function () {
          state.entityFilter = btn.dataset.filter;
          filterBtns.forEach(function (b) {
            b.classList.toggle("active", b.dataset.filter === state.entityFilter);
          });
          onChange(state);
        });
      });
    }

    function syncRouteFilter(fromOcr, fromSlam) {
      if (!routeOcr && !routeSlam) return;
      if (fromOcr === "ocr" && routeOcr && routeOcr.checked) {
        if (routeSlam) routeSlam.checked = false;
        state.routeFilter = "ocr";
        return;
      }
      if (fromSlam === "slam" && routeSlam && routeSlam.checked) {
        if (routeOcr) routeOcr.checked = false;
        state.routeFilter = "slam";
        return;
      }
      state.routeFilter = "all";
    }

    function sync() {
      state.showLineBox = showBox.checked;
      state.showLabels = showLabels.checked;
      state.showAttentionMarkers = showLabels.checked;
      if (showAllMarkers) state.showAllAttentionMarkers = showAllMarkers.checked === true;
      if (routeOcr || routeSlam) {
        if (routeOcr && routeOcr.checked) syncRouteFilter("ocr");
        else if (routeSlam && routeSlam.checked) syncRouteFilter("slam");
        else state.routeFilter = "all";
      }
      if (showUncertainty) state.showUncertainty = showUncertainty.checked;
      if (showFill) state.showMaskFill = showFill.checked;
      if (opacity) state.maskFillOpacity = parseInt(opacity.value, 10) / 100;
      if (opacityWrap && showFill) opacityWrap.hidden = !showFill.checked;
      onChange(state);
    }

    showBox.addEventListener("change", sync);
    showLabels.addEventListener("change", sync);
    if (showAllMarkers) showAllMarkers.addEventListener("change", sync);
    if (routeOcr) {
      routeOcr.addEventListener("change", function () {
        if (routeOcr.checked && routeSlam) routeSlam.checked = false;
        sync();
      });
    }
    if (routeSlam) {
      routeSlam.addEventListener("change", function () {
        if (routeSlam.checked && routeOcr) routeOcr.checked = false;
        sync();
      });
    }
    if (showUncertainty) showUncertainty.addEventListener("change", sync);
    if (showFill) showFill.addEventListener("change", sync);
    if (opacity) opacity.addEventListener("input", sync);

    function displayLayerLabel(entity, layer) {
      if (entity && entity.hud_number_glyph && entity.hud_short_label) {
        return entity.hud_number_glyph + " " + entity.hud_short_label;
      }
      var raw = layer.label || "区域";
      if (I18n && I18n.mobileSamLabel) return I18n.mobileSamLabel(raw);
      return raw;
    }

    function renderLayerToggles(entities, layers) {
      if (!layerHost) return;
      layerHost.innerHTML = "<span class='phud-layer-title'>候选区域：</span>";
      (layers || []).forEach(function (layer, i) {
        var entity = entities[i];
        if (entity && entity._hidden) layer.visible = false;
        var id = "phud-layer-" + i;
        var semColor = (entity && entity.hud_stroke) || "#4d9fff";
        var label = document.createElement("label");
        label.className = "phud-layer-chip";
        label.innerHTML =
          "<input type='checkbox' id='" + id + "' " + (layer.visible !== false ? "checked" : "") + " />" +
          "<span style='border-left:3px solid " + semColor + ";padding-left:6px'>" +
          displayLayerLabel(entity, layer) + "</span>";
        label.querySelector("input").addEventListener("change", function (ev) {
          layer.visible = ev.target.checked;
          if (entities[i]) entities[i]._hidden = !ev.target.checked;
          onChange(state);
        });
        layerHost.appendChild(label);
      });
      if (debugMode) {
        var dbg = document.createElement("details");
        dbg.className = "phud-debug-prompt";
        dbg.innerHTML = "<summary>原始提示名称（开发者）</summary><ul class='phud-raw-prompt-list'></ul>";
        var ul = dbg.querySelector("ul");
        (layers || []).forEach(function (layer) {
          var li = document.createElement("li");
          li.textContent = layer.label || "—";
          ul.appendChild(li);
        });
        layerHost.appendChild(dbg);
      }
    }

    function attentionRecordFor(entity) {
      if (!entity || !state.attentionPkg || !AttentionEngine) return null;
      return AttentionEngine.lookupRecord(state.attentionPkg, entity.entity_id);
    }

    function entityPassesFilter(entity) {
      if (!entity || entity._hidden) return false;
      if (state.routeFilter && state.routeFilter !== "all" && RouteFilter) {
        if (!RouteFilter.passesRouteFilter(entity, attentionRecordFor(entity), state.routeFilter)) {
          return false;
        }
      }
      if (!LabelPolicy) return true;
      return LabelPolicy.matchesFilter(entity, state.entityFilter);
    }

    return {
      renderLayerToggles: renderLayerToggles,
      sync: sync,
      entityPassesFilter: entityPassesFilter,
      bindAttentionPkg: function (pkg) {
        state.attentionPkg = pkg || null;
      }
    };
  }

  global.PerceptionHUDControls = { create: createHUDControls };
})(typeof window !== "undefined" ? window : this);
