/**
 * Model Test Lens — Visual Compare renderer v1 (before / after).
 */
(function (global) {
  "use strict";

  var Ex = global.VisualOverlayExamples;
  var R = global.VisualOverlayRenderer;

  function renderDetectionCompareView() {
    return { reserved: true };
  }

  function renderOcrCompareView() {
    return { reserved: true };
  }

  function renderSlamFrameCompareView() {
    return { reserved: true };
  }

  function renderDetectionBoxesOnCanvas() {
    return null;
  }

  function renderOcrBoxesOnCanvas() {
    return null;
  }

  function renderSlamKeypointsOnFrame() {
    return null;
  }

  function renderComparePanels(leftCanvas, rightCanvas, baseImage, layers, options) {
    options = options || {};
    var maxW = options.maxWidth || 480;
    var maxH = options.maxHeight || 360;
    var mode = options.mode || "compare";
    var leftMeta = R.renderBaseImage(leftCanvas, baseImage, maxW, maxH);
    var warnings = [];

    if (mode === "original" || mode === "compare") {
      /* left already drawn */
    }

    if (mode === "original") {
      rightCanvas.width = 0;
      rightCanvas.height = 0;
      return Promise.resolve({ warnings: warnings });
    }

    var rightMode = mode === "mask_only" ? "mask_only" : "overlay";
    if (!options.showLayers) rightMode = "original";

    return Promise.resolve(R.renderSegmentationOverlay(rightCanvas, baseImage, layers, {
      maxWidth: maxW,
      maxHeight: maxH,
      mode: rightMode,
      opacity: options.opacity,
      showLabels: options.showLabels,
      showOutline: true
    })).then(function (meta) {
      if (leftMeta.width !== meta.width || leftMeta.height !== meta.height) {
        rightCanvas.width = leftMeta.width;
        rightCanvas.height = leftMeta.height;
      }
      return meta;
    });
  }

  global.VisualCompareRenderer = {
    renderComparePanels: renderComparePanels,
    renderDetectionCompareView: renderDetectionCompareView,
    renderOcrCompareView: renderOcrCompareView,
    renderSlamFrameCompareView: renderSlamFrameCompareView,
    renderDetectionBoxesOnCanvas: renderDetectionBoxesOnCanvas,
    renderOcrBoxesOnCanvas: renderOcrBoxesOnCanvas,
    renderSlamKeypointsOnFrame: renderSlamKeypointsOnFrame,
    loadImage: R.loadImage,
    artifactUrl: Ex.artifactUrl
  };
})(typeof window !== "undefined" ? window : this);
