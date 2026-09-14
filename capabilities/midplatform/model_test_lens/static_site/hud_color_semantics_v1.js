/**
 * HUD Color Semantics V1 — task/risk/uncertainty-first color policy.
 */
(function (global) {
  "use strict";

  var SEMANTIC = {
    task_target: {
      id: "task_target",
      stroke: "#3ecf8e",
      fill: "rgba(62, 207, 142, 0.28)",
      statusLabel: "任务相关"
    },
    risk: {
      id: "risk",
      stroke: "#f07178",
      fill: "rgba(240, 113, 120, 0.28)",
      statusLabel: "需关注"
    },
    uncertainty: {
      id: "uncertainty",
      stroke: "#f0b429",
      fill: "rgba(240, 180, 41, 0.22)",
      statusLabel: "需复核",
      dashed: true
    },
    environment: {
      id: "environment",
      stroke: "#4d9fff",
      fill: "rgba(77, 159, 255, 0.22)",
      statusLabel: "环境结构"
    },
    ocr_text: {
      id: "ocr_text",
      stroke: "#ba55d3",
      fill: "rgba(186, 85, 211, 0.22)",
      statusLabel: "需 OCR 复核"
    },
    weak_background: {
      id: "weak_background",
      stroke: "#8b9cb3",
      fill: "rgba(139, 156, 179, 0.15)",
      statusLabel: "弱相关"
    },
    inferred_boundary: {
      id: "inferred_boundary",
      stroke: "#ffffff",
      fill: null,
      statusLabel: "推测边界",
      dashed: true
    }
  };

  var NAV_TASKS = ["street_navigation_test", "crossing_road_test"];
  var TEXT_TASKS = ["find_text_test"];

  function normKey(label) {
    return String(label || "").trim().toLowerCase().replace(/\s+/g, "_");
  }

  function taskContextType(taskContext) {
    if (!taskContext) return "general_scene_understanding";
    return taskContext.task_context_type || taskContext.task_context || "general_scene_understanding";
  }

  function isNavTask(ctx) {
    return NAV_TASKS.indexOf(taskContextType(ctx)) >= 0;
  }

  function isTextTask(ctx) {
    return TEXT_TASKS.indexOf(taskContextType(ctx)) >= 0;
  }

  function resolveMobileSamSemantics(rawLabel, confidence, taskContext, entity) {
    var key = normKey(rawLabel);
    var lowConf = confidence != null && confidence < 0.75;
    var nav = isNavTask(taskContext);
    var textTask = isTextTask(taskContext);

    if (entity && entity.task_semantic_candidate) {
      var ts = entity.task_semantic_candidate;
      if (ts.indexOf("文字") >= 0) return SEMANTIC.ocr_text;
      if (ts.indexOf("动态") >= 0) return lowConf ? SEMANTIC.uncertainty : SEMANTIC.risk;
      if (ts.indexOf("通行") >= 0) return nav ? SEMANTIC.task_target : SEMANTIC.environment;
      if (ts.indexOf("屏幕") >= 0 || ts.indexOf("标识") >= 0) return SEMANTIC.ocr_text;
      if (ts.indexOf("结构") >= 0) return SEMANTIC.environment;
      return SEMANTIC.environment;
    }

    if (key.indexOf("people_region") >= 0 || key.indexOf("person") >= 0) {
      return lowConf ? SEMANTIC.uncertainty : SEMANTIC.risk;
    }
    if (key.indexOf("station_direction") >= 0 || key.indexOf("station_name") >= 0 || key.indexOf("route_map") >= 0) {
      return SEMANTIC.ocr_text;
    }
    if (key.indexOf("floor_walkable") >= 0 || key.indexOf("warning_line") >= 0) {
      return nav ? SEMANTIC.task_target : SEMANTIC.environment;
    }
    if (key.indexOf("generic_region") >= 0) return SEMANTIC.uncertainty;

    if (key.indexOf("road_sign") >= 0 || key === "road_sign") {
      if (textTask || nav) return SEMANTIC.ocr_text;
      return lowConf ? SEMANTIC.uncertainty : SEMANTIC.ocr_text;
    }
    if (key.indexOf("building") >= 0 || key.indexOf("large_structure") >= 0) {
      return SEMANTIC.environment;
    }
    if (key.indexOf("advertisement") >= 0 || key.indexOf("sign_or_ad") >= 0) {
      return SEMANTIC.ocr_text;
    }
    if (key.indexOf("vehicle") >= 0 || key.indexOf("dynamic_object") >= 0) {
      if (nav) return SEMANTIC.risk;
      return lowConf ? SEMANTIC.uncertainty : SEMANTIC.risk;
    }
    if (key.indexOf("crosswalk") >= 0 || key.indexOf("road_or") >= 0 || key.indexOf("large_plane") >= 0) {
      if (nav) return SEMANTIC.task_target;
      return SEMANTIC.environment;
    }
    if (key.indexOf("street_facility") >= 0 || key.indexOf("pole") >= 0 || key.indexOf("edge_object") >= 0) {
      return SEMANTIC.uncertainty;
    }
    if (lowConf) return SEMANTIC.uncertainty;
    if (key.indexOf("background") >= 0 || key.indexOf("sky") >= 0) return SEMANTIC.weak_background;
    return SEMANTIC.environment;
  }

  function applyToEntity(entity, taskContext) {
    var raw = (entity._overlay && entity._overlay.label) || entity.label || "";
    var conf = entity.confidence;
    var sem = resolveMobileSamSemantics(raw, conf, taskContext, entity);
    entity.hud_semantic = sem.id;
    entity.hud_stroke = sem.stroke;
    entity.hud_fill = sem.fill;
    entity.hud_status_label = sem.statusLabel;
    entity.hud_dashed = !!sem.dashed;
    if (conf != null && conf < 0.72) {
      entity.hud_semantic = "uncertainty";
      entity.hud_stroke = SEMANTIC.uncertainty.stroke;
      entity.hud_fill = SEMANTIC.uncertainty.fill;
      entity.hud_status_label = SEMANTIC.uncertainty.statusLabel;
      entity.hud_dashed = true;
    }
    return entity;
  }

  function summarizeRisk(entities) {
    var hasRed = false;
    var hasYellow = false;
    (entities || []).forEach(function (e) {
      if (e.hud_semantic === "risk") hasRed = true;
      if (e.hud_semantic === "uncertainty" || e.hud_semantic === "ocr_text") hasYellow = true;
    });
    if (hasRed) return "风险：存在需关注目标";
    if (hasYellow) return "不确定：存在需复核区域";
    return "主要风险：未发现显著失败";
  }

  global.HudColorSemantics = {
    version: "hud_color_semantics_v1",
    SEMANTIC: SEMANTIC,
    resolveMobileSamSemantics: resolveMobileSamSemantics,
    applyToEntity: applyToEntity,
    summarizeRisk: summarizeRisk,
    taskContextType: taskContextType
  };
})(typeof window !== "undefined" ? window : this);
