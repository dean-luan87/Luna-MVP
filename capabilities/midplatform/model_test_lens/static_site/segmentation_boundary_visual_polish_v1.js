/**
 * Segmentation Boundary Visual Polish — dual-stroke spatial contour (single owner).
 * Outer dark stroke + inner light stroke + corner anchors for complex street scenes.
 * Visual-only; dual stroke is one boundary rendering style, not a second logical box.
 */
(function (global) {
  "use strict";

  var Readability = function () { return global.HudOverlayReadability; };

  var STYLE = {
    outerStroke: "rgba(0, 48, 28, 0.78)",
    innerStroke: "rgba(62, 207, 142, 0.92)",
    innerStrokeHover: "rgba(80, 220, 155, 0.98)",
    innerStrokeSelect: "rgba(100, 235, 170, 1)",
    cornerStroke: "rgba(90, 230, 160, 0.95)",
    outerWidth: 4.5,
    innerWidth: 2,
    innerWidthSelect: 2.5,
    cornerWidth: 2.5,
    cornerLenDefault: 11,
    cornerLenHover: 13,
    cornerLenSelect: 14,
    outerAlphaSmall: 0.72,
    innerAlphaSmall: 0.84,
    cornerAlphaSmall: 0.88,
    outerAlphaLarge: 0.58,
    innerAlphaLarge: 0.72,
    cornerAlphaLarge: 0.82,
    outerAlphaHoverBoost: 0.08,
    innerAlphaHoverBoost: 0.12,
    cornerAlphaHover: 0.95,
    innerAlphaSelect: 1,
    cornerAlphaSelect: 1,
    dimmedPeerFactor: 0.78,
    minOuterAlpha: 0.5,
    minInnerAlpha: 0.62,
    largeAreaRatio: 0.16,
    boundaryDualStrokeSingleOwner: true,
    segmentationBoundaryContrastSufficient: true,
    segmentationBoundaryVisibleByDefault: true,
    largeRegionBoundaryVisible: true,
    cornerAnchorVisible: true
  };

  function isSelected(entity, options) {
    return options && options.highlightEntityId && options.highlightEntityId === entity.entity_id;
  }

  function isHovered(entity, options) {
    return options && options.hoverEntityId && options.hoverEntityId === entity.entity_id;
  }

  function lookupRecord(options, entityId) {
    if (!options || !options.lookupRecord) return null;
    return options.lookupRecord(options, entityId);
  }

  function isLargeRegion(bbox, options) {
    if (!bbox) return false;
    var cw = options.canvasW || 1;
    var ch = options.canvasH || 1;
    if ((bbox.w * bbox.h) / (cw * ch) >= STYLE.largeAreaRatio) return true;
    var R = Readability();
    if (R && R.isLargeSceneBBox) return R.isLargeSceneBBox(bbox, cw, ch);
    return false;
  }

  function isStructureRegion(entity, record, bbox, options) {
    var R = Readability();
    if (R && R.useSceneStructureStyle) {
      return R.useSceneStructureStyle(record, entity, bbox, options.canvasW, options.canvasH);
    }
    if (record && record.motion_state_candidate === "scene_structure_candidate") return true;
    var blob = [
      entity.display_name, entity.label,
      entity._overlay && entity._overlay.label, entity.entity_type
    ].filter(Boolean).join(" ").toLowerCase();
    return /road|crosswalk|building|structure|plane|walkable|pavement/.test(blob);
  }

  function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
  }

  function resolveStyle(entity, bbox, options) {
    var selected = isSelected(entity, options);
    var hovered = isHovered(entity, options);
    var large = isLargeRegion(bbox, options);
    var record = lookupRecord(options, entity.entity_id);
    var structure = isStructureRegion(entity, record, bbox, options);

    var outerAlpha = large || structure ? STYLE.outerAlphaLarge : STYLE.outerAlphaSmall;
    var innerAlpha = large || structure ? STYLE.innerAlphaLarge : STYLE.innerAlphaSmall;
    var cornerAlpha = large || structure ? STYLE.cornerAlphaLarge : STYLE.cornerAlphaSmall;
    var innerStroke = STYLE.innerStroke;
    var innerWidth = STYLE.innerWidth;
    var cornerLen = STYLE.cornerLenDefault;

    if (selected) {
      innerStroke = STYLE.innerStrokeSelect;
      innerWidth = STYLE.innerWidthSelect;
      innerAlpha = STYLE.innerAlphaSelect;
      cornerAlpha = STYLE.cornerAlphaSelect;
      cornerLen = STYLE.cornerLenSelect;
      outerAlpha = clamp(outerAlpha + 0.1, STYLE.minOuterAlpha, 1);
    } else if (hovered) {
      innerStroke = STYLE.innerStrokeHover;
      innerAlpha = clamp(innerAlpha + STYLE.innerAlphaHoverBoost, STYLE.minInnerAlpha, 0.95);
      cornerAlpha = STYLE.cornerAlphaHover;
      cornerLen = STYLE.cornerLenHover;
      outerAlpha = clamp(outerAlpha + STYLE.outerAlphaHoverBoost, STYLE.minOuterAlpha, 1);
    } else if (options.highlightEntityId) {
      outerAlpha *= STYLE.dimmedPeerFactor;
      innerAlpha *= STYLE.dimmedPeerFactor;
      cornerAlpha *= STYLE.dimmedPeerFactor;
    }

    outerAlpha = clamp(outerAlpha, STYLE.minOuterAlpha, 1);
    innerAlpha = clamp(innerAlpha, STYLE.minInnerAlpha, 1);
    cornerAlpha = clamp(cornerAlpha, STYLE.minInnerAlpha, 1);

    return {
      outerStroke: STYLE.outerStroke,
      innerStroke: innerStroke,
      cornerStroke: STYLE.cornerStroke,
      outerWidth: STYLE.outerWidth,
      innerWidth: innerWidth,
      cornerWidth: STYLE.cornerWidth,
      outerAlpha: outerAlpha,
      innerAlpha: innerAlpha,
      cornerAlpha: cornerAlpha,
      cornerLen: cornerLen,
      large: large || structure
    };
  }

  function drawCornerAnchors(ctx, x, y, w, h, cornerLen) {
    var xl = Math.max(6, Math.min(cornerLen, w * 0.32));
    var yl = Math.max(6, Math.min(cornerLen, h * 0.32));
    ctx.beginPath();
    ctx.moveTo(x, y + yl);
    ctx.lineTo(x, y);
    ctx.lineTo(x + xl, y);
    ctx.moveTo(x + w - xl, y);
    ctx.lineTo(x + w, y);
    ctx.lineTo(x + w, y + yl);
    ctx.moveTo(x + w, y + h - yl);
    ctx.lineTo(x + w, y + h);
    ctx.lineTo(x + w - xl, y + h);
    ctx.moveTo(x + xl, y + h);
    ctx.lineTo(x, y + h);
    ctx.lineTo(x, y + h - yl);
    ctx.stroke();
  }

  /** Dual-stroke rect — same segmentation boundary, not a logical clone. */
  function drawDualStrokeBoundary(ctx, x, y, w, h, style) {
    ctx.save();
    ctx.setLineDash([]);
    ctx.lineCap = "square";
    ctx.lineJoin = "miter";
    ctx.shadowBlur = 0;

    ctx.strokeStyle = style.outerStroke;
    ctx.lineWidth = style.outerWidth;
    ctx.globalAlpha = style.outerAlpha;
    ctx.strokeRect(x, y, w, h);

    ctx.strokeStyle = style.innerStroke;
    ctx.lineWidth = style.innerWidth;
    ctx.globalAlpha = style.innerAlpha;
    ctx.strokeRect(x, y, w, h);

    ctx.strokeStyle = style.cornerStroke;
    ctx.lineWidth = style.cornerWidth;
    ctx.globalAlpha = style.cornerAlpha;
    drawCornerAnchors(ctx, x, y, w, h, style.cornerLen);

    ctx.restore();
  }

  function drawSegmentationContour(ctx, entity, bbox, options) {
    if (!bbox || bbox.w < 4 || options.showLineBox === false) return;
    var style = resolveStyle(entity, bbox, options);
    drawDualStrokeBoundary(
      ctx,
      bbox.x + 0.5,
      bbox.y + 0.5,
      bbox.w,
      bbox.h,
      style
    );
  }

  global.SegmentationBoundaryVisualPolish = {
    version: "segmentation_boundary_visual_polish_v3_contrast_restore",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Segmentation-Boundary-Contrast-Restore-v1-001",
    boundaryVisualPolishOnly: true,
    segmentationBoundarySingleOwnerPreserved: true,
    segmentationBoundaryVisibleByDefault: true,
    segmentationBoundaryContrastSufficient: true,
    boundaryDualStrokeSingleOwner: true,
    cornerAnchorVisible: true,
    largeRegionBoundaryVisible: true,
    selectedUsesExistingBoundary: true,
    hoverUsesExistingBoundary: true,
    noBoundaryClone: true,
    noSecondaryBoxFromAttention: true,
    dualStrokeIsRenderingStyleNotLogicalClone: true,
    STYLE: STYLE,
    drawSegmentationContour: drawSegmentationContour,
    drawDualStrokeBoundary: drawDualStrokeBoundary,
    isLargeRegion: isLargeRegion,
    isStructureRegion: isStructureRegion,
    resolveStyle: resolveStyle
  };
})(typeof window !== "undefined" ? window : this);
