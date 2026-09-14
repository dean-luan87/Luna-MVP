/**
 * Subway platform prompt set — no legacy outdoor street prompts.
 */
(function (global) {
  "use strict";

  global.ScenePromptSetSubwayPlatform = {
    version: "scene_prompt_set_subway_platform_v1",
    scene_type_candidate: "subway_platform",
    prompt_set_id: "scene_prompt_set_subway_platform_v1",
    prompts: [
      "station_direction_sign",
      "station_name_board",
      "route_map_or_line_info",
      "platform_screen_door",
      "train_door_area",
      "advertisement_panel",
      "warning_line_or_platform_edge",
      "floor_walkable_area",
      "people_region",
      "large_static_structure"
    ],
    ocr_route_prompt_ids: [
      "station_direction_sign",
      "station_name_board",
      "route_map_or_line_info",
      "advertisement_panel"
    ],
    forbidden_legacy_outdoor_prompts: [
      "road_sign",
      "left_building",
      "center_advertisement_screen",
      "front_vehicle",
      "crosswalk_or_road_region"
    ]
  };
})(typeof window !== "undefined" ? window : this);
