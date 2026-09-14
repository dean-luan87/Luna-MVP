/**
 * Prompt label display policy — task semantics on canvas, prompt as hint in detail only.
 */
(function (global) {
  "use strict";

  var FORBIDDEN_MAIN_LABELS = {
    road_sign: true,
    front_vehicle: true,
    center_advertisement_screen: true,
    crosswalk_or_road_region: true,
    left_building: true,
    "路牌": true,
    "前方车辆": true,
    "广告屏": true,
    "道路区域": true,
    "左侧建筑": true
  };

  var PROMPT_TO_TASK_SEMANTIC = {
    road_sign: "文字观察候选",
    road_sign_candidate: "文字观察候选",
    station_direction_sign: "文字观察候选",
    station_name_board: "文字观察候选",
    route_map_or_line_info: "文字观察候选",
    front_vehicle: "动态目标候选",
    vehicle_candidate: "动态目标候选",
    people_region: "动态目标候选",
    train_door_area: "动态目标候选",
    crosswalk_or_road_region: "通行结构候选",
    floor_walkable_area: "通行结构候选",
    warning_line_or_platform_edge: "通行结构候选",
    center_advertisement_screen: "屏幕/标识候选",
    advertisement_panel: "屏幕/标识候选",
    platform_screen_door: "屏幕/标识候选",
    left_building: "大型结构候选",
    building_structure: "大型结构候选",
    large_static_structure: "大型结构候选",
    generic_region_candidate_1: "静态区域候选",
    generic_region_candidate_2: "静态区域候选",
    generic_region_candidate_3: "静态区域候选",
    generic_region_candidate_4: "静态区域候选",
    generic_region_candidate_5: "静态区域候选"
  };

  function normKey(s) {
    return String(s || "").trim().toLowerCase().replace(/\s+/g, "_");
  }

  function taskSemanticShort(promptId, layer) {
    if (layer && layer.display_task_semantic) {
      return String(layer.display_task_semantic).replace(/^P\d\s+/, "").trim();
    }
    var key = normKey(promptId);
    return PROMPT_TO_TASK_SEMANTIC[key] || "观察候选";
  }

  function isForbiddenMainLabel(label) {
    var k = normKey(label);
    return !!FORBIDDEN_MAIN_LABELS[k] || !!FORBIDDEN_MAIN_LABELS[label];
  }

  function enrichLayerMeta(layer) {
    if (!layer) return layer;
    var pid = layer.label || layer.layer_id || layer.output_id || "";
    layer.source_prompt_hint = layer.source_prompt_hint || (pid + "_prompt");
    layer.prompt_is_not_fact = true;
    layer.display_label_source = "midplatform_task_semantics";
    layer.display_task_semantic = layer.display_task_semantic || taskSemanticShort(pid, layer);
    layer.original_prompt_label = pid;
    return layer;
  }

  var BOUNDARY_FLAGS = {
    prompt_label_display_not_fact: true,
    no_prompt_label_fact_upgrade: true,
    ui_marker_uses_task_semantics_not_prompt_label: true,
    source_prompt_hint_not_display_fact: true
  };

  global.PromptLabelDisplayPolicy = {
    version: "prompt_label_display_policy_v1",
    boundary_flags: BOUNDARY_FLAGS,
    no_prompt_label_fact_upgrade: true,
    taskSemanticShort: taskSemanticShort,
    isForbiddenMainLabel: isForbiddenMainLabel,
    enrichLayerMeta: enrichLayerMeta,
    PROMPT_TO_TASK_SEMANTIC: PROMPT_TO_TASK_SEMANTIC
  };
})(typeof window !== "undefined" ? window : this);
