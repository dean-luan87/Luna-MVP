/**
 * HUD Attention Visual Language V1 — semantic separation (segmentation owner vs annotation layer).
 * Segmentation: one boundary per region_id. Attention: text float markers only, no boundary clone.
 */
(function (global) {
  "use strict";

  var AttentionEngine = function () { return global.ObservationAttentionEngine; };
  var LabelPolicy = function () { return global.HudLabelLayoutPolicy; };
  var Readability = function () { return global.HudOverlayReadability; };
  var Copy = function () { return global.ObservationAttentionCopy || {}; };
  var HiDPI = function () { return global.HudHiDPIRenderer; };
  var SegPolish = function () { return global.SegmentationBoundaryVisualPolish; };

  var PRIORITY_SHORT = {
    P0_immediate_attention: "P0",
    P1_high_attention: "P1",
    P2_medium_attention: "P2",
    P3_low_attention: "P3",
    ignore_for_now: ""
  };

  var PRIORITY_DRAW_ORDER = {
    ignore_for_now: 0,
    P3_low_attention: 1,
    P2_medium_attention: 2,
    P1_high_attention: 3,
    P0_immediate_attention: 4
  };

  var SEG = {
    stroke: "rgba(62, 207, 142, 0.92)",
    strokeSelect: "rgba(100, 235, 170, 1)",
    strokeHover: "rgba(80, 220, 155, 0.98)",
    line: 2,
    lineSelect: 2.5,
    lineHover: 2
  };

  function markerVisibleByDedupe(entity, options) {
    if (!options || !options.markerDedupeSet) return true;
    if (isHighlighted(entity, options)) return true;
    return options.markerDedupeSet[entity.entity_id] === true;
  }

  function buildMarkerDedupeSet(items, options) {
    var allowed = {};
    var claimedLabels = {};
    var sorted = sortDrawItems(items || [], options || {}).slice().reverse();
    var i;
    for (i = 0; i < sorted.length; i++) {
      var item = sorted[i];
      var entity = item.entity;
      var record = lookupRecord(options, entity.entity_id);
      if (!record) continue;
      if (isHighlighted(entity, options)) {
        allowed[entity.entity_id] = true;
        continue;
      }
      if (!shouldShowMarkerOnCanvas(record, entity, options)) continue;
      if (options.showAllAttentionMarkers) {
        allowed[entity.entity_id] = true;
        continue;
      }
      var label = shortRegionName(entity);
      if (claimedLabels[label]) continue;
      claimedLabels[label] = entity.entity_id;
      allowed[entity.entity_id] = true;
    }
    return allowed;
  }

  function lookupRecord(options, entityId) {
    if (!options || !options.attentionPkg || !AttentionEngine()) return null;
    return AttentionEngine().lookupRecord(options.attentionPkg, entityId);
  }

  function isSelected(entity, options) {
    return options && options.highlightEntityId && options.highlightEntityId === entity.entity_id;
  }

  function isHovered(entity, options) {
    return options && options.hoverEntityId && options.hoverEntityId === entity.entity_id;
  }

  function isHighlighted(entity, options) {
    return isSelected(entity, options) || isHovered(entity, options);
  }

  function priorityShort(record) {
    if (!record || !record.priority_level) return "";
    return PRIORITY_SHORT[record.priority_level] || "";
  }

  function shortRegionName(entity) {
    if (entity.hud_short_label) return entity.hud_short_label;
    if (LabelPolicy()) return LabelPolicy().shortName(entity);
    return entity.display_name || "区域";
  }

  function primarySemanticHint(record) {
    if (!record) return "";
    var c = Copy();
    var motion = record.motion_state_candidate;
    if (motion === "needs_tracking_review" || motion === "dynamic_candidate") {
      return (c.flags && c.flags.tracking) ? c.flags.tracking + "候选" : "跟踪候选";
    }
    if (record.ocr_required) return (c.flags && c.flags.ocr) ? c.flags.ocr + "候选" : "OCR候选";
    if (motion === "scene_structure_candidate") return "结构候选";
    if (motion === "static_candidate") return "静态候选";
    return "";
  }

  function hoverFollowupHint(record) {
    return "";
  }

  function boundaryAlpha(entity, options) {
    if (!options.highlightEntityId) return 1;
    if (isSelected(entity, options) || isHovered(entity, options)) return 1;
    return 0.72;
  }

  function formatFloatMarker(entity, record, options) {
    var glyph = entity.hud_number_glyph || "";
    var pri = priorityShort(record);
    var name = shortRegionName(entity);
    var text = glyph + (pri ? " " + pri : "") + " " + name;
    if (isHovered(entity, options)) {
      var hint = primarySemanticHint(record);
      if (hint) text += "｜" + hint;
    }
    return text.trim();
  }

  function shouldShowMarkerOnCanvas(record, entity, options) {
    if (options.showAttentionMarkers === false) return false;
    if (!record) return false;
    if (record.priority_level === "ignore_for_now") return false;
    var pri = record.priority_level;
    var isP01 = pri === "P0_immediate_attention" || pri === "P1_high_attention";
    if (options.showAllAttentionMarkers) return true;
    if (isHovered(entity, options)) return true;
    if (isSelected(entity, options)) return isP01;
    return isP01;
  }

  function markerAlpha(entity, options) {
    if (!options.highlightEntityId) return 1;
    if (isHighlighted(entity, options)) return 1;
    return 0.38;
  }

  function sortDrawItems(items, options) {
    return items.slice().sort(function (a, b) {
      var ra = lookupRecord(options, a.entity.entity_id);
      var rb = lookupRecord(options, b.entity.entity_id);
      var pa = PRIORITY_DRAW_ORDER[ra && ra.priority_level] != null
        ? PRIORITY_DRAW_ORDER[ra.priority_level] : 2;
      var pb = PRIORITY_DRAW_ORDER[rb && rb.priority_level] != null
        ? PRIORITY_DRAW_ORDER[rb.priority_level] : 2;
      if (pa !== pb) return pa - pb;
      var aa = (a.bbox && a.bbox.w * a.bbox.h) || 0;
      var ab = (b.bbox && b.bbox.w * b.bbox.h) || 0;
      return ab - aa;
    });
  }

  /** Segmentation overlay owner — spatial contour, one boundary per region. */
  function drawSegmentationBoundary(ctx, entity, bbox, options) {
    if (!bbox || bbox.w < 4 || options.showLineBox === false) return;
    var polish = SegPolish();
    if (polish && polish.drawSegmentationContour) {
      var polishOpts = Object.assign({}, options, { lookupRecord: lookupRecord });
      polish.drawSegmentationContour(ctx, entity, bbox, polishOpts);
      return;
    }
    var selected = isSelected(entity, options);
    var hovered = isHovered(entity, options);
    ctx.save();
    ctx.globalAlpha = boundaryAlpha(entity, options);
    if (selected) {
      ctx.strokeStyle = SEG.strokeSelect;
      ctx.lineWidth = SEG.lineSelect;
    } else if (hovered) {
      ctx.strokeStyle = SEG.strokeHover;
      ctx.lineWidth = SEG.lineHover;
    } else {
      ctx.strokeStyle = SEG.stroke;
      ctx.lineWidth = SEG.line;
    }
    ctx.strokeRect(bbox.x + 0.5, bbox.y + 0.5, bbox.w, bbox.h);
    ctx.restore();
  }

  function measureMarker(ctx, text, fontSize) {
    var R = Readability();
    if (R && R.measureChip) return R.measureChip(ctx, text, fontSize);
    var fs = fontSize || 12;
    ctx.font = "600 " + fs + "px system-ui, sans-serif";
    return { w: ctx.measureText(text).width + 14, h: fs + 10, fontSize: fs };
  }

  function pickPlacement(bbox, chipW, chipH, placed, canvasW, canvasH, avoidBboxes) {
    var R = Readability();
    if (R && R.pickLabelPlacement) {
      return R.pickLabelPlacement(bbox, chipW, chipH, placed, canvasW, canvasH, avoidBboxes);
    }
    return { x: bbox.x, y: bbox.y - 4, rect: { x: bbox.x, y: bbox.y - chipH, w: chipW, h: chipH } };
  }

  function collectAvoidBboxes(items, selfId) {
    var R = Readability();
    if (R && R.collectAvoidBboxes) return R.collectAvoidBboxes(items, selfId);
    return [];
  }

  /** Annotation layer only — readable text float marker, no boundary. */
  function drawAttentionFloatMarker(ctx, entity, bbox, record, options, placedLabels, allItems, canvasW, canvasH) {
    if (!bbox || !shouldShowMarkerOnCanvas(record, entity, options)) return null;
    if (!markerVisibleByDedupe(entity, options)) return null;
    var text = formatFloatMarker(entity, record, options);
    var fs = isHighlighted(entity, options) ? 13 : 12;
    var chip = measureMarker(ctx, text, fs);
    var avoid = collectAvoidBboxes(allItems, entity.entity_id);
    var placement = pickPlacement(bbox, chip.w, chip.h, placedLabels || [], canvasW, canvasH, avoid);

    ctx.save();
    ctx.globalAlpha = markerAlpha(entity, options);
    var H = HiDPI();
    if (H && H.drawLabelChip) {
      H.drawLabelChip(ctx, placement.x, placement.y, text, null, {
        fontSize: fs,
        fillAlpha: isHighlighted(entity, options) ? 0.9 : 0.82
      });
    } else {
      ctx.font = "600 " + fs + "px system-ui, sans-serif";
      ctx.fillStyle = "rgba(0,0,0,0.82)";
      ctx.fillRect(placement.rect.x, placement.rect.y, chip.w, chip.h);
      ctx.fillStyle = "#fff";
      ctx.fillText(text, placement.rect.x + 7, placement.rect.y + chip.h - 5);
    }
    ctx.restore();
    if (placedLabels) placedLabels.push(placement.rect);
    return placement.rect;
  }

  function hitTest(items, x, y, options) {
    var sorted = sortDrawItems(items || [], options || {}).reverse();
    var i;
    for (i = 0; i < sorted.length; i++) {
      var b = sorted[i].bbox;
      if (!b) continue;
      if (x >= b.x && x <= b.x + b.w && y >= b.y && y <= b.y + b.h) {
        return sorted[i].entity;
      }
    }
    return null;
  }

  function canvasPoint(canvas, clientX, clientY, displayW, displayH) {
    var rect = canvas.getBoundingClientRect();
    return {
      x: (clientX - rect.left) * (displayW / rect.width),
      y: (clientY - rect.top) * (displayH / rect.height)
    };
  }

  global.HudAttentionVisualLanguage = {
    version: "hud_attention_visual_language_v6_boundary_contrast_restore",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Segmentation-Boundary-Contrast-Restore-v1-001",
    annotationLayerOnly: true,
    segmentationSoleBoundaryOwner: true,
    noAttentionBoundaryOwner: true,
    noBoundaryClone: true,
    noDuplicateMarkerForSameRegion: true,
    SEG: SEG,
    lookupRecord: lookupRecord,
    isHighlighted: isHighlighted,
    isSelected: isSelected,
    sortDrawItems: sortDrawItems,
    drawSegmentationBoundary: drawSegmentationBoundary,
    drawAttentionFloatMarker: drawAttentionFloatMarker,
    buildMarkerDedupeSet: buildMarkerDedupeSet,
    markerVisibleByDedupe: markerVisibleByDedupe,
    shouldShowMarkerOnCanvas: shouldShowMarkerOnCanvas,
    formatFloatMarker: formatFloatMarker,
    hitTest: hitTest,
    canvasPoint: canvasPoint,
    priorityShort: priorityShort
  };
})(typeof window !== "undefined" ? window : this);
