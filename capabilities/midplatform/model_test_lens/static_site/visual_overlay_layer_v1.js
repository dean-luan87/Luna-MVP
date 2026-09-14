/**
 * Model Test Lens — Visual Overlay layer orchestration v1.
 */
(function (global) {
  "use strict";

  var Ex = global.VisualOverlayExamples;
  var R = global.VisualOverlayRenderer;

  function renderOverlayView(host, envelope, options) {
    options = options || {};
    var debugMode = !!options.debugMode;
    host.innerHTML =
      "<section class='vol-section'>" +
      "<h3>原图识别视图</h3>" +
      "<div id='vol-controls-host'></div>" +
      "<div id='vol-warning' class='vol-warning' hidden></div>" +
      "<div class='vol-canvas-wrap'><canvas id='vol-canvas' class='vol-canvas'></canvas></div>" +
      "<div id='vol-detail' class='vol-detail muted'></div>" +
      (debugMode ? "<div id='vol-debug' class='vol-debug'></div>" : "") +
      "</section>";

    var sourceRef = Ex.pickSourceImageRef(envelope);
    var layers = Ex.buildOverlayLayers(envelope);
    var warningEl = host.querySelector("#vol-warning");
    var canvas = host.querySelector("#vol-canvas");
    var detailEl = host.querySelector("#vol-detail");

    if (!sourceRef) {
      warningEl.hidden = false;
      warningEl.textContent = "缺少原图，无法叠加识别层。";
      return { layers: layers, sourceRef: null };
    }
    if (!layers.length) {
      warningEl.hidden = false;
      warningEl.textContent = "模型结果中没有可显示的识别区域。";
      return { layers: layers, sourceRef: sourceRef };
    }

    var state = { showLayers: true, showLabels: true, opacity: 0.45, mode: "overlay", layers: layers };
    var controlsApi = global.VisualOverlayControls.create(
      host.querySelector("#vol-controls-host"),
      state,
      function () { redraw(); }
    );
    controlsApi.renderLayerToggles(layers);

    function redraw() {
      var url = Ex.artifactUrl(sourceRef);
      R.loadImage(url).then(function (img) {
        var renderMode = state.mode === "original" ? "original" : state.mode === "mask_only" ? "mask_only" : "overlay";
        if (!state.showLayers) renderMode = "original";
        return R.renderSegmentationOverlay(canvas, img, layers, {
          maxWidth: 640,
          maxHeight: 480,
          mode: renderMode,
          opacity: state.opacity,
          showLabels: state.showLabels,
          showOutline: true
        });
      }).then(function (meta) {
        if (meta.warnings && meta.warnings.length) {
          warningEl.hidden = false;
          warningEl.textContent = meta.warnings.indexOf("mask_image_dimension_mismatch_warning") >= 0
            ? "部分识别层与原图尺寸不一致，已按比例映射显示。"
            : "部分识别层文件无法读取。";
        } else {
          warningEl.hidden = true;
        }
      }).catch(function () {
        warningEl.hidden = false;
        warningEl.textContent = "原图无法加载。请确认本地测试服务 (8787) 已启动。";
      });
    }

    canvas.addEventListener("click", function () {
      detailEl.textContent = "点击图层可在高级模式中查看详情。";
    });

    if (debugMode) {
      var dbg = host.querySelector("#vol-debug");
      if (dbg) {
        dbg.innerHTML = "<pre class='raw-json-pre'>" +
          JSON.stringify({ source_image_ref: sourceRef, layers: layers }, null, 2) + "</pre>";
      }
    }

    redraw();
    return { layers: layers, sourceRef: sourceRef, redraw: redraw, state: state };
  }

  global.VisualOverlayLayer = { render: renderOverlayView };
})(typeof window !== "undefined" ? window : this);
