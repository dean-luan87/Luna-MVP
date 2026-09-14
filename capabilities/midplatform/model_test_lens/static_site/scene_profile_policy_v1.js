/**
 * Scene profile policy — heuristic scene_type_candidate (not fact).
 */
(function (global) {
  "use strict";

  var SUBWAY_KEYWORDS = ["subway", "station", "platform", "jiahuihu", "metro", "地铁站", "站台"];
  var SHOP_KEYWORDS = ["shop_sign", "shopfront", "nostalgic", "店招", "招牌", "广告牌"];
  var CORRIDOR_KEYWORDS = ["corridor", "hallway", "走廊", "通道"];
  var STREET_KEYWORDS = ["street", "urban", "road_scene", "街景"];

  function inferFromEnvelope(envelope) {
    if (!envelope) return null;
    if (envelope.scene_profile_candidate) return envelope.scene_profile_candidate;
    var refs = envelope.input_asset_refs || [];
    var blob = refs.join(" ").toLowerCase();
    var name = blob;
    if (envelope._source_file_name) name += " " + String(envelope._source_file_name).toLowerCase();
    return inferFromFileName(name);
  }

  function inferFromFileName(fileName) {
    var name = String(fileName || "").toLowerCase();
    var hints = [];
    var sceneType = "unknown_scene";
    var confidence = 0.55;

    if (SUBWAY_KEYWORDS.some(function (k) { return name.indexOf(k) >= 0; })) {
      sceneType = "subway_platform";
      confidence = 0.82;
      hints.push("filename:subway_hint");
    } else if (SHOP_KEYWORDS.some(function (k) { return name.indexOf(k) >= 0; })) {
      sceneType = "shopfront_sign";
      confidence = 0.88;
      hints.push("filename:shopfront_hint");
    } else if (CORRIDOR_KEYWORDS.some(function (k) { return name.indexOf(k) >= 0; })) {
      sceneType = "corridor";
      confidence = 0.8;
      hints.push("filename:corridor_hint");
    } else if (STREET_KEYWORDS.some(function (k) { return name.indexOf(k) >= 0; })) {
      sceneType = "outdoor_street";
      confidence = 0.78;
      hints.push("filename:street_hint");
    } else {
      hints.push("heuristic:unknown_scene");
    }

    return {
      scene_profile_id: "spc_ui_" + sceneType + "_" + String(Date.now()),
      scene_type_candidate: sceneType,
      confidence: confidence,
      evidence_refs: hints,
      candidate_only: true,
      not_fact: true,
      scene_profile_candidate_not_fact: true
    };
  }

  function taskContextForScene(sceneType) {
    if (sceneType === "subway_platform" || sceneType === "indoor_station") {
      return "indoor_navigation_test";
    }
    if (sceneType === "shopfront_sign" || sceneType === "text_signage_scene") {
      return "text_reading_test";
    }
    if (sceneType === "outdoor_street" || sceneType === "outdoor_street_crossing") return "street_navigation_test";
    return "general_scene_understanding";
  }

  global.SceneProfilePolicy = {
    version: "scene_profile_policy_v1",
    inferFromEnvelope: inferFromEnvelope,
    inferFromFileName: inferFromFileName,
    taskContextForScene: taskContextForScene
  };
})(typeof window !== "undefined" ? window : this);
