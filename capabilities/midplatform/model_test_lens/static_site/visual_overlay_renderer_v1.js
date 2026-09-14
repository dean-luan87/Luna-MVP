/**
 * Model Test Lens — Visual Overlay renderer v1 (canvas, read-only).
 */
(function (global) {
  "use strict";

  var Ex = global.VisualOverlayExamples;

  function loadImage(url) {
    return new Promise(function (resolve, reject) {
      if (!url) {
        reject(new Error("missing_url"));
        return;
      }
      var img = new Image();
      img.crossOrigin = "anonymous";
      img.onload = function () { resolve(img); };
      img.onerror = function () { reject(new Error("image_load_failed")); };
      img.src = url;
    });
  }

  function fitSize(imgW, imgH, maxW, maxH) {
    var scale = Math.min(maxW / imgW, maxH / imgH, 1);
    return { w: Math.round(imgW * scale), h: Math.round(imgH * scale), scale: scale };
  }

  function maskBoundingBox(maskCtx, w, h, threshold) {
    var data;
    try {
      data = maskCtx.getImageData(0, 0, w, h).data;
    } catch (e) {
      return null;
    }
    var minX = w; var minY = h; var maxX = 0; var maxY = 0; var found = false;
    for (var y = 0; y < h; y++) {
      for (var x = 0; x < w; x++) {
        var i = (y * w + x) * 4;
        if (data[i] > threshold || data[i + 1] > threshold || data[i + 2] > threshold) {
          found = true;
          if (x < minX) minX = x;
          if (y < minY) minY = y;
          if (x > maxX) maxX = x;
          if (y > maxY) maxY = y;
        }
      }
    }
    if (!found) return null;
    return { x: minX, y: minY, w: maxX - minX + 1, h: maxY - minY + 1 };
  }

  function drawMaskOverlay(ctx, baseImg, maskImg, layer, options) {
    var w = options.width;
    var h = options.height;
    var opacity = options.opacity != null ? options.opacity : layer.opacity;
    var color = layer.color || "rgba(255, 99, 71, 0.55)";
    var outline = layer.outline_color || "#ff6347";

    var off = document.createElement("canvas");
    off.width = w;
    off.height = h;
    var octx = off.getContext("2d");
    octx.drawImage(maskImg, 0, 0, w, h);
    var bbox = maskBoundingBox(octx, w, h, 40);

    octx.globalCompositeOperation = "source-in";
    octx.fillStyle = color;
    octx.fillRect(0, 0, w, h);

    ctx.globalAlpha = opacity;
    ctx.drawImage(off, 0, 0);
    ctx.globalAlpha = 1;

    if (options.showOutline !== false && bbox && bbox.w > 2 && bbox.h > 2) {
      ctx.strokeStyle = outline;
      ctx.lineWidth = 2;
      ctx.strokeRect(bbox.x, bbox.y, bbox.w, bbox.h);
    }

    if (options.showLabels !== false && layer.label) {
      var lx = bbox ? bbox.x : 8;
      var ly = bbox ? Math.max(8, bbox.y - 4) : 8;
      var conf = layer.confidence != null ? Math.round(layer.confidence * 100) + "%" : "";
      var text = layer.label + (conf ? " " + conf : "");
      ctx.font = "12px system-ui, sans-serif";
      var tw = ctx.measureText(text).width + 10;
      ctx.fillStyle = "rgba(0,0,0,0.65)";
      ctx.fillRect(lx, ly - 14, tw, 18);
      ctx.fillStyle = "#fff";
      ctx.fillText(text, lx + 5, ly);
    }
  }

  function renderBaseImage(canvas, image, maxW, maxH) {
    var fit = fitSize(image.naturalWidth, image.naturalHeight, maxW, maxH);
    canvas.width = fit.w;
    canvas.height = fit.h;
    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, fit.w, fit.h);
    ctx.drawImage(image, 0, 0, fit.w, fit.h);
    return { ctx: ctx, width: fit.w, height: fit.h, scale: fit.scale };
  }

  function renderSegmentationOverlay(canvas, baseImage, layers, options) {
    options = options || {};
    var maxW = options.maxWidth || 520;
    var maxH = options.maxHeight || 400;
    var base = renderBaseImage(canvas, baseImage, maxW, maxH);
    var ctx = base.ctx;
    var w = base.width;
    var h = base.height;
    var mode = options.mode || "overlay";

    if (mode === "original") {
      return Promise.resolve({ width: w, height: h, warnings: [] });
    }

    var warnings = [];
    var visible = (layers || []).filter(function (l) { return l.visible !== false; });

    return Promise.all(visible.map(function (layer) {
      return loadImage(Ex.artifactUrl(layer.artifact_ref)).then(function (maskImg) {
        if (maskImg.naturalWidth !== baseImage.naturalWidth || maskImg.naturalHeight !== baseImage.naturalHeight) {
          warnings.push("mask_image_dimension_mismatch_warning");
        }
        if (mode === "mask_only") {
          ctx.clearRect(0, 0, w, h);
          ctx.fillStyle = "#111";
          ctx.fillRect(0, 0, w, h);
        }
        drawMaskOverlay(ctx, baseImage, maskImg, layer, {
          width: w,
          height: h,
          opacity: options.opacity,
          showLabels: options.showLabels,
          showOutline: options.showOutline
        });
      }).catch(function () {
        warnings.push("mask_unreadable:" + layer.label);
      });
    })).then(function () {
      return { width: w, height: h, warnings: warnings };
    });
  }

  function renderDetectionBoxesOverlay() {
    return Promise.resolve({ placeholder: true, message: "Detection overlay reserved" });
  }

  function renderOcrTextBoxesOverlay() {
    return Promise.resolve({ placeholder: true, message: "OCR overlay reserved" });
  }

  function renderSlamFrameOverlay() {
    return Promise.resolve({ placeholder: true, message: "SLAM frame overlay reserved" });
  }

  function renderDepthMapOverlay() {
    return Promise.resolve({ placeholder: true, message: "Depth overlay reserved" });
  }

  global.VisualOverlayRenderer = {
    loadImage: loadImage,
    fitSize: fitSize,
    maskBoundingBox: maskBoundingBox,
    renderBaseImage: renderBaseImage,
    renderSegmentationOverlay: renderSegmentationOverlay,
    renderDetectionBoxesOverlay: renderDetectionBoxesOverlay,
    renderOcrTextBoxesOverlay: renderOcrTextBoxesOverlay,
    renderSlamFrameOverlay: renderSlamFrameOverlay,
    renderDepthMapOverlay: renderDepthMapOverlay
  };
})(typeof window !== "undefined" ? window : this);
