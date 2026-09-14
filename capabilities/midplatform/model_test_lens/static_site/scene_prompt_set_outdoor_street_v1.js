/**
 * Outdoor street prompt set — region candidates, not semantic facts.
 */
(function (global) {
  "use strict";

  global.ScenePromptSetOutdoorStreet = {
    version: "scene_prompt_set_outdoor_street_v1",
    scene_type_candidate: "outdoor_street",
    prompt_set_id: "scene_prompt_set_outdoor_street_v1",
    prompts: [
      "road_sign_candidate",
      "crosswalk_or_road_region",
      "vehicle_candidate",
      "advertisement_panel",
      "building_structure"
    ],
    forbidden_legacy_prompts: []
  };
})(typeof window !== "undefined" ? window : this);
