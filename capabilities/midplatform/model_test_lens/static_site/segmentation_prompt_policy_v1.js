/**
 * Segmentation prompt policy — select prompt set from scene_profile_candidate.
 */
(function (global) {
  "use strict";

  var Outdoor = function () { return global.ScenePromptSetOutdoorStreet; };
  var Subway = function () { return global.ScenePromptSetSubwayPlatform; };
  var Display = function () { return global.PromptLabelDisplayPolicy; };

  var GENERIC_PROMPTS = [
    "generic_region_candidate_1",
    "generic_region_candidate_2",
    "generic_region_candidate_3",
    "generic_region_candidate_4",
    "generic_region_candidate_5"
  ];

  var LEGACY_OUTDOOR = [
    "road_sign", "left_building", "center_advertisement_screen",
    "front_vehicle", "crosswalk_or_road_region"
  ];

  function selectPolicy(sceneProfile) {
    var sceneType = (sceneProfile && sceneProfile.scene_type_candidate) || "unknown_scene";
    var subway = Subway();
    var outdoor = Outdoor();
    if (sceneType === "subway_platform" || sceneType === "indoor_station") {
      return {
        policy_id: "spp_" + sceneType,
        scene_type_candidate: sceneType,
        prompt_set_id: subway.prompt_set_id,
        prompt_ids: subway.prompts.slice(),
        forbidden_legacy_prompts: subway.forbidden_legacy_outdoor_prompts.slice(),
        candidate_only: true,
        not_fact: true,
        prompt_is_not_fact: true
      };
    }
    if (sceneType === "outdoor_street") {
      return {
        policy_id: "spp_outdoor_street",
        scene_type_candidate: sceneType,
        prompt_set_id: outdoor.prompt_set_id,
        prompt_ids: outdoor.prompts.slice(),
        forbidden_legacy_prompts: [],
        candidate_only: true,
        not_fact: true,
        prompt_is_not_fact: true
      };
    }
    return {
      policy_id: "spp_unknown",
      scene_type_candidate: "unknown_scene",
      prompt_set_id: "scene_prompt_set_generic_v1",
      prompt_ids: GENERIC_PROMPTS.slice(),
      forbidden_legacy_prompts: LEGACY_OUTDOOR.slice(),
      candidate_only: true,
      not_fact: true,
      prompt_is_not_fact: true
    };
  }

  function usesLegacyOutdoorPrompts(policy) {
    if (!policy || !policy.prompt_ids) return false;
    return policy.prompt_ids.some(function (id) {
      return LEGACY_OUTDOOR.indexOf(id) >= 0;
    });
  }

  function enrichEnvelopeLayers(envelope) {
    if (!envelope) return envelope;
    var layers = envelope.visualization_layers || [];
    var D = Display();
    layers.forEach(function (layer) {
      if (D) D.enrichLayerMeta(layer);
    });
    return envelope;
  }

  global.SegmentationPromptPolicy = {
    version: "segmentation_prompt_policy_v1",
    selectPolicy: selectPolicy,
    usesLegacyOutdoorPrompts: usesLegacyOutdoorPrompts,
    enrichEnvelopeLayers: enrichEnvelopeLayers,
    LEGACY_OUTDOOR_PROMPTS: LEGACY_OUTDOOR
  };
})(typeof window !== "undefined" ? window : this);
