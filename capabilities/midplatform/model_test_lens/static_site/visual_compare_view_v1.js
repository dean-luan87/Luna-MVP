/**
 * Model Test Lens — Visual Compare View v1 (before | after).
 */
(function (global) {
  "use strict";

  var Ex = global.VisualOverlayExamples;
  var CR = global.VisualCompareRenderer;

  function renderCompareView(host, envelope, options) {
    options = options || {};
    var debugMode = !!options.debugMode;
    var compact = !!options.compact;
    var cat = envelope.model_category;
    var modelId = envelope.model_id;
    var compactCls = compact ? " vcv-compact" : "";

    if (cat === "slam_vio") {
      host.innerHTML =
        "<section class='vcv-section" + compactCls + "'>" +
        (compact ? "" : "<h3>模型识别对比</h3>") +
        "<p class='muted'>SLAM 帧级对比视图预留中；请展开底部指标详情查看轨迹。</p>" +
        "</section>";
      return;
    }

    if (cat !== "segmentation" && modelId !== "mobile_sam") {
      host.innerHTML =
        "<section class='vcv-section" + compactCls + "'>" +
        (compact ? "" : "<h3>模型识别对比</h3>") +
        "<p class='muted'>当前结果只包含指标，暂时无法生成原图对比。</p></section>";
      return;
    }

    host.innerHTML =
      "<section class='vcv-section" + compactCls + "' id='visual-compare-section'>" +
      (compact ? "" : "<h3>模型识别对比</h3>") +
      "<div id='vcv-controls-host'></div>" +
      "<div id='vcv-warning' class='vcv-warning' hidden></div>" +
      "<div class='vcv-panels' id='vcv-panels'>" +
      "<div class='vcv-panel'><h4>原图</h4><canvas id='vcv-left-canvas' class='vcv-canvas lol-main-canvas'></canvas></div>" +
      "<div class='vcv-panel'><h4>模型识别结果</h4><canvas id='vcv-right-canvas' class='vcv-canvas lol-main-canvas'></canvas></div>" +
      "</div>" +
      (compact ? "" : "<p class='vcv-hint muted'>测试结果，仅供模型评估，不作为事实结果。</p>") +
      "<div id='vcv-layer-detail' class='vcv-layer-detail'></div>" +
      (debugMode ? "<div id='vcv-debug' class='vcv-debug'></div>" : "") +
      "</section>";

    var sourceRef = Ex.pickSourceImageRef(envelope);
    var layers = Ex.buildOverlayLayers(envelope);
    var warningEl = host.querySelector("#vcv-warning");
    var leftCanvas = host.querySelector("#vcv-left-canvas");
    var rightCanvas = host.querySelector("#vcv-right-canvas");
    var panelsEl = host.querySelector("#vcv-panels");
    var detailEl = host.querySelector("#vcv-layer-detail");

    if (!sourceRef) {
      warningEl.hidden = false;
      warningEl.textContent = "缺少原图，无法生成左右对比视图。";
      panelsEl.hidden = true;
      return;
    }
    if (!layers.length) {
      warningEl.hidden = false;
      warningEl.textContent = "模型结果中没有可显示的识别区域。";
      return;
    }

    var state = { showLayers: true, showLabels: true, opacity: 0.45, mode: "compare", layers: layers };
    var controlsApi = global.VisualOverlayControls.create(
      host.querySelector("#vcv-controls-host"),
      state,
      function () { redraw(); }
    );
    controlsApi.renderLayerToggles(layers);

    var modeSelect = host.querySelector("#vov-mode");
    if (modeSelect) {
      modeSelect.value = "compare";
      modeSelect.addEventListener("change", function () {
        if (state.mode === "original") {
          panelsEl.classList.add("vcv-single");
        } else if (state.mode === "mask_only" || state.mode === "overlay") {
          panelsEl.classList.remove("vcv-single");
          panelsEl.classList.toggle("vcv-mask-only", state.mode === "mask_only");
        } else {
          panelsEl.classList.remove("vcv-single", "vcv-mask-only");
        }
      });
    }

    function redraw() {
      var url = Ex.artifactUrl(sourceRef);
      var maxW = compact ? Math.max(280, Math.floor((host.clientWidth || 640) / 2) - 16) : 480;
      var maxH = compact ? Math.max(240, (host.clientHeight || 480) - 48) : 360;
      CR.loadImage(url).then(function (img) {
        var compareMode = state.mode;
        if (compareMode === "compare") {
          return CR.renderComparePanels(leftCanvas, rightCanvas, img, layers, {
            mode: "compare",
            showLayers: state.showLayers,
            opacity: state.opacity,
            showLabels: state.showLabels,
            maxWidth: maxW,
            maxHeight: maxH
          });
        }
        if (compareMode === "original") {
          panelsEl.classList.add("vcv-single");
          CR.renderComparePanels(leftCanvas, rightCanvas, img, layers, {
            mode: "original",
            maxWidth: compact ? maxW * 2 : 640,
            maxHeight: compact ? maxH : 480
          });
          return;
        }
        panelsEl.classList.remove("vcv-single");
        return CR.renderComparePanels(leftCanvas, rightCanvas, img, layers, {
          mode: compareMode,
          showLayers: state.showLayers,
          opacity: state.opacity,
          showLabels: state.showLabels,
          maxWidth: maxW,
          maxHeight: maxH
        });
      }).then(function (meta) {
        if (meta && meta.warnings && meta.warnings.length) {
          warningEl.hidden = false;
          warningEl.textContent = "部分识别层与原图尺寸不一致或无法读取，已尽力显示。";
        } else {
          warningEl.hidden = true;
        }
      }).catch(function () {
        warningEl.hidden = false;
        warningEl.textContent = "无法加载原图。请确认本地测试服务 (8787) 已启动，然后点击「重新检查服务」。";
      });
    }

    layers.forEach(function (layer) {
      layer._onSelect = function () {
        var conf = layer.confidence != null ? Math.round(layer.confidence * 100) + "%" : "—";
        detailEl.innerHTML =
          "<p><strong>" + layer.label + "</strong> · 置信度 " + conf +
          " · <span class='muted'>识别区域详情</span></p>";
      };
    });

    if (debugMode) {
      var dbg = host.querySelector("#vcv-debug");
      if (dbg) {
        dbg.innerHTML = "<pre class='raw-json-pre'>" + JSON.stringify(layers, null, 2) + "</pre>";
      }
    }

    redraw();
    return { redraw: redraw, layers: layers };
  }

  global.VisualCompareView = { render: renderCompareView };
})(typeof window !== "undefined" ? window : this);
