/**
 * Overlay route filter — classify segmentation candidates for OCR vs SLAM display filters.
 * Display-only; candidate_only / not_fact preserved.
 */
(function (global) {
  "use strict";

  var OCR_HINT_RE = /station_direction|station_name|route_map|name_board|sign|text|advertisement|screen|ocr/;
  var SLAM_HINT_RE = /floor|walkable|crosswalk|warning_line|platform_edge|building_structure|large_static|road_region|structure|platform_screen/;

  function labelBlob(entity) {
    return [
      entity.source_prompt_hint,
      entity.original_prompt_label,
      entity.label,
      entity.task_semantic_candidate,
      entity.display_name
    ].filter(Boolean).join(" ").toLowerCase();
  }

  function followupsInclude(record, model) {
    if (!record || !record.recommended_followup_model) return false;
    return record.recommended_followup_model.indexOf(model) >= 0;
  }

  /**
   * @returns {"ocr"|"slam"|"other"}
   */
  function classifyRoute(entity, attentionRecord) {
    if (!entity) return "other";

    if (entity.ocr_route_candidate) return "ocr";
    if (attentionRecord && (attentionRecord.ocr_required || attentionRecord.ocr_route_candidate)) {
      return "ocr";
    }
    if (followupsInclude(attentionRecord, "ocr")) return "ocr";

    var blob = labelBlob(entity);
    if (OCR_HINT_RE.test(blob)) {
      if (/people|person|vehicle|train_door|动态目标/.test(blob)) return "other";
      return "ocr";
    }

    if (followupsInclude(attentionRecord, "slam") || followupsInclude(attentionRecord, "slam_reference")) {
      return "slam";
    }
    if (attentionRecord && attentionRecord.motion_state_candidate === "scene_structure_candidate") {
      return "slam";
    }
    if (SLAM_HINT_RE.test(blob)) return "slam";
    if (/通行结构|大型结构/.test(entity.task_semantic_candidate || "")) return "slam";

    return "other";
  }

  function passesRouteFilter(entity, attentionRecord, routeFilter) {
    var mode = routeFilter || "all";
    if (mode === "all") return true;
    var route = classifyRoute(entity, attentionRecord);
    if (mode === "ocr") return route === "ocr";
    if (mode === "slam") return route === "slam";
    return true;
  }

  global.OverlayRouteFilter = {
    version: "overlay_route_filter_v1",
    classifyRoute: classifyRoute,
    passesRouteFilter: passesRouteFilter
  };
})(typeof window !== "undefined" ? window : this);
