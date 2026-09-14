/**
 * Model Test Lens — Perception HUD renderer v1 (single segmentation owner + annotation float markers).
 */
(function (global) {
  "use strict";

  var Ex = global.VisualOverlayExamples;
  var VR = global.VisualOverlayRenderer;
  var HiDPI = global.HudHiDPIRenderer;
  var VL = global.HudAttentionVisualLanguage;

  function drawEntityMaskFill(ctx, maskImg, w, h, fillColor, opacity) {
    if (!fillColor || opacity <= 0) return;
    var off = document.createElement("canvas");
    off.width = w;
    off.height = h;
    var octx = off.getContext("2d");
    octx.drawImage(maskImg, 0, 0, w, h);
    octx.globalCompositeOperation = "source-in";
    octx.fillStyle = fillColor;
    octx.fillRect(0, 0, w, h);
    ctx.globalAlpha = opacity;
    ctx.drawImage(off, 0, 0);
    ctx.globalAlpha = 1;
  }

  function renderHUDCanvas(canvas, baseImage, entities, layers, options) {
    options = options || {};
    var maxW = options.maxWidth || 560;
    var maxH = options.maxHeight || 420;

    if (!VR || !VR.fitSize) {
      return Promise.reject(new Error("overlay_renderer_missing"));
    }

    var fit = VR.fitSize(baseImage.naturalWidth, baseImage.naturalHeight, maxW, maxH);
    var fillOpacity = options.maskFillOpacity != null ? options.maskFillOpacity : 0.35;
    var warnings = [];

    var surface;
    if (HiDPI && HiDPI.setupHiDPICanvas) {
      surface = HiDPI.setupHiDPICanvas(canvas, fit.w, fit.h);
      HiDPI.drawImageCover(surface.ctx, baseImage, fit.w, fit.h);
    } else {
      canvas.width = fit.w;
      canvas.height = fit.h;
      surface = { ctx: canvas.getContext("2d"), displayWidth: fit.w, displayHeight: fit.h };
      surface.ctx.drawImage(baseImage, 0, 0, fit.w, fit.h);
    }

    var ctx = surface.ctx;
    var w = surface.displayWidth;
    var h = surface.displayHeight;
    options.canvasW = w;
    options.canvasH = h;

    return Promise.all((entities || []).map(function (entity, i) {
      var layer = entity._overlay || (layers || [])[i];
      if (!layer || !layer.artifact_ref) return Promise.resolve(null);
      return VR.loadImage(Ex.artifactUrl(layer.artifact_ref)).then(function (maskImg) {
        var off = document.createElement("canvas");
        off.width = w;
        off.height = h;
        var octx = off.getContext("2d");
        octx.drawImage(maskImg, 0, 0, w, h);
        var bbox = null;
        try {
          bbox = VR.maskBoundingBox ? VR.maskBoundingBox(octx, w, h, 40) : null;
        } catch (bboxErr) {
          warnings.push("mask_bbox_unreadable");
        }
        return { entity: entity, layer: layer, maskImg: maskImg, bbox: bbox };
      }).catch(function () {
        warnings.push("mask_unreadable");
        return null;
      });
    })).then(function (rawItems) {
      var items = (rawItems || []).filter(Boolean);
      if (VL) items = VL.sortDrawItems(items, options);

      items.forEach(function (item) {
        var entity = item.entity;
        var bbox = item.bbox;
        ctx.save();
        if (VL) VL.drawSegmentationBoundary(ctx, entity, bbox, options);
        entity._hud_bbox = bbox;
        ctx.restore();
      });

      items.forEach(function (item) {
        var entity = item.entity;
        if (!VL || !VL.isSelected(entity, options)) return;
        var maskOpacity = options.showMaskFill ? fillOpacity * 0.5 : 0.08;
        var fill = entity.hud_fill || "rgba(62, 207, 142, 1)";
        ctx.save();
        drawEntityMaskFill(ctx, item.maskImg, w, h, fill, maskOpacity);
        ctx.restore();
      });

      var markerOpts = options;
      if (VL && VL.buildMarkerDedupeSet) {
        markerOpts = Object.assign({}, options, {
          markerDedupeSet: VL.buildMarkerDedupeSet(items, options)
        });
      }

      var placedLabels = [];
      if (options.showLabels !== false) {
        items.forEach(function (item) {
          var entity = item.entity;
          var bbox = item.bbox;
          var record = VL ? VL.lookupRecord(markerOpts, entity.entity_id) : null;
          if (VL) {
            VL.drawAttentionFloatMarker(ctx, entity, bbox, record, markerOpts,
              placedLabels, items, w, h);
          }
        });
      }

      if (options.onHitItemsReady) options.onHitItemsReady(items, w, h);

      return { width: w, height: h, warnings: warnings, dpr: surface.dpr || 1, hitItems: items };
    });
  }

  global.PerceptionHUDRenderer = {
    version: "perception_hud_renderer_v5_boundary_contrast_restore",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Segmentation-Boundary-Contrast-Restore-v1-001",
    segmentationSoleBoundaryOwner: true,
    annotationLayerOnly: true,
    noSecondaryBoxFromAttention: true,
    boundaryVisualPolishOnly: true,
    renderHUDCanvas: renderHUDCanvas
  };
})(typeof window !== "undefined" ? window : this);
