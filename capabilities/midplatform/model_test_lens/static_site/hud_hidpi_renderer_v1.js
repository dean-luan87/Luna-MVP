/**
 * HUD HiDPI Canvas Renderer V1 — crisp lines and labels on retina displays.
 * Display-only; no model execution.
 */
(function (global) {
  "use strict";

  var MIN_LINE_WIDTH = 2;
  var MIN_FONT_SIZE = 13;
  var RECOMMENDED_FONT_SIZE = 14;
  var MAX_DPR = 3;

  function getDevicePixelRatio() {
    return Math.min(global.devicePixelRatio || 1, MAX_DPR);
  }

  function setupHiDPICanvas(canvas, displayWidth, displayHeight) {
    var dpr = getDevicePixelRatio();
    var dw = Math.max(1, Math.round(displayWidth));
    var dh = Math.max(1, Math.round(displayHeight));
    canvas.style.width = dw + "px";
    canvas.style.height = dh + "px";
    canvas.width = Math.round(dw * dpr);
    canvas.height = Math.round(dh * dpr);
    var ctx = canvas.getContext("2d");
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(dpr, dpr);
    ctx.imageSmoothingEnabled = true;
    if (ctx.imageSmoothingQuality) ctx.imageSmoothingQuality = "high";
    return {
      ctx: ctx,
      displayWidth: dw,
      displayHeight: dh,
      dpr: dpr,
      minLineWidth: MIN_LINE_WIDTH,
      fontSize: RECOMMENDED_FONT_SIZE
    };
  }

  function drawImageCover(ctx, image, displayWidth, displayHeight) {
    ctx.clearRect(0, 0, displayWidth, displayHeight);
    ctx.drawImage(image, 0, 0, displayWidth, displayHeight);
  }

  function labelFont(size) {
    var fs = Math.max(MIN_FONT_SIZE, size || RECOMMENDED_FONT_SIZE);
    return "600 " + fs + "px system-ui, -apple-system, 'Segoe UI', sans-serif";
  }

  function drawLabelChip(ctx, x, y, text, strokeColor, options) {
    options = options || {};
    var fs = options.fontSize || RECOMMENDED_FONT_SIZE;
    ctx.font = labelFont(fs);
    var padX = 7;
    var padY = 5;
    var metrics = ctx.measureText(text);
    var chipW = metrics.width + padX * 2;
    var chipH = fs + padY * 2;
    var rx = x;
    var ry = y - chipH + 2;

    var fillAlpha = options.fillAlpha != null ? options.fillAlpha : 0.82;
    ctx.fillStyle = "rgba(0, 0, 0, " + fillAlpha + ")";
    ctx.beginPath();
    if (ctx.roundRect) {
      ctx.roundRect(rx, ry, chipW, chipH, 4);
    } else {
      ctx.rect(rx, ry, chipW, chipH);
    }
    ctx.fill();

    if (strokeColor) {
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = MIN_LINE_WIDTH;
      ctx.stroke();
    }

    ctx.fillStyle = "#ffffff";
    ctx.textBaseline = "middle";
    ctx.fillText(text, rx + padX, ry + chipH / 2);
    ctx.textBaseline = "alphabetic";
    return { x: rx, y: ry, w: chipW, h: chipH };
  }

  global.HudHiDPIRenderer = {
    version: "hud_hidpi_renderer_v1",
    MIN_LINE_WIDTH: MIN_LINE_WIDTH,
    MIN_FONT_SIZE: MIN_FONT_SIZE,
    RECOMMENDED_FONT_SIZE: RECOMMENDED_FONT_SIZE,
    getDevicePixelRatio: getDevicePixelRatio,
    setupHiDPICanvas: setupHiDPICanvas,
    drawImageCover: drawImageCover,
    labelFont: labelFont,
    drawLabelChip: drawLabelChip
  };
})(typeof window !== "undefined" ? window : this);
