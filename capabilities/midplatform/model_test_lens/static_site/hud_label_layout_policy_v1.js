/**
 * HUD Label Layout Policy V1 — minimal in-image labels, rich external details.
 */
(function (global) {
  "use strict";

  var CIRCLE_NUMBERS = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩"];

  var DisplayPolicy = function () { return global.PromptLabelDisplayPolicy; };

  var SHORT_LABELS = {
    road_sign: "路牌",
    left_building: "左侧建筑",
    building_or_large_structure: "建筑",
    center_advertisement_screen: "广告屏",
    front_vehicle: "前方车辆",
    vehicle_or_small_dynamic_object: "车辆",
    crosswalk_or_road_region: "道路区域",
    road_or_crosswalk_or_large_plane: "道路区域",
    street_facility_or_pole_or_edge_object: "街边设施",
    sign_or_advertisement: "标识",
    sign_or_advertisement_screen: "广告屏"
  };

  var EXPLANATION_BY_SEMANTIC = {
    task_target: "区域边界较稳定，可作为任务相关观察参考。",
    risk: "当前只是分割候选，不能确认真实类别。",
    uncertainty: "置信度偏低或边界不清，需要进一步确认。",
    environment: "环境结构区域，边界相对稳定。",
    ocr_text: "疑似文字或标识区域，分割不能代替文字识别。",
    weak_background: "弱相关背景区域，观察优先级较低。"
  };

  var SUGGESTION_BY_SEMANTIC = {
    task_target: "结合 SLAM / 深度判断可通行性与空间关系。",
    risk: "接入目标检测确认类别与位置。",
    uncertainty: "建议人工复核或换帧重测。",
    environment: "可用于场景结构理解，不建议单独作为导航依据。",
    ocr_text: "接入 OCR 检查文字内容。",
    weak_background: "可隐藏或降低显示优先级。"
  };

  function normKey(s) {
    return String(s || "").trim().toLowerCase().replace(/\s+/g, "_");
  }

  function rawLabel(entity) {
    return (entity._overlay && entity._overlay.label) || entity.label || "";
  }

  function shortName(entity) {
    if (entity && entity.hud_short_label && !DisplayPolicy()) return entity.hud_short_label;
    if (entity && entity.task_semantic_candidate) return entity.task_semantic_candidate;
    if (entity && entity._overlay && entity._overlay.display_task_semantic) {
      var D = DisplayPolicy();
      if (D) return D.taskSemanticShort(entity._overlay.label, entity._overlay);
    }
    var key = normKey(rawLabel(entity));
    var Dp = DisplayPolicy();
    if (Dp && Dp.taskSemanticShort) {
      var semantic = Dp.taskSemanticShort(key, entity && entity._overlay);
      if (semantic && !Dp.isForbiddenMainLabel(semantic)) return semantic;
    }
    if (SHORT_LABELS[key] && Dp && Dp.isForbiddenMainLabel(SHORT_LABELS[key])) {
      return Dp.taskSemanticShort(key, entity && entity._overlay) || "观察候选";
    }
    if (SHORT_LABELS[key]) return SHORT_LABELS[key];
    var I18n = global.LunaObservationLabelI18n;
    var full = I18n && I18n.mobileSamLabel
      ? I18n.mobileSamLabel(rawLabel(entity))
      : (entity.display_name || "识别区域");
    if (Dp && Dp.isForbiddenMainLabel(full)) {
      return Dp.taskSemanticShort(key, entity && entity._overlay) || "观察候选";
    }
    return full.replace(/候选$/g, "").replace(/\s*\/\s*.+$/, "").trim() || full;
  }

  function numberGlyph(index) {
    return CIRCLE_NUMBERS[index] || "(" + (index + 1) + ")";
  }

  function formatPercent(confidence) {
    if (confidence == null || isNaN(confidence)) return "";
    return Math.round(confidence * 100) + "%";
  }

  function formatInImageLabel(entity) {
    var glyph = entity.hud_number_glyph || numberGlyph((entity.hud_number || 1) - 1);
    var short = entity.hud_short_label || shortName(entity);
    var pct = formatPercent(entity.confidence);
    return {
      glyph: glyph,
      shortName: short,
      percent: pct,
      text: glyph + " " + short + (pct ? " " + pct : "")
    };
  }

  function buildExternalDetail(entity, index) {
    var sem = entity.hud_semantic || "environment";
    var label = formatInImageLabel(entity);
    return {
      entity_id: entity.entity_id,
      index: index,
      number: entity.hud_number || index + 1,
      number_glyph: label.glyph,
      name: (entity.task_semantic_candidate || label.shortName) + "候选",
      short_name: label.shortName,
      confidence: entity.confidence,
      confidence_text: formatPercent(entity.confidence),
      status: entity.hud_status_label || "环境结构",
      semantic: sem,
      stroke: entity.hud_stroke || "#4d9fff",
      explanation: entity.hud_external_explanation || EXPLANATION_BY_SEMANTIC[sem] || EXPLANATION_BY_SEMANTIC.environment,
      suggestion: entity.hud_external_suggestion || SUGGESTION_BY_SEMANTIC[sem] || SUGGESTION_BY_SEMANTIC.environment,
      source_prompt_hint: entity.source_prompt_hint || "",
      original_prompt_label: entity.original_prompt_label || rawLabel(entity),
      prompt_is_not_fact: entity.prompt_is_not_fact !== false,
      display_label_source: entity.display_label_source || "midplatform_task_semantics",
      hidden: !!entity._hidden
    };
  }

  function assignNumbers(entities) {
    (entities || []).forEach(function (entity, i) {
      entity.hud_number = i + 1;
      entity.hud_number_glyph = numberGlyph(i);
      entity.hud_short_label = shortName(entity);
      var detail = buildExternalDetail(entity, i);
      entity.hud_external_explanation = detail.explanation;
      entity.hud_external_suggestion = detail.suggestion;
    });
    return entities;
  }

  function enrichEntity(entity, index) {
    entity.hud_number = index + 1;
    entity.hud_number_glyph = numberGlyph(index);
    entity.hud_short_label = shortName(entity);
    var detail = buildExternalDetail(entity, index);
    entity.hud_external_explanation = detail.explanation;
    entity.hud_external_suggestion = detail.suggestion;
    return entity;
  }

  function matchesFilter(entity, filterId) {
    if (!filterId || filterId === "all") return true;
    var sem = entity.hud_semantic || "";
    if (filterId === "task") return sem === "task_target";
    if (filterId === "risk") return sem === "risk";
    if (filterId === "uncertain") {
      return sem === "uncertainty" || sem === "ocr_text";
    }
    return true;
  }

  function chipStatusShort(entity) {
    var sem = entity.hud_semantic || "";
    if (sem === "task_target") return "任务";
    if (sem === "risk") return "风险";
    if (sem === "ocr_text") return "OCR";
    if (sem === "uncertainty") return "需复核";
    if (sem === "environment") {
      return entity.confidence != null && entity.confidence >= 0.85 ? "稳定" : "环境";
    }
    if (entity.confidence != null && entity.confidence >= 0.85) return "稳定";
    return "需复核";
  }

  global.HudLabelLayoutPolicy = {
    version: "hud_label_layout_policy_v1",
    CIRCLE_NUMBERS: CIRCLE_NUMBERS,
    assignNumbers: assignNumbers,
    enrichEntity: enrichEntity,
    shortName: shortName,
    formatInImageLabel: formatInImageLabel,
    buildExternalDetail: buildExternalDetail,
    matchesFilter: matchesFilter,
    chipStatusShort: chipStatusShort
  };
})(typeof window !== "undefined" ? window : this);
