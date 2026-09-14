/**
 * HUD Overlay Readability V1 — label avoidance, priority tiers, scene-structure denoise.
 * Display-only; does not change attention engine decisions.
 */
(function (global) {
  "use strict";

  var LabelPolicy = function () { return global.HudLabelLayoutPolicy; };
  var AttentionEngine = function () { return global.ObservationAttentionEngine; };
  var Copy = function () { return global.ObservationAttentionCopy || {}; };

  var PRIORITY_DRAW_ORDER = {
    ignore_for_now: 0,
    P3_low_attention: 1,
    P2_medium_attention: 2,
    P1_high_attention: 3,
    P0_immediate_attention: 4
  };

  var PRIORITY_SHORT = {
    P0_immediate_attention: "P0",
    P1_high_attention: "P1",
    P2_medium_attention: "P2",
    P3_low_attention: "P3",
    ignore_for_now: "—"
  };

  function lookupRecord(options, entityId) {
    if (!options || !options.attentionPkg || !AttentionEngine()) return null;
    return AttentionEngine().lookupRecord(options.attentionPkg, entityId);
  }

  function labelBlob(entity) {
    var parts = [
      entity.display_name,
      entity.label,
      entity.entity_type,
      entity._overlay && entity._overlay.label
    ];
    return parts.filter(Boolean).join(" ").toLowerCase();
  }

  function isSceneStructure(record, entity) {
    if (record && record.motion_state_candidate === "scene_structure_candidate") return true;
    var blob = labelBlob(entity);
    return /road|crosswalk|walkable|plane|ground|pavement/.test(blob);
  }

  function isHighlighted(entity, options) {
    if (!entity || !options) return false;
    if (options.highlightEntityId && options.highlightEntityId === entity.entity_id) return true;
    if (options.hoverEntityId && options.hoverEntityId === entity.entity_id) return true;
    return false;
  }

  function priorityAlpha(record, entity, options) {
    if (isHighlighted(entity, options)) return 1;
    if (options && options.debugMode) return 1;
    var pri = record && record.priority_level ? record.priority_level : "P2_medium_attention";
    if (pri === "P0_immediate_attention" || pri === "P1_high_attention") return 1;
    if (pri === "P2_medium_attention") return options.dimP2Opacity != null ? options.dimP2Opacity : 0.4;
    return options.dimP3Opacity != null ? options.dimP3Opacity : 0.26;
  }

  function isLargeSceneBBox(bbox, canvasW, canvasH) {
    if (!bbox) return false;
    return bbox.w * bbox.h >= canvasW * canvasH * 0.1 || bbox.h >= canvasH * 0.45;
  }

  function useSceneStructureStyle(record, entity, bbox, canvasW, canvasH) {
    if (!isSceneStructure(record, entity)) return false;
    return isLargeSceneBBox(bbox, canvasW, canvasH);
  }

  function priorityShort(record) {
    if (!record || !record.priority_level) return "";
    return PRIORITY_SHORT[record.priority_level] || "";
  }

  function motionHint(record) {
    if (!record) return "";
    var c = Copy();
    var motion = record.motion_state_candidate;
    if (motion === "needs_tracking_review" || motion === "dynamic_candidate") {
      return (c.flags && c.flags.tracking) || "跟踪候选";
    }
    if (record.ocr_required) return (c.flags && c.flags.ocr) || "OCR候选";
    if (record.depth_required && motion === "scene_structure_candidate") {
      return "结构候选";
    }
    return "";
  }

  function formatOverlayLabel(entity, record, mode) {
    var P = LabelPolicy();
    if (!P) return { text: entity.display_name || "对象", compact: true };
    var base = P.formatInImageLabel(entity);
    var pri = priorityShort(record);
    var hint = motionHint(record);

    if (mode === "full") {
      var flags = [];
      if (record) {
        if (record.tracking_required) flags.push((Copy().flags || {}).tracking || "跟踪");
        if (record.ocr_required) flags.push((Copy().flags || {}).ocr || "OCR");
        if (record.depth_required) flags.push((Copy().flags || {}).depth || "深度");
      }
      var route = record && record.recommended_followup_model && record.recommended_followup_model[0]
        ? ((Copy().followupModel || {})[record.recommended_followup_model[0]] || record.recommended_followup_model[0])
        : "";
      var tail = flags.length ? " · " + flags.join("/") : "";
      if (route) tail += " · " + route;
      return {
        text: base.glyph + " " + (pri ? pri + " " : "") + base.shortName +
          (base.percent ? " " + base.percent : "") + tail,
        compact: false
      };
    }

    if (mode === "compact" && hint) {
      return {
        text: base.glyph + " " + (pri ? pri + " " : "") + base.shortName + " · " + hint,
        compact: true
      };
    }

    return {
      text: base.glyph + " " + (pri ? pri + " " : "") + base.shortName +
        (base.percent ? " " + base.percent : ""),
      compact: true
    };
  }

  function measureChip(ctx, text, fontSize) {
    var fs = fontSize || 14;
    ctx.font = "600 " + fs + "px system-ui, -apple-system, 'Segoe UI', sans-serif";
    var padX = 7;
    var padY = 5;
    var chipW = ctx.measureText(text).width + padX * 2;
    var chipH = fs + padY * 2;
    return { w: chipW, h: chipH, padX: padX, padY: padY, fontSize: fs };
  }

  function chipRect(x, y, chipW, chipH) {
    return { x: x, y: y - chipH + 2, w: chipW, h: chipH };
  }

  function rectsOverlap(a, b, pad) {
    pad = pad == null ? 4 : pad;
    return !(
      a.x + a.w + pad < b.x ||
      b.x + b.w + pad < a.x ||
      a.y + a.h + pad < b.y ||
      b.y + b.h + pad < a.y
    );
  }

  function clamp(val, min, max) {
    return Math.max(min, Math.min(max, val));
  }

  function anchorCandidates(bbox, chipW, chipH, canvasW, canvasH) {
    var gap = 6;
    var cx = bbox.x + bbox.w / 2 - chipW / 2;
    return [
      { x: clamp(cx, 4, canvasW - chipW - 4), y: bbox.y - gap, id: "top" },
      { x: clamp(bbox.x + bbox.w - chipW, 4, canvasW - chipW - 4), y: bbox.y - gap, id: "top-right" },
      { x: clamp(bbox.x, 4, canvasW - chipW - 4), y: bbox.y - gap, id: "top-left" },
      { x: clamp(bbox.x + bbox.w - chipW, 4, canvasW - chipW - 4), y: bbox.y + bbox.h + gap + chipH, id: "bottom-right" },
      { x: clamp(bbox.x, 4, canvasW - chipW - 4), y: bbox.y + bbox.h + gap + chipH, id: "bottom-left" }
    ];
  }

  function pickLabelPlacement(bbox, chipW, chipH, placed, canvasW, canvasH, avoidBboxes) {
    var anchors = anchorCandidates(bbox, chipW, chipH, canvasW, canvasH);
    var i;
    for (i = 0; i < anchors.length; i++) {
      var rect = chipRect(anchors[i].x, anchors[i].y, chipW, chipH);
      if (rect.x < 2 || rect.y < 2 || rect.x + rect.w > canvasW - 2 || rect.y + rect.h > canvasH - 2) {
        continue;
      }
      var hit = false;
      var j;
      for (j = 0; j < placed.length; j++) {
        if (rectsOverlap(rect, placed[j], 3)) { hit = true; break; }
      }
      if (!hit && avoidBboxes) {
        for (j = 0; j < avoidBboxes.length; j++) {
          var ob = avoidBboxes[j];
          if (ob && rectsOverlap(rect, ob, 2)) { hit = true; break; }
        }
      }
      if (!hit) return { x: anchors[i].x, y: anchors[i].y, rect: rect, anchor: anchors[i].id };
    }
    var fallback = {
      x: clamp(bbox.x + 4, 4, canvasW - chipW - 4),
      y: clamp(bbox.y + 14, chipH + 4, canvasH - 4)
    };
    return { x: fallback.x, y: fallback.y, rect: chipRect(fallback.x, fallback.y, chipW, chipH), anchor: "compact-in" };
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

  function collectAvoidBboxes(items, selfId) {
    return items
      .filter(function (it) { return it.entity.entity_id !== selfId && it.bbox; })
      .map(function (it) { return it.bbox; });
  }

  global.HudOverlayReadability = {
    version: "hud_overlay_readability_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Observation-Attention-Overlay-Readability-Patch-v1-001",
    lookupRecord: lookupRecord,
    isSceneStructure: isSceneStructure,
    isHighlighted: isHighlighted,
    priorityAlpha: priorityAlpha,
    useSceneStructureStyle: useSceneStructureStyle,
    formatOverlayLabel: formatOverlayLabel,
    measureChip: measureChip,
    pickLabelPlacement: pickLabelPlacement,
    sortDrawItems: sortDrawItems,
    collectAvoidBboxes: collectAvoidBboxes,
    PRIORITY_DRAW_ORDER: PRIORITY_DRAW_ORDER
  };
})(typeof window !== "undefined" ? window : this);
